from datetime import timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
from database.trip.conditions import (
    RoadCondition,
    WeatherCondition,
    TrafficCondition,
)
from database.trip.point import Trip


class Analysis(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip | None"] = relationship(back_populates="analysis")

    name: Mapped[str | None]

    road_conditions: Mapped[set["RoadCondition"]] = relationship(
        back_populates="analysis"
    )
    weather_conditions: Mapped[set["WeatherCondition"]] = relationship(
        back_populates="analysis"
    )
    traffic_conditions: Mapped[set["TrafficCondition"]] = relationship(
        back_populates="analysis"
    )

    time_day: Mapped[timedelta]
    time_night: Mapped[timedelta]
