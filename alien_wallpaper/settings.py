"""Alien Wallpaper settings, e.g. Reddit API configuration."""

import os


def get_reddit_client_id() -> str:
    """Returns Reddit Client ID from the environment."""
    return os.environ["ALIEN_WALLPAPER_CLIENT_ID"]


def get_reddit_client_secret() -> str:
    """Returns Reddit Client Secret from the environment."""
    return os.environ["ALIEN_WALLPAPER_CLIENT_SECRET"]
