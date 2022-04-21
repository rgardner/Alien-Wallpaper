# Alien Wallpaper

![Tests Status](https://github.com/rgardner/Alien-Wallpaper/workflows/CI/badge.svg)

Download images from subreddits. Great for beautiful wallpaper. Requires Python
3.10+.

```bash
# Download images from default subreddits to output directory
alien_wallpaper download --out output

# Download images from specific subreddits
alien_wallpaper download --out output --subreddits pics

# Download images from custom feeds
alien_wallpaper download --out output --custom-feeds user/feed_name
```

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.

Alien Wallpaper also supports running automatically as a daemon:

```bash
$ # generate default config
$ alien_wallpaper daemon generate-config >config.toml
$ # fill in the config file
$ vim config.toml
$ # load the daemon
$ alien_wallpaper daemon load config.toml
$ # check on the status of the daemon
$ alien_wallpaper daemon status
Launchd Agent: Installed
Debug logs: /Users/user/Logs/com.alienwallpaper.alienwallpaper/com.alienwallpaper.alienwallpaper.out.log
Error logs: /Users/user/Logs/com.alienwallpaper.alienwallpaper/com.alienwallpaper.alienwallpaper.err.log
$ # unload the daemon
$ alien_wallpaper daemon unload
```

## Features

- Can be easily set up to run on a schedule on macOS using `launchctl`
- Supports downloading images from subreddits and [Custom Feeds][reddit-custom-feed]

## Installation

This project requires Python 3.10\* and [Poetry](https://python-poetry.org/).

Install dependencies:

```bash
poetry install
```

Given this is a personal-use script, `alien_wallpaper` uses the
[Application-Only (Client Credentials)](https://praw.readthedocs.io/en/v6.5.1/getting_started/authentication.html#application-only-client-credentials)
form of authentication. To use this script:

1. [Register the application with Reddit](https://www.reddit.com/prefs/apps/)
2. Set the `ALIEN_WALLPAPER_CLIENT_ID` environment variable to the app's client ID
3. Set the `ALIEN_WALLPAPER_CLIENT_SECRET` environment variable to the app's client secret

## Contributing

This project uses [pre-commit](https://pre-commit.com/) for git pre-commit
hook management.

Running the test suite:

```sh
poetry shell
invoke test
```

## Future Improvements

1. Download all images that RES can preview.
   - Flickr lightbox.
   - urls without a file extension.

[reddit-custom-feed]: https://www.reddit.com/r/announcements/comments/bpfyx1/introducing_custom_feeds_plus_a_community_contest/
