# tasks.py
from invoke import task

@task
def build(c):
    """Build all containers."""
    c.run("docker-compose build")

@task
def up(c, env="dev"):
    """
    Bring up containers. 
    Usage: 
        inv up                 # uses dev
        inv up --env=prod
        inv up --env=staging
    """
    compose_base = "docker-compose.yml"
    compose_override = f"docker-compose.{env}.yml"
    c.run(f"docker-compose -f {compose_base} -f {compose_override} up -d")

@task
def down(c, env="dev"):
    """
    Bring down containers.
    Usage:
        inv down
        inv down --env=prod
        inv down --env=staging
    """
    compose_base = "docker-compose.yml"
    compose_override = f"docker-compose.{env}.yml"
    c.run(f"docker-compose -f {compose_base} -f {compose_override} down")

@task
def shell(c):
    """
    Open a bash shell in the dev_env container.
    """
    c.run("docker exec -it dev_env /bin/bash")

@task
def test(c):
    """
    Run pytest in dev_env container.
    """
    c.run("docker exec -it dev_env pytest")
