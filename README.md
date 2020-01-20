# Alien Wallpaper

Download images from subreddits. Great for beautiful wallpaper. Requires Python
3.3+.

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.

```bash
$ alien_wallpaper --help
usage: alien_wallpaper.py [-h] [--subreddits [SUBREDDITS [SUBREDDITS ...]]]
                          [--multireddit [MULTIREDDIT]] --out OUT [-v]

Download images from Reddit.

optional arguments:
  -h, --help            show this help message and exit
  --subreddits [SUBREDDITS [SUBREDDITS ...]]
  --multireddit [MULTIREDDIT]
                        USER/multi_name
  --out OUT
  -v, --verbose
```

## Features

- Can be easily set up to run on a schedule on macOS using `launchctl`
- Supports downloading images from one or more subreddits, or a multireddit

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
