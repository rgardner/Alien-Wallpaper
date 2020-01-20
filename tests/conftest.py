import sys

import pytest

ALL_PLATFORMS = set("darwin linux win32".split())


def pytest_runtest_setup(item):
    supported_platforms = ALL_PLATFORMS.intersection(
        mark.name for mark in item.iter_markers()
    )
    plat = sys.platform
    if supported_platforms and plat not in supported_platforms:
        pytest.skip("cannot run on platform {}".format(plat))
