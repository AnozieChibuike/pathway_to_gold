from flask import request, jsonify
from app.models.user import Users
from app import app
import os

from lib.utils.protection import protected


HTTP_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
]

app_api_key = os.getenv("x-api-key")


@app.errorhandler(404)
def page_not_found(error):
    # You can customize the response here
    return jsonify({"message": "Data you are looking for cannot be found"})


@app.errorhandler(500)
def page_not_found(error):
    # You can customize the response here
    return jsonify({"message": "Server issue"}), 500


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
            fullname = body["fullname"]
            email = body["email"]
            password = body["password"]
            username = body.get("username")
            pin = body.get("pin")

            if Users.get(email=email):
                message = f"User exists with supplied email"
                data = {"message": message, "data": {}, "status": "error"}
                return jsonify(data), 406
            if Users.get(username=username):
                message = f"User exists with supplied username"
                data = {"message": message, "data": {}, "status": "error"}
                return jsonify(data), 406

            user = Users(fullname=fullname, email=email, username=username, pin=pin)
            user.set_password(password)
            user.save()
            message = f"User created successfully"
            data = {"message": message, "data": user.to_dict(), "status": "success"}
            return jsonify(data), 201

        except KeyError as e:
            message = f"Could not create user, missing required parameter: {e}"
            data = {"message": message, "data": {}, "status": "error"}
            return jsonify(data), 406
    args = request.args
    email = args.get("email")
    user_id = args.get("id")
    username = args.get("username")
    if user_id:
        user = Users.get(id=user_id)
        if not user:
            return jsonify({"data": {}}), 404
        return jsonify({"data": user.to_dict()}), 200
    if email:
        user = Users.get(email=email)
        if not user:
            return jsonify({"data": {}}), 404
        return jsonify({"data": user.to_dict()}), 200
    if username:
        user = Users.get(username=username)
        if not user:
            return jsonify({"data": {}}), 404
        return jsonify({"data": user.to_dict()}), 200
    return jsonify(None), 200
