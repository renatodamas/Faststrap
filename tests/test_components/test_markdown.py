"""Tests for optional Markdown rendering component."""

from types import SimpleNamespace

import pytest
from fasthtml.common import to_xml

from faststrap.components.display import markdown as markdown_module
from faststrap.components.display.markdown import Markdown, render_markdown


def test_render_markdown_sanitizes_html(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sanitization strips unsafe markup by default."""

    def fake_import(name: str):
        if name == "markdown":
            return SimpleNamespace(
                markdown=lambda *_args, **_kwargs: "<h1>Title</h1><script>x()</script>"
            )
        if name == "bleach":
            return SimpleNamespace(
                clean=lambda html, **_kwargs: html.replace("<script>x()</script>", "")
            )
        raise ImportError

    monkeypatch.setattr(markdown_module.importlib, "import_module", fake_import)
    rendered = render_markdown("# Title")
    assert "<h1>Title</h1>" in rendered
    assert "<script>" not in rendered


def test_markdown_component_wraps_rendered_output(monkeypatch: pytest.MonkeyPatch) -> None:
    """Markdown component returns a div with rendered HTML content."""

    def fake_import(name: str):
        if name == "markdown":
            return SimpleNamespace(
                markdown=lambda *_args, **_kwargs: "<p>Hello <strong>world</strong></p>"
            )
        if name == "bleach":
            return SimpleNamespace(clean=lambda html, **_kwargs: html)
        raise ImportError

    monkeypatch.setattr(markdown_module.importlib, "import_module", fake_import)
    component = Markdown("Hello **world**", cls="mt-3")
    html = to_xml(component)
    assert "faststrap-markdown mt-3" in html
    assert "<strong>world</strong>" in html


def test_markdown_missing_dependency_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """A clear error is raised if markdown dependency is absent."""

    def fake_import(_name: str):
        raise ImportError

    monkeypatch.setattr(markdown_module.importlib, "import_module", fake_import)
    with pytest.raises(ImportError, match="Install with `pip install faststrap\\[markdown\\]`"):
        render_markdown("# Missing")
