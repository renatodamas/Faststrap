"""Tests for DateRangePicker component."""

from fasthtml.common import to_xml

from faststrap import DateRangePicker


def test_date_range_picker_basic():
    html = to_xml(DateRangePicker())

    assert "faststrap-date-range" in html
    assert "start_date" in html
    assert "end_date" in html


def test_date_range_picker_presets():
    html = to_xml(
        DateRangePicker(
            presets=[("Last 7 days", "2026-01-01", "2026-01-07")],
            endpoint="/reports",
            hx_target="#results",
        )
    )

    assert "Last 7 days" in html
    assert 'hx-get="/reports?start_date=2026-01-01&amp;end_date=2026-01-07"' in html
