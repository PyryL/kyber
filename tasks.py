from invoke import task

@task
def test(ctx):
    ctx.run("pytest tests/", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run -m pytest tests/", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
