from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

from database.trip.analysis import Analysis


class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    start: Mapped[datetime]
    end: Mapped[datetime]

    points: Mapped[list["Point"]] = relationship(back_populates="trip")
    analysis: Mapped["Analysis | None"] = relationship(back_populates="trip", lazy="joined")



class Point(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip"] = relationship(back_populates="points", lazy="joined")

    time: Mapped[datetime]

    lat: Mapped[float]
    lng: Mapped[float]
