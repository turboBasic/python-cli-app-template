"""
CLI for fetch command
"""

import logging

import requests
import typer

app = typer.Typer()


@app.command()
def astronauts():
    """List of astronauts which are currently in space."""

    url = 'http://api.open-notify.org/astros.json'

    response = requests.get(url, timeout=10)
    if response.status_code == 200:  # noqa: PLR2004
        data = response.json()
        logging.getLogger(__name__).debug('data retrieved: %s', data)
        for astronaut in data['people']:
            typer.echo(f'- {astronaut["name"]} on {astronaut["craft"]}')
    else:
        typer.echo(f'Failed to retrieve data: {response.status_code}')
        typer.Exit(code=1)


@app.command()
def location():
    """Approximate geo coordinates of the computer which executes this code."""

    url = 'https://ipinfo.io'

    response = requests.get(url, timeout=10)
    if response.status_code == 200:  # noqa: PLR2004
        logging.getLogger(__name__).debug('data retrieved: %s', response.json())
        latitude, longitude = [float(i) for i in response.json()['loc'].split(',')]
        result = [
            f'{-latitude}S' if latitude < 0 else f'{latitude}N',
            f'{-longitude}W' if longitude < 0 else f'{longitude}E',
        ]
        typer.echo(f'{" ".join(result)}')
    else:
        typer.echo(f'Failed to retrieve data: {response.status_code}')
        typer.Exit(code=1)


@app.command()
def population():
    """Current human population of planet Earth."""

    # TODO implement
    typer.echo(f'{1}')


@app.callback()
def main(ctx: typer.Context):
    """Fetch various data from public API endpoints."""
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.command.name}/{ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
