"""
Creates CLI commands and sub-commands using [Typer](https://typer.tiangolo.com) package.

This module can be invoked from shell by executing `pca` command. This is
enabled in the following lines in `pyproject.toml`:

```toml
[project.scripts]
pca = "python_cli_app_template.cli.main:app"
```

Read detailed help about commands and parameters by executing `pca --help`
"""

import logging
from typing import Annotated

import typer
from rich.logging import RichHandler

from python_cli_app_template import __version__
from python_cli_app_template.cli import config, factorial, fetch, geo, prime
from python_cli_app_template.config import load_config_file

GLOBAL_LOG_LEVEL = logging.INFO
logging.basicConfig(
    level=GLOBAL_LOG_LEVEL,
    format='(%(name)s) %(message)s',
    datefmt='%H:%M:%S',
    handlers=(RichHandler(show_time=False),),
)
app = typer.Typer(help=f'Python CLI experimental. Version: {__version__}')

# Inject `config` and `fetch` as subcommands which in turn can have its own subcommands
app.add_typer(config.app, name='config')
app.add_typer(fetch.app, name='fetch')
app.add_typer(geo.app, name='geo')

# Because cli_prime and cli.factorial do not have subcommands, we inject it directly
# as commands, not as a sub-typer (see https://github.com/fastapi/typer/issues/119)
app.command(name='factorial')(factorial.main)
app.command(name='prime')(prime.main)


def get_current_log_level(module: str | None) -> str:
    if module:
        return logging.getLevelName(logging.getLogger(module).getEffectiveLevel())
    else:
        return logging.getLevelName(logging.root.getEffectiveLevel())


def verbose_callback(value: bool) -> None:  # noqa: FBT001
    if value is None:
        return
    if value:
        logging.root.setLevel(logging.DEBUG)
        logging.getLogger(__name__).debug('Setting log level to DEBUG')
    else:
        logging.root.setLevel(logging.WARNING)


def version_callback(value: bool):  # noqa: FBT001
    """Print version and exit."""
    if value:
        typer.echo(f'Python CLI app template: {__version__}')
        logging.getLogger(__name__).debug('Exiting as --version is expected to do nothing but print version')
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    config_file: Annotated[list[str] | None, typer.Option(help='Specify config file.')] = None,
    verbose: Annotated[
        bool | None, typer.Option(help='Verbose mode.', callback=verbose_callback, is_eager=True)
    ] = None,
    version: Annotated[
        bool | None,
        typer.Option('--version', help='Print version and exit.', callback=version_callback, is_eager=True),
    ] = None,
):
    """Python CLI Application template: boilerplate project for modern CLI utility"""
    logging.root.debug(f'Current {__name__} log level: {get_current_log_level(__name__)}')

    # TODO Remove parameters processed by the callbacks
    logging.root.debug(f'Global arguments: config-file={config_file}, verbose={verbose}, version={version}')

    logging.root.debug(f'Config file: {config_file}')
    for config_file_item in config_file or []:
        logging.root.debug(f'Loading config item: {config_file_item}')
        load_config_file(config_file_item)


if __name__ == '__main__':
    app()
