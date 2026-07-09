"""Simple WSGI application to serve static files built by mkdocs.

Usage:
    gunicorn --bind 0.0.0.0:8000 app:application
"""

from http import HTTPStatus
import mimetypes
from pathlib import Path

SITE_DIR = Path("/build/site")


def application(environ, start_response):
    """WSGI application for serving static files."""
    path = environ.get("PATH_INFO", "").lstrip("/")

    if path.endswith(".md"):
        redirect_path = path[:-3]
        redirect_url = f"/{redirect_path}"
        start_response(
            str(int(HTTPStatus.MOVED_PERMANENTLY)),
            [("Location", redirect_url)],
        )
        return [b"Moved Permanently"]

    if not path or path.endswith("/"):
        path = path.rstrip("/")
        path = path + "/index.html" if path else "index.html"

    file_path = SITE_DIR / path.lstrip("/")

    if file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        content_type = content_type or "application/octet-stream"
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            start_response(
                str(int(HTTPStatus.OK)),
                [("Content-Type", content_type)],
            )
            return [content]
        except Exception:
            start_response(
                str(int(HTTPStatus.INTERNAL_SERVER_ERROR)),
                [("Content-Type", "text/plain")],
            )
            return [b"Internal Server Error"]

    if file_path.is_dir():
        index_file = file_path / "index.html"
        if index_file.is_file():
            try:
                with open(index_file, "rb") as f:
                    content = f.read()
                start_response(
                    str(int(HTTPStatus.OK)),
                    [("Content-Type", "text/html")],
                )
                return [content]
            except Exception:
                start_response(
                    str(int(HTTPStatus.INTERNAL_SERVER_ERROR)),
                    [("Content-Type", "text/plain")],
                )
                return [b"Internal Server Error"]

    start_response(str(int(HTTPStatus.NOT_FOUND)), [("Content-Type", "text/plain")])
    return [b"Not Found"]
