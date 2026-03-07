"""Tests for Sheet component."""

from fasthtml.common import to_xml

from faststrap.components.display import Sheet


def test_sheet_defaults_to_bottom_drawer() -> None:
    sheet = Sheet("Body", sheet_id="mobile-sheet")
    html = to_xml(sheet)
    assert 'id="mobile-sheet"' in html
    assert "offcanvas-bottom" in html
    assert "rounded-top-4" in html


def test_sheet_applies_height_for_dict_style() -> None:
    sheet = Sheet("Body", sheet_id="height-sheet", height="60vh", style={"color": "red"})
    html = to_xml(sheet)
    assert "height: 60vh" in html
    assert "max-height: 90vh" in html
    assert "color: red" in html


def test_sheet_applies_height_for_string_style() -> None:
    sheet = Sheet("Body", sheet_id="height-sheet-2", height="50%", style="margin-top: 1rem;")
    html = to_xml(sheet)
    assert "height: 50%" in html
    assert "max-height: 90vh" in html
    assert "margin-top: 1rem" in html
