import math
import gpxpy
from tracklog.db.models import Workout


def parse_gpx(file_path: str) -> Workout:
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
    elevation = gpx.get_uphill_downhill().uphill
    workout_data["distance_km"] = round(moving_data.moving_distance) / 1000
    workout_data["elevation_m"] = math.floor(elevation)
    workout_data["grade"] = round(100 * elevation / distance, 2)
    workout_data["moving_time_sec"] = round(moving_data.moving_time, 3)
    workout_data["pace_min_km"] = (
        moving_data.moving_time / 60
    ) / workout_data["distance_km"]

    for key, value in workout_data.items():
        print(f"{key}: {value} ({type(value)})")

    workout = Workout(**workout_data)
    return workout
