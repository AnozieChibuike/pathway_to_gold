from flask import jsonify, Response
from app import app
from flask import request
from app.models.user import Users
from lib.utils.protection import protected
    
@app.post('/api/verify-otp')
@protected
def verify_otp() -> tuple[Response, int]:
    try:
        data: dict[str,str] = request.json # type: ignore[assignment]
        email = data['email']
        otp = str(data['otp'])
        int(otp) # Used to raise error incase
        user: Users = Users.get_or_404(email=email)
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

@app.post('/api/login')
@protected
def login():
    try:
        data: dict[str, str] = request.json # type: ignore[assignment]
        email = data['email']
        password = data['password']
        user: Users = Users.get_or_404(email=email)
        if user.check_password(password):
            return jsonify({'message': "Logged in"}), 200
        else:
            return jsonify({'error': "Incorrect password"}), 401
    except KeyError as e:
        return jsonify({'error': str(e) + "required"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500