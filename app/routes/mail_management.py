from flask import jsonify, request, Response
from app import app
from lib.utils.tokens import *
from lib.utils.mail import *
import os
import random
from app.models.user import Users
from lib.utils.protection import protected
from flask_jwt_extended import get_jwt_identity, jwt_required

base_url = os.getenv("BASE_URL")

@app.post("/api/send-otp")
@jwt_required()
@protected
def send_email() -> tuple[Response, int]:
    user: Users = Users.get_or_404(id=get_jwt_identity())
    try:
        otp: str = str(random.randint(1000, 9999))
        token = generate_token(user.email, otp)
        user.otp_token = token 
        user.save()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    subject: str = request.json.get("subject") or "OTP code"  # Email subject
    # template = data.get("template")  # email body
    email_body = "Here is your otp: " + otp + "\nExpires in 10 minutes"
    
    message, code, status = send_mail(subject, user.email, body=email_body)
    if not status:
        data = {"message": message, "status": "pending"}    
    else:
        data = {"message": message, "status": "success"}
    return jsonify(data), code
