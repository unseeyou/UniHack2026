from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

import database.trip.analysis
import database.trip.conditions
import database.trip.point
import database.trip.trip
