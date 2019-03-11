import click


@click.group()
def cli():
    pass


@cli.command()
def start():
    print('To be implemented...')


if __name__ == '__main__':
    cli()
