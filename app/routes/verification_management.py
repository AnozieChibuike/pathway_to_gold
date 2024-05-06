from flask import jsonify, Response
from app import app
from flask import request
from app.models.user import Users
from lib.utils.protection import protected
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
    
@app.post('/api/verify-otp')
@jwt_required()
@protected
def verify_otp() -> tuple[Response, int]:
    try:
        data: dict[str,str] = request.json # type: ignore[assignment]
        user: Users = Users.get_or_404(id=get_jwt_identity())
        # email = user.email
        otp = str(data['otp'])
        int(otp) # Used to raise error incase
        message, status, code = user.verify_otp(otp)
        if not status:
            return jsonify({'error': message}), code
        return jsonify({'message': message, 'status': status}), code
    except KeyError as e:
        return jsonify({'error': str(e)}), 400
    except ValueError as e:
        return jsonify({'error': "Otp should all be numbers"}), 400   
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@app.post("/api/login") 
@protected
def login():
    """Login"""
    data: dict = request.json # type: ignore[assignment]
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
