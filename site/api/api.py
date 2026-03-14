from flask import Blueprint, request
from api.model.trip import AddTrip
from database.base import db
from database.trip.analysis import Trip
from flask import jsonify

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/trip", methods=["POST"])
def add_trip():
    trip_model = AddTrip.model_validate_json(request.get_data())

    db.session.add(trip_model.to_orm_obj())
    db.session.commit()

    return {"success": True}


@api.route("/get_trips", methods=["GET"])
def get_all_trips():
    trips = Trip.query.all()
    trips_data = []

    for trip in trips:
        formatted_points = []
        for p in trip.points:
            formatted_points.append(
                {
                    "lat": p.lat,
                    "lng": p.lng,
                    "time": p.time.isoformat() if p.time else None,
                }
            )

        trips_data.append(
            {
                "id": trip.id,
                "start": trip.start.isoformat() if trip.start else None,
                "end": trip.end.isoformat() if trip.end else None,
                "points": formatted_points,
            }
        )

    return jsonify(trips_data)
