"""Alien Wallpaper tests."""

import pytest

import alien_wallpaper
from alien_wallpaper import CustomFeed, __version__


def test_version():
    """Verifies version string is correct."""
    assert __version__ == "1.0.0"


@pytest.mark.large
def test_download_images_from_subreddits(tmp_path):
    """Verifies images can be downloaded."""
    subreddits = ["pics"]
    limit = 1
    out_dir = tmp_path / "output"
    out_dir.mkdir()
    image_downloader = alien_wallpaper.ImageDownloader(out_dir)

    image_downloader.download_images_from_subreddits(subreddits, limit)
    assert len(list(out_dir.iterdir())) == 1


@pytest.mark.large
def test_download_images_from_custom_feed(tmp_path):
    """Verifies images can be downloaded."""
    custom_feed = CustomFeed("wolf_blackout", "wallpaper")
    limit = 1
    out_dir = tmp_path / "output"
    out_dir.mkdir()
    image_downloader = alien_wallpaper.ImageDownloader(out_dir)

    image_downloader.download_images_from_custom_feed(custom_feed, limit)
    assert len(list(out_dir.iterdir())) == 1
