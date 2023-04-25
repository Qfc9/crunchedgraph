# Loading up our custom environment variables
from dotenv import load_dotenv
load_dotenv(".env")

# Importing our libraries
from libs.dbInit import db
from libs.db import User, Post, Photo, PhotoTags
from datetime import datetime
import libs.test
import libs.auth
import libs.user
import libs.post
import libs.photo
import libs.likes
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask import Flask
import os

# Creating our app
app = Flask(__name__)

# Loading vars from our environment variables
username = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
database = os.environ['DB_NAME']

# Setting up our database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
db.init_app(app)

# Setting up our API
api = Api(app)

# Creating our tables
with app.app_context():
    db.create_all()

# Extra data we want to send to our resources
extraData = {
    "db": db
}

# Adding our resources
api.add_resource(libs.auth.Login, '/login', resource_class_kwargs=extraData)
api.add_resource(libs.auth.SignUp, '/signup', resource_class_kwargs=extraData)

api.add_resource(libs.user.Me, '/me', resource_class_kwargs=extraData)
api.add_resource(libs.post.Posting, '/post', resource_class_kwargs=extraData)
api.add_resource(libs.likes.Likes, '/like', resource_class_kwargs=extraData)

api.add_resource(libs.photo.Photo, '/photo', resource_class_kwargs=extraData)

api.add_resource(libs.test.Test, '/test', resource_class_kwargs=extraData)

if __name__ == '__main__':
    app.run(debug=True)
