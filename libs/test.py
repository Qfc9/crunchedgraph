from flask_restful import Resource, Api
from flask import request
import jwt
import os
from libs.db import User
from libs.utils import isAuthed

class Test(Resource):
    """
    This class handles the test process
    """
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader: dict):
        # Getting the user from the database
        user: User = self.db.session.execute(self.db.select(User).filter_by(username=userHeader["username"])).scalar_one()

        return {
            "username": user.username,
            "password": user.password,
            "disabled": user.disabled
        }