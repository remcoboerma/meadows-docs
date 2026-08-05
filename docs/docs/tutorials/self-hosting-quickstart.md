---
title: Self-Hosting Quickstart
description: Run your own MEADOWS server on a laptop, Raspberry Pi, or home server
tags:
  - hobbyist
---

# Self-Hosting Quickstart

MEADOWS is built to be run by a trusted operator on your own hardware. Spinning up your own instance is the first project.

## What you need

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- [edwh](https://github.com/educationwarehouse/edwh) task runner
- A machine with network access (laptop, Pi, home server)

No cloud account. No domain name. No TLS certificate for local use.

## 1. Clone and install

```bash
git clone https://github.com/remcoboerma/meadows-server.git
cd meadows-server
uv pip install -e ".[dev]"
uv pip install edwh
```

## 2. Set up environment

```bash
uv run edwh local.setup
```

This generates a shared JWT key at `./shared_keys/jwt.key` and checks required environment variables.

## 3. Start the server

```bash
uv run python -m meadows.server
```

The server starts on `http://localhost:8080`.

## 4. Generate tokens

```bash
# Token for yourself (human user)
uv run edwh local.user-jwt --name=alice

# Token for a bot
uv run edwh local.bot-jwt --name=echo
```

Copy the printed tokens.

## 5. Serve the web frontend

The web UI is a separate package:

```bash
cd ../meadows-web
uv pip install -e ".[dev]"
uv run python -m meadows.web.build   # required: generates dist/index.html
uv run python -m meadows.web
```

The web UI starts on `http://localhost:8081`. Open it in a browser, paste your user token, and connect.

## 6. Run a bot

```bash
cd ../meadows-bot
uv pip install -e .
MEADOWS_JWT_TOKEN=<bot-token> uv run python -m meadows.bot.examples.echo_bot
```

Type `@echo ping` in the web UI. You'll get a pong.

## Optional: Docker

For production or containerized setups:

```bash
cd meadows-server
docker compose up -d
```

See [Docker guide](../development/docker.md) for Traefik TLS and multi-service configuration.

## Optional: TUI client

Connect from the terminal:

```bash
cd ../meadows-tui
uv pip install -e .
MEADOWS_JWT=<user-token> meadows-tui
```

See [TUI Package](../tui/index.md) for options.

## Architecture recap

```
Browser ──Socket.IO──▶ meadows-server :8080
Browser ◀──HTTP─────── meadows-web   :8081 (static files only)
Bot     ──Socket.IO──▶ meadows-server :8080
TUI     ──Socket.IO──▶ meadows-server :8080
```

The server is the only process that handles WebSocket connections. The web host serves static files. Bots and TUI connect outbound — no public IP needed.

## Check your understanding

- Why does `meadows-web` not handle Socket.IO connections?
- What does the trusted-operator assumption mean for your security model?
- How would you run a bot on a different machine than the server?

See the [Concepts](../concepts/index.md) page for the building blocks, or the [first bot tutorial](first-bot.md) to write your first bot.
