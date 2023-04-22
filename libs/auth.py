from flask_restful import Resource, Api
from flask import request
import jwt
import os
from libs.db import User
from flask_sqlalchemy import SQLAlchemy

class SignUp(Resource):
    """
    This class handles the sign up process
    """
    def __init__(self, db):
        self.db = db

    def post(self):
        # Get json data from the body of the request
        data = request.get_json()

        try:
            username = data["username"]
            password = data["password"]

            # Create a new user
            user = User(username=username, password=password)

            # Add the user to the database
            self.db.session.add(user)
            self.db.session.commit()

        except Exception as e:
            print(e)
            return {"error": "Bad data"}, 400
        
        return {
            "message": "User created successfully"
        }


class Login(Resource):
    """
    This class handles the login process
    """
    def __init__(self, db):
        self.db = db

    def post(self):
        data = request.get_json()

        try:
            username = data["username"]
            password = data["password"]

            # Get the user from the database
            user: User = self.db.session.execute(self.db.select(User).filter_by(username=username, password=password)).scalar_one()
        except Exception:
            return {"error": "Bad data"}, 400

        # Check if the user exists
        if user is None:
            return {"error": "User not found"}, 404

        # Generate a token backed on the user's username
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
    
