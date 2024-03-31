from flask import jsonify, request
from app import app
from lib.utils.tokens import *
from lib.utils.mail import *
import os

base_url = os.getenv("BASE_URL")


@app.post("/api/send-mail")
def send_email():
    data = request.json
    try:
        recipients = data["recipients"]
        if not isinstance(recipients, list):
            jsonify({"message": "Recipients must be an array of emails"}), 400
    except:
        return jsonify({"message": "Missing required data in body: email"}), 400

    subject = data.get("subject")  # Email subject
    recipients = data.get("recipients")  # List of emails
    reason = data.get("reason")  # email body
    if reason.lower() == "magic_link":
        total = []
        not_sent = []
        for email in recipients:
            token = generate_token(email)
            body = f"Here is your verification link : {base_url}/verify?token={token}\nExpires in 1 hour"
            message, code, status = send_mail(subject, recipients, body)
            if not status:
                not_sent.append(email)
            total.append(status)
        if all(total):
            return jsonify(message), code
        else:
            return jsonify(
                {"message": "not all emails was sent", "email_not_sent": not_sent}
            )
