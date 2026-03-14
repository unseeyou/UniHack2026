from flask import Blueprint, request


backend = Blueprint("api", __name__)
backend.url_prefix = "/backend"


@backend.route("/add-trip-location", methods=["POST"])
def add_trip_location():
    data = request.get_json()
    print(data)
    return {"success": True}
