from sqlalchemy.orm import Mapped, relationship
from site.database.base import db
from site.database.point import Point

class Trip(db.Model):
    points: Mapped[list["Point"]] = relationship(back_populates="trip")
