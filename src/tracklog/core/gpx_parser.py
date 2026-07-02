import math
import gpxpy
from pathlib import Path

SPORTS_WITH_ELEVATION = ["running", "hiking", "walking", "cycling"]


class EmptyGPXError(ValueError):
    """Exception raised if GPX file doesn't contain tracks"""

    pass


def parse_gpx(file_path: Path) -> dict:
    """Parse GPX file.

    Args:
        file_path (Path): path to GPX file

    Returns:
        Workout:    instance of Workout class
                    that contains information about workout
    """
    with open(file_path, "r") as file:
        gpx = gpxpy.parse(file)

    if not gpx.tracks:
        raise EmptyGPXError("No GPX tracks found")

    workout_data = {}
    workout_data["type"] = gpx.tracks[0].type
    if workout_data["type"] == "trail_running":
        workout_data["type"] = "running"
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

    return workout_data
