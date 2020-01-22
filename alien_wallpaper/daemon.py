"""Contains daemon-related functionality."""

import argparse
import plistlib
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import CalledProcessError
from typing import Any, Dict, List

import toml

LAUNCHD_LABEL = "com.alienwallpaper.alienwallpaper"
LAUNCHD_PLIST_NAME = "com.alienwallpaper.alienwallpaper.plist"


@dataclass
class DaemonConfig:
    """Data object for configuration file."""

    python3_path: Path = Path()
    subreddits: List[str] = field(default_factory=list)
    custom_feeds: List[str] = field(default_factory=list)
    output_directory: Path = Path()

    @staticmethod
    def load_toml(path: Path) -> "DaemonConfig":
        """Parses config file into strongly-typed data object."""
        config = toml.load(path)
        return DaemonConfig(
            python3_path=Path(config["python3_path"]),
            subreddits=config["subreddits"],
            custom_feeds=config["custom_feeds"],
            output_directory=Path(config["output_directory"]),
        )

    def dumps_toml(self) -> str:
        """Dumps self as toml, converting empty paths to empty strings."""

        def path_to_str(path: Path) -> str:
            return str(path) if path.parts else ""

        data = {
            "python3_path": path_to_str(self.python3_path),
            "subreddits": self.subreddits,
            "custom_feeds": self.custom_feeds,
            "output_directory": path_to_str(self.output_directory),
        }
        return toml.dumps(data)


def generate_launchd_config(config: DaemonConfig) -> Dict[Any, Any]:
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


def load_daemon(user_config_file: Path):
    """Installs Alien Wallpaper launchd agent."""
    # first unload the daemon
    unload_daemon()

    user_config = DaemonConfig.load_toml(user_config_file)

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


def get_daemon_status():
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


def unload_daemon():
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


def run_generate_config_command(_args):
    """Displays default daemon config on stdout."""
    print(DaemonConfig().dumps_toml())


def run_load_daemon_command(args: argparse.Namespace):
    """Loads daemon using config file settings."""
    load_daemon(args.config)


def run_unload_daemon_command(_args):
    """Unloads the daemon and cleans up log files."""
    unload_daemon()


def run_daemon_status_command(_args):
    """Queries daemon status and displays additional information."""
    get_daemon_status()
