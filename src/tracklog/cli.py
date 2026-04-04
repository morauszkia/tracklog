import click
import datetime
from pathlib import Path
from tracklog.db.engine import create_tables, Session
from tracklog.db.repo import WorkoutRepo
from tracklog.core.gpx_parser import parse_gpx, process_dir

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

    click.echo("Your recent workouts:\n")

    for workout in workouts:
        workout_icon = WORKOUT_ICONS.get(workout.type, DEFAULT_ICON)
        click.echo(
            f"{workout.datetime.strftime('📅 %Y-%m-%d (%a) 🕒 %H:%M')}: "
            f"{workout_icon} {workout.type}: {workout.distance_km:.1f}km "
            f"({workout.elevation_m}m+) "
            f"in {datetime.timedelta(
                seconds=round(workout.moving_time_sec)
                )}"
        )
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
    for key, val in stats.items():
        print(f"{key}: {val}")


# command to inspect workout
# command to compare workouts
