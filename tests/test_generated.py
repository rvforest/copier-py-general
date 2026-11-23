"""Slow tests: post-copy tasks, pre-commit, and nox in a generated project."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import git, load_answers, render


def _current_python() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    # Don't leak the template repo's venv into the generated project.
    env.pop("VIRTUAL_ENV", None)
    env.pop("UV_PROJECT", None)
    env.pop("UV_PROJECT_ENVIRONMENT", None)
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
        env=env,
    )


@pytest.mark.slow
def test_copy_tasks_succeed(tmp_path: Path) -> None:
    project = render(tmp_path / "project", skip_tasks=False)
    assert (project / ".git").is_dir()
    log = git("log", "--oneline", cwd=project).stdout
    assert "Initial commit" in log
    # Tasks commit only the README so the rest can be edited first.
    names = git("ls-tree", "--name-only", "-r", "HEAD", cwd=project).stdout.splitlines()
    assert names == ["README.md"]


@pytest.mark.slow
def test_generated_project_pre_commit_and_nox(tmp_path: Path) -> None:
    python = _current_python()
    project = render(
        tmp_path / "project",
        data={"py_min_version": python, "py_max_version": python},
        skip_tasks=False,
    )
    assert load_answers(project)["py_min_version"] == python

    # Track every rendered file so pre-commit --all-files can see them.
    # The post-copy task leaves the repo on main with only README committed;
    # switch off main so the no-commit-to-branch hook (which forbids main)
    # does not fail a --all-files run.
    git("checkout", "-b", "template-tests", cwd=project)
    git("add", "-A", cwd=project)

    _run(["uv", "lock"], cwd=project)
    _run(["uv", "sync", "--group", "dev"], cwd=project)
    try:
        _run(["uv", "run", "pre-commit", "run", "--all-files"], cwd=project)
    except subprocess.CalledProcessError as exc:
        raise AssertionError(
            "pre-commit failed in generated project\n"
            f"stdout:\n{exc.stdout}\nstderr:\n{exc.stderr}"
        ) from exc

    try:
        _run(["uv", "run", "nox", "-s", "types", "test"], cwd=project)
    except subprocess.CalledProcessError as exc:
        raise AssertionError(
            "nox sessions failed in generated project\n"
            f"stdout:\n{exc.stdout}\nstderr:\n{exc.stderr}"
        ) from exc
