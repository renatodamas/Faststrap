"""Helpers for mapping backend validation errors to FormGroup."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from fasthtml.common import H6, Div, Li, Ul

from ...core.registry import register
from ...core.theme import resolve_defaults
from ..feedback.alert import Alert
from .formgroup import FormGroup


def extract_field_error(errors: Mapping[str, Any] | None, field: str) -> str | None:
    """Extract a single displayable error message for a field."""
    if not errors or field not in errors:
        return None
    value = errors[field]
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        if not value:
            return None
        return str(value[0])
    if isinstance(value, dict):
        if "msg" in value:
            return str(value["msg"])
        if "message" in value:
            return str(value["message"])
    return str(value)


def map_formgroup_validation(
    errors: Mapping[str, Any] | None,
    field: str,
) -> dict[str, Any]:
    """Return FormGroup-ready validation flags for a given field."""
    error = extract_field_error(errors, field)
    return {
        "error": error,
        "is_invalid": bool(error),
    }


@register(category="forms")
def FormErrorSummary(
    errors: Mapping[str, Any] | Iterable[str] | str | None,
    *,
    title: str = "Please fix the following",
    variant: str | None = None,
    heading_cls: str | None = None,
    list_cls: str | None = None,
    show_field_names: bool = True,
    dismissible: bool | None = None,
    **kwargs: Any,
) -> Any | None:
    """Render a compact alert summary for validation errors."""
    if not errors:
        return None

    cfg = resolve_defaults(
        "Alert",
        variant=variant,
        dismissible=dismissible,
        heading_cls=heading_cls,
    )
    c_variant = cfg.get("variant", variant)
    c_dismissible = cfg.get("dismissible", dismissible)
    c_heading_cls = cfg.get("heading_cls", heading_cls) or "alert-heading h6 mb-2"

    items: list[str] = []

    if isinstance(errors, Mapping):
        for field, _value in errors.items():
            message = extract_field_error(errors, field)
            if message is None:
                continue
            if show_field_names:
                items.append(f"{field}: {message}")
            else:
                items.append(message)
    elif isinstance(errors, str):
        items.append(errors)
    elif isinstance(errors, Iterable):
        for value in errors:
            if value is None:
                continue
            items.append(str(value))

    if not items:
        return None

    list_class = list_cls or "mb-0"
    list_el = Ul(*(Li(item) for item in items), cls=list_class)
    content = Div(
        H6(title, cls=c_heading_cls),
        list_el,
    )
    return Alert(
        content,
        variant=c_variant,
        dismissible=c_dismissible,
        **kwargs,
    )


@register(category="forms")
def FormGroupFromErrors(
    input_element: Any,
    field: str,
    errors: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Build FormGroup and auto-apply backend error state for one field."""
    mapping = map_formgroup_validation(errors, field)
    return FormGroup(input_element, **mapping, **kwargs)
