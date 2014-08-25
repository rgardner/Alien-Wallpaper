# Alien Wallpaper
Download images from Subreddits. Great for beautiful wallpaper. See 'usage' for
the default number of images to download, subreddits to download from, and the
output directory.

## Getting Started
### Quick Setup
```
wget https://github.com/rgardner/Alien-Image-Downloader/blob/master/alien_wallpaper.rb
gem install snoo
gem install trollop
```

### Usage
```
$ ./alien_wallpaper.rb -h
Download Wallpaper from Subreddits
            --n, -n <i>:   Number of images to download for each subreddit
                           (default: 25)
          --out, -o <s>:   Directory to save wallpaper to (default: Dir.pwd)
     --password, -p <s>:   Your Reddit password
  --subreddits, -s <s+>:   Comma separated subreddits to download images from;
                           the defaults are SFW (default: ArchitecturePorn,
                           CityPorn, EarthPorn, SkyPorn, spaceporn, winterporn,
                           quoteporn)
     --username, -u <s>:   Your Reddit username
             --help, -h:   Show this message
```

## TODO
1. Download all images that RES can preview.
  - Flickr lightbox.
  - urls without a file extension.
