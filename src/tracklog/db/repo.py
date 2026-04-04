import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from tracklog.db.models import Workout


class WorkoutRepo:
    def __init__(self, session_maker: Session):
        self.session_maker = session_maker

    def add(self, workout: Workout):
        session = self.session_maker()
        try:
            session.add(workout)
            session.commit()
        finally:
            session.close()

    def list_all(self, limit: int) -> list[Workout]:
        session = self.session_maker()
        stmt = select(Workout).order_by(Workout.datetime.desc())
        if limit:
            stmt = stmt.limit(limit)

        results = session.scalars(stmt)
        workouts = [w for w in results.all()]
        session.close()
        return workouts

    def reset(self):
        raise NotImplementedError()

    def stats(self, period: str):
        tod = datetime.date.today()
        start_date = None
        if period == "week":
            start_date = tod - datetime.timedelta(days=tod.weekday())
        elif period == "month":
            start_date = datetime.date(tod.year, tod.month, 1)
        elif period == "ytd":
            start_date = datetime.date(tod.year, 1, 1)

        session = self.session_maker()
        stmt = (
            select(
                func.sum(Workout.distance_km).label("total_dist"),
                func.sum(Workout.moving_time_sec).label("total_time"),
                func.sum(Workout.elevation_m).label("total_elevation"),
                func.count(Workout.id).label("workout_count"),
            )
            .select_from(Workout)
            .filter(
                func.DATE(Workout.datetime) >= func.coalesce(start_date, 0)
            )
        )

        result = session.execute(stmt).fetchone()._asdict()
        result["average_pace"] = (result["total_time"] / 60) / result[
            "total_dist"
        ]
        result["average_grade"] = (
            0.1 * result["total_elevation"] / result["total_dist"]
        )

        return result
