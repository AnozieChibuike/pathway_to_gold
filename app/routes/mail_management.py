from flask import jsonify, request, Response
from app import app
from lib.utils.tokens import *
from lib.utils.mail import *
import os
import random
from app.models.user import Users
from lib.utils.protection import protected
from flask_babel import gettext

base_url = os.getenv("BASE_URL")

@app.post("/api/send-otp")
@protected
def send_email() -> tuple[Response, int]:
    data: dict = request.json # type: ignore[assignment]
    try:
        email = data["email"]
    except:
        return jsonify({"error": gettext("Missing required data in body: email")}), 400

    try:
        user: Users = Users.get_or_404(email=email)
        otp: str = str(random.randint(1000, 9999))
        token = generate_token(email, otp)
        user.otp_token = token 
        user.save()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    subject: str = data.get("subject") or "OTP code"  # Email subject
    # template = data.get("template")  # email body
    email_body = gettext("Here is your otp: ") + otp + gettext("\nExpires in 10 minutes")
    
    message, code, status = send_mail(subject, email, body=email_body)
    if not status:
        data = {"message": message, "status": "pending"}    
    else:
        data = {"message": message, "status": "success"}
    return jsonify(data), code
