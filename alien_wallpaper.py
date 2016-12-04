#!/usr/bin/env python3
"""
Download images from Reddit.

```bash
$ alien_wallpaper --help
```

"""

import argparse
import json
import logging
import multiprocessing
import os.path
import re
import shutil
import sys
import typing
import urllib.parse
import urllib.request

IMAGES_PER_SUBREDDIT = 25
DEFAULT_SUBREDDITS = ['ArchitecturePorn', 'CityPorn', 'EarthPorn', 'SkyPorn',
                      'spaceporn', 'winterporn', 'quoteporn']
USER_AGENT = 'AlienWallpaper by /u/WolfBlackout'

FILE_EXTENSION_PROG = re.compile('.*.(jpg|jpeg|gif|png)$', re.IGNORECASE)
Url = typing.NewType('Url', str)


class Post:
    def __init__(self, post_id: str, is_self: bool, url: Url) -> None:
        self.id = post_id
        self.is_self = is_self
        self.url = url

    @property
    def is_valid(self) -> bool:
        return not self.is_self and bool(FILE_EXTENSION_PROG.match(self.url))

    @property
    def filename(self) -> typing.Optional[str]:
        if self.extension is not None:
            return self.id + '.' + self.extension

    @property
    def extension(self) -> typing.Optional[str]:
        match = FILE_EXTENSION_PROG.match(self.url)
        if match is not None:
            return match.group(1)

    def download(self, out_dir):
        path = os.path.join(out_dir, self.filename)
        logging.debug(path)

        try:
            with urllib.request.urlopen(self.url) as response, open(path, 'wb+') as out_file:
                shutil.copyfileobj(response, out_file)
        except urllib.error.HTTPError as e:
            logging.exception(e)

    @staticmethod
    def from_json(data) -> 'Post':
        return Post(data['id'], bool(data['is_self']), Url(data['url']))


def subreddit_to_url(subreddit: str) -> Url:
    return Url('https://www.reddit.com/r/{}'.format(subreddit))


def fetch_posts(subreddit: Url, limit=25, after=''):
    params = urllib.parse.urlencode({'limit': limit, 'after': after})
    url = '{}.json?{}'.format(subreddit, params)
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode('utf-8'))
    return [Post.from_json(p['data']) for p in result['data']['children']]


def download_images(subreddit_name, n, out_dir) -> None:
    posts = fetch_posts(subreddit_name, limit=n)
    num_images = 0
    while True:
        for post in posts:
            if post.is_valid:
                post.download(out_dir)
                num_images += 1
                if num_images >= n:
                    return

        posts = fetch_posts(subreddit_name, limit=n, after=posts[-1].id)


def download_all_images(subreddits: typing.Sequence[Url], n, out_dir):
    """Download n images in parallel for each subreddit to out_dir."""
    with multiprocessing.Pool() as pool:
        for subreddit in subreddits:
            pool.apply(download_images, args=(subreddit, n, out_dir))


def parse_cli():
    parser = argparse.ArgumentParser(description='Download images from Reddit.')
    parser.add_argument('--subreddits', nargs='*')
    parser.add_argument('--multireddit', nargs='?', help='USER/multi_name')
    parser.add_argument('--out', required=True)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    return parser.parse_args()


def main():
    args = parse_cli()
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, level=logging_level)

    if not args.subreddits and not args.multireddit:
        subreddits = [subreddit_to_url(s) for s in DEFAULT_SUBREDDITS]
    else:
        subreddits = []
        if args.subreddits:
            subreddits.extend([subreddit_to_url(s) for s in args.subreddits])

        if args.multireddit:
            user, multi = args.multireddit.split('/')
            multi_url = 'https://www.reddit.com/user/{}/m/{}'.format(user, multi)
            subreddits.append(multi_url)

    download_all_images(subreddits, IMAGES_PER_SUBREDDIT, args.out)

if __name__ == '__main__':
    main()
