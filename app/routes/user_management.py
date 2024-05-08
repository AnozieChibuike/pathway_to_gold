""""
    User Management
"""

from flask import request, jsonify, Response
from app.models.user import Users
from app import app
import os
from lib.utils.tokens import *
from lib.utils.mail import *
from lib.utils.protection import protected
from lib.methods import HTTP_METHODS
import random
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

base_url: str | None = os.getenv("BASE_URL")
app_api_key: str | None = os.getenv("x-api-key")


@app.route("/api/user/all")
@protected
def _all_users() -> tuple[Response, int]:
    """Get all users"""
    all_users = [i.to_dict() for i in Users.all()]
    return jsonify(all_users), 200

@app.route("/api/user", methods=HTTP_METHODS)
@jwt_required()
@protected
def user() -> tuple[Response, int]:
    """User Management

    methods:
        GET:
            description - Get a user from db
            parameters:
                id -- ID of user <str>
                email -- email of user <str>
                username -- username of user <str>

            Return: returns a User json if exists | handle if not exists
        POST:
            description - Creates a new user
            json:
                fullname (required) <str>
                email (required) <str>
                password (required) <str>
                username <str>
                pin <str>
            Return: returns User json if created success | handle if not created
        PUT:
            description - Update a user
            parameters:
                id -- ID of user (required) <str>
            json:
                fullname <str>
                email <str>
                password (required) <str>
                username <str>
                pin <str>
    """
    message: str
    data: dict
    user: Users = Users.get_or_404(id=get_jwt_identity())
    if request.method == "POST":
        return jsonify({'message': "Call <post> '/api/user/create' instead"}), 500
    if request.method == "DELETE":
        try:
            return delete_user(user)
        except Exception as e:
            return jsonify({'error': str(e)}), 500   
    if request.method == "PUT":
        try:
            body: dict = request.json # type: ignore[assignment]
            return update_user(user,body)
        except KeyError as e:
            message = f"Could not update user, missing required parameter: {e}"
            data = {"error": message, 
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    return jsonify(user.to_dict()), 200

def update_user(user: Users,body: dict) -> tuple[Response, int]:
    message: str
    user_exist: Users | None
    data: dict[str, str | dict]
    if "fullname" in body:
        user.fullname = body["fullname"]
    # if "email" in body:
    #     user_exist = Users.get(email=body["email"])
    #     if user_exist:
    #         message = f"User exists with supplied email"
    #         data = {
    #             "error": message,
    #             # "data": {},
    #             # "status": "error",
    #             # "reason": "email",
    #         }
    #         return jsonify(data), 406
    #     user.email = body["email"]
    if "password" in body:
        user.set_password(body["password"])
    if "username" in body:
        user_exist = Users.get(username=body["username"])
        if user_exist:
            message = f"User exists with supplied username"
            data = {
                "error": message,
                # "data": {},
                # "status": "error",
                # "reason": "username",
            }
            return jsonify(data), 406
        user.username = body["username"]
    # if "phone" in body:
    #     user_exist = Users.get(phone=body["phone"])
    #     if user_exist:
    #         message = f"User exists with supplied Phone number"
    #         data = {
    #             "error": message,
    #             # "data": {},
    #             # "status": "error",
    #             # "reason": "phone",
    #         }
    #         return jsonify(data), 406
    #      user.phone = body["phone"]
    if "pin" in body:
        if len(body["pin"]) != 4:
            message = f"Pin must be 4 digits"
            data = {
                "error": message,
                # "data": {},
                # "status": "error",
                # "reason": "pin",
            }
            return jsonify(data), 406
        user.pin = body["pin"]
    user.save()
    return jsonify({"message": "User updated"}), 201

def delete_user(user: Users) -> tuple[Response, int]:
    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200



@app.post('/api/set-pin')
@jwt_required()
@protected
def set_pin() -> tuple[Response, int]:
    """Set Pin"""
    try:
        user: Users = Users.get_or_404(id=get_jwt_identity()) # type: ignore[index]
        user.pin = request.json['pin'] # type: ignore[index]
        user.save()
        return jsonify({"message": "Pin set successfully"}), 200
    except KeyError as e:
        message: str = f"Could not set pin, missing required parameter: {e}"
        data: dict = {"error": message,
                # "data": {}, "status": "error"
                }
        return jsonify(data), 406
    except Exception as e:
        return jsonify({'error': str(e)}), 500