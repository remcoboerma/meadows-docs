---
title: meadows-tui
description: Terminal UI client
---

# meadows-tui

> MEADOWS terminal UI client: a Textual-based TUI chat client for MEADOWS.
> Uses click for CLI argument parsing and Textual for the terminal interface.
> Connects directly to meadows-server via Socket.IO using meadows-client.

**Repository:** [github.com/remcoboerma/meadows-tui](https://github.com/remcoboerma/meadows-tui)

## Overview

`meadows-tui` provides a terminal-based chat interface for MEADOWS. It's a full-featured client with:

- Multi-group chat with sidebar navigation
- Message send/receive with typing indicators
- Dark and light color themes (toggle at runtime)
- Collapsible sidebar
- Emoji reactions (quick pick from 9 emojis)
- Reply to messages (quote preview)
- Message removal
- User and bot lists per group
- JWT authentication (pasted token or local secret)
- Auto-connect via env vars

## Install

```bash
cd meadows-tui
uv pip install -e ".[dev]"
uv pip install edwh
```

## Run

```bash
# With a JWT token
MEADOWS_JWT=eyJ... meadows-tui

# Or with a shared secret
MEADOWS_JWT_SECRET=secret MEADOWS_USERNAME=alice meadows-tui

# Or specify server explicitly
meadows-tui --server http://chat.example.com:8080 --token eyJ...
```

## CLI Options

| Option | Env var | Default | Description |
|---|---|---|---|
| `--server` | `MEADOWS_SERVER_URL` | `http://localhost:8080` | Socket.IO server URL |
| `--token` | `MEADOWS_JWT` | — | JWT token (pasted) |
| `--jwt-secret` | `MEADOWS_JWT_SECRET` | — | Secret for local token gen |
| `--username` | `MEADOWS_USERNAME` | — | Username for local token gen |
| `--theme` | `MEADOWS_THEME` | `auto` | `dark`, `light`, or `auto` |
| `--log-level` | `MEADOWS_LOG_LEVEL` | `WARNING` | Logging verbosity |

## Keybindings

| Key | Action |
|---|---|
| `Ctrl+t` | Toggle dark/light theme |
| `Ctrl+b` | Toggle sidebar |
| `Ctrl+n` | Focus input |
| `Ctrl+g` | Focus groups list |
| `Ctrl+q` | Quit |

## Architecture invariants

1. **Protocol constants only.** The only import from `meadows.protocol` is `EventName`.
2. **Transport via meadows-client.** No raw Socket.IO usage; all transport goes through `MeadowClient`.
3. **Event bridge.** Socket.IO events are translated to Textual `Message` subclasses in `client_bridge.py`.
4. **PEP 420 namespace.** `src/meadows/tui/__init__.py` exists; no `src/meadows/__init__.py`.
