from flask import jsonify, request, Response
from app import app
from lib.utils.tokens import *
from lib.utils.mail import *
from lib.utils.sms import send_code_to_sms
import os
import random
from app.models.user import Users
from lib.utils.protection import protected
from flask_jwt_extended import get_jwt_identity, jwt_required
from lib.templates import otp as send_code

base_url = os.getenv("BASE_URL")

@app.post("/api/send-otp")
@protected
def send_email() -> tuple[Response, int]:
    email = request.json.get('email','')
    user: Users = Users.get_or_404(email=email)
    try:
        otp: str = str(random.randint(1000, 9999))
        token = generate_token(user.email, otp)
        user.otp_token = token 
        user.save()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    # subject: str = request.json.get("subject") or "OTP code"  # Email subject
    # # template = data.get("template")  # email body
    # email_body = "Here is your otp: " + otp + "\nExpires in 10 minutes"
    
    message, code, status = send_mail("OTP Request", email, html=send_code(code=otp), image='logo.png')
    if not status:
        data = {"message": message, "status": "pending"}    
    else:
        data = {"message": message, "status": "success"}
    return jsonify(data), code    
@app.post("/api/send-otp-sms")
@protected
def send_phone() -> tuple[Response, int]:
    phone = request.json.get('phone','')
    if not phone:
        return jsonify(error='Specify <phone> in json'), 403
    _ = Users.get_or_404(phone=phone)
    message, status = send_code_to_sms(phone=phone)
    if not status:
        return jsonify(error=message), 400
    return jsonify(message=message), 200