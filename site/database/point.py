from site.database.trip import Trip
from sqlalchemy.orm import Mapped, relationship
from site.database.base import db

class Point(db.Model):
    trip: Mapped["Trip"] = relationship(back_populates="points")

    lat: Mapped[float]
    long: Mapped[float]
