#!/usr/bin/env python3

import argparse
import os
import os.path
import shutil
import string

BIN = 'alien_wallpaper.py'
LAUNCHD_PLIST_TEMPL = '_com.alienwallpaper.alienwallpaper.plist'
LAUNCHD_PLIST_FINAL = 'com.alienwallpaper.alienwallpaper.plist'


def main():
    args = parse_cli_args()
    if args.uninstall:
        uninstall()
    else:
        install()

def parse_cli_args():
    parser = argparse.ArgumentParser(description='Install helper')
    parser.add_argument('--uninstall', action='store_true')
    return parser.parse_args()


def install():
    # first uninstall to unload launch agent
    uninstall()

    subreddits = input('subreddits (comma-separated): ')
    multireddit = input('multireddit (USERNAME/MULTINAME): ')
    out = input('out (e.g. /Users/user/Pictures): ')

    with open(LAUNCHD_PLIST_TEMPL) as f:
        templ = string.Template(f.read())
    final = templ.substitute(subreddits=subreddits, multireddit=multireddit,
                             out=out)
    with open(LAUNCHD_PLIST_FINAL, 'w+') as f:
        f.write(str(final))

    shutil.copy2(BIN, '/usr/local/bin')
    la_dir = os.path.join(os.path.expanduser('~'), 'Library/LaunchAgents')
    shutil.copy2(LAUNCHD_PLIST_FINAL, la_dir)
    os.system('launchctl load -w ' + os.path.join(la_dir, LAUNCHD_PLIST_FINAL))


def uninstall():
    os.remove(os.path.join('/usr/local/bin', BIN))
    la_dir = os.path.join(os.path.expanduser('~'), 'Library/LaunchAgents')
    plist = os.path.join(la_dir, LAUNCHD_PLIST_FINAL)
    os.system('launchctl unload -w ' + plist)
    os.remove(plist)
    os.remove('/tmp/com.alienwallpaper.alienwallpaper.out')
    os.remove('/tmp/com.alienwallpaper.alienwallpaper.err')


if __name__ == '__main__':
    main()
