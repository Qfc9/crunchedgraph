from flask_restful import Resource, Api
from flask import request
import jwt
import os
from libs.db import User
from flask_sqlalchemy import SQLAlchemy

class SignUp(Resource):
    def __init__(self, db):
        self.db = db

    def post(self):
        data = request.get_json()

        try:
            username = data["username"]
            password = data["password"]

            user = User(username=username, password=password)

            self.db.session.add(user)
            self.db.session.commit()

        except Exception as e:
            print(e)
            return {"error": "Bad data"}, 400
        
        # TODO add the user to the database

        return {
            "message": "User created successfully"
        }


class Login(Resource):
    def __init__(self, db):
        self.db = db

    def post(self):
        # TODO handle bad data
        data = request.get_json()

        try:
            username = data["username"]
            password = data["password"]

            user: User = self.db.session.execute(self.db.select(User).filter_by(username=username, password=password)).scalar_one()
        except Exception:
            return {"error": "Bad data"}, 400

    
        if user is None:
            return {"error": "User not found"}, 404

        encoded = jwt.encode(
            {
                "username": username,
            },
            os.environ['JWT_SECRET'],
            algorithm="HS256"
            )

        return {
            "message": "User logged in successfully",
            "token": encoded
        }
    
