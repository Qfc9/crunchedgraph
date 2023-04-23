from libs.db import Post, Photo, PhotoTags, User
from flask import request
from flask_restful import Resource, Api
import jwt
import os


class Posting(Resource):
    def __init__(self, db):
        self.db = db

    def get(self) -> dict:
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
        
        # TODO figure out filtering so we dont get other peoples posts
        post: list[Post] = self.db.session.query(Post).all()
        if post is None:
            return {}, 500
        
        data = [p.toDict() for p in post]
        # for p in post:
        #     data.append(p.toDict())
        return data
    
    def post(self) -> dict:
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


        try:
            request.get_json()

            userId = data["id"]
            text = request.get_json()["text"]

            user: User = self.db.session.query(User).filter_by(id=userId).first()
        except Exception:
            return {"error": "Invalid request"}, 400

        post: Post = Post(userId=userId, text=text)
        self.db.session.add(post)
        self.db.session.commit()

        return post.toDict(), 201