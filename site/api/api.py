from flask import Blueprint, request
from api.model.trip import AddTrip
from database.base import db

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/trip", methods=["POST"])
def add_trip():
    trip_model = AddTrip.model_validate_json(request.get_data())

    db.session.add(trip_model.to_orm_obj())
    db.session.commit()

    return {"success": True}
