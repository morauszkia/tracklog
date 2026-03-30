from sqlalchemy import select
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

    def list_all(self) -> list[Workout]:
        session = self.session_maker()
        stmt = select(Workout).order_by(Workout.datetime.desc())
        results = session.scalars(stmt)
        workouts = [w for w in results.all()]
        session.close()
        return workouts

    def reset(self):
        raise NotImplementedError()

    def stats(self, period: str = "week"):
        raise NotImplementedError("method not implemented")
