""""
    User Management
"""

from flask import request, jsonify
from app.models.user import Users
from app import app
import os
from lib.utils.tokens import *
from lib.utils.mail import *
from lib.utils.protection import protected
from lib.methods import HTTP_METHODS
import random

base_url = os.getenv("BASE_URL")
app_api_key = os.getenv("x-api-key")


@app.route("/api/user", methods=HTTP_METHODS)
@protected
def user():
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
    if request.method == "POST":
        try:
            body = request.json
            return create_user(body)
        except KeyError as e:
            message = f"Could not create user, missing required parameter: {e}"
            data = {"error": message, 
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
    if request.method == "DELETE":
        try:
            body = request.json
            return delete_user(body)
        except KeyError as e:
            message = f"Could not delete user, missing required parameter: {e}"
            data = {"error": message,
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
    
    if request.method == "PUT":
        try:
            body = request.json
            return update_user(body)
        except KeyError as e:
            message = f"Could not update user, missing required parameter: {e}"
            data = {"error": message, 
                    # "data": {}, "status": "error"
                    }
            return jsonify(data), 406
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
    return jsonify(Users.all()), 200


def create_user(body):
    fullname = body["fullname"]
    email = body["email"]
    password = body["password"]
    phone = body["phone"]
    username = body["username"]

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
    otp = random.randint(1000, 9999)
    token = generate_token(email, otp)
    user = Users(
        fullname=fullname, email=email, username=username, phone=phone, otp_token=token
    )
    user.set_password(password)
    user.save()
    email_body = f"Here is your otp: {otp} Expires in 10 minutes"
    message, code, status = send_mail("Verify Email", email, body=email_body)
    if not status:
        data = {"message": message, "user": user.to_dict(), "status": "email pending"}, code
    else:
        data = {"message": message, "user": user.to_dict(), "status": "success"}, code
    return jsonify(data), 201


def update_user(body):
    user_id = body["id"]
    user = Users.get_or_404(id=user_id)
    if "fullname" in body:
        user.fullname = body["fullname"]
    # if "email" in body:
        user_exist = Users.get(email=body["email"])
        if user_exist:
            message = f"User exists with supplied email"
            data = {
                "message": message,
                "data": {},
                "status": "error",
                "reason": "email",
            }
            return jsonify(data), 406
        user.email = body["email"]
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
        user_exist = Users.get(phone=body["phone"])
        if user_exist:
            message = f"User exists with supplied Phone number"
            data = {
                "message": message,
                "data": {},
                "status": "error",
                "reason": "phone",
            }
            return jsonify(data), 406
        user.phone = body["phone"]
    if "pin" in body:
        user.pin = body["pin"]
    user.save()
    return jsonify({"data": user.to_dict()}), 201

def delete_user(body):
    user_id = body["id"]
    user = Users.get_or_404(id=user_id)
    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200
