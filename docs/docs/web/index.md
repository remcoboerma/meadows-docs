---
title: meadows-web
description: Dumb HTTP host for the web UI
---

# meadows-web

> MEADOWS web host: a dumb HTTP host that serves `index.html` and static assets.
> No Socket.IO, no auth, no domain logic. The browser is the client; the Socket.IO connection runs browser→meadows-server, NOT via this Python webserver.

**Repository:** [github.com/remcoboerma/meadows-web](https://github.com/remcoboerma/meadows-web)

## Overview

`meadows-web` is the simplest package. It:

- Serves `/` → `dist/index.html`
- Serves `/static/*` → static assets
- Injects protocol constants + env config into the template
- Does **nothing else**

The browser connects directly to `meadows-server` via Socket.IO. This Python server is just a file host.

## Architecture

```
Browser (JS)
  ├── Socket.IO ──→ meadows-server:8080
  └── HTTP ──→ meadows-web:8081 (static files only)
```

## Install

```bash
cd meadows-web
uv pip install -e ".[dev]"
uv pip install edwh
```

## Build the template

```bash
uv run python -m meadows.web.build
```

This reads `templates/index.html`, injects protocol constants + env config, writes `dist/index.html`.

## Run

```bash
# Development
uv run python -m meadows.web

# Or via uvicorn
uv run uvicorn meadows.web.app:app --host 0.0.0.0 --port 8081

# Docker
docker compose up -d
```

## Configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_WEB_HOST` | `0.0.0.0` | Bind address |
| `MEADOWS_WEB_PORT` | `8081` | Bind port |
| `MEADOWS_SERVER_URL` | `http://localhost:8080` | Server URL (injected into page) |
| `MEADOWS_SYSTEM_NAME` | `MEADOWS Chat` | Display name (injected into page) |
| `PROJECT` | `meadows` | Traefik router prefix |
| `HOSTINGDOMAIN` | `localhost` | Traefik host domain |

## Architecture invariants

1. **Dumb host.** No Socket.IO, no auth, no JWT, no message parsing. It serves files.
2. **TLS is not a concern.** Traefik terminates TLS. No cert logic here.
3. **Protocol constants only.** The only import from `meadows.protocol` is `EventName` (for template injection).
4. **PEP 420 namespace.** `src/meadows/web/__init__.py` exists; no `src/meadows/__init__.py`.
