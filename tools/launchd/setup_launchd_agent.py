#!/usr/bin/env python3

"""Helper tool to install Alien Wallpaper as a launchd agent."""

import argparse
import plistlib
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Dict, List

import toml

LAUNCHD_LABEL = "com.alienwallpaper.alienwallpaper"
LAUNCHD_PLIST_NAME = "com.alienwallpaper.alienwallpaper.plist"


@dataclass
class AlienWallpaperConfig:
    """Data object for Alien Wallpaper configuration file."""

    python3_path: Path
    subreddits: List[str]
    custom_feeds: List[str]
    output_directory: Path

    @staticmethod
    def from_config_file(path: Path) -> "AlienWallpaperConfig":
        """Parse config file into strongly-typed data object."""
        raw_config = toml.load(path)
        section = raw_config["launchd_config"]
        return AlienWallpaperConfig(
            python3_path=Path(section["python3-path"]),
            subreddits=section["subreddits"],
            custom_feeds=section["custom-feeds"],
            output_directory=Path(section["output-directory"]),
        )


def generate_launchd_config(config: AlienWallpaperConfig) -> Dict[Any, Any]:
    """Generates launchd config that runs the program on a schedule."""
    program_args = [
        str(config.python3_path),
        "-m",
        "alien_wallpaper",
        "--verbose",
        "--out",
        str(config.output_directory),
    ]  # type: List[str]

    if config.subreddits:
        program_args.append("--subreddits")
        program_args.extend(config.subreddits)

    if config.custom_feeds:
        program_args.append("--custom-feeds")
        program_args.extend(config.custom_feeds)

    return {
        "Label": LAUNCHD_LABEL,
        "ProgramArguments": program_args,
        "StartCalendarInterval": {"Hour": 17, "Minute": 0},
        "StandardOutPath": str(get_agent_stdout_log()),
        "StandardErrorPath": str(get_agent_stderr_log()),
    }


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
    return get_agent_log_dir() / "com.alienwallpaper.alienwallpaper.out.log"


def get_agent_stderr_log() -> Path:
    """Returns path to stderr log file."""
    return get_agent_log_dir() / "com.alienwallpaper.alienwallpaper.err.log"


def install():
    """Installs Alien Wallpaper launchd agent."""
    # first uninstall to unload launch agent
    uninstall()

    user_config_file = Path.cwd() / "launchd_config.toml"
    user_config = AlienWallpaperConfig.from_config_file(user_config_file)

    agent_config = generate_launchd_config(user_config)
    agent_config_file = get_launch_agents_dir() / LAUNCHD_PLIST_NAME
    with open(agent_config_file, "wb") as f:
        plistlib.dump(agent_config, f, fmt=plistlib.FMT_XML)

    subprocess.run(["launchctl", "load", "-w", agent_config_file], check=True)
    print(f"Run `launchctl start {LAUNCHD_LABEL}` to run the agent now.")


def is_launchd_agent_installed() -> bool:
    """Returns True if launchd agent is loaded."""
    try:
        subprocess.run(
            ["launchctl", "list", LAUNCHD_LABEL],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except CalledProcessError:
        return False


def status():
    """Displays status and log file information."""
    is_installed = is_launchd_agent_installed()

    debug_logs = None
    error_logs = None
    if is_installed:
        agent_config_path = get_launch_agents_dir() / LAUNCHD_PLIST_NAME
        with open(agent_config_path, "rb") as f:
            agent_config = plistlib.load(f, fmt=plistlib.FMT_XML)

        debug_logs = Path(agent_config["StandardOutPath"])
        error_logs = Path(agent_config["StandardErrorPath"])

    print(f"Launchd Agent: {'Installed' if is_installed else 'Not installed'}")
    if debug_logs is not None:
        print(f"Debug logs: {debug_logs}")
    if error_logs is not None:
        print(f"Error logs: {error_logs}")


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
    shutil.rmtree(get_agent_log_dir())


def parse_cli_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Install Alien Wallpaper launchd agent"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="install",
        choices=("install", "status", "uninstall"),
    )
    return parser.parse_args()


def main():
    """Main entrypoint."""
    args = parse_cli_args()
    if args.command == "install":
        install()
    elif args.command == "status":
        status()
    else:
        uninstall()


if __name__ == "__main__":
    main()
