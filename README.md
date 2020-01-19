# Alien Wallpaper

Download images from subreddits. Great for beautiful wallpaper. Requires Python
3.3+.

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.

```bash
$ python3 alien_wallpaper.py --help
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

## Installation

```bash
# run installation helper script
./install_helper.py
```

## TODO

1. Download all images that RES can preview.
   - Flickr lightbox.
   - urls without a file extension.
