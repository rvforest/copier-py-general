# {{ project_name }} documentation

[![GitHub](https://img.shields.io/badge/GitHub-{{ github_owner }}%2F{{ project_name }}-blue?logo=github)](https://github.com/{{ github_owner }}/{{ project_name }})
[![Read the Docs](https://img.shields.io/readthedocs/{{ project_name }})](https://{{ project_name }}.readthedocs.io)

[![Checks](https://img.shields.io/github/check-runs/{{ github_owner }}/{{ project_name }}/main)](https://github.com/{{ github_owner }}/{{ project_name }}/actions/workflows/run-checks.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/{{ github_owner }}/{{ project_name }}/graph/badge.svg?token=JXB4LR2241)](https://codecov.io/gh/{{ github_owner }}/{{ project_name }})

[![PyPI](https://img.shields.io/pypi/v/{{ project_name }}.svg)](https://pypi.org/project/{{ project_name }}/)
[![Python Versions](https://img.shields.io/pypi/pyversions/{{ project_name }}.svg)](https://pypi.org/project/{{ project_name }}/)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

{{ description }}

```{toctree}
:maxdepth: 1
:caption: Getting Started:
:hidden:

getting_started/installation.md
getting_started/quickstart.md

```

```{toctree}
:maxdepth: 1
:caption: User Guide:
:hidden:

```{toctree}
:maxdepth: 1
:caption: Reference:
:hidden:

apidocs/index
```

```{toctree}
:maxdepth: 1
:caption: Development:
:hidden:

development/contributing.md
```
