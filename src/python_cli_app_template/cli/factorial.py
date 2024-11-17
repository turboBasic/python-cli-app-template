"""
CLI for Factorial calculation
"""

import logging
import math
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def main(ctx: typer.Context, x: Annotated[float, typer.Argument(..., help='Real number')]):
    """Calculate factorial of any real n using Gamma function."""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.command.name}')
    typer.echo(f'{x}! = 𝛤({x + 1}) = {math.gamma(x + 1)}')


if __name__ == '__main__':
    app()
