"""
CLI for calculation of n-th prime number
"""

from typing import Annotated

import sympy
import typer

app = typer.Typer()


@app.command()
def main(n: Annotated[int, typer.Argument(..., min=1, help='Positive integer')]):
    """Calculate n-th prime number."""
    typer.echo(f'The {n}-th prime number is {sympy.prime(n)}')


if __name__ == '__main__':
    app()
