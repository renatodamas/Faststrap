"""NotificationCenter component for aggregated notifications."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from fasthtml.common import A, Div, Span

from ...core._stability import beta
from ...core.base import merge_classes
from ...core.registry import register
from ...core.theme import resolve_defaults
from ...core.types import VariantType
from ...utils.attrs import convert_attrs
from ...utils.icons import Icon
from ..forms.button import Button

_NOTIFICATION_CENTER_COUNTS: dict[str, int] = {}


def _unique_center_id(base_id: str) -> str:
    count = _NOTIFICATION_CENTER_COUNTS.get(base_id, 0) + 1
    _NOTIFICATION_CENTER_COUNTS[base_id] = count
    if count == 1:
        return base_id
    return f"{base_id}-{count}"


def _stable_center_id(title: str, count: int | None, items_len: int) -> str:
    digest = hashlib.sha1(
        json.dumps(
            {"title": title, "count": count, "items_len": items_len},
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()[:10]
    return f"notification-center-{digest}-auto"


@register(category="feedback", requires_js=True)
@beta
def NotificationCenter(
    *items: Any,
    count: int | None = None,
    title: str = "Notifications",
    endpoint: str | None = None,
    center_id: str | None = None,
    menu_cls: str | None = None,
    button_cls: str | None = None,
    badge_variant: VariantType | None = None,
    empty_text: str = "No notifications",
    max_items: int | None = None,
    hx_swap: str | None = "innerHTML",
    push_url: bool = False,
    **kwargs: Any,
) -> Div:
    """Notification bell + dropdown menu."""
    cfg = resolve_defaults(
        "NotificationCenter",
        badge_variant=badge_variant,
        empty_text=empty_text,
        hx_swap=hx_swap,
        push_url=push_url,
    )
    c_badge_variant = cfg.get("badge_variant", badge_variant) or "danger"
    c_empty_text = cfg.get("empty_text", empty_text)
    c_hx_swap = cfg.get("hx_swap", hx_swap)
    c_push_url = cfg.get("push_url", push_url)

    item_list = list(items)
    if max_items is not None:
        item_list = item_list[:max_items]

    wrapper_id = center_id
    if wrapper_id is None:
        wrapper_id = _unique_center_id(_stable_center_id(title, count, len(item_list)))

    menu_id = f"{wrapper_id}-menu"

    badge = None
    if count is not None:
        badge = Span(
            str(count),
            cls=f"badge bg-{c_badge_variant} position-absolute top-0 start-100 translate-middle",
        )

    toggle_attrs: dict[str, Any] = {
        "cls": merge_classes("position-relative faststrap-notification-toggle", button_cls),
        "data_bs_toggle": "dropdown",
        "aria_expanded": "false",
        "type": "button",
    }

    if endpoint:
        toggle_attrs["hx_get"] = endpoint
        toggle_attrs["hx_target"] = f"#{menu_id}"
        toggle_attrs["hx_swap"] = c_hx_swap
        toggle_attrs["hx_trigger"] = "click"
        if c_push_url:
            toggle_attrs["hx_push_url"] = "true"

    toggle = Button(
        Icon("bell"),
        badge,
        variant="link",
        **toggle_attrs,
    )

    menu_items: list[Any] = []
    if title:
        menu_items.append(Span(title, cls="dropdown-header text-uppercase"))

    if item_list:
        for item in item_list:
            if isinstance(item, tuple) and len(item) == 2:
                label, href = item
                menu_items.append(A(label, href=href, cls="dropdown-item"))
            elif isinstance(item, str):
                menu_items.append(Div(item, cls="dropdown-item-text"))
            else:
                menu_items.append(item)
    else:
        menu_items.append(Div(c_empty_text, cls="dropdown-item-text text-muted"))

    menu = Div(
        *menu_items,
        id=menu_id,
        cls=merge_classes("dropdown-menu dropdown-menu-end faststrap-notification-menu", menu_cls),
    )

    attrs: dict[str, Any] = {
        "cls": merge_classes("dropdown faststrap-notification-center", kwargs.pop("cls", "")),
        "id": wrapper_id,
    }
    attrs.update(convert_attrs(kwargs))

    return Div(toggle, menu, **attrs)
