import datetime
import uuid
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List, Dict
from tracklog.db.models import Workout


class WorkoutRepo:
    def __init__(self, session_maker: Session):
        self.session_maker = session_maker

    def add(self, workout: Workout) -> None:
        """Add workout to database"""
        session = self.session_maker()
        try:
            session.add(workout)
            session.commit()
        finally:
            session.close()

    def list_all(self, limit: int) -> List[Workout]:
        """List workouts in the database"""
        session = self.session_maker()
        stmt = select(Workout).order_by(Workout.datetime.desc())
        if limit:
            stmt = stmt.limit(limit)

        results = session.scalars(stmt)
        workouts = [w for w in results.all()]
        session.close()
        return workouts

    def get_workout(self, id: uuid.uuid7) -> Workout:
        """Find workout by id."""
        session = self.session_maker()
        stmt = select(Workout).where(Workout.id == id)
        result = session.scalar(stmt)
        return result

    def stats(self, period: str) -> List[Dict]:
        """Return stats grouped by workout type."""
        start_date = self._get_period_cutoff(period)
        try:
            session = self.session_maker()
            stmt = (
                select(
                    Workout.type,
                    func.coalesce(func.sum(Workout.distance_km), 0).label(
                        "total_dist"
                    ),
                    func.coalesce(
                        func.sum(Workout.moving_time_sec),
                        0,
                    ).label("total_time"),
                    func.coalesce(
                        func.sum(Workout.elevation_m),
                        0,
                    ).label("total_elevation"),
                    func.count(Workout.id).label("workout_count"),
                )
                .select_from(Workout)
                .group_by(Workout.type)
                .where(func.DATE(Workout.datetime) >= start_date)
            )

            results = session.execute(stmt).fetchall()

            stats_by_type = []

            for row in results:
                row_dict = row._asdict()
                print(row_dict)
                total_dist = float(row_dict["total_dist"] or 0)
                total_time = float(row_dict["total_time"] or 0)

                stats = {
                    "type": row_dict["type"],
                    "total_dist_km": total_dist,
                    "total_time": total_time,
                    "total_elevation_m": int(row_dict["total_elevation"] or 0),
                    "workout_count": int(row_dict["workout_count"]),
                }

                if total_dist > 0:
                    stats["avg_pace_min_km"] = (total_time / 60) / total_dist
                    stats["avg_grade_pct"] = (
                        0.1 * stats["total_elevation_m"] / total_dist
                    )

                stats_by_type.append(stats)

            return stats_by_type

        finally:
            session.close()

    def _get_period_cutoff(self, period: str) -> datetime.date:
        # TODO: use SQL Functions (sqlite, postgresql)
        tod = datetime.date.today()
        start_date = datetime.date(1900, 1, 1)
        if period == "week":
            start_date = tod - datetime.timedelta(days=tod.weekday())
        elif period == "month":
            start_date = datetime.date(tod.year, tod.month, 1)
        elif period == "ytd":
            start_date = datetime.date(tod.year, 1, 1)
        return start_date

    def reset(self):
        raise NotImplementedError()
