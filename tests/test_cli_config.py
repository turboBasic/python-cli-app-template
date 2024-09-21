from typer.testing import CliRunner

from python_cli_app_template.cli.main import app

runner = CliRunner()


def test_cli_config(mock_config_files):
    """CLI Tests: config command"""

    # WHEN
    result = runner.invoke(app, ['config', 'show', '--show-origin'])

    # THEN
    assert result.exit_code == 0
    assert 'URL: https://foo' in result.stdout
    assert 'USERNAME: john_doe' in result.stdout

    # WHEN
    result = runner.invoke(app, ['config', 'show'])

    # THEN
    assert result.exit_code == 0
    assert 'URL: https://foo' in result.stdout
    assert 'USERNAME: john_doe' in result.stdout

    # WHEN
    result = runner.invoke(app, ['--config-file', '/foo/some-file.toml', 'config', 'show'])
    assert result.exit_code == 0
    assert 'URL: https://foo' in result.stdout
    assert 'USERNAME: from-some-file' in result.stdout
