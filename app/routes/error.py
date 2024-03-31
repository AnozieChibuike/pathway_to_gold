from app import app
from flask import jsonify

@app.errorhandler(404)
def page_not_found(error):
    # You can customize the response here
    return jsonify({"message": "Data you are looking for cannot be found: {}".format(error)})


@app.errorhandler(500)
def server_error(error):
    # You can customize the response here
    return jsonify({"message": f"Server issue: {error}"}), 500

@app.errorhandler(415)
def bad_content_type(error):
    return jsonify({"message": f"Unsupported content-type: {error}"}), 415

@app.errorhandler(405)
def bad_method(error):
    return jsonify({"message": f"Unsupported method: {error}"}), 415
