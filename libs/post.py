from libs.db import Post, Photo, PhotoTags, User
from flask import request
from flask_restful import Resource, Api
import jwt
import os
from libs.utils import isAuthed

class Posting(Resource):
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader) -> dict:
        # TODO figure out filtering so we dont get other peoples posts
        post: list[Post] = self.db.session.query(Post).all()
        if post is None:
            return {}, 500
        
        data = [p.toDict() for p in post]
        # for p in post:
        #     data.append(p.toDict())
        return data
    
    @isAuthed
    def post(self, userHeader) -> dict:
        try:
            request.get_json()

            userId = userHeader["id"]
            text = request.get_json()["text"]

            user: User = self.db.session.query(User).filter_by(id=userId).first()
        except Exception:
            return {"error": "Invalid request"}, 400

        post: Post = Post(userId=userId, text=text)
        self.db.session.add(post)
        self.db.session.commit()

        return post.toDict(), 201