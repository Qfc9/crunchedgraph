from flask_restful import Resource, Api
from flask import request
import jwt
import os
from libs.db import User


class Test(Resource):
    def __init__(self, db):
        self.db = db

    def get(self):
        encoded = request.args
        token = encoded["token"]

        token = request.headers.get("Authorization")

        if type(token) is str:
            token = token.split(" ")[1]

        try:
            data = jwt.decode(token, os.environ['JWT_SECRET'], algorithms=["HS256"])
        except Exception:
            return {"error": "Invalid token"}, 401


        user: User = self.db.session.execute(self.db.select(User).filter_by(username=data["username"])).scalar_one()


        return {
            "username": user.username,
            "password": user.password,
            "disabled": user.disabled
        }