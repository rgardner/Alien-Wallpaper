# Alien Wallpaper

![Tests Status](https://github.com/rgardner/Alien-Wallpaper/workflows/CI/badge.svg)

Download images from subreddits. Great for beautiful wallpaper. Requires Python
3.8+.

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.

```bash
$ alien_wallpaper --help
usage: alien_wallpaper [-h] [-s [SUBREDDITS [SUBREDDITS ...]]]
                       [-c [CUSTOM_FEEDS [CUSTOM_FEEDS ...]]] -o OUT [--verbose]

Download images from Reddit.

optional arguments:
  -h, --help            show this help message and exit
  -s [SUBREDDITS [SUBREDDITS ...]], --subreddits [SUBREDDITS [SUBREDDITS ...]]
                        one or more subreddits.
  -c [CUSTOM_FEEDS [CUSTOM_FEEDS ...]], --custom-feeds [CUSTOM_FEEDS [CUSTOM_FEEDS ...]]
                        one or more custom feeds in the format USER/CUSTOM_FEED_NAME
  -o OUT, --out OUT     output directory
  --verbose
```

## Features

- Can be easily set up to run on a schedule on macOS using `launchctl`
- Supports downloading images from subreddits and [Custom Feeds][reddit-custom-feed]

## Installation

This project requires Python 3.8\* and [Poetry](https://python-poetry.org/).

Install dependencies:

```bash
# Use `--extras launchd` to facilitate launchd support on macOS
poetry install --extras launchd
```

### Set up launchd agent

```bash
cd tools/launchd

# Edit launchd_config.toml
cp launchd_config.example.toml launchd_config.toml
vim launchd_config.toml

# Run installer
./setup_launchd_agent.py
```

Logs are available here:

```bash
$ tools/launchd/setup_launchd_agent.py status
Launchd Agent: Installed
Debug logs: /Users/user/Logs/com.alienwallpaper.alienwallpaper/com.alienwallpaper.alienwallpaper.out.log
Error logs: /Users/user/Logs/com.alienwallpaper.alienwallpaper/com.alienwallpaper.alienwallpaper.err.log
```

To uninstall the agent and remove the log files:

```bash
tools/launchd/setup_launchd_agent.py uninstall
```

## Contributing

This project uses [pre-commit](https://pre-commit.com/) for git pre-commit
hook management. Run `invoke setup` to configure them.

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
