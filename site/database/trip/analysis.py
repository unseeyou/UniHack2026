from datetime import timedelta
from enum import StrEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db
from datetime import datetime

# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
# from database.trip.conditions import (
#     RoadCondition,
#     WeatherCondition,
#     TrafficCondition,
# )
# from database.trip.trip import Trip


class Trip(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    start: Mapped[datetime]
    end: Mapped[datetime]

    points: Mapped[list["Point"]] = relationship(back_populates="trip")
    analysis: Mapped["Analysis | None"] = relationship(back_populates="trip")


class Point(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip"] = relationship(back_populates="points")

    time: Mapped[datetime]

    lat: Mapped[float]
    lng: Mapped[float]


class RoadConditionType(StrEnum):
    Sealed = "sealed"
    Unsealed = "unsealed"
    QuietStreet = "quiet_street"
    MainRoad = "main_road"
    MultiLaned = "multi_laned"


class RoadCondition(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_id: Mapped[int] = mapped_column(ForeignKey("analysis.id"))
    analysis: Mapped["Analysis | None"] = relationship(back_populates="road_conditions")

    type: Mapped[RoadConditionType]


class WeatherConditionType(StrEnum):
    Fine = "fine"
    Raining = "raining"
    Snow = "snow"
    Icy = "icy"
    Fog = "fog"


class WeatherCondition(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_id: Mapped[int] = mapped_column(ForeignKey("analysis.id"))
    analysis: Mapped["Analysis | None"] = relationship(
        back_populates="weather_conditions"
    )

    type: Mapped[WeatherConditionType]


class TrafficConditionType(StrEnum):
    Light = "light"
    Moderate = "moderate"
    Heavy = "heavy"


class TrafficCondition(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    analysis_id: Mapped[int] = mapped_column(ForeignKey("analysis.id"))
    analysis: Mapped["Analysis | None"] = relationship(
        back_populates="traffic_conditions"
    )

    type: Mapped[TrafficConditionType]


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
