# Alien Wallpaper
Download images from subreddits. Great for beautiful wallpaper. See 'usage' for
the default number of images to download, subreddits to download from, and the
output directory.


## Getting Started
### Quick Setup
```
wget https://raw.githubusercontent.com/rgardner/Alien-Wallpaper/master/alien_wallpaper.rb
```

### Usage
```
$ ruby alien_wallpaper.rb -h
Download beautiful wallpaper from subreddits
Usage: alien_wallpaper [options]
    -n N                             Number of images to download for each subreddit
    -o, --out DIR                    Directory to save wallpaper to
    -s, --subreddits S               Comma separated subreddits todownload images from; the defaults are SFW
    -h, --help                       Display this screen
```


## TODO
1. Download all images that RES can preview.
  - Flickr lightbox.
  - urls without a file extension.
