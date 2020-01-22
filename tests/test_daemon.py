"""Alien Wallpaper daemon tests."""

import alien_wallpaper


def test_generate_default_daemon_config():
    """Verifies default daemon config is valid."""
    default_config = alien_wallpaper.daemon.DaemonConfig()
    default_toml = default_config.dumps_toml()
    assert (
        default_toml
        == """subreddits = []
custom_feeds = []
output_directory = ""
"""
    )
