from enum import StrEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from database.trip.analysis import Analysis


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
    analysis: Mapped["Analysis | None"] = relationship(back_populates="weather_conditions")

    type: Mapped[WeatherConditionType]

    
class TrafficConditionType(StrEnum):
    Light = "light"
    Moderate = "moderate"
    Heavy = "heavy"


class TrafficCondition(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    analysis_id: Mapped[int] = mapped_column(ForeignKey("analysis.id"))
    analysis: Mapped["Analysis | None"] = relationship(back_populates="traffic_conditions")

    type: Mapped[TrafficConditionType]
