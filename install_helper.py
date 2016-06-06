#!/usr/bin/env python3

import os
from pathlib import Path
import shutil
import string

BIN = 'alien_wallpaper'
LAUNCHD_PLIST_TEMPL = '_com.alienwallpaper.alienwallpaper.plist'
LAUNCHD_PLIST_FINAL = 'com.alienwallpaper.alienwallpaper.plist'


def main():
    # prompt user for subreddits, multireddit, and output directory
    subreddits = input('subreddits (comma-separated): ')
    multireddit = input('multireddit (USER/MULTI): ')
    out = input('out (e.g. /Users/user/Pictures): ')

    # read plist template and write config variables
    with open(LAUNCHD_PLIST_TEMPL) as f:
        templ = string.Template(f.read())
    final = templ.substitute(subreddits=subreddits, multireddit=multireddit,
                             out=out)
    with open(LAUNCHD_PLIST_FINAL, 'w+') as f:
        f.write(str(final))

    # install wallpaper script and initialize launchd job
    shutil.copy2(BIN, '/usr/local/bin')
    dst = Path.home().joinpath('Library/LaunchAgents')
    shutil.copy2(LAUNCHD_PLIST_FINAL, str(dst))
    os.system('launchctl load -w ' + str(dst.joinpath(LAUNCHD_PLIST_FINAL)))


if __name__ == '__main__':
    main()
