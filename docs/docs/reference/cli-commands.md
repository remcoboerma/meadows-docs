---
title: CLI Commands
description: edwh task runner commands
---

# CLI Commands

All packages use `edwh` as the task runner. Commands are run inside the package directory.

## Standard commands (all packages)

```bash
uv run edwh local.setup   # check/create env vars, generate shared keys
uv run edwh local.test    # run tests (uv run pytest -q)
uv run edwh local.lint    # lint with ruff
uv run edwh local.fmt     # format with ruff + auto-fix
```

## Server-specific commands

```bash
# Generate JWT tokens (run from meadows-server/)
uv run edwh local.user-jwt --name=alice          # mint a user JWT
uv run edwh local.user-jwt --name=alice --expiry=30d  # with custom expiry
uv run edwh local.bot-jwt --name=echo            # mint a bot JWT
uv run edwh local.permissions-list               # list available permissions
```

## Root orchestrator commands

The root `tasks.py` provides multi-package orchestration:

```bash
inv setup     # generate JWTs for all bots in meadows-compose.yaml
inv start     # start server + all enabled bots (blocks)
inv stop      # terminate all tracked processes
inv status    # show configured bots and their running status
inv add --name=foo --module=meadows.bot.examples.foo_bot  # add a bot
inv tui       # launch TUI client
inv tui --branch=main --username=alice
inv tui --debug
```

## Docs commands

```bash
# From meadows-docs/
uv run edwh local.build   # build static site via Docker
uv run edwh local.update  # build + restart server
uv run edwh local.serve   # dev server (localhost:8000)
uv run edwh local.clean   # remove built site/
```

## Testing

```bash
# Standard test run
uv run edwh local.test

# With coverage
uv run pytest --cov=src --cov-report=term-missing

# Integration tests (server, requires extra deps)
uv pip install -e ".[integration]"
uv run pytest -q
```
