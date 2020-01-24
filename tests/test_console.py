"""Alien Wallpaper Command Line Interface tests."""

import pytest

from alien_wallpaper import console


def test_parse_cli_args_when_called_with_no_args_fails(capsys):
    """Verifies parse_cli_args stderr output when called with no arguments."""
    raw_args = []
    with pytest.raises(SystemExit):
        console.parse_cli_args(raw_args)
    output = capsys.readouterr().err
    assert "the following arguments are required: cmd" in output


def test_parse_cli_args_when_called_with_short_v_returns_verbose():
    """Verifies parse_cli_args when called with -v is the same as --verbose."""
    raw_args = ["-v", "download", "--out", "output"]
    args = console.parse_cli_args(raw_args)
    assert args.verbose
