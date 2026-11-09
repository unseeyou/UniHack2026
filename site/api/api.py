from flask import Blueprint, redirect, request, jsonify
from flask_security import auth_required
from api.model.trip import AddTrip
from database.base import db
from database.trip.trip import Trip
import trip_analyser.analyser as analyser

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/trip", methods=["POST"])
# @auth_required()
def add_trip():
    print("HIT /api/trip ROUTE!")
    print(request.get_data())

    trip_model = AddTrip.model_validate_json(request.get_data())
    trip = trip_model.to_orm_obj()

    db.session.add(trip)
    db.session.commit()

    return jsonify({})


@api.route("/trip/<int:trip_id>/analyse", methods=["POST"])
# @auth_required()
def analyse_trip(trip_id: int):
    trip = db.get_or_404(Trip, trip_id)

    if trip.analysis is not None:
        return redirect(f"/log-book/trip/{trip_id}")

    analyser.analyse(trip)

    return redirect(f"/log-book/trip/{trip_id}")
