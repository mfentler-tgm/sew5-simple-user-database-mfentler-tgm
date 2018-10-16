from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

users = [
    {
        "id":0,
        "name": "Mario",
        "email":"mfentler@student.tgm.ac.at"
    },
    {
        "id":1,
        "name":"Max",
        "email":"mmuster@gmail.com"
    }

]

class User(Resource):

    def get(self, name="nix"):
        for user in users:
            if(name=="nix"):
                return user,200
            elif(name==user["name"]):
                return user, 200
        return "User not found",404
    def post(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        args = parser.parse_args()

        userCounter = 0

        for user in users:
            userCounter += 1
            if(name == user["name"]):
                return "User with name {} already exists".format(name),400

        user = {
            "id": userCounter,
            "name":name,
            "email":args["email"]
        }
        users.append(user)
        return user,201

    def put(self,name):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        args = parser.parse_args()

        userCounter = 0

        for user in users:
            userCounter += 1
            if (name == user["name"]):
                user["email"] = args["email"]
                return user,200

        user = {
            "id": userCounter,
            "name": name,
            "email": args["email"]
        }
        users.append(user)
        return user, 201

    def delete(self,name):
        global users
        users = [user for user in users if user["name"] != name]
        return "{} is deleted.".format(name),200


if __name__=='__main__':
    api.add_resource(User,"/user/<string:name>")
    app.run(debug=True)