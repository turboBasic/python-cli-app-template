import logging

from typer.testing import CliRunner

from python_cli_app_template.cli.main import app

runner = CliRunner()


def test_cli_factorial_simple():
    """CLI Tests: factorial simple command"""
    result = runner.invoke(app, ['factorial', 'simple', '7'])
    assert result.exit_code == 0
    assert result.stdout.rstrip() == '7! = 5040'


def test_cli_prime():
    """CLI Tests: prime command"""
    result = runner.invoke(app, ['prime', '99'])
    assert result.exit_code == 0
    assert result.stdout.rstrip() == 'The 99-th prime number is 523'


def test_cli_factorial_gamma():
    """CLI Tests: factorial gamma command"""
    result = runner.invoke(app, ['factorial', 'gamma', '5'])
    assert result.exit_code == 0
    assert result.stdout.rstrip() == '5.0! = 𝛤(6.0) = 120.0'


def logger():
    return logging.getLogger(__name__)
