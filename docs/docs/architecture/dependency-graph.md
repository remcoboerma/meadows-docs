---
title: Dependency Graph
description: Package dependency relationships
---

# Dependency Graph

```
meadows-protocol  ←  meadows-client  ←  meadows-bot
meadows-protocol  ←  meadows-server
meadows-protocol  ←  meadows-web
meadows-client + meadows-protocol  ←  meadows-tui
```

## Rules

1. **`meadows-protocol` is the only leaf** — everyone depends on it; it depends on nothing.
2. **`meadows-server` and `meadows-bot` never import each other** — they meet only via protocol types.
3. **`meadows-web` does not depend on `meadows-client`** — it is a dumb HTTP host; the browser is the Socket.IO client.
4. **`meadows-client` makes the second implementation cheap** — bots and (future non-browser) clients share transport.

## Import paths

| Package | Import path |
|---|---|
| `meadows-protocol` | `meadows.protocol` |
| `meadows-client` | `meadows.client` |
| `meadows-bot` | `meadows.bot` |
| `meadows-server` | `meadows.server` |
| `meadows-web` | `meadows.web` |
| `meadows-tui` | `meadows.tui` |

## Dependency details

| Package | Depends on | Install |
|---|---|---|
| `meadows-protocol` | `pydantic` only | `uv pip install -e .` |
| `meadows-client` | `meadows-protocol`, `python-socketio` | `uv pip install -e .` |
| `meadows-bot` | `meadows-client`, `meadows-protocol` | `uv pip install -e .` |
| `meadows-server` | `meadows-protocol`, `python-socketio`, `endow` | `uv pip install -e ".[dev]"` |
| `meadows-web` | `meadows-protocol`, `starlette` | `uv pip install -e ".[dev]"` |
| `meadows-tui` | `meadows-client`, `meadows-protocol`, `textual` | `uv pip install -e ".[dev]"` |

## Editable dependencies

Each `pyproject.toml` maps sibling packages to editable paths:

```toml
[tool.uv.sources]
meadows-protocol = { path = "../meadows-protocol", editable = true }
```

This ensures local development uses the latest sibling code without publishing.
