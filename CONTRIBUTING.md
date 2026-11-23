# Contributing

## Testing the template

Install the test group and run the fast subset by default. Pass `--run-slow`
for the full suite, including post-copy tasks and checks inside a generated
project (`pre-commit` and nox). Those tests need `git` and `uv`.

```bash
uv sync --group test
uv run pytest
uv run pytest --run-slow
```
