from flask_restful import Resource, Api
from flask import request
import jwt
import os
from libs.db import User


class Test(Resource):
    """
    This class handles the test process
    """
    def __init__(self, db):
        self.db = db

    def get(self):
        # Getting query params
        encoded = request.args
        token = encoded["token"]

        # Getting headers
        token = request.headers.get("Authorization")

        # Extracting the token from the header
        if type(token) is str:
            token = token.split(" ")[1]

        try:
            # Decoding the token, works as validation
            data = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])
        except Exception:
            return {"error": "Invalid token"}, 401

        # Getting the user from the database
        user: User = self.db.session.execute(self.db.select(User).filter_by(username=data["username"])).scalar_one()

        return {
            "username": user.username,
            "password": user.password,
            "disabled": user.disabled
        }