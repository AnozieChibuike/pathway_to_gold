from flask import Flask, request, jsonify, make_response
from functools import wraps
import os

APP_API_KEY = os.getenv('x-api-key')

def protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Access the API key from the request headers
        api_key = request.headers.get('X-API-KEY')
        
        # Check if the API key is present and matches the app's API key
        if api_key != APP_API_KEY:
            # Return an unauthorized error response
            return make_response(jsonify({"error": "Unauthorized"}), 401)
        
        # Call the decorated function if the API key is valid
        return f(*args, **kwargs)
    
    return decorated_function
