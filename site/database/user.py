from database.base import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from typing import List
from datetime import datetime


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
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime())
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime())
    current_login_at: Mapped[datetime | None] = mapped_column(DateTime())
    last_login_ip: Mapped[str | None] = mapped_column()
    current_login_ip: Mapped[str | None] = mapped_column()
    login_count: Mapped[int | None] = mapped_column()
    roles: Mapped[List[Role]] = relationship(secondary="roles_users", backref="users")
