import datetime as dt
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from tracklog.db.models import Workout

WORKOUT_ICONS = {
    "running": "🏃",
    "hiking": "🚶",
    "cycling": "🚴",
    "walking": "🚶",
    "Canoeing": "🚣",
}

DEFAULT_ICON = "🤸‍♀️"


def format_pace(pace_min: float):
    seconds = int(pace_min * 60)
    minutes = seconds // 60
    seconds = minutes % 60
    return f"{minutes}:{seconds:02d}"


def render_workout_list(workouts: List[Workout]) -> None:
    console = Console()
    table = Table(title="YOUR WORKOUTS", box=box.ROUNDED)
    table.add_column("📅")
    table.add_column("🕒")
    table.add_column("Activity")
    table.add_column("Distance")
    table.add_column("Elevation")
    table.add_column("Time")
    table.add_column("ID")

    for workout in workouts:
        workout_icon = WORKOUT_ICONS.get(workout.type, DEFAULT_ICON)
        table.add_row(
            f"{workout.datetime.strftime('%Y-%m-%d (%a)')}",
            f"{workout.datetime.strftime('%H:%M')}",
            f"{workout_icon} {workout.type}",
            f"{workout.distance_km:.1f}km",
            f"{workout.elevation_m}m",
            f"{dt.timedelta(
                seconds=round(workout.moving_time_sec)
                )}",
            f"{workout.id}",
        )
    console.print(table)


def render_stats_table(stats: List[Dict], period: str) -> None:
    console = Console()
    table = Table(
        title=f"STATS FOR PERIOD: {period.upper()}",
        box=box.ROUNDED,
    )
    table.add_column("Sport")
    table.add_column("Workouts")
    table.add_column("Distance")
    table.add_column("Time")
    table.add_column("Elevation")
    table.add_column("Avg. Grade")
    table.add_column("Avg. Pace / Speed")
    for sport in stats:
        pace = sport["avg_pace_min_km"]
        perf_value = (
            format_pace(pace)
            if sport["type"] == "running"
            else round(60 / pace, 1)
        )
        perf_metric = "min/km" if sport["type"] == "running" else "km/h"

        table.add_row(
            sport["type"],
            f"{sport["workout_count"]}",
            f"{sport["total_dist_km"]:.1f} km",
            str(dt.timedelta(seconds=sport["total_time"])),
            f"{sport["total_elevation_m"]} m",
            f"{sport["avg_grade_pct"]:.2f} %",
            f"{perf_value} {perf_metric}",
        )

    console.print(table)


def render_workout_details(workout: Workout) -> None:
    console = Console()
    header = Panel(
        Text(
            f"{workout.type.title()} - {workout.datetime:%Y-%m-%d (%a) %H:%M}"
        )
    )

    overview = Panel(
        (
            f"ID: {workout.id}\n"
            f"Distance: {workout.distance_km:.2f} km\n"
            f"Moving time: {dt.timedelta(seconds=workout.moving_time_sec)}\n"
            f"Starting location: {workout.start_lat:.5f}°N, "
            f"{workout.start_lon:.5f}°E\n"
        ),
        title="Overview",
    )

    perf_metric = "pace" if workout.type == "running" else "speed"
    perf_value = (
        format_pace(workout.pace_min_km)
        if workout.type == "running"
        else round(60 / workout.pace_min_km, 1)
    )
    perf_unit = "min/km" if workout.type == "running" else "km/h"

    performance = Panel(
        (
            f"Elevation gain: {workout.elevation_m}m\n"
            f"Average grade: {workout.grade}%\n"
            f"Average {perf_metric}: {perf_value}{perf_unit}"
        ),
        title="Performance",
    )

    console.print(header)
    console.print(Columns([overview, performance]))
