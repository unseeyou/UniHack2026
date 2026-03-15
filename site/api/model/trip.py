from pydantic import BaseModel
from datetime import datetime
from database.trip.trip import Trip, Point as DBPoint


class Point(BaseModel):
    time: datetime

    lat: float
    lng: float


class AddTrip(BaseModel):
    start: datetime
    end: datetime

    odometer_start: float
    odometer_end: float

    points: list[Point]

    def to_orm_obj(self) -> Trip:
        trip = Trip(
            start=self.start,
            end=self.end,
            odometer_start=self.odometer_start,
            odometer_end=self.odometer_end,
            points=list(
                map(
                    lambda point: DBPoint(
                        time=point.time, lat=point.lat, lng=point.lng
                    ),
                    self.points,
                )
            ),
        )

        return trip
