from flask import Flask,request, jsonify
from flask_restful import reqparse, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from pathlib import Path
import os
import base64
import configparser

from flask_httpauth import HTTPDigestAuth
from hashlib import md5 as basic_md5

auth = HTTPDigestAuth(use_ha1_pw=True)

app = Flask(__name__)
#https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
app.secret_key = "super secret key"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'usercrud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


#enable CORS
CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('user')

class User_DB(db.Model):
    '''
    Databasemodel for the user in the sqlite db
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    picture = db.Column(db.String(2048), default=None)
    password = db.Column(db.String(255))

    def __init__(self, username, password, email,picture=None):
        '''
        This Methods adds a new user to the db
        :param username: The username of the user
        :param email: The Email of the user
        :param picture: The picture of the user.
        '''
        self.username = username
        #self.password = hashlib.sha256(password)
        #self.password = password
        self.password = get_ha1(username,password,auth.realm)
        self.email = email
        self.picture = picture


class UserSchema(ma.Schema):
    '''
    Describes the Schema, how a user in the db will be exposed
    '''
    class Meta:
        # Fields to expose
        fields = ('id','username', 'password', 'email','picture')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def md5(str):
    str = str.encode('utf-8')
    return basic_md5(str)

def get_ha1(user, pw, realm):
    a1 = user + ":" + realm + ":" + pw
    return md5(a1).hexdigest()

@auth.get_password
def get_password(username):
    all_users = User_DB.query.all()
    result = users_schema.dump(all_users)
    print(result.data)
    for user in result.data:
        if user["username"] == username:
            print(user["password"])
            return user["password"]
    return None



class User(Resource):
    '''
    The REST-Class with the methods that can be accessed over /user/<id>
    '''
    @auth.login_required
    def get(self, user_id):
        '''
        Method that handles the HTTP-GET method.
        :param user_id: The userid of the user
        :return: returns a user in json format
        '''
        user = User_DB.query.get(user_id)
        return user_schema.jsonify(user)

    @auth.login_required
    def delete(self, user_id):
        '''
        Method that handles the HTTP-DELETE method.
        :param user_id: The userid of the user
        :return: returns the deleted user in json format
        '''
        user = User_DB.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

        return user_schema.jsonify(user)

    @auth.login_required
    def put(self, user_id):
        '''
        Method that handles the HTTP-PUT method.
        :param user_id: The userid of the user
        :return: returns the updated user in json format
        '''
        user = User_DB.query.get(user_id)
        if ('username' in request.json):
            username = request.json['username']
            user.username = username
        if ('password' in request.json):
            password = request.json['password']
            user.password = password
        if ('email' in request.json):
            email = request.json['email']
            user.email = email
        if ('picture' in request.json):
            picture = request.json['picture']
            user.picture = picture

        db.session.commit()
        return user_schema.jsonify(user)

class UserList(Resource):
    '''
    The REST-Class with the methods that can be accessed over /user
    '''
    @auth.login_required
    def get(self):
        '''
        Method that handles the HTTP-GET method without a userid.
        :return: returns all users in json format
        '''
        all_users = User_DB.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)

    #@auth.login_required
    def post(self):
        '''
        Method that handles the HTTP-POST method and creates a new user.
        :return: returns the created user in json format
        '''
        print(request.json)
        if('username' not in request.json):
            raise ValueError('Give username a value')
        if('password' not in request.json):
            raise ValueError('No password provided')
        if ('email' not in request.json):
            raise ValueError('Give email a value')

        username = request.json['username']
        password = request.json['password']
        email = request.json['email']
        try:
            picture = request.json['picture']
            new_user = User_DB(username, password, email, picture=picture)
        except:
            try:
                new_user = User_DB(username, password, email)
            except:
                raise ValueError('The user exists already')

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)



##
## Actually setup the Api resource routing here
##
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')

if __name__ == '__main__':
    config = configparser.ConfigParser()

    # https://stackoverflow.com/questions/27844088/python-get-directory-two-levels-up
    #pathToConfig = Path(os.getcwd()).parents[1]
    #pathToConfig = os.path.join(pathToConfig,'customConfig.ini')
    #print(pathToConfig)
    #config.read(pathToConfig)
    config.read('../../customConfig.ini')

    if(config['Flask']['port'] != ""):
        port = config['Flask']['port']
    else:
        port = 5000

    db.create_all()

    try:
        newUser = User_DB("admin", "1234", "admin@mail.com")

        db.session.add(newUser)
        db.session.commit()
    except:
        pass
    finally:
        app.run(port=port, debug=True)


