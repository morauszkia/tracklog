from datetime import datetime
from pydantic import (
    BaseModel,
    PositiveFloat,
    NonNegativeInt,
    NonNegativeFloat,
    ConfigDict,
)
from uuid import UUID


class WorkoutSchemaBase(BaseModel):
    type: str
    datetime: datetime
    start_lat: float
    start_lon: float
    distance_km: PositiveFloat
    elevation_m: NonNegativeInt
    grade: NonNegativeFloat
    moving_time_sec: PositiveFloat
    pace_min_km: PositiveFloat


class WorkoutSchemaDB(WorkoutSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
