# Alien Wallpaper

Download images from subreddits. Great for beautiful wallpaper.

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.

```bash
$ alien_wallpaper --help
usage: alien_wallpaper [-h] [--subreddits [SUBREDDITS [SUBREDDITS ...]]]
                       [--multireddit [MULTIREDDIT]] --out OUT

Download Reddit images.

optional arguments:
  -h, --help            show this help message and exit
  --subreddits [SUBREDDITS [SUBREDDITS ...]]
  --multireddit [MULTIREDDIT]
  --out OUT
```


## Installation

```bash
$ # download project
$ curl -LOk https://github.com/rgardner/Alien-Wallpaper/archive/master.zip
$ unzip master.zip && cd Alien-Wallpaper-master
$ # install script
$ cp alien_wallpaper /usr/local/bin
$ # install launchd plist
$ # edit wallpaper.job.plist
$ cp wallpaper.job.plist ~/Library/LaunchAgents
$ launchctl load -w ~/Library/LaunchAgents/wallpaper.job.plist
```


## TODO

1. Download all images that RES can preview.
  - Flickr lightbox.
  - urls without a file extension.
