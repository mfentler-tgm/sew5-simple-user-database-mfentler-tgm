from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from server import db,User_DB

if __name__ == '__main__':

    db.create_all()

    try:
        print("Adding new user ...")
        newUser = User_DB("admin", "1234", "admin@mail.com")

        db.session.add(newUser)
        db.session.commit()
    except:
        print("User already added, continuing ...")