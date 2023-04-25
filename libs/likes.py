from libs.db import Post, Photo, PhotoTags, User, Like
from flask import request, send_file
from flask_restful import Resource, Api

from libs.utils import isAuthed

class Likes(Resource):
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader) -> dict:
        queryParams = request.args
        postId = queryParams.get("postId")

        if postId is None:
            return {"error": "Invalid request"}, 400

        likes: list[Like] = self.db.session.query(Like).filter_by(postId=postId).all()

        data = {
            "likes": [like.toDict() for like in likes],
            "count": len(likes),
        }

        return data

    @isAuthed
    def post(self, userHeader) -> dict:
        try:
            request.get_json()

            userId = userHeader["id"]
            postId = request.get_json()["postId"]

            # Check if user has already liked this post
            like: Like = self.db.session.query(Like).filter_by(userId=userId, postId=postId).first()

            if like is None:
                like: Like = Like(userId=userId, postId=postId)
                self.db.session.add(like)
                self.db.session.commit()
            else:
                self.db.session.delete(like)
                self.db.session.commit()

            return {"message": "success"}

        except Exception as e:
            print(e)

            return {"error": "Invalid request"}, 400