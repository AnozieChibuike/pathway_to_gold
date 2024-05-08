"""
Bank management endpoints
"""

from app import app
from flask import request, Response, jsonify
from app.models.user import Users
from app.models.bank_accounts import BankAccount
from lib.utils.protection import protected
from lib.methods import HTTP_METHODS
import typing
import requests # type: ignore[import-untyped]
from lib.utils.checkBank import check_bank_details
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/api/bank',methods=HTTP_METHODS)
@jwt_required()
@protected
def bank() -> tuple[Response, int]:
    data: dict
    code: int
    user: Users = Users.get_or_404(id=get_jwt_identity())
    body: dict = request.json  # type: ignore[assignment]
    if request.method == 'POST':
        return create_bank(user,body)
    return jsonify(data), code

def create_bank(user: Users, body: dict[str,typing.Any]) -> tuple[Response, int]:
    data: dict
    try:
        bank_details: dict[str, str]  = body['bank'] # bank_name, account_number, bank_code
        required_fields: list[str] = ['bank_name', 'account_number', 'bank_code']
        if not all(field in bank_details for field in required_fields):
            return jsonify({'error': f'missing required field: {required_fields}'}), 400
        result, returned_name, bank_is_valid = check_bank_details(name=user.fullname,**bank_details)
        if not bank_is_valid:
            return jsonify({'error': result}), 400
        filtered_bank: dict[str, str] = {key: value for key, value in bank_details.items() if key in required_fields}
        filter_user_account: list[BankAccount] = list(filter(lambda bank: bank.bank_code == bank_details["bank_code"], user.bank_accounts))
        if len(filter_user_account) > 0:
            data = {'user': user.to_dict(), 'bank': filter_user_account[0].to_dict()}
            return jsonify(data), 201
        bank: BankAccount = BankAccount(user=user, account_name=returned_name,**filtered_bank)
        bank.save()
        data = {'user': user.to_dict(), 'bank': bank.to_dict()}
        return jsonify(data), 201
    except KeyError as e:
        return jsonify({'error': str(e)}), 400
    except TypeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/bank/all")
@protected
def all_users() -> tuple[Response, int]:
    """Get all users"""
    all_banks  = [i.to_dict() for i in BankAccount.all()]
    return jsonify(all_banks), 200