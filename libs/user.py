from flask_restful import Resource, Api
from flask import request
import jwt
import os
from libs.db import User
import sqlalchemy
from libs.utils import isAuthed

class Me(Resource):
    """
    This class handles the test process
    """
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader: dict):

        # Getting the user from the database
        user: User = self.db.session.execute(self.db.select(User).filter_by(id=userHeader["id"])).scalar_one()

        return user.toDict()
    
    @isAuthed
    def post(self, userHeader: dict):
        # Getting the user from the database
        # TODO duplicate entries are not allowed, protect against that
        user: User = self.db.session.execute(self.db.select(User).filter_by(id=userHeader["id"])).scalar_one()

        for key in request.get_json():
            if key in User.editable():
                setattr(user, key, request.get_json()[key])

        # Committing the changes to the database
        try:
            self.db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return {"error": "Duplicate entry"}, 400

        return {"message": "User updated successfully"}