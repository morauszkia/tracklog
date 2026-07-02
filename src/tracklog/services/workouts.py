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


# TODO: Error class
class ProcessWorkoutFileError(Exception):
    """Exception raised for errors during file processing"""

    pass


def process_file(file_path: Path) -> Workout:
    workout_data = parse_gpx(file_path)
    validated_data = WorkoutSchemaBase(workout_data)
    workout = Workout(**validated_data)
    return workout


def process_dir(dir_path: Path) -> dict:
    """Process all GPX files inside a directory or its subdirectories

    Args:
        dir_path (Path): path to directory containing GPX files

    Returns:
        dict:   a dictionary with the list of Workout instances
                and a dictionary of errors mapped to subpath
    """
    output = {"workouts": [], "errors": {}}
    print(f"Processing directory: {dir_path}")
    for subpath in dir_path.iterdir():
        if subpath.is_dir():
            output["workouts"].extend(process_dir(subpath))
        elif subpath.is_file() and subpath.suffix == ".gpx":
            try:
                print(f"Parsing: {subpath}")
                output["workouts"].append(process_file(subpath))
            except Exception as e:
                print(f"Error - Skipping file: {subpath}")
                output["errors"]["subpath"] = e
                continue
        else:
            print(f"Skipping file: {subpath}")
            continue
    return output


def record_workouts(workouts: List[Workout]):
    repo = WorkoutRepo(Session)
    for workout in workouts:
        repo.add(workout)
