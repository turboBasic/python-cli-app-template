"""
CLI for configuration management
"""

import logging
from typing import Annotated

import typer

from python_cli_app_template import config

app = typer.Typer()


@app.command()
def show(
    show_origin: Annotated[  # noqa: FBT002
        bool, typer.Option('--show-origin', help='Show origin of each configuration item.')
    ] = False,
):
    """Show all configuration items"""
    if show_origin:
        typer.echo(config.settings_history())
    else:
        typer.echo(config.settings_as_str())


@app.callback()
def main(ctx: typer.Context):
    """Manage app configuration"""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
