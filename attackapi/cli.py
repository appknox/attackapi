import click


from .core import attack as _attack
from .core import monitor as _monitor


@click.group()
def cli():
    pass


@cli.command()
def run():
    """
    Monitor and attack API.
    """
    _monitor()


@cli.command()
def attack():
    """
    Find if there are any vulnerabilities in API.
    """
    _attack()
