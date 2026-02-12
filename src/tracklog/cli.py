import click


@click.group()
def cli():
    pass


@cli.command("log")
def log():
    print("Logging...")
