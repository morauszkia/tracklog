import click
from tracklog.db.engine import create_tables


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
