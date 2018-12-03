from flask import Flask,request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import base64

app = Flask(__name__)
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

    def __init__(self, username, email,picture=None):
        '''
        This Methods adds a new user to the db
        :param username: The username of the user
        :param email: The Email of the user
        :param picture: The picture of the user.
        '''
        self.username = username
        self.email = email
        self.picture = picture

class UserSchema(ma.Schema):
    '''
    Describes the Schema, how a user in the db will be exposed
    '''
    class Meta:
        # Fields to expose
        fields = ('id','username', 'email','picture')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class User(Resource):
    '''
    The REST-Class with the methods that can be accessed over /user/<id>
    '''
    def get(self, user_id):
        '''
        Method that handles the HTTP-GET method.
        :param user_id: The userid of the user
        :return: returns a user in json format
        '''
        user = User_DB.query.get(user_id)
        return user_schema.jsonify(user)

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
    def get(self):
        '''
        Method that handles the HTTP-GET method without a userid.
        :return: returns all users in json format
        '''
        all_users = User_DB.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)

    def post(self):
        '''
        Method that handles the HTTP-POST method and creates a new user.
        :return: returns the created user in json format
        '''
        if('username' not in request.json):
            raise ValueError('Give username a value')
        if ('email' not in request.json):
            raise ValueError('Give email a value')

        username = request.json['username']
        email = request.json['email']
        try:
            picture = request.json['picture']
            new_user = User_DB(username, email, picture=picture)
        except:
            new_user = User_DB(username, email)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)

##
## Actually setup the Api resource routing here
##
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)