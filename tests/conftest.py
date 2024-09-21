"""
Dummy conftest.py for `python-cli-app-template`.

If you don't know what this is for, just leave it empty.
Read more about conftest.py under:
- https://docs.pytest.org/en/stable/fixture.html
- https://docs.pytest.org/en/stable/writing_plugins.html
"""

import logging
import os
from contextlib import contextmanager

import pytest


@pytest.fixture(scope='session')
def logging_format():
    @contextmanager
    def context(new_format: str):
        handler = logging.getLogger().handlers[0]
        original_formatter = handler.formatter
        try:
            handler.setFormatter(logging.Formatter(new_format))
            yield
        finally:
            handler.setFormatter(original_formatter)

    return context


@pytest.fixture(autouse=True)
def mock_config_files(fs):
    current_dir = '/foo'
    fs.create_file(
        f'{current_dir}/settings.pca.toml',
        contents="""
            url = "https://foo"
        """,
    )
    fs.create_file(
        f'{current_dir}/.secrets.pca.toml',
        contents="""
             username = "john_doe"
             http_password = "Påsswørd123!"
        """,
    )
    os.chdir(current_dir)

    from python_cli_app_template.config import settings  # noqa: F401
