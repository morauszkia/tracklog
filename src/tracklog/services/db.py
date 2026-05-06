from typing import List

from tracklog.db.engine import Session
from tracklog.db.models import Workout
from tracklog.db.repo import WorkoutRepo


def record_workouts(workouts: List[Workout]):
    repo = WorkoutRepo(Session)
    for workout in workouts:
        repo.add(workout)
