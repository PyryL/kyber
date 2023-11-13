from invoke import task

@task
def test(ctx):
    ctx.run("pytest tests/", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run -m pytest --ignore tests/test_integration.py tests/", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint kyber/", pty=True)
