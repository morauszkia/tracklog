import click
from rich.console import Console
from tracklog.db.engine import create_tables, Session, engine
from tracklog.db.repo import WorkoutRepo
from tracklog.db.util import is_db_initialized
from tracklog.cli.render import (
    render_workout_list,
    render_workout_details,
    render_stats_table,
)
from tracklog.cli.log import log_workout_from_path


@click.group()
def cli():
    """Workout Tracker"""
    pass


@cli.command("init-db")
def init_database():
    """Initialize database"""
    console = Console()
    try:
        if is_db_initialized(engine):
            console.print("[yellow]Database schema already exists.[/]")
        else:
            create_tables()
            console.print("[green]Database created[/]")
    except Exception as e:
        raise click.ClickException(str(e))


@cli.command("log")
@click.argument("path")
def log(path: str):
    """Log workout(s) from GPX file or folder containing GPX files"""
    log_workout_from_path(path)


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
    try:
        repo = WorkoutRepo(Session)
        workouts = repo.list_all(limit)

        if not workouts:
            Console().print(
                "[yellow]No workouts logged yet. Try logging some with 'tracklog log'[/]"
            )
            return

        render_workout_list(workouts)
        click.echo(f"{len(workouts)} workouts listed")
    except Exception as e:
        raise click.ClickException(str(e))


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
    try:
        repo = WorkoutRepo(Session)
        stats = repo.stats(period)
        if not stats:
            Console().print(
                "[yellow]No workouts logged yet. Try logging some with 'tracklog log'[/]"
            )
            return
        render_stats_table(stats, period)
    except Exception as e:
        raise click.ClickException(str(e))


@cli.command()
@click.argument("id")
def show(id: str):
    """Show details of selected workout"""
    try:
        repo = WorkoutRepo(Session)
        workout = repo.get_workout(id)
        if not workout:
            raise click.ClickException(f"No workout found for id {id}")
        render_workout_details(workout)
    except Exception as e:
        raise click.ClickException(str(e))
