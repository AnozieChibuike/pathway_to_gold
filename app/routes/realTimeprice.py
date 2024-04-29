from flask import jsonify, request, Response
from app import app
import os
from lib.utils.path_crypto import client

base_url = os.getenv("BASE_URL")


@app.get("/api/price")
def coins() -> tuple[Response, int]:
    data: dict = request.args  # type: ignore[assignment]
    try:
        coin = data["coin"]
    except:
        return jsonify({"error": "Missing required argument: coin"}), 400

    try:
        response: dict = client.get_pair_price(coin)
        return jsonify({"body": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
