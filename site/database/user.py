from database.base import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from typing import List


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column("user_id", ForeignKey("user.id"))
    role_id: Mapped[int] = mapped_column("role_id", ForeignKey("role.id"))


class Role(db.Model, RoleMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    fs_uniquifier: Mapped[str] = mapped_column(unique=True, nullable=False)
    confirmed_at: Mapped[DateTime | None] = mapped_column(DateTime())
    roles: Mapped[List[Role]] = relationship(secondary="roles_users", backref="users")
