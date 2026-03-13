import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid


class Base(DeclarativeBase):
    pass


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[str]
    datetime: Mapped[datetime.datetime]
    start_lat: Mapped[float]
    start_lon: Mapped[float]
    distance_km: Mapped[float]
    elevation_m: Mapped[int]
    grade: Mapped[float]
    moving_time_sec: Mapped[float]
    pace_min_km: Mapped[float]

    def __repr__(self):
        return f"Workout({self.type}: {self.distance_km}, {self.elevation_m}+)"
