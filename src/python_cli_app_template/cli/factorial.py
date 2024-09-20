"""
CLI for Factorial calculation
"""

import logging
import math
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def simple(
    n: Annotated[int, typer.Argument(..., min=1, help='Positive integer')],
):
    """Calculate traditional factorial of positive integer n"""
    typer.echo(f'{n}! = {math.factorial(n)}')


@app.command()
def gamma(
    x: Annotated[float, typer.Argument(..., help='Real number')],
):
    """Calculate factorial of any real n using Gamma function"""
    typer.echo(f'{x}! = 𝛤({x + 1}) = {math.gamma(x + 1)}')


@app.callback()
def main(ctx: typer.Context):
    """Calculate factorial function"""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
