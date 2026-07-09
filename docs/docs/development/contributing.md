---
title: Contributing
description: How to contribute to MEADOWS
---

# Contributing

## Git conventions

### Commit messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

<body>  # optional
```

**Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`

**Scopes:** `server`, `protocol`, `client`, `bot`, `web`, `tui`, `docs`, `tests`

**Examples:**

```
feat(server): add inbound webhook endpoint POST /r/{group_id}
feat(server): enforce bot rate limiting (30 msg/min, 60s cooldown)
fix(server): enforce POST-only on webhook endpoint
docs: expand README with Socket.IO API reference
test(server): add webhook endpoint tests
refactor(server): extract _check_rate_limit helper
```

### Pre-commit gate

Before committing:

1. Run `uv run edwh local.lint` — must pass
2. Run `uv run edwh local.test` — must pass
3. Answer the certification question in `ARCHITECTURE_INTENT.md`
4. No `--no-verify` or force-push

### Signature changes

Before changing a function signature:

1. Grep tests that call it
2. Update all call sites in the same change
3. Cross-reference with code that imports the changed symbol

## Code style

- **Line length:** 120
- **Linting:** `ruff` with select=F,E,W,Q,A,SIM,ARG,PTH,RUF,C90,N,YTT
- **Formatting:** `ruff format`
- **No comments** unless explicitly asked
- **Docstrings:** every module, class, and key function must include a docstring explaining *why* it exists

## Architecture decisions

Before making architectural changes:

1. Read `ARCHITECTURE_INTENT.md`
2. Read `MEADOWS-migration-intent.md`
3. Ask: does this change violate any of the core principles?
4. Answer the certification question before committing

## Code exploration

Use `edwh codemap` to get a structured overview of any package:

```bash
cd meadows-server
uv run edwh codemap
uv run edwh codemap | rg "def test_"
uv run edwh codemap | rg "class Hub"
```
