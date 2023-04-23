from libs.db import Post, Photo, PhotoTags, User
from flask import request, send_file
from flask_restful import Resource, Api

from libs.utils import isAuthed
import base64

class Photo(Resource):
    def __init__(self, db):
        self.db = db

    @isAuthed
    def get(self, userHeader) -> dict:
        # TODO add custom image sizes

        queryParams = request.args
        photoId = queryParams.get("photoId")

        if photoId is None:
            return {"error": "Invalid request"}, 400
        
        fileName = f"images/{photoId}.png"

        return send_file(fileName, mimetype='image/png')
    