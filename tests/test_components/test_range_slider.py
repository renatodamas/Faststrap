"""Tests for RangeSlider component."""

from fasthtml.common import to_xml

from faststrap import RangeSlider


def test_range_slider_single():
    html = to_xml(RangeSlider("score", value=50, min_value=0, max_value=100))
    assert 'type="range"' in html
    assert 'name="score"' in html
    assert 'value="50"' in html


def test_range_slider_dual():
    html = to_xml(RangeSlider("range", dual=True, min_selected=10, max_selected=90))
    assert 'name="range_min"' in html
    assert 'name="range_max"' in html
