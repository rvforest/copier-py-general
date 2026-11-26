"""Render the template with defaults and without post-copy tasks."""

from __future__ import annotations

import re
import warnings
from pathlib import Path

from tests.conftest import KEY_FILES, load_answers, render

# GitHub Actions expressions use ${{ ... }}; leftover Copier Jinja does not.
_JINJA_RE = re.compile(r"(?<!\$)\{\{|\{%|\{#")
_SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2"}


def _iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.suffix.lower() in _SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        yield path, text


def test_render_defaults_skip_tasks(tmp_path: Path) -> None:
    project = render(tmp_path / "project", skip_tasks=True)

    missing = [name for name in KEY_FILES if not (project / name).is_file()]
    assert missing == [], f"missing rendered files: {missing}"

    answers = load_answers(project)
    assert answers["project_name"] == "demo-project"
    assert answers["py_min_version"] == "3.11"
    assert answers["py_max_version"] == "3.15"
    assert answers["has_cli"] is False
    assert not (project / "src/demo_project/cli").exists()

    leftovers = []
    for path, text in _iter_text_files(project):
        for lineno, line in enumerate(text.splitlines(), 1):
            if _JINJA_RE.search(line):
                leftovers.append(f"{path.relative_to(project)}:{lineno}: {line.strip()}")
    assert leftovers == [], "leftover Jinja in rendered project:\n" + "\n".join(
        leftovers
    )

    agents = (project / "AGENTS.md").read_text()
    assert answers["description"] in agents
    assert "AI generated commit messages" not in agents
    conf = (project / "docs/source/conf.py").read_text()
    assert f'author = "{answers["author"]}"' in conf
    index = (project / "docs/source/index.md").read_text()
    assert "development/development_guide.md" in index
    guide = (project / "docs/source/development/development_guide.md").read_text()
    assert "run-checks.yaml.jinja" not in guide
    assert "pyproject.toml.jinja" not in guide


def test_render_defaults_emit_no_copier_warnings(tmp_path: Path) -> None:
    """The template should not use Copier's deprecated now() or invalid escapes."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        render(tmp_path / "project", skip_tasks=True)
    interesting = [
        w for w in caught if issubclass(w.category, (DeprecationWarning, FutureWarning))
    ]
    assert interesting == [], "".join(
        f"{w.category.__name__}: {w.message}\n" for w in interesting
    )


def test_render_python_classifiers_have_no_blank_lines(tmp_path: Path) -> None:
    pyproject = (render(tmp_path / "project", skip_tasks=True) / "pyproject.toml").read_text()
    expected = """
classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Programming Language :: Python :: 3.15",
]
"""
    assert expected.strip() in pyproject

