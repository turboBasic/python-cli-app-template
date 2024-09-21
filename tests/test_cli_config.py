from typer.testing import CliRunner

runner = CliRunner()


def test_cli_config():
    """CLI Tests: config command"""

    # GIVEN
    from python_cli_app_template.cli.main import app

    # WHEN
    result = runner.invoke(app, ['config', 'show', '--show-origin'])

    # THEN
    assert result.exit_code == 0
    assert 'URL: https://foo' in result.stdout
    assert 'USERNAME: john_doe' in result.stdout
