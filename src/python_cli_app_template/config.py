import importlib.resources
import logging
import os
import sys
from pathlib import Path

import typer
from dynaconf import Dynaconf
from dynaconf.base import Settings

__PUBLIC_SETTINGS_FILE = 'settings.pca.toml'
__SECRET_SETTINGS_FILE = '.secrets.pca.toml'
__FALLBACK_SETTINGS_FILE = str(importlib.resources.files(__package__) / 'config' / __PUBLIC_SETTINGS_FILE)

__settings = Dynaconf(
    root_path=os.environ['HOME'],
    # Load settings files in specified order, settings from later files override those loaded before:
    settings_files=[
        __FALLBACK_SETTINGS_FILE,
        __PUBLIC_SETTINGS_FILE,
        __SECRET_SETTINGS_FILE,
    ],
    envvar_prefix='PCA',  # Read settings from envvars set by `export PCA_FOO=bar`
)


# TODO convert to property
def settings() -> Settings:
    # noinspection PyTypeChecker
    return __settings


def set_config_file(config_file: str) -> None:
    config_file_path = Path(config_file).resolve()
    if not config_file_path.exists():
        logging.getLogger(__name__).warning(f'{config_file_path} does not exist')
        return
    logging.getLogger(__name__).debug(f'Loading config file: {config_file_path}')
    __settings.load_file(config_file_path)


if __name__ == '__main__':
    typer.echo('This module is not intended to be executed directly')
    sys.exit(1)
