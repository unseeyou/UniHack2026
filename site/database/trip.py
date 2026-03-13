from sqlalchemy.orm import Mapped, relationship
from database.base import db
from database.point import Point


class Trip(db.Model):
    points: Mapped[list["Point"]] = relationship(back_populates="trip")
