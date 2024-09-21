"""
Read configuration (settings) of application.

Configuration is read from the sources in the order described below.
Every step overwrites configuration values obtained in previous steps.
- 'defaults' directory of the package
- current working directory
- environment variables with 'PCA_' prefix, i.e., `export PCA_FOO=bar` will
  assign value 'bar' to configuration item 'foo'
- configuration files provided in command line arguments

Implementation uses Dynaconf package, read more about Dynaconf:
- https://www.dynaconf.com
"""

import importlib.resources
import logging
import os
import sys
from os import PathLike
from pathlib import Path

import typer
from dynaconf import Dynaconf, inspect_settings
from dynaconf.base import Settings

__PACKAGE_PATH = importlib.resources.files(__package__)
__DEFAULT_SETTINGS_DIR = 'defaults'
__PUBLIC_SETTINGS_FILE = 'settings.pca.toml'
__SECRET_SETTINGS_FILE = '.secrets.pca.toml'
__DEFAULT_PUBLIC_SETTINGS_FILE = __PACKAGE_PATH / __DEFAULT_SETTINGS_DIR / __PUBLIC_SETTINGS_FILE
__DEFAULT_SECRET_SETTINGS_FILE = __PACKAGE_PATH / __DEFAULT_SETTINGS_DIR / __SECRET_SETTINGS_FILE
__ENV_VAR_PREFIX = 'PCA'

__settings: Settings | None = None


def settings() -> Settings:
    global __settings  # noqa: PLW0603
    if not __settings:
        __settings = Dynaconf(
            root_path=os.getenv('HOME'),
            settings_files=[
                __DEFAULT_PUBLIC_SETTINGS_FILE,
                __DEFAULT_SECRET_SETTINGS_FILE,
                Path(__PUBLIC_SETTINGS_FILE).resolve(),
                Path(__SECRET_SETTINGS_FILE).resolve(),
            ],
            envvar_prefix=__ENV_VAR_PREFIX,
        )
    return __settings


def load_config_file(config_file: str | PathLike) -> None:
    config_file_path = Path(config_file).resolve()
    if not config_file_path.exists():
        logging.getLogger(__name__).warning(f'{config_file_path} does not exist')
        return

    logging.getLogger(__name__).debug(f'Loading config file: {config_file_path}')
    settings().load_file(config_file_path)


def settings_history() -> str:
    result: list[str] = []
    for item, value in settings().as_dict().items():
        result.append(f'{item}: {value}')
        for event in _get_history(item):
            if event['loader'] == 'toml':
                try:
                    rel_path = Path(event['identifier']).relative_to(Path.cwd())
                except ValueError:
                    rel_path = Path(event['identifier']).resolve()
                result.append(f'  file({rel_path}):  {event["value"]}')
            else:
                result.append(f'  event({event["loader"]}):  {event["value"]}')
    return '\n'.join(result)


def settings_as_str() -> str:
    result: list[str] = []
    for k, v in settings().as_dict().items():
        result.append(f'{k}: {v}')
    return '\n'.join(result)


def _get_history(item: str) -> list[dict]:
    result = []
    for event in inspect_settings(settings())['history']:
        if item in event['value']:
            result.append({**event, **{'value': event['value'][item]}})
    return result


if __name__ == '__main__':
    typer.echo('This module is not intended to be executed directly')
    sys.exit(1)
