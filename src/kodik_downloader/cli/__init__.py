import click

from .ftor import ftor
from .list import list
from .search import search

@click.group()
def cli():
    pass

cli.add_command(ftor)
cli.add_command(list)
cli.add_command(search)
