from invoke import task


@task
def run(c):
    c.run("poetry run python3 -m alien_wallpaper")


@task
def test(c):
    c.run("poetry run pytest tests")
