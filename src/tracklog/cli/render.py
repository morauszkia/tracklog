import click
import datetime as dt
from typing import List, Dict
from rich.console import Console
from rich.table import Table
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


def render_workout_list(workouts: List[Workout]):
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


def render_stats_table(stats: List[Dict], period: str):
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
    table.add_column("Avg. Pace")
    table.add_column("Avg. Grade")
    for sport in stats:
        table.add_row(
            sport["type"],
            f"{sport["workout_count"]}",
            f"{sport["total_dist_km"]:.1f} km",
            str(dt.timedelta(seconds=sport["total_time"])),
            f"{sport["total_elevation_m"]} m",
            str(dt.timedelta(minutes=sport["avg_pace_min_km"])),
            f"{sport["avg_grade_pct"]:.2f}%",
        )

    console.print(table)


def render_workout_details(workout: Workout):
    workout_icon = WORKOUT_ICONS.get(workout.type, DEFAULT_ICON)
    click.echo("Workout details")
    click.echo(f"Id: {workout.id}")
    click.echo(f"Sport: {workout.type} {workout_icon}")
    click.echo(f"Date: {workout.datetime.date().strftime("%Y-%m-%d (%a)")}")
    click.echo(
        f"Start coordinates: {round(workout.start_lat, 1)},"
        f" {round(workout.start_lon, 1)}"
    )
    click.echo(f"Start time: {workout.datetime.time().strftime("%H:%M")}")
    click.echo(f"Moving time: {dt.timedelta(seconds=workout.moving_time_sec)}")
    click.echo(f"Distance: {workout.distance_km}km")
    click.echo(f"Elevation: {workout.elevation_m}m (grade: {workout.grade}%)")
    if workout.type == ["cycling", "Canoeing"]:
        click.echo(f"Average speed: 60 / {round(workout.pace_min_km, 1)}")
    else:
        click.echo(
            f"Average pace: {dt.timedelta(minutes=workout.pace_min_km)}"
        )
