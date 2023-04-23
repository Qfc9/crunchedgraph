from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    This class represents the user table
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bio = db.Column(db.String(255))
    disabled = db.Column(db.Boolean, default=False)

    # BETTER WAY IS TO USE YOUR OWN CONSTRUCTOR
    # def __init__(self, username: str, password: str):
    #     super().__init__()
    #     self.username = username
    #     self.password = password

    def editable() -> list:
        return ["bio", "password", "username"]

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "bio": self.bio,
            "disabled": self.disabled
        }
    
    # def __str__(self):
    #     return f"User(id={self.id}, username={self.username}, password={self.password}, created_at={self.created_at}, updated_at={self.updated_at}, disabled={self.disabled})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    photoId = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)

    def toDict(self) -> dict:
        return {
            "id": self.id,
            "userId": self.userId,
            "text": self.text,
            "photoId": self.photoId,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "disabled": self.disabled
        }

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)

class PhotoTags(db.Model):
    photoId = db.Column(db.Integer, db.ForeignKey("photo.id"), primary_key=True)
    tag = db.Column(db.String(255))