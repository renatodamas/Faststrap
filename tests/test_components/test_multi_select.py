"""Tests for MultiSelect component."""

from fasthtml.common import to_xml

from faststrap import MultiSelect


def test_multi_select_selected_values():
    html = to_xml(
        MultiSelect(
            "teams",
            ("eng", "Engineering"),
            ("ops", "Operations"),
            selected=["ops"],
        )
    )

    assert "multiple" in html
    assert "Operations" in html
    assert "selected" in html
