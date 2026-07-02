from pathlib import Path
from typing import List
from tracklog.db.models import Workout
from tracklog.db.repo import WorkoutRepo
from tracklog.db.engine import Session
from tracklog.core.gpx_parser import parse_gpx
from tracklog.core.schemas import WorkoutSchemaBase


class InvalidPathError(ValueError):
    """Exception raised for invalid path"""

    pass


def log_workout_from_path(path: Path):
    """Log one or more workouts from gpx files

    Args:
        path (Path): path to file or directory containing gpx files

    Raises:
        InvalidPathError: if path is neither directory nor gpx file
    """
    pass

    # access repo
    # log file


def process_file(file_path: Path) -> Workout:
    workout_data = parse_gpx(file_path)
    validated_data = WorkoutSchemaBase(workout_data)
    workout = Workout(**validated_data)
    return workout


def process_dir(dir_path: Path) -> list[Workout]:
    """Parse all GPX files inside a directory or its subdirectories

    Args:
        dir_path (Path): path to directory containing GPX files

    Returns:
        list[Workout]:  list of Workout instances containing information
                        about workouts
    """
    processed_workouts = []
    errors = {}
    print(f"Processing directory: {dir_path}")
    for subpath in dir_path.iterdir():
        if subpath.is_dir():
            processed_workouts.extend(process_dir(subpath))
        elif subpath.is_file() and subpath.suffix == ".gpx":
            try:
                print(f"Parsing: {subpath}")
                processed_workouts.append(process_file(subpath))
            except Exception as e:
                print(f"Error - Skipping file: {subpath}")
                errors[subpath] = e
                continue
        else:
            print(f"Skipping file: {subpath}")
            continue
    return processed_workouts
