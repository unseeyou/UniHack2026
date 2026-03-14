from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

from database.trip.point import Point
from database.trip.analysis import Analysis


class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    points: Mapped[list["Point"]] = relationship(back_populates="trip")
    analysis: Mapped["Analysis"] = relationship(back_populates="trip")
