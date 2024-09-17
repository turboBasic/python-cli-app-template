"""
Creates a set of CLI commands using [Typer](https://typer.tiangolo.com/) package.

This is a skeleton file that can serve as a starting point for a Python
console script. This is accomplished via the following lines in `pyproject.toml`:

```toml
[project.scripts]
pca = "python_cli_app_template.cli:app"
```

Then run `hatch run pca fib 10` to execute this in your default environment or
`hatch shell` to enter the default environment, followed by `pca fib 10`.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import logging
from typing import Annotated

import typer

from python_cli_app_template import __version__, cli_config, cli_factorial, cli_fibonacci
from python_cli_app_template.config import set_config_file

app = typer.Typer(help=f'Python CLI experimental. Version: {__version__}')

# Inject `factorial` as subcommand which in turn can have its own subcommands
app.add_typer(cli_factorial.app, name='factorial')

# Inject `config` as subcommand which in turn can have its own subcommands
app.add_typer(cli_config.app, name='config')

# Because cli_fibonacci does not need a subcommand, we inject it as a command, not as a sub-typer
# (see https://github.com/fastapi/typer/issues/119)
app.command(name='fib')(cli_fibonacci.main)


@app.callback()
def main(
    ctx: typer.Context,
    config_file: Annotated[str | None, typer.Option(help='Config file')] = None,
):
    """Python CLI Experimental: boilerplate project for modern CLI utility"""
    if config_file:
        set_config_file(config_file)
    logging.getLogger(__name__).debug(f'About to execute command: {ctx.invoked_subcommand}')


if __name__ == '__main__':
    app()
