"""Configuration for pytest."""

import sys

import pytest

ALL_PLATFORMS = {"darwin", "linux", "win32"}


def pytest_runtest_setup(item):
    """https://docs.pytest.org/en/latest/writing_plugins.html."""
    supported_platforms = ALL_PLATFORMS.intersection(
        mark.name for mark in item.iter_markers()
    )
    plat = sys.platform
    if supported_platforms and plat not in supported_platforms:
        pytest.skip(f"cannot run on platform {plat}")
