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

    def list_all(self):
        session = self.session_maker()
        stmt = select(Workout)
        results = session.execute(stmt)
        for workout in results.all():
            print(workout)
        session.close()

    def reset(self):
        raise NotImplementedError()

    def stats(self, period: str = "week"):
        raise NotImplementedError("method not implemented")
