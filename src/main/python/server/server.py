from flask import Flask,request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'C:\\Users\\mario\\git\\sew5-simple-user-database-mfentler-tgm\\usercrud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user')


class User_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    picture = db.Column(db.String(400))

    def __init__(self, username, email,picture):
        self.username = username
        self.email = email
        self.picture = picture

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','username', 'email','picture')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class User(Resource):

    def get(self, user_id):
        user = User_DB.query.get(user_id)
        return user_schema.jsonify(user)

    def delete(self, user_id):
        user = User_DB.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

        return user_schema.jsonify(user)

    def put(self, user_id):
        user = User_DB.query.get(user_id)
        username = request.json['username']
        email = request.json['email']

        user.email = email
        user.username = username

        db.session.commit()
        return user_schema.jsonify(user)

class UserList(Resource):

    def get(self):
        all_users = User_DB.query.all()
        result = users_schema.dump(all_users)
        return jsonify(result.data)

    def post(self):
        username = request.json['username']
        email = request.json['email']
        picture = request.json['picture']

        new_user = User_DB(username, email, picture)

        db.session.add(new_user)
        db.session.commit()

        return user_schema.jsonify(new_user)

##
## Actually setup the Api resource routing here
##
api.add_resource(UserList, '/user')
api.add_resource(User, '/user/<user_id>')

if __name__ == '__main__':
    app.run(debug=True)