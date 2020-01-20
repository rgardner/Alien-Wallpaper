# Alien Wallpaper

![Tests Status](https://github.com/rgardner/Alien-Wallpaper/workflows/CI/badge.svg)

Download images from subreddits. Great for beautiful wallpaper. Requires Python
3.3+.

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.

```bash
$ alien_wallpaper --help
usage: alien_wallpaper [-h] [-s [SUBREDDITS [SUBREDDITS ...]]] [-c [CUSTOM_FEEDS [CUSTOM_FEEDS ...]]] -o OUT [--verbose]

Download images from Reddit.

optional arguments:
  -h, --help            show this help message and exit
  -s [SUBREDDITS [SUBREDDITS ...]], --subreddits [SUBREDDITS [SUBREDDITS ...]]
                        One or more subreddits.
  -c [CUSTOM_FEEDS [CUSTOM_FEEDS ...]], --custom-feeds [CUSTOM_FEEDS [CUSTOM_FEEDS ...]]
                        One or more custom feeds in the format USER/CUSTOM_FEED_NAME
  -o OUT, --out OUT     Output directory
  --verbose
```

## Features

- Can be easily set up to run on a schedule on macOS using `launchctl`
- Supports downloading images from subreddits and [Custom Feeds][reddit-custom-feed]

## Installation

This project requires Python 3.8\* and [Poetry](https://python-poetry.org/).

```bash
# Install dependencies
poetry install

# Using the interactive installer, set up the program to run via launchctl
tools/scripts/setup_launchctl.py
```

## Contributing

Run the test suite.

```sh
invoke test
```

Use the `automerge` label on your Pull Request to automatically merge the pull
request when the status checks pass.

## Future Improvements

1. Download all images that RES can preview.
   - Flickr lightbox.
   - urls without a file extension.

[reddit-custom-feed]: https://www.reddit.com/r/announcements/comments/bpfyx1/introducing_custom_feeds_plus_a_community_contest/
