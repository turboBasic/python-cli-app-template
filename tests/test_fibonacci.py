import pytest

from python_cli_app_template.fibonacci import fibonacci


def test_fibonacci():
    """API Tests: fibonacci"""
    assert fibonacci(1) == 1
    assert fibonacci(2) == 1
    assert fibonacci(7) == 13
    with pytest.raises(RuntimeError):
        fibonacci(-10)
