import jwt
import os
from flask import request

def isAuthed(func):
    def wrapper(*args, **kwargs):
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

        result = func(userHeader=data, *args, **kwargs)

        return result
    return wrapper