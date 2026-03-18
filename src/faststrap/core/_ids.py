"""Thread-safe helpers for generated component IDs."""

from __future__ import annotations

import threading

_ID_LOCK = threading.Lock()
_PREFIX_COUNTS: dict[str, int] = {}
_BASE_ID_COUNTS: dict[str, int] = {}


def next_sequential_id(prefix: str) -> str:
    """Return a process-unique ID using a shared prefix.

    Example:
        >>> next_sequential_id("navbar")
        "navbar1"
    """
    with _ID_LOCK:
        count = _PREFIX_COUNTS.get(prefix, 0) + 1
        _PREFIX_COUNTS[prefix] = count
        return f"{prefix}{count}"


def uniquify_id(base_id: str) -> str:
    """Return a unique variant of a deterministic base ID."""
    with _ID_LOCK:
        count = _BASE_ID_COUNTS.get(base_id, 0) + 1
        _BASE_ID_COUNTS[base_id] = count
        if count == 1:
            return base_id
        return f"{base_id}-{count}"

