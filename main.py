from flask import Flask
from flask_restful import Resource, Api
import libs.auth

app = Flask(__name__)
api = Api(app)

api.add_resource(libs.auth.Login, '/login')
api.add_resource(libs.auth.SignUp, '/signup')

if __name__ == '__main__':
    app.run(debug=True)
