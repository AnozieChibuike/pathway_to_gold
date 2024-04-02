from flask import jsonify, request
from app import app
from lib.utils.tokens import *
from lib.utils.mail import *
import os
import random
from app.models.user import Users
from lib.utils.protection import protected

base_url = os.getenv("BASE_URL")


@app.post("/api/send-otp")
@protected
def send_email():
    data = request.json
    try:
        email = data["email"]
    except:
        return jsonify({"error": "Missing required data in body: email"}), 400

    user = Users.get_or_404(email=email)
    otp = random.randint(1000, 9999)
    token = generate_token(email, otp)
    user.otp_token = token
    user.save()
    
    subject = data.get("subject") or "OTP code"  # Email subject
    template = data.get("template")  # email body
    email_body = f"Here is your otp: {otp} Expires in 10 minutes"
    
    message, code, status = send_mail(subject, email, body=email_body)
    if not status:
        data = {"message": message, "status": "pending"}, code    
    else:
        data = {"message": message, "status": "success"}, code
    return jsonify(data), 200
