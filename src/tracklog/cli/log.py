from click import ClickException
from pathlib import Path

# from rich.console import Console
# from gpxpy.gpx import GPXException
from tracklog.services.workouts import (
    process_dir,
    record_workouts,
)
from tracklog.db.engine import Session
from tracklog.db.repo import WorkoutRepo


def log_workout_from_path(path: Path):
    """Log one or more workouts from gpx files

    Args:
        path (Path): path to file or directory containing gpx files

    Raises:
        ClickException: for any user-facing error
            (e.g. nonexistent of invalid path, parsing error, etc.)
    """
    path = Path(path).resolve()
    if not path.exists():
        raise ClickException(f"Invalid path: {path}")

    try:
        processed_data = process_dir(path)
        print(f"{len(processed_data["workouts"])} workouts processed")
        if len(processed_data["errors"]):
            print("We encountered the following errors:")
        # for error in errors print error

        print("Storing workouts")
        repo = WorkoutRepo(Session)
        for workout in processed_data["workouts"]:
            repo.add(workout)
        print("Workouts stored.  \
            Run `tracklog list` to view recently logged workouts")
    except Exception as e:
        raise ClickException(f"Something went wrong: {str(e)}")
