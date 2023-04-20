from flask_restful import Resource, Api
from flask import request


class SignUp(Resource):
    def post(self):
        data = request.get_json()

        try:
            username = data["username"]
            password = data["password"]

        except Exception:
            return {"error": "Bad data"}, 400
        
        # TODO add the user to the database

        return {
            "message": "User created successfully"
        }


class Login(Resource):
    def post(self):
        # TODO handle bad data
        data = request.get_json()

        try:
            username = data["username"]
            password = data["password"]
        except Exception:
            return {"error": "Bad data"}, 400

        return {
            "message": "User logged in successfully"
        }
    
