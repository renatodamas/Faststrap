"""Static path extraction and URL helpers used by Faststrap asset mounting."""

from __future__ import annotations

import atexit
import threading
from contextlib import ExitStack
from importlib.resources import as_file, files

# ---------- core helpers ----------
from pathlib import Path
from typing import Any

from fasthtml.common import Link

# Thread-safe singleton management for static file extraction
_STATIC_LOCK = threading.Lock()
_APP_STATIC_STACK: ExitStack | None = None
_EXTRACTED_STATIC_PATH: Path | None = None
_ATEXIT_REGISTERED = False
_MAX_STATIC_URL_ATTEMPTS = 100


def get_static_path() -> Path:
    """
    Thread-safe extraction of static files from package.
    Returns a Path to the static directory. Uses ExitStack + as_file to
    ensure the extracted path remains valid while _APP_STATIC_STACK is live.
    """
    global _APP_STATIC_STACK, _EXTRACTED_STATIC_PATH, _ATEXIT_REGISTERED

    if _EXTRACTED_STATIC_PATH is not None:
        return _EXTRACTED_STATIC_PATH

    with _STATIC_LOCK:
        if _EXTRACTED_STATIC_PATH is not None:
            return _EXTRACTED_STATIC_PATH

        # Create context stack which will own the as_file resource
        stack = ExitStack()
        try:
            static_traversable = files("faststrap").joinpath("static")
            # context manager yields a real path (works for editable/wheel/zip)
            static_path_obj = stack.enter_context(as_file(static_traversable))
            static_path = Path(static_path_obj)

            # Persist stack and path globally (so path remains available until process exit
            _APP_STATIC_STACK = stack
            _EXTRACTED_STATIC_PATH = static_path

            # Also ensure cleanup at interpreter exit if not already
            if not _ATEXIT_REGISTERED:
                atexit.register(stack.close)
                _ATEXIT_REGISTERED = True

            return static_path

        except Exception:
            # ensure we always close stack on failure
            try:
                stack.close()
            except Exception:
                pass
            raise


def is_mounted(app: Any, path: str) -> bool:
    """Robust check whether a route path is already mounted."""
    # Ensure path starts with / and is normalized
    if not path.startswith("/"):
        path = f"/{path}"
    target = path.rstrip("/") or "/"

    routes = getattr(app, "routes", [])
    for route in routes:
        # Starlette Route/Mount objects usually have a 'path' attribute
        # We also check 'path_format' as a fallback used in some versions/middleware
        for attr in ("path", "path_format"):
            r_path = getattr(route, attr, None)
            if isinstance(r_path, str):
                normalized = r_path.rstrip("/") or "/"
                if normalized == target:
                    return True

    return False


def resolve_static_url(app: Any, preferred_url: str) -> str:
    """
    Find a non-conflicting static URL for FastStrap.

    Rules:
    1. If preferred_url is available, use it
    2. If not, try preferred_url + "/faststrap"
    3. If that's taken, append a counter
    """
    # Clean the URL
    preferred_url = preferred_url.rstrip("/")

    # Try the preferred URL first
    if not is_mounted(app, preferred_url):
        return preferred_url

    # Try with "/faststrap" suffix
    fallback_url = f"{preferred_url}/faststrap"
    if not is_mounted(app, fallback_url):
        return fallback_url

    # Last resort: append a counter
    for counter in range(1, _MAX_STATIC_URL_ATTEMPTS + 1):
        numbered_url = f"{preferred_url}/faststrap-{counter}"
        if not is_mounted(app, numbered_url):
            return numbered_url
    raise RuntimeError(
        f"Could not find available static URL after {_MAX_STATIC_URL_ATTEMPTS} attempts"
    )


def get_faststrap_static_url(app: Any) -> str | None:
    """
    Get the URL where FastStrap static files are mounted for this specific app.

    Args:
        app: The FastHTML app instance

    Returns:
        The static URL if mounted, None otherwise
    """
    return getattr(app, "_faststrap_static_url", None)


# Cleanup helper (useful for tests)
def cleanup_static_resources() -> None:
    """Clean up extracted static resources."""
    global _APP_STATIC_STACK, _EXTRACTED_STATIC_PATH, _ATEXIT_REGISTERED
    if _APP_STATIC_STACK:
        try:
            _APP_STATIC_STACK.close()
        finally:
            _APP_STATIC_STACK = None
            _EXTRACTED_STATIC_PATH = None
            _ATEXIT_REGISTERED = False


def create_favicon_links(favicon_url: str) -> list[Any]:
    """
    Create favicon link elements.

    Returns:
        List of Link elements (favicon + apple-touch-icon if applicable)
    """
    # Detect favicon type
    favicon_lower = favicon_url.lower()

    if favicon_lower.endswith(".svg"):
        mime_type = "image/svg+xml"
    elif favicon_lower.endswith(".png"):
        mime_type = "image/png"
    elif favicon_lower.endswith(".ico"):
        mime_type = "image/x-icon"
    elif favicon_lower.endswith(".jpg") or favicon_lower.endswith(".jpeg"):
        mime_type = "image/jpeg"
    elif favicon_lower.endswith(".webp"):
        mime_type = "image/webp"
    else:
        mime_type = "image/svg+xml"

    links = [Link(rel="icon", type=mime_type, href=favicon_url)]

    # Add apple-touch-icon for PNG
    if mime_type == "image/png":
        links.append(Link(rel="apple-touch-icon", href=favicon_url))

    return links


def get_default_favicon_url(use_cdn: bool, static_url: str) -> str:
    """Get the default FastStrap favicon URL."""
    if use_cdn:
        return "https://cdn.jsdelivr.net/gh/Faststrap-org/Faststrap@main/src/faststrap/static/favicon.svg"
    else:
        return f"{static_url.rstrip('/')}/favicon.svg"
