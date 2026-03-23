import click
from tracklog.db.engine import create_tables
from tracklog.core.gpx_parser import parse_gpx


@click.group()
def cli():
    pass


@cli.command("log")
def log():
    print("Logging...")


@cli.command("init-db")
def init_database():
    print("Initializing database...")
    create_tables()
    print("Database created")


@cli.command("parse")
@click.argument("path")
def parse(path):
    print(f"Parsing: {path}")
    print(parse_gpx(path))
