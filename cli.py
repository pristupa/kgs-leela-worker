import click

from src.application import Application
from src.scheduler import Scheduler


@click.group()
def cli():
    pass


@cli.command()
def start():
    application = Application()
    application.start()


@cli.command()
@click.argument('n')
@click.argument('kilo_playouts')
def schedule(n: str, kilo_playouts: str):
    try:
        n = int(n)
    except ValueError:
        n = None

    try:
        kilo_playouts = int(kilo_playouts)
    except ValueError:
        kilo_playouts = None
    scheduler = Scheduler()
    scheduler.schedule(n, kilo_playouts)


@cli.command()
@click.argument('n')
def extract(n: str):
    try:
        n = int(n)
    except ValueError:
        n = None

    application = Application()
    application.extract(n)


if __name__ == '__main__':
    cli()
