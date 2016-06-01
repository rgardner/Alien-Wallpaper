#!/usr/bin/env python3
"""
Download images from Reddit.

```bash
$ python3 alien_wallpaper.py --help
```
"""

import argparse
from functools import partial
import multiprocessing

IMAGES_PER_SUBREDDIT = 25
DEFAULT_SUBREDDITS = ['ArchitecturePorn', 'CityPorn', 'EarthPorn', 'SkyPorn',
                      'spaceporn', 'winterporn', 'quoteporn']

# FILE_EXTENSION_REGEX = /\.(jpg|jpeg|gif|png)$/i


def multireddit_to_subreddits(multireddit):
    return ...


def download_images(subreddit, out_dir):
    print('Subreddit: {}\tOutput: {}'.format(subreddit, out_dir))


def parse_cli():
    parser = argparse.ArgumentParser(description='Download Reddit images.')
    parser.add_argument('--subreddits', nargs='*')
    parser.add_argument('--multireddit', nargs='?')
    parser.add_argument('--out', required=True)
    return parser.parse_args()


def main():
    # Parse CLI arguments to get subreddits and output directory.
    args = parse_cli()
    if args.subreddits is None and args.multireddit is None:
        subreddits = DEFAULT_SUBREDDITS
    else:
        subreddits = args.subreddits or []
        subreddits.extend(multireddit_to_subreddits(args.multireddit))

    pool = multiprocessing.Pool()
    download_images_to_dir = partial(download_images, out_dir=args.out)
    pool.map(download_images_to_dir, subreddits)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
