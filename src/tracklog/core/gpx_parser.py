import math
import gpxpy
from pathlib import Path
from tracklog.db.models import Workout


SPORTS_WITH_ELEVATION = ["running", "hiking", "walking", "cycling"]


def parse_gpx(file_path: Path) -> Workout:
    with open(file_path, "r") as file:
        gpx = gpxpy.parse(file)

    workout_data = {}
    workout_data["type"] = gpx.tracks[0].type
    workout_data["datetime"] = gpx.get_time_bounds().start_time
    start_coordinates = gpx.get_location_at(workout_data["datetime"])[0]
    workout_data["start_lat"] = start_coordinates.latitude
    workout_data["start_lon"] = start_coordinates.longitude
    moving_data = gpx.get_moving_data()
    distance = moving_data.moving_distance
    workout_data["distance_km"] = round(moving_data.moving_distance) / 1000

    elevation = (
        gpx.get_uphill_downhill().uphill
        if workout_data["type"] in SPORTS_WITH_ELEVATION
        else 0
    )

    workout_data["elevation_m"] = math.floor(elevation)
    workout_data["grade"] = round(100 * elevation / distance, 2)
    workout_data["moving_time_sec"] = round(moving_data.moving_time, 3)
    workout_data["pace_min_km"] = (
        moving_data.moving_time / 60
    ) / workout_data["distance_km"]

    workout = Workout(**workout_data)
    return workout


def process_dir(dir_path: Path) -> list[Workout]:
    parsed_workouts = []
    print(f"Processing directory: {dir_path}")
    for subpath in dir_path.iterdir():
        if subpath.is_dir():
            parsed_workouts.extend(process_dir(subpath))
        elif subpath.is_file() and subpath.suffix == ".gpx":
            print(f"Parsing: {subpath}")
            parsed_workouts.append(parse_gpx(subpath))
        else:
            print(f"Skipping file: {subpath}")
            continue
    return parsed_workouts
