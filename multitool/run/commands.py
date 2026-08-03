import click

from multitool.cls import AliasedGroup


@click.group(cls=AliasedGroup)
def run():
    """Run installed plugin commands."""
    pass