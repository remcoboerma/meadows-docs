"""MEADOWS documentation site tasks.

Usage:
    edwh local.setup   # check env vars
    edwh local.build   # build static site via Docker
    edwh local.update  # build + restart server
    edwh local.serve   # dev server (mkdocs serve)
"""

from pathlib import Path

import invoke.exceptions
from edwh import tasks, task
from invoke import Context

check_env = tasks.check_env

DOCS_DIR = Path(__file__).parent / "docs"
SITE_DIR = Path(__file__).parent / "site"


@task
def setup(c: Context) -> None:
    """Check environment variables and create .env if needed."""
    check_env("PROJECT", default="meadows-docs", comment="Project name")
    check_env("NAME_SERVICE", default="meadows", comment="Name of the service")
    check_env("HOSTINGDOMAIN", default="meadows.chat", comment="Hosting domain")


@task
def build(c: Context) -> None:
    """Build the documentation site using Docker.

    Runs the builder container which copies docs into the image, builds
    the static site, and outputs to ./site via a volume mount.
    """
    try:
        c.run("docker compose down builder", warn=True)
        c.run("docker compose run --rm builder", warn=False)
        c.run("docker compose logs builder", warn=True)
        print("✓ Documentation built successfully")
    except invoke.exceptions.UnexpectedExit as e:
        print(f"✗ Build failed: {e}")
        raise


@task
def update(c: Context) -> None:
    """Build documentation and restart hosting service on success."""
    try:
        build(c)
        print("\nRestarting hosting service...")
        c.run("docker compose restart server")
        print("✓ Hosting service restarted successfully")
    except invoke.exceptions.UnexpectedExit as e:
        print(f"✗ Build failed: {e}")
        raise


@task
def serve(c: Context) -> None:
    """Run MkDocs development server (localhost:8000).

    Mounts ./docs into the container for live reload.
    """
    c.run(
        "docker compose up mkdocs",
        pty=True,
    )


@task
def clean(c: Context) -> None:
    """Remove built site directory."""
    if SITE_DIR.exists():
        import shutil

        shutil.rmtree(SITE_DIR)
        print("✓ Removed site/")
    else:
        print("Nothing to clean.")
