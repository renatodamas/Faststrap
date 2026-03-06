"""Faststrap CLI."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import os
import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DoctorIssue:
    level: str
    code: str
    message: str


def _iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if ".venv" in path.parts or "site-packages" in path.parts:
            continue
        yield path


def check_import_source(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    mod = importlib.import_module("faststrap")
    mod_path = Path(mod.__file__ or "").resolve()
    if "site-packages" in mod_path.parts and (root / "src" / "faststrap").exists():
        issues.append(
            DoctorIssue(
                level="warn",
                code="import-source",
                message=f"Imported faststrap from site-packages: {mod_path}",
            )
        )
    return issues


def check_static_mount_conflicts(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    for file in _iter_python_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        if "mount_assets(" not in text:
            continue
        if 'url_path="/static"' in text and "allow_override=True" not in text:
            issues.append(
                DoctorIssue(
                    level="warn",
                    code="static-conflict",
                    message=f"Potential /static conflict in {file}",
                )
            )
    return issues


def check_toast_container(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    has_toast_response = False
    has_container = False
    for file in _iter_python_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        if "toast_response(" in text:
            has_toast_response = True
        if "ToastContainer(" in text:
            has_container = True
    if has_toast_response and not has_container:
        issues.append(
            DoctorIssue(
                level="warn",
                code="missing-toast-container",
                message="Found toast_response usage but no ToastContainer found in project files.",
            )
        )
    return issues


def check_common_preset_misuse(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    for file in _iter_python_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        if "ActiveSearch(" in text and "target=" not in text:
            issues.append(
                DoctorIssue(
                    level="warn",
                    code="preset-target",
                    message=f"ActiveSearch call may be missing target in {file}",
                )
            )
    return issues


def _is_serverless_env() -> bool:
    return bool(
        os.getenv("VERCEL") == "1"
        or os.getenv("AWS_LAMBDA_FUNCTION_NAME")
        or os.getenv("K_SERVICE")
    )


def _parse_min_fasthtml_version(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    text = pyproject.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"python-fasthtml>=([0-9][0-9A-Za-z.\-]*)", text)
    return match.group(1) if match else None


def _version_key(version: str) -> tuple[int, ...]:
    parts = []
    for token in re.split(r"[.\-+]", version):
        if token.isdigit():
            parts.append(int(token))
        else:
            break
    return tuple(parts)


def check_fasthtml_version(root: Path) -> list[DoctorIssue]:
    issues: list[DoctorIssue] = []
    min_required = _parse_min_fasthtml_version(root)
    if not min_required:
        return issues

    try:
        installed = importlib.metadata.version("python-fasthtml")
    except importlib.metadata.PackageNotFoundError:
        issues.append(
            DoctorIssue(
                level="warn",
                code="fasthtml-missing",
                message="python-fasthtml is not installed in this environment.",
            )
        )
        return issues

    if _version_key(installed) < _version_key(min_required):
        issues.append(
            DoctorIssue(
                level="warn",
                code="fasthtml-version",
                message=(
                    f"python-fasthtml {installed} is below required minimum {min_required}. "
                    "Upgrade dependency to avoid runtime issues."
                ),
            )
        )
    return issues


def check_add_bootstrap_called(root: Path) -> list[DoctorIssue]:
    for file in _iter_python_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        if "add_bootstrap(" in text:
            return []
    return [
        DoctorIssue(
            level="warn",
            code="add-bootstrap-missing",
            message=(
                "No add_bootstrap(...) call found in project files. "
                "Bootstrap/Faststrap assets may not be injected."
            ),
        )
    ]


def check_serverless_cdn(root: Path) -> list[DoctorIssue]:
    if not _is_serverless_env():
        return []
    for file in _iter_python_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        if "add_bootstrap(" in text and "use_cdn=True" in text:
            return []
    return [
        DoctorIssue(
            level="warn",
            code="serverless-cdn",
            message=(
                "Serverless environment detected but no use_cdn=True found. "
                "Use add_bootstrap(app, use_cdn=True) on Vercel/Lambda/Cloud Run."
            ),
        )
    ]


def check_serve_in_serverless(root: Path) -> list[DoctorIssue]:
    if not _is_serverless_env():
        return []
    issues: list[DoctorIssue] = []
    for file in _iter_python_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        if "serve(" in text:
            issues.append(
                DoctorIssue(
                    level="warn",
                    code="serverless-serve",
                    message=(
                        f"serve() call found in {file}. Remove serve() in serverless "
                        "deployments and expose the ASGI app object directly."
                    ),
                )
            )
    return issues


def run_doctor(path: str = ".") -> int:
    root = Path(path).resolve()
    all_issues = [
        *check_fasthtml_version(root),
        *check_import_source(root),
        *check_add_bootstrap_called(root),
        *check_serverless_cdn(root),
        *check_serve_in_serverless(root),
        *check_static_mount_conflicts(root),
        *check_toast_container(root),
        *check_common_preset_misuse(root),
    ]
    if not all_issues:
        print("faststrap doctor: OK")
        return 0

    print("faststrap doctor: issues found")
    for issue in all_issues:
        print(f"[{issue.level}] {issue.code}: {issue.message}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="faststrap", description="Faststrap CLI")
    subparsers = parser.add_subparsers(dest="command")

    doctor = subparsers.add_parser("doctor", help="Run Faststrap diagnostics")
    doctor.add_argument("--path", default=os.getcwd(), help="Project path to scan")

    args = parser.parse_args()
    if args.command == "doctor":
        return run_doctor(path=args.path)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
