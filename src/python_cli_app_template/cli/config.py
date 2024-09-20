"""
CLI for configuration management
"""

import logging
from pathlib import Path
from typing import Annotated

import typer
from dynaconf import inspect_settings

from python_cli_app_template.config import settings

app = typer.Typer()


@app.command()
def show(
    show_origin: Annotated[bool, typer.Option(help='Show origin of each item.')] = False,  # noqa: FBT002
):
    """Show all configuration items"""
    if show_origin:
        _print_settings_history()
    else:
        for k, v in _get_current_settings().items():
            typer.echo(f'{k}: {v}')


@app.callback()
def main(ctx: typer.Context):
    """Manage app configuration"""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.invoked_subcommand}')


def _print_settings_history() -> None:
    for item, value in _get_current_settings().items():
        typer.echo(f'{item}: {value}')
        for event in _get_history(item):
            if event['loader'] == 'toml':
                rel_path = Path(event['identifier']).relative_to(Path.cwd())
                typer.echo(f'  ({rel_path}):  {event["value"]}')
            else:
                typer.echo(f'  ({event["loader"]}):  {event["value"]}')


def _get_history(item: str) -> list[dict]:
    result = []
    for event in inspect_settings(settings())['history']:
        if item in event['value']:
            result.append({**event, **{'value': event['value'][item]}})
    return result


def _get_current_settings() -> dict:
    return inspect_settings(settings())['current']


if __name__ == '__main__':
    app()
