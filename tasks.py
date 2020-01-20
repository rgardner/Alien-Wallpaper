"""Alien Wallpaper Invoke tasks."""

from invoke import task


@task
def run(ctx):
    """Runs alien_wallpaper tool."""
    ctx.run("poetry run alien_wallpaper")


@task
def test(ctx):
    """Runs tests."""
    ctx.run("poetry run pytest tests")


@task
def lint(ctx):
    """Runs linters."""
    ctx.run("pre-commit run")
