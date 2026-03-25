import datetime
from tracklog.db.repo import WorkoutRepo
from tracklog.db.models import Workout


def test_add_workout(session_factory):
    repo = WorkoutRepo(session_factory)
    workout = Workout(
        type="running",
        datetime=datetime.datetime.now(),
        start_lat=47.67,
        start_lon=19.07,
        distance_km=10.5,
        elevation_m=124,
        grade=1.18,
        moving_time_sec=3586.3,
        pace_min_km=5.69,
    )
    repo.add(workout)
    assert len(repo.list_all()) == 1


def test_add_multiple_workouts(session_factory):
    repo = WorkoutRepo(session_factory)
    workout_one = Workout(
        type="running",
        datetime=datetime.datetime.now(),
        start_lat=47.67,
        start_lon=19.07,
        distance_km=10.5,
        elevation_m=124,
        grade=1.18,
        moving_time_sec=3586.3,
        pace_min_km=5.69,
    )
    workout_two = Workout(
        type="running",
        datetime=datetime.datetime.now(),
        start_lat=47.77,
        start_lon=19.37,
        distance_km=15.5,
        elevation_m=342,
        grade=2.45,
        moving_time_sec=7586.3,
        pace_min_km=4.69,
    )
    workout_three = Workout(
        type="running",
        datetime=datetime.datetime.now(),
        start_lat=44.67,
        start_lon=29.07,
        distance_km=7.5,
        elevation_m=46,
        grade=0.48,
        moving_time_sec=1586.3,
        pace_min_km=3.92,
    )

    repo.add(workout_one)
    repo.add(workout_two)
    repo.add(workout_three)
    assert len(repo.list_all()) == 3
