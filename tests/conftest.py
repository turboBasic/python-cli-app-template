"""
Fixtures for pytest

Read more about conftest.py:
- https://docs.pytest.org/en/stable/fixture.html
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


@pytest.fixture
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
    fs.create_file(
        f'{current_dir}/some-file.toml',
        contents="""
             username = "from-some-file"
             http_password = "from-some-file"
        """,
    )
    os.chdir(current_dir)
