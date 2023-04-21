# Loading up our custom environment variables
from dotenv import load_dotenv
load_dotenv(".env")

# Importing our libraries
from libs.db import User
from datetime import datetime
import libs.test
import libs.auth
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask import Flask
import os


app = Flask(__name__)

username = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
host = os.environ['DB_HOST']
database = os.environ['DB_NAME']

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}/{database}"
db = SQLAlchemy(app)
api = Api(app)

with app.app_context():
    db.create_all()

extraData = {
    "db": db
}

api.add_resource(libs.auth.Login, '/login', resource_class_kwargs=extraData)
api.add_resource(libs.auth.SignUp, '/signup', resource_class_kwargs=extraData)

api.add_resource(libs.test.Test, '/test', resource_class_kwargs=extraData)

if __name__ == '__main__':
    app.run(debug=True)
