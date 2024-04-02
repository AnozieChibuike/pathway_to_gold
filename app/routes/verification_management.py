from flask import jsonify
from app import app
from flask import request
from app.models.user import Users
from lib.utils.protection import protected
    
@app.post('/api/verify-otp')
@protected
def verify_otp():
    try:
        data = request.json
        email = data['email']
        otp = data['otp']
        user = Users.get_or_404(email=email)
        message, status, code = user.verify_otp(int(otp))
        return jsonify({'message': message, 'status': status}), code
    except KeyError as e:
        return jsonify({'message': str(e)}), 400
    except ValueError as e:
        return jsonify({'message': "Otp should all be numbers"}), 400    

@app.post('/api/login')
@protected
def login():
    try:
        data = request.json
        email = data['email']
        password = data['password']
        user = Users.get_or_404(email=email)
        if user.check_password(password):
            return jsonify({'message': "Logged in"}), 200
        else:
            return jsonify({'message': "Incorrect password"}), 401
    except KeyError as e:
        return jsonify({'message': str(e) + "required"}), 400