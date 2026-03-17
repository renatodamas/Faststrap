"""Tests for NotificationCenter component."""

from fasthtml.common import to_xml

from faststrap import NotificationCenter


def test_notification_center_basic():
    html = to_xml(NotificationCenter("Update complete", count=3, center_id="notif"))

    assert "faststrap-notification-center" in html
    assert "badge" in html
    assert "dropdown-menu" in html
    assert "notif-menu" in html


def test_notification_center_endpoint():
    html = to_xml(
        NotificationCenter(
            count=2,
            endpoint="/notifications",
            center_id="notif",
            hx_swap="innerHTML",
        )
    )

    assert 'hx-get="/notifications"' in html
    assert 'hx-target="#notif-menu"' in html
