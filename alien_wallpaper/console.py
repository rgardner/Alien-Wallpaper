"""Alien Wallpaper main entrypoint."""

import argparse
import logging
import sys
from pathlib import Path

from .image_downloader import CustomFeed, ImageDownloader

DEFAULT_SUBREDDITS = [
    "ArchitecturePorn",
    "CityPorn",
    "EarthPorn",
    "SkyPorn",
    "spaceporn",
    "winterporn",
    "quoteporn",
]
IMAGE_DOWNLOAD_LIMIT = 25


def parse_cli_args():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        prog="alien_wallpaper", description="Download images from Reddit."
    )
    parser.add_argument("-s", "--subreddits", nargs="*", help="one or more subreddits.")
    parser.add_argument(
        "-c",
        "--custom-feeds",
        nargs="*",
        help="one or more custom feeds in the format USER/CUSTOM_FEED_NAME",
    )
    parser.add_argument(
        "-o", "--out", required=True, type=Path, help="output directory"
    )
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main():
    args = parse_cli_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level)

    image_downloader = ImageDownloader(args.out)
    if not args.subreddits and not args.custom_feeds:
        image_downloader.download_images_from_subreddits(
            DEFAULT_SUBREDDITS, IMAGE_DOWNLOAD_LIMIT
        )
    else:
        if args.subreddits:
            image_downloader.download_images_from_subreddits(
                args.subreddits, IMAGE_DOWNLOAD_LIMIT
            )

        if args.custom_feeds:
            for feed in args.custom_feeds:
                user, feed_name = feed.split("/")
                custom_feed = CustomFeed(user=user, feed_name=feed_name)
                image_downloader.download_images_from_custom_feed(
                    custom_feed, IMAGE_DOWNLOAD_LIMIT
                )
