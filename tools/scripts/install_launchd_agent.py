#!/usr/bin/env python3

"""Helper tool to install Alien Wallpaper as a launchd agent."""

import argparse
import plistlib
import subprocess
from pathlib import Path
from typing import Any, Dict, List

LAUNCHD_PLIST_NAME = "com.alienwallpaper.alienwallpaper.plist"


def generate_launchd_config(program_argv: List[str]) -> Dict[Any, Any]:
    """Generates launchd config that runs the program on a schedule."""
    return {
        "Label": "com.alienwallpaper.alienwallpaper",
        "ProgramArguments": program_argv,
        "StartCalendarInterval": {"Hour": 17, "Minute": 0},
        "StandardOutPath": str(get_agent_stdout_log()),
        "StandardErrorPath": str(get_agent_stderr_log()),
    }


def install():
    """Installs Alien Wallpaper launchd agent."""
    # first uninstall to unload launch agent
    uninstall()

    # subreddits = input("subreddits (comma-separated): ")
    multireddit = input("multireddit (USERNAME/MULTINAME): ")
    default_pics_dir = Path.home() / "Pictures"
    out = input(f"out (e.g. {default_pics_dir}): ")

    program_args = [
        "/Users/bobgardner/.pyenv/shims/python3",
        "-m",
        "alien_wallpaper",
        "--multireddit",
        multireddit,
        "--out",
        out,
    ]
    agent_config = generate_launchd_config(program_args)
    agent_config_file = get_launch_agents_dir() / LAUNCHD_PLIST_NAME
    with open(agent_config_file, "wb") as f:
        plistlib.dump(agent_config, f, fmt=plistlib.FMT_XML)

    subprocess.run(["launchctl", "load", "-w", agent_config_file], check=True)


def uninstall():
    """Uninstalls Alien Wallpaper launchd agent."""
    plist = get_launch_agents_dir() / LAUNCHD_PLIST_NAME
    subprocess.run(
        ["launchctl", "unload", "-w", plist],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    plist.unlink(missing_ok=True)

    # Remove log files
    get_agent_stdout_log().unlink(missing_ok=True)
    get_agent_stderr_log().unlink(missing_ok=True)


def get_launch_agents_dir() -> Path:
    """Returns user LaunchAgents directory."""
    launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
    assert launch_agents_dir.is_dir()
    return launch_agents_dir


def get_agent_log_dir() -> Path:
    """Returns user log directory."""
    log_root_dir = (
        Path.home() / "Library" / "Logs" / "com.alienwallpaper.alienwallpaper"
    )
    log_root_dir.mkdir(parents=True, exist_ok=True)
    assert log_root_dir.is_dir()
    return log_root_dir


def get_agent_stdout_log() -> Path:
    """Returns path to stdout log file."""
    return get_agent_log_dir() / "com.alienwallpaper.alienwallpaper.out"


def get_agent_stderr_log() -> Path:
    """Returns path to stderr log file."""
    return get_agent_log_dir() / "com.alienwallpaper.alienwallpaper.err"


def parse_cli_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Install Alien Wallpaper launchd agent"
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall Alien Wallpaper launchd agent",
    )
    return parser.parse_args()


def main():
    """Main entrypoint."""
    args = parse_cli_args()
    if args.uninstall:
        uninstall()
    else:
        install()


if __name__ == "__main__":
    main()
