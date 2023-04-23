from libs.db import Post, Photo, PhotoTags, User
from flask import request
from flask_restful import Resource, Api
import jwt
import os
from libs.utils import isAuthed
import base64

class Posting(Resource):
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader) -> dict:
        queryParams = request.args
        userId = queryParams.get("userId")
        limit = queryParams.get("limit", 10)

        # TODO add pagination
        # page = queryParams.get("page", 1)

        post: list[Post] = None

        if userId is None:
            post: list[Post] = self.db.session.query(Post).limit(limit).all()

        elif userId is not None:
            post: list[Post] = self.db.session.query(Post).filter_by(userId=userId).limit(limit).all()

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
            imageBase64 = request.get_json().get("image")

            # TODO allow for more photo types besides png

            user: User = self.db.session.query(User).filter_by(id=userId).first()
        except Exception:
            return {"error": "Invalid request"}, 400

        post: Post = Post(userId=userId, text=text)
        self.db.session.add(post)
        self.db.session.commit()

        if imageBase64 is not None:
            photo = Photo(
                postId=post.id,
                url=""
                )
            self.db.session.add(photo)
            self.db.session.commit()

            # TODO validate photo
            with open(f"images/{photo.id}.png", "wb") as f:
                f.write(base64.b64decode(imageBase64))

            # TODO add photoTags, with ML
            # photoTags = PhotoTags(photoId=photo.id, userId=userId)
            # self.db.session.add(photoTags)
            # self.db.session.commit()

            # Fixing the chicken and the egg problem
            post.photoId = photo.id

        # When the records fully save
        self.db.session.commit()

        return post.toDict(), 201