import random
from flask import jsonify, Response
from app import app
from flask import request
from app.models.user import Users
from lib.utils.mail import send_mail
from lib.utils.protection import protected
from lib.utils.sms import verify_code
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from lib.utils.tokens import generate_token, verify_token
from lib.templates import sign_up as su
from lib.templates import otp as send_code
from lib.utils.generate_qr import generate_qr, verify_totp_code

@app.post("/api/verify-otp")
@protected
def verify_otp() -> tuple[Response, int]:
    data: dict[str, str] = request.json  # type: ignore[assignment]

    try:
        email = request.json.get("email", "")
        user: Users = Users.get_or_404(email=email)
        # email = user.email
        otp = str(data["otp"])
        int(otp)  # Used to raise error incase
        message, status, code = user.verify_otp(otp)
        if not status:
            return jsonify({"error": message}), code
        return jsonify({"message": message, "status": status}), code
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Otp should all be numbers"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.post("/api/verify-otp-sms")
@protected
def verify_otp_sms() -> tuple[Response, int]:
    data: dict[str, str] | None = request.json
    try:
        otp = data['otp']
        int(otp)
        phone = data['phone']
        user = Users.get_or_404(phone=phone)
        if not user.otp_token:
            return jsonify(error="User has not requested OTP"), 400
        data, code, status = verify_token(user.otp_token)
        if not status:
            return jsonify(error=data['reason']), code
        payload: dict = data["payload"]
        if payload["otp"] != otp:
            return jsonify(error="Invalid OTP"), 400
        user.otp_token = ''
        user.save()
        return jsonify(message="OTP Verified"), 200
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": "Otp should all be numbers"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/login")
@protected
def login():
    """Login"""
    data: dict = request.json  # type: ignore[assignment]
    try:
        email: str = data["email"]
        password: str = data["password"]
    except KeyError as e:
        return jsonify({"error": f"Missing required parameter: {e}"}), 406
    try:
        user: Users = Users.get_or_404(email=email)
        if user.check_password(password):
            token: str = create_access_token(identity=user.id)
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/api/signup")
@protected
def signup() -> tuple[Response, int]:
    body: dict = request.json  # type: ignore[assignment]
    return create_user(body)


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
    # email_body: str = f"Here is your otp: {otp} Expires in 10 minutes"
    send_mail("Welcome", email, html=su(user.fullname), image='logo.png')
    message, code, status = send_mail("Verify Email", email, html=send_code(code=otp), image='logo.png')
    # token: str = create_access_token(identity=user.id)
    if not status:
        data = {"message": message, "body": user.to_dict(), "status": "email pending"}
    else:
        data = {"message": message, "body": user.to_dict(), "status": "success"}
    return jsonify(data), code

@app.post("/api/activate-totp")
@jwt_required()
@protected
def activate_totp() -> tuple[Response, int]:
    try:
        user: Users = Users.get_or_404(id=get_jwt_identity())
        qrbase = generate_qr(user)
        return jsonify(body=qrbase), 200
    except KeyError as e:
        return jsonify({"error": f"Missing required parameter: {e}"}), 406
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.post("/api/verify-totp")
@jwt_required()
@protected
def verify_totp() -> tuple[Response, int]:
    data: dict = request.json
    try:
        user: Users = Users.get_or_404(id=get_jwt_identity())
        code = data['code']
        message, status = verify_totp_code(user, code)
        if not status:
            return jsonify(error=message), 400
        return jsonify(message=message), 200
    except KeyError as e:
        return jsonify({"error": f"Missing required parameter: {e}"}), 406
    except Exception as e:
        return jsonify({"error": str(e)}), 500