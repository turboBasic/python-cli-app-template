import logging
import re

from typer.testing import CliRunner

from python_cli_app_template.cli.main import app

runner = CliRunner()


def test_cli_factorial():
    """CLI Tests: factorial command"""
    # WHEN
    result = runner.invoke(app, ['factorial', '5'])
    # THEN
    assert result.exit_code == 0
    assert result.stdout.rstrip() == '5.0! = 𝛤(6.0) = 120.0'

    # WHEN
    result = runner.invoke(app, ['factorial', '--', '-4.5'])
    # THEN
    assert result.exit_code == 0
    assert result.stdout.rstrip() == '-4.5! = 𝛤(-3.5) = 0.27008820585226917'

    # WHEN
    result = runner.invoke(app, ['factorial', '--', '-10'])
    # THEN
    assert result.exit_code != 0


def test_cli_fetch(requests_mock):
    """CLI Tests: fetch command"""

    # GIVEN
    requests_mock.get(
        'https://ipinfo.io',
        text="""{
            "ip": "1.1.1.1",
            "hostname": "foo.example.com",
            "city": "Santa Teresita",
            "region": "Buenos Aires",
            "country": "AR",
            "loc": "-36.533014,-56.694836",
            "org": "Alvarez PLC",
            "postal": "7107",
            "timezone": "America/Argentina/Buenos_Aires",
            "readme": "https://ipinfo.io/missingauth"
        }""",
    )
    requests_mock.get(
        'http://api.open-notify.org/astros.json',
        text="""{
            "people": [
                { "craft": "Startrek", "name": "Dr(a). Felicitas Benitez" },
                { "craft": "Startrek", "name": "Amy Bevan-Allen" }
            ]
        }""",
    )

    # WHEN
    result = runner.invoke(app, ['fetch', 'astronauts'])
    # THEN
    assert result.exit_code == 0
    assert len(result.stdout.rstrip().splitlines()) > 0

    # WHEN
    result = runner.invoke(app, ['fetch', 'location'])
    # THEN
    assert result.exit_code == 0
    assert re.match(r'\d+\.\d+[NS] \d+\.\d+[EW]', result.stdout.rstrip())

    # WHEN
    result = runner.invoke(app, ['fetch', 'population'])
    # THEN
    assert result.exit_code == 0
    assert re.match(r'^\d+$', result.stdout.rstrip())


def test_cli_prime():
    """CLI Tests: prime command"""
    result = runner.invoke(app, ['prime', '99'])
    assert result.exit_code == 0
    assert result.stdout.rstrip() == 'The 99-th prime number is 523'


def test_cli_version():
    """CLI Tests: --version option"""
    result = runner.invoke(app, ['--version'])
    assert result.exit_code == 0
    assert re.match(r'Python CLI app template: (\d+\.){2,}(.+)', result.stdout.rstrip())


def logger():
    return logging.getLogger(__name__)
