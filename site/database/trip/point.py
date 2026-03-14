from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from database.trip.trip import Trip


class Point(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip"] = relationship(back_populates="points")

    time: Mapped[datetime]

    lat: Mapped[float]
    lng: Mapped[float]
