from flask import Blueprint, request


backend = Blueprint("api", __name__)
backend.url_prefix = "/api"


@backend.route("/trip", methods=["POST"])
def add_trip():
    data = request.get_json()
    print(data)
    return {"success": True}
