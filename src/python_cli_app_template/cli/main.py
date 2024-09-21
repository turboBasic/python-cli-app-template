"""
Creates a set of CLI commands using [Typer](https://typer.tiangolo.com) package.

This command is made available to the user via the following lines in `pyproject.toml`:

```toml
[project.scripts]
pca = "python_cli_app_template.cli.cli:app"
```

Then run `hatch run pca prime 10` to execute this in your default environment.
If you install the package using `pip install`, the application can be invoked
by `pca prime 10` command

"""

import logging
from typing import Annotated

import typer

from python_cli_app_template import __version__
from python_cli_app_template.cli import config, factorial, prime
from python_cli_app_template.config import load_config_file

app = typer.Typer(help=f'Python CLI experimental. Version: {__version__}')

# Inject `factorial` as subcommand which in turn can have its own subcommands
app.add_typer(factorial.app, name='factorial')

# Inject `config` as subcommand which in turn can have its own subcommands
app.add_typer(config.app, name='config')

# Because cli_prime does not have subcommands, we inject it directly
# as command, not as a sub-typer (see https://github.com/fastapi/typer/issues/119)
app.command(name='prime')(prime.main)


@app.callback()
def main(
    ctx: typer.Context,
    config_file: Annotated[str | None, typer.Option(help='Config file')] = None,
):
    """Python CLI Experimental: boilerplate project for modern CLI utility"""
    if config_file:
        load_config_file(config_file)
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
