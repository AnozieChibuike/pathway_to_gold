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
import typing

base_url: str | None = os.getenv("BASE_URL")
app_api_key: str | None = os.getenv("x-api-key")


@app.route("/api/user", methods=HTTP_METHODS)
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
    user: Users
    if request.method == "POST":
        try:
            body: dict = request.json # type: ignore[assignment]
            return create_user(body)
        except KeyError as e:
            message = f"Could not create user, missing required parameter: {e}"
            data = {"error": message, 
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    if request.method == "DELETE":
        try:
            body = request.json # type: ignore[assignment]
            return delete_user(body)
        except KeyError as e:
            message = f"Could not delete user, missing required parameter: {e}"
            data = {"error": message,
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    if request.method == "PUT":
        try:
            body = request.json # type: ignore[assignment]
            return update_user(body)
        except KeyError as e:
            message = f"Could not update user, missing required parameter: {e}"
            data = {"error": message, 
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    args = request.args
    email = args.get("email")
    user_id = args.get("id")
    username = args.get("username")
    if user_id:
        user = Users.get_or_404(id=user_id)
        return jsonify({"data": user.to_dict()}), 200
    if email:
        user = Users.get_or_404(email=email)
        return jsonify({"data": user.to_dict()}), 200
    if username:
        user = Users.get_or_404(username=username)
        return jsonify({"data": user.to_dict()}), 200
    all_users  = [i.to_dict() for i in Users.all()]
    return jsonify(all_users), 200


def create_user(body: dict) -> tuple[Response, int]:
    fullname: str = body["fullname"]
    email: str = body["email"]
    password: str = body["password"]
    phone: str = body["phone"]
    username: str = body["username"]
    message: str
    data: dict[str, str | dict]

    if Users.get(email=email):
        message = f"User exists with supplied email"
        data = {
            "error": message,
            # "data": {},
            # "status": "error",
            # "reason": "email",
        }
        return jsonify(data), 406
    if Users.get(username=username):
        message = f"User exists with supplied username"
        data = {
            "error": message,
            # "data": {},
            # "status": "error",
            # "reason": "username",
        }
        return jsonify(data), 406
    if Users.get(phone=phone):
        message = f"User exists with supplied Phone number"
        data = {
            "error": message,
            # "data": {},
            # "status": "error",
            # "reason": "phone",
        }
        return jsonify(data), 406
    otp: str = str(random.randint(1000, 9999))
    token: str = generate_token(email, otp)
    user: Users = Users(
        fullname=fullname, email=email, username=username, phone=phone, otp_token=token
    )
    user.set_password(password)
    user.save()
    email_body: str = f"Here is your otp: {otp} Expires in 10 minutes"
    message, code, status = send_mail("Verify Email", email, body=email_body)
    if not status:
        data = {"message": message, "user": user.to_dict(), "status": "email pending"}
    else:
        data = {"message": message, "user": user.to_dict(), "status": "success"}
    return jsonify(data), code

def update_user(body: dict) -> tuple[Response, int]:
    user_id: str = body["id"]
    message: str
    user_exist: Users | None
    data: dict[str, str | dict]
    user: Users = Users.get_or_404(id=user_id)
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
    return jsonify({"data": user.to_dict()}), 201

def delete_user(body: dict) -> tuple[Response, int]:
    user_id: str = body["id"]
    user: Users = Users.get_or_404(id=user_id)
    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200

@app.post('/api/set-pin')
@protected
def set_pin() -> tuple[Response, int]:
    """Set Pin"""
    try:
        user: Users = Users.get_or_404(id=request.json['id']) # type: ignore[index]
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