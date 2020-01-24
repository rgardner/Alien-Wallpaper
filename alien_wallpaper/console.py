"""Alien Wallpaper main entrypoint."""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

from . import daemon
from .image_downloader import CustomFeed, ImageDownloader

LOG_FORMAT = "%(levelname)s|%(asctime)s|%(message)s"

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


def run_download_images_command(args: argparse.Namespace):
    """Downloads images."""
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


def add_download_arg_parser(subparsers):
    """Adds command line argument subparser for downloading images."""
    parser = subparsers.add_parser("download", help="download images")
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
    parser.set_defaults(func=run_download_images_command)


def add_daemon_arg_parser(subparsers):
    """Adds command line argument subparser for daemon management."""
    parser = subparsers.add_parser("daemon", help="configure daemon")
    daemon_subparsers = parser.add_subparsers()

    gen_config_parser = daemon_subparsers.add_parser(
        "generate-config", help="generate daemon config"
    )
    gen_config_parser.set_defaults(func=daemon.run_generate_config_command)

    load_parser = daemon_subparsers.add_parser("load", help="load daemon")
    load_parser.add_argument("config", type=Path, help="daemon config file")
    load_parser.set_defaults(func=daemon.run_load_daemon_command)

    unload_parser = daemon_subparsers.add_parser("unload", help="unload daemon")
    unload_parser.set_defaults(func=daemon.run_unload_daemon_command)

    status_parser = daemon_subparsers.add_parser("status", help="status daemon")
    status_parser.set_defaults(func=daemon.run_daemon_status_command)


def parse_cli_args(args: List[str]):
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        prog="alien_wallpaper", description="Download images from Reddit."
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    subparsers = parser.add_subparsers(dest="cmd", required=True)
    add_download_arg_parser(subparsers)
    add_daemon_arg_parser(subparsers)

    return parser.parse_args(args)


def main():
    args = parse_cli_args(sys.argv[1:])
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format=LOG_FORMAT, stream=sys.stdout, level=logging_level)

    # Run subcommand
    args.func(args)
