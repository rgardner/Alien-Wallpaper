#!/usr/bin/env python3

import os
import os.path
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
