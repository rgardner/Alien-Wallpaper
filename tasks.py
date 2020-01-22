"""Alien Wallpaper Invoke tasks."""

from invoke import task


@task
def run(ctx):
    """Runs alien_wallpaper tool."""
    ctx.run("poetry run alien_wallpaper")


@task
def test(ctx, large=False):
    """Runs tests."""
    if large:
        ctx.run("poetry run pytest tests")
    else:
        ctx.run("poetry run pytest tests -m 'not large'")


@task
def lint(ctx):
    """Runs linters."""
    ctx.run("pre-commit run")


@task
def lint_ci(ctx):
    """Runs linters in CI configuration."""
    ctx.run("poetry run pre-commit run --all-files")
