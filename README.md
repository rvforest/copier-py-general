# Copier Python General Template

A modern, opinionated [Copier](https://copier.readthedocs.io/) template for Python projects.

## Features

- **Project Naming & Validation**: Enforces lowercase, dash-separated project names starting with a letter.
- **Auto-generated Package Name**: Converts dashes to underscores for Python package naming.
- **Python Version Management**:
  - Prompts for the minimum Python version (`requires-python`) and the newest version to test in CI and nox (also used for `.python-version`). The test max is not a package cap.
  - Auto-generates a list of supported Python versions for classifiers, nox, and CI.
- **Metadata Prompts**:
  - Project description
  - GitHub owner/organization (defaults from environment)
  - Author name and email (defaults from environment)
- **CLI Support**:
  - Optional CLI tool generation.
  - Prompts for CLI command name if enabled.
  - Excludes CLI files if not selected.
- **Current Year Variable**: Auto-generated for copyright.
- **Initial Git Commit**: On project creation, initializes a git repo and commits only the README for dynamic version lookup.
- **Customizable Exclusions**: Template files and directories are conditionally included/excluded based on your choices.
- **Hardened CI**: GitHub Actions locked to commit SHAs with a workflow lockfile (`actions.lock`), least-privilege permissions, zizmor, actionlint, and gitleaks pre-commit hooks, and grouped monthly Dependabot updates.
- **Diff Coverage**: Codecov with a 90% patch target, plus a local pre-push `diff-coverage` check.
- **Extensible**: Designed for easy extension and customization.

## Usage

```bash
copier copy gh:rvforest/copier-py-general your-new-project
```

## Template Questions

- Project name (validated)
- Description
- GitHub owner/org (default from `$GITHUB_USER`)
- Author name/email (default from `$GIT_AUTHOR_NAME`/`$GIT_AUTHOR_EMAIL`)
- Minimum Python version (free-text `3.x`, at least 3.11, default: 3.13). Sets `requires-python` to `>=` this version, with no upper cap.
- Maximum Python version (free-text `3.x`, default: 3.15). This is the newest version tested in CI and nox, and the version written to `.python-version`. It is not a package cap. After a new Python release, bump a project's test range with `copier update --data py_max_version=3.16`.
- CLI support (yes/no)
  - If yes: CLI command name (default: project name)

## How it Works

- **Dynamic Defaults**: Many fields use environment variables or Jinja logic for sensible defaults.
- **Conditional Prompts**: Some questions only appear if relevant (e.g., CLI options).
- **Post-Generation Tasks**: Runs git init and makes an initial commit with only the README.

## Customization

You can easily extend this template by editing `copier.yaml` and the files in the `template/` directory.

### Updating the actions lockfile

The template ships a pre-generated `template/.github/workflows/actions.lock`. Never edit it by hand. When you change any `uses:` line in `template/.github/workflows/`, regenerate it: `gh actions-lock` only scans a repository's root `.github/workflows/`, so render a project and lock that.

```bash
gh extension install github/gh-actions-lock   # once
copier copy --vcs-ref HEAD --defaults --trust -d project_name=lock-demo -d description=Demo -d has_cli=true . /tmp/lock-demo
cd /tmp/lock-demo && gh actions-lock
cp .github/workflows/actions.lock "$OLDPWD/template/.github/workflows/actions.lock"
```

Use exact version tags such as `actions/checkout@v7.0.1`, not `@v7`. Review the diff in the rendered project too: `gh actions-lock` may rewrite `uses:` refs, and any rewrite must be copied back into the template's workflows.

## Requirements

- Python 3.13+
- [Copier](https://copier.readthedocs.io/)

## License

MIT
