from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db
from database.trip.point import Trip

class Analysis(db.Model):
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip | None"] = relationship(back_populates="analysis")

    name: Mapped[str | None]
    # conditions: Mapped[list["RoadCondition"]] = relationship()