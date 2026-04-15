import click
import datetime
from pathlib import Path
from tracklog.db.engine import create_tables, Session
from tracklog.db.repo import WorkoutRepo
from tracklog.core.gpx_parser import parse_gpx, process_dir
from rich.console import Console
from rich.table import Table
from rich import box

WORKOUT_ICONS = {
    "running": "🏃",
    "hiking": "🚶",
    "cycling": "🚴",
    "walking": "🚶",
    "Canoeing": "🚣",
}

DEFAULT_ICON = "🤸‍♀️"


@click.group()
def cli():
    """Workout Tracker"""
    pass


@cli.command("log")
@click.argument("path")
def log(path: Path):
    """Log workout(s) from GPX file or folder containing GPX files"""
    path = Path(path)
    if not path.exists():
        click.echo(f"❌ path {path} does not exist")
        return

    workouts = []
    if path.is_dir():
        workouts.extend(process_dir(path))
    elif path.is_file and path.suffix == ".gpx":
        workouts.append(parse_gpx(path))
    else:
        click.echo(f"❌ invalid path: {path}")
        return

    repo = WorkoutRepo(Session)
    for workout in workouts:
        repo.add(workout)

    click.echo(f"{len(workouts)} workouts logged successfully")


@cli.command("init-db")
def init_database():
    """Initialize database"""
    create_tables()
    click.echo("Database created")


@cli.command()
@click.option(
    "--limit",
    "-l",
    default=None,
    help="Number of workouts to show",
    type=click.IntRange(1),
)
def list(limit: int):
    """List recent workouts"""
    repo = WorkoutRepo(Session)
    workouts = repo.list_all(limit)

    if not workouts:
        click.echo(
            "No workouts logged yet. Try logging some with 'tracklog log'"
        )
        return

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
            f"{datetime.timedelta(
                seconds=round(workout.moving_time_sec)
                )}",
            f"{workout.id}",
        )
    console.print(table)
    click.echo(f"{len(workouts)} workouts listed")


@cli.command()
@click.option(
    "--period",
    "-p",
    type=click.Choice(["week", "month", "ytd", "all"]),
    default="all",
    help="Stats period",
)
def stats(period):
    """Calculate statistics for provided PERIOD"""
    repo = WorkoutRepo(Session)
    stats = repo.stats(period)

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
            str(datetime.timedelta(seconds=sport["total_time"])),
            f"{sport["total_elevation_m"]} m",
            str(datetime.timedelta(minutes=sport["avg_pace_min_km"])),
            f"{sport["avg_grade_pct"]:.2f}%",
        )

    console.print(table)


@cli.command()
@click.argument("id")
def show(id: str):
    repo = WorkoutRepo(Session)
    workout = repo.get_workout(id)
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
    click.echo(
        f"Moving time: {datetime.timedelta(seconds=workout.moving_time_sec)}"
    )
    click.echo(f"Distance: {workout.distance_km}km")
    click.echo(f"Elevation: {workout.elevation_m}m (grade: {workout.grade}%)")
    if workout.type == ["cycling", "Canoeing"]:
        click.echo(f"Average speed: 60 / {round(workout.pace_min_km, 1)}")
    else:
        click.echo(
            f"Average pace: {datetime.timedelta(minutes=workout.pace_min_km)}"
        )
