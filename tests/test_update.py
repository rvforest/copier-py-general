"""Update round-trip: a non-default py_max_version must survive copier update.

This is a regression test for the narrowing bug where an update replaced a
project's py_max_version with the template default.
"""

from __future__ import annotations

from pathlib import Path

from copier import run_copy, run_update

from tests.conftest import BASE_DATA, copy_template_snapshot, git, load_answers


def _set_py_max_default(copier_yaml: Path, value: str) -> None:
    text = copier_yaml.read_text()
    old = '  default: "3.15"\n'
    if old not in text:
        raise AssertionError("expected py_max_version default 3.15 in copier.yaml")
    # The 3.15 default appears only on py_max_version.
    copier_yaml.write_text(text.replace(old, f'  default: "{value}"\n', 1))


def test_update_preserves_nondefault_py_max_version(tmp_path: Path) -> None:
    template = copy_template_snapshot(tmp_path / "template")
    _set_py_max_default(template / "copier.yaml", "3.13")

    git("init", "--initial-branch=main", cwd=template)
    git("add", "-A", cwd=template)
    git("commit", "-m", "Initial template (default py_max_version 3.13)", cwd=template)

    project = tmp_path / "project"
    run_copy(
        str(template),
        project,
        data={**BASE_DATA, "py_max_version": "3.15"},
        defaults=True,
        unsafe=True,
        skip_tasks=True,
        vcs_ref="HEAD",
        quiet=True,
    )
    assert load_answers(project)["py_max_version"] == "3.15"
    assert (project / ".python-version").read_text().strip() == "3.15"

    git("init", "--initial-branch=main", cwd=project)
    git("add", "-A", cwd=project)
    git("commit", "-m", "Initial project from template", cwd=project)

    # Second revision keeps the narrower default but changes the template
    # so there is something to update to.
    yaml_text = (template / "copier.yaml").read_text()
    (template / "copier.yaml").write_text(
        yaml_text.replace(
            "Newest Python version to test in CI and nox",
            "Newest Python version to test in CI and nox (default remains 3.13)",
            1,
        )
    )
    git("add", "-A", cwd=template)
    git(
        "commit",
        "-m",
        "Update template; py_max_version default remains 3.13",
        cwd=template,
    )

    run_update(
        project,
        defaults=True,
        overwrite=True,
        unsafe=True,
        skip_tasks=True,
        vcs_ref="HEAD",
        quiet=True,
    )

    answers = load_answers(project)
    assert answers["py_max_version"] == "3.15"
    assert (project / ".python-version").read_text().strip() == "3.15"
    pyproject = (project / "pyproject.toml").read_text()
    assert "Programming Language :: Python :: 3.15" in pyproject
    assert 'requires-python = ">=3.11"' in pyproject
