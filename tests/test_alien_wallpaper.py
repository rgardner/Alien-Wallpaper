"""Alien Wallpaper tests."""

import json

import pytest

import alien_wallpaper
from alien_wallpaper import Post, Url, __version__


def test_version():
    """Verifies version string is correct."""
    assert __version__ == "0.1.0"


class MockPost:
    """Mock Post to facilitate testing."""

    def __init__(self, post: Post, json_data):
        self.post = post
        self.json = json.loads(json_data)


# pylint: disable=line-too-long
TEST_POST = MockPost(
    Post("5gfjre", False, Url("http://i.imgur.com/XQgSj3o.jpg")),
    """
{
    "contest_mode": false,
    "banned_by": null,
    "domain": "i.imgur.com",
    "subreddit": "EarthPorn",
    "selftext_html": null,
    "selftext": "",
    "likes": null,
    "suggested_sort": null,
    "user_reports": [

    ],
    "secure_media": null,
    "saved": false,
    "id": "5gfjre",
    "gilded": 0,
    "secure_media_embed": {

    },
    "clicked": false,
    "report_reasons": null,
    "author": "lukaas2",
    "media": null,
    "name": "t3_5gfjre",
    "score": 3959,
    "approved_by": null,
    "over_18": false,
    "removal_reason": null,
    "hidden": false,
    "preview": {
        "images": [
            {
                "source": {
                    "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?s=d2ee7033a5824fa60f68b7c08c82cf81",
                    "width": 5135,
                    "height": 3327
                },
                "resolutions": [
                    {
                        "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?fit=crop&amp;crop=faces%2Centropy&amp;arh=2&amp;w=108&amp;s=5d93c132b0c4654d234b1a0716a53235",
                        "width": 108,
                        "height": 69
                    },
                    {
                        "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?fit=crop&amp;crop=faces%2Centropy&amp;arh=2&amp;w=216&amp;s=de00d76fbebb5ba2307d0ae3e7fd5467",
                        "width": 216,
                        "height": 139
                    },
                    {
                        "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?fit=crop&amp;crop=faces%2Centropy&amp;arh=2&amp;w=320&amp;s=fb87cbe947e07a720598fd6e30c53d5a",
                        "width": 320,
                        "height": 207
                    },
                    {
                        "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?fit=crop&amp;crop=faces%2Centropy&amp;arh=2&amp;w=640&amp;s=8ee71f9f20d159f29f36ad0b2e4af4a5",
                        "width": 640,
                        "height": 414
                    },
                    {
                        "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?fit=crop&amp;crop=faces%2Centropy&amp;arh=2&amp;w=960&amp;s=65946023127783328b5498dce111f412",
                        "width": 960,
                        "height": 621
                    },
                    {
                        "url": "https://i.redditmedia.com/QRosL3xOUwuzgDhm3SsmyBjYHrVH3w9B1lz101krEYg.jpg?fit=crop&amp;crop=faces%2Centropy&amp;arh=2&amp;w=1080&amp;s=5f1538ac08d1bee1ccb8c878c32a38a6",
                        "width": 1080,
                        "height": 699
                    }
                ],
                "variants": {

                },
                "id": "2grwxIgMiygG4BM3VipcujVWm6iC7nn4PZndaY5oISw"
            }
        ]
    },
    "thumbnail": "http://a.thumbs.redditmedia.com/OsggFhJKhNraNrMFK-GvIKKFST9-1GH6uEBW1YdlNN4.jpg",
    "subreddit_id": "t5_2sbq3",
    "edited": false,
    "link_flair_css_class": null,
    "author_flair_css_class": "Camera",
    "downs": 0,
    "mod_reports": [

    ],
    "archived": false,
    "media_embed": {

    },
    "post_hint": "image",
    "is_self": false,
    "hide_score": false,
    "spoiler": false,
    "permalink": "/r/EarthPorn/comments/5gfjre/verdon_gorge_france_provence_oc_5135x3327/",
    "locked": false,
    "stickied": false,
    "created": 1480889161.0,
    "url": "http://i.imgur.com/XQgSj3o.jpg",
    "author_flair_text": null,
    "quarantine": false,
    "title": "Verdon Gorge, France (Provence) [OC, 5135x3327]",
    "created_utc": 1480860361.0,
    "link_flair_text": null,
    "distinguished": null,
    "num_comments": 52,
    "visited": false,
    "num_reports": null,
    "ups": 3959
}
""",
)

# pylint: disable=line-too-long
TEST_SELF_POST = MockPost(
    Post(
        "5f9zc4",
        True,
        Url(
            "https://www.reddit.com/r/rust/comments/5f9zc4/whats_everyone_working_on_this_week_422016/"
        ),
    ),
    """
{
    "contest_mode": false,
    "banned_by": null,
    "domain": "self.rust",
    "subreddit": "rust",
    "selftext_html": "things",
    "selftext": "Answer here or on the [rust-users thread](https://users.rust-lang.org/t/whats-everyone-working-on-this-week-42-2016/8188?u=llogiq)!",
    "likes": null,
    "suggested_sort": null,
    "user_reports": [

    ],
    "secure_media": null,
    "saved": false,
    "id": "5f9zc4",
    "gilded": 0,
    "secure_media_embed": {

    },
    "clicked": false,
    "report_reasons": null,
    "author": "llogiq",
    "media": null,
    "name": "t3_5f9zc4",
    "score": 20,
    "approved_by": null,
    "over_18": false,
    "removal_reason": null,
    "hidden": false,
    "thumbnail": "",
    "subreddit_id": "t5_2s7lj",
    "edited": false,
    "link_flair_css_class": null,
    "author_flair_css_class": "contrib",
    "downs": 0,
    "mod_reports": [

    ],
    "archived": false,
    "media_embed": {

    },
    "is_self": true,
    "hide_score": false,
    "spoiler": false,
    "permalink": "/r/rust/comments/5f9zc4/whats_everyone_working_on_this_week_422016/",
    "locked": false,
    "stickied": true,
    "created": 1480339845.0,
    "url": "https://www.reddit.com/r/rust/comments/5f9zc4/whats_everyone_working_on_this_week_422016/",
    "author_flair_text": "clippy · twir · rust · metacollect · flamer · overflower",
    "quarantine": false,
    "title": "What's everyone working on this week (42/2016)?",
    "created_utc": 1480311045.0,
    "link_flair_text": null,
    "distinguished": "moderator",
    "num_comments": 42,
    "visited": false,
    "num_reports": null,
    "ups": 20
}
""",
)


@pytest.mark.parametrize("test_post", [TEST_POST, TEST_SELF_POST])
def test_image_post_from_json(test_post: MockPost):
    """Verifies post can be parsed from JSON correctly."""
    post = alien_wallpaper.Post.from_json(test_post.json)
    assert post == test_post.post


@pytest.mark.large
def test_download_all_images(tmp_path):
    """Verifies images can be downloaded."""
    subreddits = [alien_wallpaper.custom_feed_to_url("wolf_blackout", "wallpaper")]
    num_images = 1
    out_dir = tmp_path / "output"
    out_dir.mkdir()

    alien_wallpaper.download_all_images(subreddits, num_images, out_dir)
    assert len(list(out_dir.iterdir())) == 1
