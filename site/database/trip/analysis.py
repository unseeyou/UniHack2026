from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import db

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from database.trip.point import Trip

class Analysis(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    trip_id: Mapped[int] = mapped_column(ForeignKey("trip.id"))
    trip: Mapped["Trip | None"] = relationship(back_populates="analysis")

    name: Mapped[str | None]
    # conditions: Mapped[list["RoadCondition"]] = relationship()