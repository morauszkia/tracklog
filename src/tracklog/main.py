import click
from pathlib import Path
from tracklog.db.engine import create_tables, Session
from tracklog.db.repo import WorkoutRepo
from tracklog.core.gpx_parser import parse_gpx, process_dir
from tracklog.cli.render import (
    render_workout_list,
    render_workout_details,
    render_stats_table,
)


@click.group()
def cli():
    """Workout Tracker"""
    pass


@cli.command("log")
@click.argument("path")
def log(path: str):
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

    render_workout_list(workouts)
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
    render_stats_table(stats, period)


@cli.command()
@click.argument("id")
def show(id: str):
    repo = WorkoutRepo(Session)
    workout = repo.get_workout(id)
    render_workout_details(workout)
