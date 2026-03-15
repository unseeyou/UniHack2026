from flask import send_file, render_template

from constants import app
from database.base import db
from database.trip.trip import Trip
from api.api import api
from log_book.log_book import log_book
from datetime import timedelta
from zoneinfo import ZoneInfo

@app.template_filter('sydney_time')
def sydney_time_filter(dt):
    if dt is None:
        return ""
    
    utc_tz = ZoneInfo("UTC")
    sydney_tz = ZoneInfo("Australia/Sydney")
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=utc_tz)
    
    return dt.astimezone(sydney_tz)


@app.route("/")
def index():
    trips: list[Trip] = Trip.query.all()
    analysed_trips = list(filter(lambda trip: trip.analysis is not None, trips))

    day_time = sum(map(lambda trip: trip.analysis.time_day, analysed_trips), timedelta())
    night_time = sum(map(lambda trip: trip.analysis.time_night, analysed_trips), timedelta())

    day_time_hours_logged = round(day_time.total_seconds() / 3600, 2)
    night_hours_logged = round(night_time.total_seconds() / 3600, 2)

    total_hours_logged = day_time_hours_logged + night_hours_logged

    return render_template("index.html", trips=trips, hours_logged=total_hours_logged, night_hours_logged=night_hours_logged)


@app.route("/manifest.json")
def serve_manifest():
    return send_file("manifest.json", mimetype="application/manifest+json")


@app.route("/sw.js")
def serve_sw():
    return send_file("static/js/sw.js", mimetype="application/javascript")


if __name__ == "__main__":
    app.register_blueprint(api)
    app.register_blueprint(log_book)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(
        debug=True,
        host="0.0.0.0",
    )  # ssl_context='adhoc')
