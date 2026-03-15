from datetime import datetime
from math import asin, cos, radians, sin, sqrt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

from database.trip.analysis import Analysis


class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    start: Mapped[datetime]
    end: Mapped[datetime]

    odometer_start: Mapped[int]
    odometer_end: Mapped[int]

    points: Mapped[list["Point"]] = relationship(back_populates="trip", lazy="joined")
    analysis: Mapped["Analysis | None"] = relationship(back_populates="trip", lazy="joined")

    def get_dist(self) -> float:
        return sum(map(lambda tup: tup[0].dist(tup[1]), zip(self.points, self.points[1:])))



class Point(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip"] = relationship(back_populates="points", lazy="joined")

    time: Mapped[datetime]

    lat: Mapped[float]
    lng: Mapped[float]

    def dist(self, other: "Point") -> float:
        """Distance is in kilometres"""
        lng1, lat1, lng2, lat2 = map(radians, [self.lng, self.lat, other.lng, other.lat])

        # Haversine formula 
        dlon = lng2 - lng1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return c * r
