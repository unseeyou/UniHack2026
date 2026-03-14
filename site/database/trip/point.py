from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db
from database.trip.trip import Trip

class Point(db.Model):
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip"] = relationship(back_populates="points")

    lat: Mapped[float]
    long: Mapped[float]
