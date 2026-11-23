"""Python version question validators (free-text, added in #29)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import load_answers, render


@pytest.mark.parametrize(
    ("data", "match"),
    [
        (
            {"py_min_version": "3.x"},
            "must be of the form 3.x",
        ),
        (
            {"py_min_version": "4.0"},
            "must be of the form 3.x",
        ),
        (
            {"py_min_version": "3.10"},
            "must be 3.11 or higher",
        ),
        (
            {"py_min_version": "3.13", "py_max_version": "3.12"},
            "must be at least the minimum",
        ),
        (
            {"py_max_version": "3.x"},
            "must be of the form 3.x",
        ),
        (
            {"py_max_version": "4.0"},
            "must be of the form 3.x",
        ),
    ],
)
def test_python_version_validators_reject(
    tmp_path: Path, data: dict[str, str], match: str
) -> None:
    with pytest.raises(ValueError, match=match):
        render(tmp_path / "project", data=data)


def test_python_version_validators_accept_3_16(tmp_path: Path) -> None:
    project = render(
        tmp_path / "project",
        data={"py_min_version": "3.11", "py_max_version": "3.16"},
    )
    answers = load_answers(project)
    assert answers["py_max_version"] == "3.16"
    assert (project / ".python-version").read_text().strip() == "3.16"
    pyproject = (project / "pyproject.toml").read_text()
    assert 'requires-python = ">=3.11"' in pyproject
    assert "Programming Language :: Python :: 3.16" in pyproject
