"""Alien Wallpaper main entrypoint."""

import argparse
import json
import logging
import multiprocessing
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import List, NewType, Optional, Sequence
from urllib.error import HTTPError

IMAGES_PER_SUBREDDIT = 5
DEFAULT_SUBREDDITS = [
    "ArchitecturePorn",
    "CityPorn",
    "EarthPorn",
    "SkyPorn",
    "spaceporn",
    "winterporn",
    "quoteporn",
]
USER_AGENT = "AlienWallpaper by /u/WolfBlackout"

FILE_EXTENSION_PROG = re.compile(".*.(jpg|jpeg|gif|png)$", re.IGNORECASE)
Url = NewType("Url", str)

logger = logging.getLogger(__name__)


@dataclass
class Post:
    """Reddit post."""

    post_id: str
    is_self: bool
    url: Url

    @property
    def filename(self) -> Optional[str]:
        """Returns image filename if valid."""
        if self.extension is not None:
            return self.post_id + "." + self.extension
        return None

    @property
    def extension(self) -> Optional[str]:
        """Returns image extension if valid."""
        match = FILE_EXTENSION_PROG.match(self.url)
        if match is not None:
            return match.group(1)
        return None

    def to_image_post(self) -> Optional["ImagePost"]:
        """Converts post to image post if valid, otherwise returns None."""
        if self.is_self or not bool(FILE_EXTENSION_PROG.match(self.url)):
            return None

        return ImagePost(self)

    @staticmethod
    def from_json(data) -> "Post":
        """Constructs Post from json."""
        return Post(
            post_id=data["id"], is_self=bool(data["is_self"]), url=Url(data["url"])
        )


class ImagePost:
    """Reddit image post."""

    def __init__(self, post: Post):
        self.post_id = post.post_id
        self.url = post.url

        if post.filename is None:
            raise ValueError("filename cannot be None")
        self.filename = post.filename

    def download(self, out_dir: Path):
        """Downloads image to out_dir."""
        path = out_dir / self.filename
        logger.debug("Downloading %s to %s", self.filename, path)

        try:
            with urllib.request.urlopen(self.url) as response, open(
                path, "wb+"
            ) as out_file:
                shutil.copyfileobj(response, out_file)
        except urllib.error.HTTPError as ex:
            logger.exception(ex)
            raise


def fetch_image_posts(subreddit: Url, limit=25, after="") -> List[ImagePost]:
    """Fetches image posts from subreddit."""
    params = urllib.parse.urlencode({"limit": limit, "after": after})
    url = "{}.json?{}".format(subreddit, params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode("utf-8"))
    posts = [Post.from_json(p["data"]) for p in result["data"]["children"]]

    # Avoid walrus operator until black supports it
    image_posts = []
    for post in posts:
        image_post = post.to_image_post()
        if image_post is not None:
            image_posts.append(image_post)

    return image_posts


def download_images(subreddit_name: Url, num_images: int, out_dir: Path) -> None:
    """Downloads n images from subreddit_name to out_dir."""
    posts = fetch_image_posts(subreddit_name, limit=num_images)
    curr_images = 0
    while True:
        for post in posts:
            with suppress(HTTPError):
                post.download(out_dir)

            curr_images += 1
            if curr_images >= num_images:
                return

        posts = fetch_image_posts(
            subreddit_name, limit=num_images, after=posts[-1].post_id
        )


def download_all_images(subreddits: Sequence[Url], num_images: int, out_dir: Path):
    """Download n images in parallel for each subreddit to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with multiprocessing.Pool() as pool:
        for subreddit in subreddits:
            pool.apply(download_images, args=(subreddit, num_images, out_dir))


def subreddit_to_url(subreddit: str) -> Url:
    """Converts subreddit name to a URL."""
    return Url(f"https://www.reddit.com/r/{subreddit}")


def custom_feed_to_url(user: str, custom_feed_name: str) -> Url:
    """Converts Reddit Custom Feed to a URL."""
    return Url(f"https://www.reddit.com/user/{user}/m/{custom_feed_name}")


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
    """Main entrypoint."""
    args = parse_cli_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level)

    reddit_urls = []
    if args.subreddits:
        reddit_urls.extend([subreddit_to_url(s) for s in args.subreddits])

    if args.custom_feeds:
        for feed in args.custom_feeds:
            user, multi = feed.split("/")
            reddit_urls.append(custom_feed_to_url(user, multi))

    # if user doesn't specify any Reddit URLs, use the defaults
    if not reddit_urls:
        reddit_urls = [subreddit_to_url(s) for s in DEFAULT_SUBREDDITS]

    download_all_images(reddit_urls, IMAGES_PER_SUBREDDIT, args.out)
