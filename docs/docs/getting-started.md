---
title: Getting Started
description: Quick start guide for MEADOWS
---

# Getting Started

Get MEADOWS running in under 5 minutes.

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional, for production)

## Quick start (development)

### 1. Clone the repository

```bash
git clone https://github.com/meadows-chat/meadows.git
cd meadows
```

### 2. Set up the server

```bash
cd meadows-server
uv pip install -e ".[dev]"
uv pip install edwh

# Generate shared JWT key
uv run edwh local.setup

# Start the server
uv run python -m meadows.server
```

The server starts on `http://localhost:8080`.

### 3. Generate a user token

```bash
cd meadows-server
uv run edwh local.user-jwt --name=alice
```

Copy the printed JWT token.

### 4. Connect with the TUI

```bash
cd meadows-tui
uv pip install -e ".[dev]"
uv pip install edwh

MEADOWS_JWT=<your-token> meadows-tui
```

Or connect via the web UI — see the [Web Package](web/index.md) docs.

## Quick start: write a bot

```python
from meadows.bot import BaseBot

class MyBot(BaseBot):
    BOT_NAME = "mybot"
    BOT_DESCRIPTION = "My custom bot"
    BOT_COMMANDS = [{"name": "greet", "description": "Say hello"}]

    def should_handle(self, command, args):
        return command == "greet"

    def handle(self, command, args, raw_args, message, thread_context):
        return f"Hello {args[0] if args else 'user'}!"

if __name__ == "__main__":
    MyBot().connect()
```

Set the `MEADOWS_JWT_TOKEN` env var (generate with `inv bot-jwt --name=mybot`), then:

```bash
cd meadows-bot
uv pip install -e ".[dev]"
MEADOWS_JWT_TOKEN=<bot-token> python -m my_bot
```

See the [Bot Package](bot/index.md) for the full bot-author surface.

## Docker deployment

For production, use Docker Compose:

```bash
cd meadows-server
docker compose up -d
```

See the [Docker](development/docker.md) guide for details.

## Next steps

- [Architecture Overview](architecture/overview.md) — understand the design
- [Bot Package](bot/index.md) — build bots
- [Server Package](server/index.md) — run and configure the server
- [Socket.IO API](reference/socketio-api.md) — the full event reference
