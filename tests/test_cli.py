"""Tests for Faststrap CLI doctor checks."""

import importlib.metadata
from pathlib import Path

from faststrap.cli import (
    check_add_bootstrap_called,
    check_common_preset_misuse,
    check_fasthtml_version,
    check_serve_in_serverless,
    check_serverless_cdn,
    check_toast_container,
)


def test_doctor_missing_toast_container(tmp_path: Path):
    app_file = tmp_path / "app.py"
    app_file.write_text(
        "from faststrap.presets import toast_response\n"
        "def x():\n"
        "    return toast_response(content='ok', message='done')\n",
        encoding="utf-8",
    )
    issues = check_toast_container(tmp_path)
    assert any(issue.code == "missing-toast-container" for issue in issues)


def test_doctor_preset_target_warning(tmp_path: Path):
    app_file = tmp_path / "app.py"
    app_file.write_text(
        "from faststrap.presets import ActiveSearch\nActiveSearch('/x')", encoding="utf-8"
    )
    issues = check_common_preset_misuse(tmp_path)
    assert any(issue.code == "preset-target" for issue in issues)


def test_doctor_fasthtml_version_warns_if_below_min(tmp_path: Path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies = ["python-fasthtml>=0.6.0"]\n', encoding="utf-8"
    )
    monkeypatch.setattr(importlib.metadata, "version", lambda _: "0.5.0")
    issues = check_fasthtml_version(tmp_path)
    assert any(issue.code == "fasthtml-version" for issue in issues)


def test_doctor_fasthtml_version_warns_if_not_installed(tmp_path: Path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(
        '[project]\ndependencies = ["python-fasthtml>=0.6.0"]\n', encoding="utf-8"
    )

    def _raise(_: str) -> str:
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", _raise)
    issues = check_fasthtml_version(tmp_path)
    assert any(issue.code == "fasthtml-missing" for issue in issues)


def test_doctor_add_bootstrap_detected(tmp_path: Path):
    (tmp_path / "main.py").write_text(
        "from faststrap import add_bootstrap\nadd_bootstrap(app)\n", encoding="utf-8"
    )
    issues = check_add_bootstrap_called(tmp_path)
    assert issues == []


def test_doctor_add_bootstrap_missing_warns(tmp_path: Path):
    (tmp_path / "main.py").write_text("print('hello')\n", encoding="utf-8")
    issues = check_add_bootstrap_called(tmp_path)
    assert any(issue.code == "add-bootstrap-missing" for issue in issues)


def test_doctor_serverless_cdn_warns_when_missing(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    (tmp_path / "main.py").write_text(
        "from faststrap import add_bootstrap\nadd_bootstrap(app)\n", encoding="utf-8"
    )
    issues = check_serverless_cdn(tmp_path)
    assert any(issue.code == "serverless-cdn" for issue in issues)


def test_doctor_serverless_cdn_passes_when_configured(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("K_SERVICE", "svc")
    (tmp_path / "main.py").write_text(
        "from faststrap import add_bootstrap\nadd_bootstrap(app, use_cdn=True)\n",
        encoding="utf-8",
    )
    issues = check_serverless_cdn(tmp_path)
    assert issues == []


def test_doctor_serve_in_serverless_warns(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("AWS_LAMBDA_FUNCTION_NAME", "fn")
    (tmp_path / "main.py").write_text(
        "from fasthtml.common import serve\nserve()\n", encoding="utf-8"
    )
    issues = check_serve_in_serverless(tmp_path)
    assert any(issue.code == "serverless-serve" for issue in issues)


def test_doctor_serve_in_non_serverless_no_warning(tmp_path: Path, monkeypatch):
    monkeypatch.delenv("VERCEL", raising=False)
    monkeypatch.delenv("K_SERVICE", raising=False)
    monkeypatch.delenv("AWS_LAMBDA_FUNCTION_NAME", raising=False)
    (tmp_path / "main.py").write_text(
        "from fasthtml.common import serve\nserve()\n", encoding="utf-8"
    )
    issues = check_serve_in_serverless(tmp_path)
    assert issues == []
