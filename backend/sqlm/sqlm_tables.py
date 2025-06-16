from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from sqlalchemy import MetaData, String, Boolean, DateTime, ForeignKey
from geoalchemy2 import Geometry
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=True)

    items: Mapped[list[RoadFeature]] = relationship(back_populates="user", lazy="selectin")

class RoadFeature(Base):
    __tablename__ = "road_features"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    highway: Mapped[str] = mapped_column(String, nullable=True)
    ref: Mapped[str] = mapped_column(String, nullable=True)
    lanes: Mapped[str] = mapped_column(String, nullable=True)
    oneway: Mapped[str] = mapped_column(String, nullable=True)
    length: Mapped[str] = mapped_column(String, nullable=True)
    width: Mapped[str] = mapped_column(String, nullable=True)

    geometry: Mapped[str] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=4326), nullable=False
    )

    is_current: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=None, nullable=True)

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="items", lazy="selectin")
