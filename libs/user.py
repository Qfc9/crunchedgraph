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
    
class GetBy(Resource):
    """
    This class handles the test process
    """
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userId, userHeader: dict):
        # Getting the user from the database
        queryParams = request.args
        userIdType = queryParams.get("type", "id")

        try:
            if userIdType == "username":
                user: User = self.db.session.execute(self.db.select(User).filter_by(username=userId)).scalar_one()
            elif userIdType == "id":
                user: User = self.db.session.execute(self.db.select(User).filter_by(id=userId)).scalar_one()
        except:
            return {"error": "User not found"}, 404

        if user is None:
            return {"error": "User not found"}, 404

        return user.toDict()

class Search(Resource):
    """
    This class handles the test process
    """
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader: dict):
        # Getting the user from the database
        queryParams = request.args
        username = queryParams.get("username")
        limit = queryParams.get("limit", 5)

        if username is None:
            return {"error": "No username provided"}, 400

        users: list[tuple[User]] = self.db.session.execute(self.db.select(User).filter(User.username.like(f"{username}%"))).all()

        if users is None:
            return {}, 500
        
        # print(users[0][0].toDict())

        if len(users) == 0:
            return [], 200
        
        data = [u[0].toDict() for u in users]

        return data
