from flask import Blueprint, render_template
from database.base import db
from database.trip.trip import Trip


log_book = Blueprint("log_book", __name__, url_prefix="/log-book")


@log_book.route("/")
def log_book_home():
    trips = Trip.query.all()
    return render_template("log_book/index.html", trips=trips)


@log_book.route("/new")
def new_log():
    return render_template("log_book/new.html")


@log_book.route("/trip/<int:trip_id>")
def view_trip(trip_id: int):
    trip = db.get_or_404(Trip, trip_id)
    return render_template("log_book/trip.html", trip=trip)
