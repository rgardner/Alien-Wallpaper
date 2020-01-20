"""Alien Wallpaper main entrypoint."""

import argparse
import json
import logging
import multiprocessing
import os.path
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import List, NewType, Optional, Sequence

IMAGES_PER_SUBREDDIT = 25
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


@dataclass
class Post:
    id: str
    is_self: bool
    url: Url

    @property
    def is_valid(self) -> bool:
        return not self.is_self and bool(FILE_EXTENSION_PROG.match(self.url))

    @property
    def filename(self) -> Optional[str]:
        if self.extension is not None:
            return self.id + "." + self.extension
        return None

    @property
    def extension(self) -> Optional[str]:
        match = FILE_EXTENSION_PROG.match(self.url)
        if match is not None:
            return match.group(1)
        return None

    @staticmethod
    def from_json(data) -> "Post":
        return Post(id=data["id"], is_self=bool(data["is_self"]), url=Url(data["url"]))


class ImagePost:
    def __init__(self, post: Post):
        self.id = post.id
        self.url = post.url

        if post.filename is None:
            raise ValueError("filename cannot be None")
        self.filename = post.filename

    def download(self, out_dir: Path):
        path = out_dir / self.filename
        logging.debug(path)

        try:
            with urllib.request.urlopen(self.url) as response, open(
                path, "wb+"
            ) as out_file:
                shutil.copyfileobj(response, out_file)
        except urllib.error.HTTPError as e:
            logging.exception(e)
            raise


def subreddit_to_url(subreddit: str) -> Url:
    return Url("https://www.reddit.com/r/{}".format(subreddit))


def fetch_image_posts(subreddit: Url, limit=25, after="") -> List[ImagePost]:
    params = urllib.parse.urlencode({"limit": limit, "after": after})
    url = "{}.json?{}".format(subreddit, params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode("utf-8"))
    posts = [Post.from_json(p["data"]) for p in result["data"]["children"]]
    return [ImagePost(post) for post in posts if post.is_valid]


def download_images(subreddit_name: Url, n: int, out_dir: Path) -> None:
    posts = fetch_image_posts(subreddit_name, limit=n)
    num_images = 0
    while True:
        for post in posts:
            post.download(out_dir)
            num_images += 1
            if num_images >= n:
                return

        posts = fetch_image_posts(subreddit_name, limit=n, after=posts[-1].id)


def download_all_images(subreddits: Sequence[Url], n, out_dir: Path):
    """Download n images in parallel for each subreddit to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with multiprocessing.Pool() as pool:
        for subreddit in subreddits:
            pool.apply(download_images, args=(subreddit, n, out_dir))


def custom_feed_to_url(user: str, custom_feed_name: str) -> Url:
    return Url(f"https://www.reddit.com/user/{user}/m/{custom_feed_name}")


def parse_cli_args():
    parser = argparse.ArgumentParser(description="Download images from Reddit.")
    parser.add_argument("--subreddits", nargs="*")
    parser.add_argument("--multireddit", nargs="?", help="USER/multi_name")
    parser.add_argument("--out", required=True, type=Path, help="Output directory")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main():
    args = parse_cli_args()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level)

    if not args.subreddits and not args.multireddit:
        subreddits = [subreddit_to_url(s) for s in DEFAULT_SUBREDDITS]
    else:
        subreddits = []
        if args.subreddits:
            subreddits.extend([subreddit_to_url(s) for s in args.subreddits])

        if args.multireddit:
            user, multi = args.multireddit.split("/")
            subreddits.append(custom_feed_to_url(user, multi))

    download_all_images(subreddits, IMAGES_PER_SUBREDDIT, args.out)
