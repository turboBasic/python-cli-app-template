"""
CLI for Fibonacci sequence calculation
"""

import logging
from typing import Annotated

import typer

from python_cli_app_template.fibonacci import fibonacci

app = typer.Typer()


@app.command()
def main(n: Annotated[int, typer.Argument(..., min=1, help='Positive integer')]):
    """Calculate Fibonacci sequence"""
    typer.echo(f'The {n}-th Fibonacci number is {fibonacci(n)}')
    logging.getLogger(__name__).debug('Script ends here')


if __name__ == '__main__':
    app()
