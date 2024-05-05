import click

from .search import search
from .list import list

@click.group()
def cli():
    pass

cli.add_command(search)
cli.add_command(list)
