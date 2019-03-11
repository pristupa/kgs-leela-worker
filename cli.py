import click

from src.worker import Worker


@click.group()
def cli():
    pass


@cli.command()
def start():
    worker = Worker()
    worker.start()


if __name__ == '__main__':
    cli()
