"""Responsible for image downloading."""

import logging
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from urllib.error import HTTPError

import praw

from . import settings

USER_AGENT = "AlienWallpaper by /u/WolfBlackout"
FILE_EXTENSION_PROG = re.compile(".*.(jpg|jpeg|gif|png)$", re.IGNORECASE)

logger = logging.getLogger(__name__)


@dataclass
class CustomFeed:
    """Reddit custom feed."""

    user: str
    feed_name: str


def is_valid_image_post(post: praw.models.Submission) -> bool:
    """Returns True if the post links to a valid image."""
    return not post.is_self and bool(FILE_EXTENSION_PROG.match(post.url))


def generate_filename_for_post(post: praw.models.Submission) -> Path:
    """Returns unique filename for post with correct extension."""
    match = FILE_EXTENSION_PROG.match(post.url)
    assert match is not None
    return Path(f"{post.id}.{match.group(1)}")


class ImageDownloader:
    """Downloads images from Reddit."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        client_id = settings.get_reddit_client_id()
        client_secret = settings.get_reddit_client_secret()
        self.reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=USER_AGENT
        )
        self.reddit.read_only = True

    def download_images_from_subreddits(self, subreddits: List[str], limit: int):
        """Downloads images from one or more subreddits.

        If multiple subreddits are supplied, `limit` is the combined limit.
        """

        combined = "+".join(subreddits)
        subreddits_view = self.reddit.subreddit(combined)
        self._download_images_from_feed(subreddits_view, limit)

    def download_images_from_custom_feed(self, custom_feed: CustomFeed, limit: int):
        """Downloads images from a Custom Feed."""
        multireddit = self.reddit.multireddit(custom_feed.user, custom_feed.feed_name)
        self._download_images_from_feed(multireddit, limit)

    def download_images_from_posts(
        self, posts: praw.models.ListingGenerator, limit: int
    ) -> Tuple[int, Optional[str]]:
        """Downloads linked image for each post.

        Non-image posts and posts that cannot be downloaded successfully are
        skipped.

        Returns (num_downloaded, last_post_id)
        """
        if limit <= 0:
            return (0, None)

        num_downloaded = 0
        last_post_id = None
        for post in posts:
            if not is_valid_image_post(post):
                logger.debug("Skipping %s because it is not an image", post.id)
                continue

            with suppress(HTTPError):
                self.download_image(post)
                num_downloaded += 1
                last_post_id = post.id
                if num_downloaded >= limit:
                    break

        return (num_downloaded, last_post_id)

    def download_image(self, post: praw.models.Submission):
        """Download image for post.

        Posts that have already been downloaded are skipped.
        """
        filename = generate_filename_for_post(post)
        path = self.output_dir / filename
        if path.exists():
            logger.debug("Skipping %s because it has already been downloaded.", post.id)

        logger.debug("Downloading %s to %s", filename, path)
        try:
            with urllib.request.urlopen(post.url) as response, open(
                path, "wb+"
            ) as out_file:
                shutil.copyfileobj(response, out_file)
        except urllib.error.HTTPError as ex:
            logger.exception(ex)
            raise

    def _download_images_from_feed(
        self, feed: Union[praw.models.Subreddit, praw.models.Multireddit], limit: int
    ):
        """Downloads images from feed until `limit` have been downloaded."""
        num_downloaded = 0
        last_post_id = None  # type: Optional[str]
        while num_downloaded < limit:
            params = {}  # type: Dict[str, str]
            if last_post_id is not None:
                params = {"after": last_post_id}

            posts = feed.hot(params=params)
            if not posts:
                return

            limit_to_download = limit - num_downloaded
            num_downloaded, last_post_id = self.download_images_from_posts(
                posts, limit_to_download
            )
