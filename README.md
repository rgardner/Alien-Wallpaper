# Alien Wallpaper
Download images from subreddits. Great for beautiful wallpaper. See 'usage' for
the default number of images to download, subreddits to download from, and the
output directory.

Each picture is saved to the output directory as `{reddit_id}.{filetype}`,
e.g. `2zd9do.jpg`. You can reverse lookup any of the pictures just by going to
`https://www.reddit.com/{reddit_id}`, which will take you to its comments page,
e.g. `https://www.reddit.com/2zd9do`.


## Getting Started
### Quick Setup
```bash
curl https://raw.githubusercontent.com/rgardner/Alien-Wallpaper/master/alien_wallpaper.rb >alien_wallpaper.rb
```

### Usage
```bash
$ ruby alien_wallpaper.rb -h
Download beautiful wallpaper from subreddits
Usage: alien_wallpaper [options]
        --subreddits=x,y,z           List of subreddits
        --multi M                    user/multireddit
        --out DIR                    Directory to save wallpaper to
    -h, --help                       Show this message
```

## TODO
1. Download all images that RES can preview.
  - Flickr lightbox.
  - urls without a file extension.
