# Copier Python General Template

A modern, opinionated [Copier](https://copier.readthedocs.io/) template for Python projects.

## Features

- **Project Naming & Validation**: Enforces lowercase, dash-separated project names starting with a letter.
- **Auto-generated Package Name**: Converts dashes to underscores for Python package naming.
- **Python Version Management**:
  - Prompts for minimum and maximum Python versions.
  - Auto-generates a list of supported Python versions.
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
- **Extensible**: Designed for easy extension and customization.

## Usage

```bash
copier copy gh:your-org/copier-py-general your-new-project
```

## Template Questions

- Project name (validated)
- Description
- GitHub owner/org (default from `$GITHUB_USER`)
- Author name/email (default from `$GIT_AUTHOR_NAME`/`$GIT_AUTHOR_EMAIL`)
- Minimum Python version (default: 3.13)
- Maximum Python version (hidden, default: 3.13)
- CLI support (yes/no)
  - If yes: CLI command name (default: project name)

## How it Works

- **Dynamic Defaults**: Many fields use environment variables or Jinja logic for sensible defaults.
- **Conditional Prompts**: Some questions only appear if relevant (e.g., CLI options).
- **Post-Generation Tasks**: Runs git init and makes an initial commit with only the README.

## Customization

You can easily extend this template by editing `copier.yaml` and the files in the `template/` directory.

## Requirements

- Python 3.9+
- [Copier](https://copier.readthedocs.io/)

## License

MIT
