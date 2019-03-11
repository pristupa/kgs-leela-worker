import click

from src.application import Application


@click.group()
def cli():
    pass


@cli.command()
def start():
    application = Application()
    application.start()


if __name__ == '__main__':
    cli()
