# Alien Wallpaper
Download images from Subreddits. Great for beautiful wallpaper.

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
         --out, -o <s>:   Directory to save wallpaper to
    --password, -p <s>:   Your Reddit password
  --subreddits, -s <s>:   Comma separated subreddits to download images from
    --username, -u <s>:   Your Reddit username
            --help, -h:   Show this message
```

## TODO
1. Download all images that RES can preview.
