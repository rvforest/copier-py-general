"""Shared helpers for template validity tests."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml
from copier import run_copy

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

BASE_DATA: dict[str, Any] = {
    "project_name": "demo-project",
    "description": "Template validity test project",
    "gh_owner": "rvforest",
    "author": "Test Author",
    "author_email": "test@example.com",
}

# Files that every successful defaults render should produce.
KEY_FILES = (
    ".copier-answers.yml",
    ".github/workflows/run-checks.yaml",
    ".pre-commit-config.yaml",
    ".python-version",
    "LICENSE",
    "README.md",
    "noxfile.py",
    "pyproject.toml",
    "src/demo_project/__init__.py",
    "tests/test_noop.py",
)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="run tests marked slow (generated-project pre-commit and nox)",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "slow: generated-project checks; skipped unless --run-slow is given",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if config.getoption("--run-slow"):
        return
    skip_slow = pytest.mark.skip(reason="slow; pass --run-slow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture(autouse=True)
def git_identity(
    monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory
) -> None:
    """Give git a name/email so post-copy commit tasks can succeed.

    Isolated from the developer or CI runner identity, and from global git
    config (including commit-signing settings). Copier runs tasks with
    ``plumbum.local.env``, a snapshot of ``os.environ`` at import time, so
    that snapshot is updated as well as the process environment.
    """
    name = "Template Tests"
    email = "tests@example.invalid"
    config_file = tmp_path_factory.mktemp("git-config") / "gitconfig"
    config_file.write_text(f"[user]\n\tname = {name}\n\temail = {email}\n")
    env = {
        "GIT_AUTHOR_NAME": name,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_COMMITTER_NAME": name,
        "GIT_COMMITTER_EMAIL": email,
        "GIT_CONFIG_GLOBAL": str(config_file),
        "GIT_CONFIG_NOSYSTEM": "1",
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    # See fixture docstring: monkeypatch alone does not reach Copier tasks.
    from plumbum import local

    local.env.update(env)


def render(
    dst: Path,
    *,
    data: dict[str, Any] | None = None,
    skip_tasks: bool = True,
    vcs_ref: str = "HEAD",
    src_path: Path | str | None = None,
    **kwargs: Any,
) -> Path:
    """Render the template into ``dst`` using Copier's Python API."""
    run_copy(
        str(src_path or TEMPLATE_ROOT),
        dst,
        data={**BASE_DATA, **(data or {})},
        defaults=True,
        unsafe=True,
        skip_tasks=skip_tasks,
        vcs_ref=vcs_ref,
        quiet=True,
        **kwargs,
    )
    return dst


def load_answers(project: Path) -> dict[str, Any]:
    return yaml.safe_load((project / ".copier-answers.yml").read_text())


def git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        text=True,
        capture_output=True,
    )


def copy_template_snapshot(dst: Path) -> Path:
    """Copy the template sources into a standalone tree (no git history)."""
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE_ROOT / "copier.yaml", dst / "copier.yaml")
    shutil.copytree(TEMPLATE_ROOT / "template", dst / "template")
    return dst
