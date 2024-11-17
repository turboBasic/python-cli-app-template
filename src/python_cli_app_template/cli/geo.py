"""
CLI for geo command
"""

import logging
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def draw(country: Annotated[str, typer.Argument(..., help='Country')]):
    """Draw the map of the country."""
    logging.getLogger(__name__).info(f'Country: {country}')
    pass


@app.callback()
def main(ctx: typer.Context):
    """Various Geomapping commands."""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.command.name}/{ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
