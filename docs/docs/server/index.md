---
title: meadows-server
description: The MEADOWS coordination hub
---

# meadows-server

> MEADOWS coordination hub: the server-as-object. Socket.IO AsyncServer with an ASGI wrapper, an object-oriented Hub (no module globals), and a single chokepoint emit that validates frames against `meadows.protocol` before they hit the wire.

**Repository:** [github.com/remcoboerma/meadows-server](https://github.com/remcoboerma/meadows-server)

## Overview

The server is the heart of MEADOWS. It handles:

- **Socket.IO transport** — real-time bidirectional messaging
- **JWT authentication** — user and bot identity verification
- **Message persistence** — append-only JSONL storage
- **Group management** — create, join, leave, delete groups
- **Bot routing** — `@bot` mention parsing and dispatch
- **Pattern matching** — regex-based message interception for bots
- **Rate limiting** — 30 msg/min per bot with 60s cooldown
- **Webhook API** — HTTP endpoint for injecting messages

## Architecture

```
MeadowServer (ASGI entrypoint)
  -> AuthASGIApp (JWT middleware)
    -> socketio.ASGIApp (Engine.IO/Socket.IO transport)
      -> ChatNamespace (/chat namespace)
        -> Hub (state: sessions, bots, groups, patterns, persistence)
```

## Install

```bash
cd meadows-server
uv pip install -e ".[dev]"
uv pip install edwh
```

## Run

```bash
# Development
uv run python -m meadows.server

# Or via uvicorn
uv run uvicorn meadows.server.app:app --host 0.0.0.0 --port 8080

# Docker
docker compose up -d
```

## Configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_HOST` | `0.0.0.0` | Bind address |
| `MEADOWS_PORT` | `8080` | Bind port |
| `MEADOWS_JWT_SECRET` | `./shared_keys/jwt.key` | JWT secret (32+ bytes for HS256) |
| `MEADOWS_MESSAGES_DIR` | `./messages` | JSONL message storage directory |
| `MEADOWS_CORS_ORIGINS` | `*` | CORS allowed origins |

## The Hub

All mutable state lives on the `Hub` instance — never in module globals.

| Attribute | Type | Purpose |
|---|---|---|
| `sio` | `socketio.AsyncServer` | The Socket.IO server |
| `user_sessions` | `dict[str, dict]` | Connected sessions (keyed by sid) |
| `bot_registry` | `dict[str, dict]` | Registered bots (keyed by bot_name) |
| `groups` | `dict[str, GroupState]` | Active groups (keyed by group_id) |
| `persistence` | `JSONLPersistence` | Append-only JSONL message store |
| `ntfy_prefs` | `NtfyPrefsStore` | Per-user ntfy notification preferences |

## Tasks

```bash
uv run edwh local.setup          # generate shared JWT key, check env vars
uv run edwh local.user-jwt --name=alice   # mint a user JWT
uv run edwh local.bot-jwt --name=echo     # mint a bot JWT
uv run edwh local.permissions-list        # list available permissions
uv run edwh local.test            # run tests
uv run edwh local.lint            # lint with ruff
```

See the [Socket.IO API](../reference/socketio-api.md) and [Webhook API](../reference/webhook-api.md) for the full event reference.
