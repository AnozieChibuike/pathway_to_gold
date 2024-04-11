from app import app
from flask import request, Response, jsonify
from app.models.user import Users
from app.models.bank_accounts import BankAccount
from lib.utils.protection import protected
from lib.methods import HTTP_METHODS
import typing
import requests # type: ignore[import-untyped]
from lib.utils.checkBank import check_bank_details

@app.route('/api/bank',methods=HTTP_METHODS)
@protected
def bank() -> tuple[Response, int]:
    data: dict
    code: int
    body: dict = request.json  # type: ignore[assignment]
    if request.method == 'POST':
        return create_bank(body)
    return jsonify(data), code

def create_bank(body: dict[str,typing.Any]) -> tuple[Response, int]:
    data: dict
    try:
        userId: str = body['id']
        bank_details: dict[str, str]  = body['bank'] # bank_name, account_number, bank_code
        required_fields: list[str] = ['bank_name', 'account_number', 'bank_code']
        if not all(field in bank_details for field in required_fields):
            return jsonify({'error': f'missing required field: {required_fields}'}), 400
        user: Users = Users.get(id=userId)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        result, returned_name, bank_is_valid = check_bank_details(name=user.fullname,**bank_details)
        if not bank_is_valid:
            return jsonify({'error': result}), 400
        bank: BankAccount = BankAccount(user=user, account_name=returned_name,**bank_details)
        bank.save()
        data = {'user': user.to_dict(), 'bank': bank.to_dict()}
        return jsonify(data), 201
    except KeyError as e:
        return jsonify({'error': str(e)}), 400
    except TypeError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

