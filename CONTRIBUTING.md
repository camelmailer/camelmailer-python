# Contributing

## Dev setup

```bash
git clone https://github.com/camelmailer/camelmailer-python
cd camelmailer-python
python -m venv .venv && source .venv/bin/activate
pip install -e . pytest respx pytest-asyncio mypy ruff
```

## Running checks

```bash
pytest                    # unit tests (no network)
ruff check . && ruff format --check .
mypy                      # strict, configured in pyproject.toml
```

Integration tests run only when `CAMELMAILER_API_KEY` (and optionally
`CAMELMAILER_BASE_URL`) is set; they are read-only and not part of CI.

## Conventions

- Tests first: every resource method and error path has a sync and an async test
  against a mocked HTTP layer (respx).
- Public API is fully typed; `mypy --strict` and `ruff` must pass.
- Keep commits small and focused; CI must be green.
- Follow [Keep a Changelog](https://keepachangelog.com) in `CHANGELOG.md`.
