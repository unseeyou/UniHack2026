from pydantic import BaseModel
from datetime import datetime
from database.trip.trip import Trip
from database.trip.point import Point as DBPoint

class Point(BaseModel):
    time: datetime

    lat: float
    lng: float

class AddTrip(BaseModel):
    start: datetime
    end: datetime

    points: list[Point]

    def to_orm_obj(self) -> Trip:
        return Trip(
            start=self.start,
            end=self.end,
            points=list(map(lambda point: DBPoint(time=point.time, lat=point.lat, lng=point.lng), self.points))
        )
