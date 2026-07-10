---
title: Getting Started
description: Five ways to get started with MEADOWS
---

# Getting Started

There is no single "getting started" — it depends on what you want to do. Pick your path:

| I want to... | Go to |
|---|---|
| Use MEADOWS (connect to a running server) | [Using MEADOWS](#1-using-meadows) |
| Host my own server | [Self-hosting](#2-self-hosting) |
| Develop the server locally | [Server development](#3-server-development) |
| Write a bot | [Bot development](#4-bot-development) |
| Investigate the data | [Data investigation](#5-data-investigation) |

---

## 1. Using MEADOWS

Someone hosts a MEADOWS server for you. You want to chat, interact with bots, maybe fill in a form. You don't need to install anything — just a browser.

### What is a JWT?

A JWT (JSON Web Token) is your digital identity. It's a long string that says "I am user alice" (or "I am bot echo"). The server uses it to know who you are and what you're allowed to do.

Think of it like a wristband at a festival: you get it at the entrance, it identifies you for the whole event, and it expires when the event ends.

### Getting a token

Ask the server operator for a token. They generate one with:

```bash
cd meadows-server
uv run edwh local.user-jwt --name=yourname
```

They'll give you a long string like `eyJhbGciOiJIUzI1NiIs...`. Copy it.

### Connecting via web browser

1. Open the server URL (the operator will tell you, e.g. `https://chat.example.com`)
2. Paste your JWT token in the login field
3. Click "Connect"

You're in. You'll see groups on the left, messages in the center, and a list of available bots.

### Connecting via terminal (TUI)

If you prefer a terminal interface:

```bash
pip install meadows-tui
MEADOWS_JWT=<your-token> meadows-tui --server https://chat.example.com
```

Or with more options:

```bash
meadows-tui --server https://chat.example.com --token eyJ... --theme dark
```

### Talking to bots

Type `@botname command` in the message box. For example:

- `@echo hello` — the echo bot repeats your message
- `@todo add` — the todo bot shows a form to add a task
- `@help` — shows available bots and commands

Bots respond in the same conversation. You see their responses alongside messages from other humans.

---

## 2. Self-hosting

You want to run your own MEADOWS server. Two options: Docker (simplest) or bare metal.

### Option A: Docker (recommended for production)

```bash
git clone https://github.com/remcoboerma/meadows-server.git
cd meadows-server

# Set up environment variables
uv run edwh local.setup

# Start with Docker Compose
docker compose up -d
```

The server starts on port 8080. Traefik handles TLS if configured.

See the [Docker guide](development/docker.md) for production configuration, Traefik labels, and multi-service setup.

### Option B: Bare metal (no Docker)

```bash
git clone https://github.com/remcoboerma/meadows-server.git
cd meadows-server

# Install with uv
uv pip install -e ".[dev]"
uv pip install edwh

# Generate shared JWT key
uv run edwh local.setup

# Start the server
uv run python -m meadows.server
```

The server starts on `http://localhost:8080`.

### Generate tokens for your users

```bash
# User token (for humans connecting via browser or TUI)
uv run edwh local.user-jwt --name=alice

# Bot token (for automated agents)
uv run edwh local.bot-jwt --name=echo
```

Share the user tokens with your users. They paste them in the web UI.

### Serve the web frontend

The web frontend is a separate package:

```bash
cd meadows-web
uv pip install -e ".[dev]"

# Build the template (required before serving)
uv run python -m meadows.web.build

# Start the web host
uv run python -m meadows.web
```

The web UI starts on port 8081. It serves static files — the browser connects directly to the server on port 8080 via Socket.IO.

---

## 3. Server development

You want to work on the server code itself — fix bugs, add features, understand the architecture.

### Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- [edwh](https://github.com/educationwarehouse/edwh) task runner (`uv pip install edwh`)

### Setup

```bash
git clone https://github.com/remcoboerma/meadows-server.git
cd meadows-server

# Install in editable mode with dev dependencies
uv pip install -e ".[dev]"
uv pip install edwh

# Generate shared JWT key and check environment
uv run edwh local.setup
```

### Common commands

```bash
# Run tests
uv run edwh local.test     # or: uv run pytest -q

# Lint
uv run edwh local.lint      # or: uv run ruff check src tests

# Format
uv run edwh local.fmt       # or: uv run ruff format src tests

# Run the server
uv run python -m meadows.server

# Generate tokens
uv run edwh local.user-jwt --name=alice
uv run edwh local.bot-jwt --name=echo
uv run edwh local.permissions-list
```

### Code map

Run `uv run edwh codemap` to get a structured overview of every source and test file. Pipe to `rg` to search:

```bash
uv run edwh codemap | rg "on_form_submission"
uv run edwh codemap | rg "BUSINESS RULE"
```

### Architecture

The server is in `meadows-server/src/meadows/server/`. Key files:

| File | Purpose |
|------|---------|
| `namespace.py` | Socket.IO event handlers (the main dispatch logic) |
| `hub.py` | State container: sessions, bots, groups, patterns, persistence |
| `persistence.py` | JSONL message storage |
| `chokepoint.py` | Protocol validation before emitting to clients |
| `label_evaluator.py` | JSON Logic predicate evaluation against labels |
| `label_dedup.py` | SQLite-backed dedup index for labels |

See the [Architecture Overview](architecture/overview.md) for the full design.

---

## 4. Bot development

Someone hosts a MEADOWS server. You have a user JWT and permission to generate bot JWTs. You want to write a bot.

### Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- A user JWT (from the server operator)
- Permission to generate bot JWTs

### 1. Clone the bot SDK

```bash
git clone https://github.com/remcoboerma/meadows-bot.git
cd meadows-bot
uv pip install -e ".[dev]"
```

### 2. Generate a bot token

```bash
cd meadows-server
uv run edwh local.bot-jwt --name=mybot
```

Copy the printed token. This is your bot's identity.

### 3. Write your bot

Create `my_bot.py`:

```python
from meadows.bot import BaseBot

class MyBot(BaseBot):
    BOT_NAME = "mybot"
    BOT_DESCRIPTION = "A bot that greets people"
    BOT_COMMANDS = [
        {"name": "greet", "description": "Say hello"},
        {"name": "help", "description": "Show commands"},
    ]

    def should_handle(self, command, args):
        return command in {"greet", "help"}

    def handle(self, command, args, raw_args, message, thread_context):
        if command == "greet":
            name = args[0] if args else "friend"
            return f"Hello {name}! I'm {self.BOT_NAME}."
        if command == "help":
            return self.format_help_response()
        return None

if __name__ == "__main__":
    MyBot().connect()
```

### 4. Run it

```bash
MEADOWS_JWT_TOKEN=<your-bot-token> uv run python my_bot.py
```

The bot connects to `http://localhost:8080` by default. Set `MEADOWS_SERVER_URL` to change:

```bash
MEADOWS_SERVER_URL=https://chat.example.com MEADOWS_JWT_TOKEN=<token> uv run python my_bot.py
```

### 5. Try the examples

The SDK includes example bots that demonstrate every feature:

```bash
# Simple echo
MEADOWS_JWT_TOKEN=<token> uv run python -m meadows.bot.examples.echo_bot

# Forms (interactive HTML)
MEADOWS_JWT_TOKEN=<token> uv run python -m meadows.bot.examples.todo_bot

# Labels (sentiment analysis)
MEADOWS_JWT_TOKEN=<token> uv run python -m meadows.bot.examples.sentiment_bot

# RPC (bot-to-bot service calls)
MEADOWS_JWT_TOKEN=<token> uv run python -m meadows.bot.examples.math_service_bot
```

### What bots can do

| Feature | How | Docs |
|---------|-----|------|
| Respond to commands | `should_handle()` + `handle()` | [Bot SDK](bot/index.md) |
| Send interactive forms | [`send_form()`](reference/forms.md#sending-a-form) | [Forms](reference/forms.md) |
| Subscribe to labels | [`register_label_subscription()`](architecture/labeling.md#subscriptions) | [Labeling](architecture/labeling.md) |
| Call other bots | [`call_rpc()`](architecture/labeling.md#rpc-via-labels) | [RPC](architecture/labeling.md#rpc-via-labels) |
| Produce labels on messages | `emit_label()` | [Labeling](architecture/labeling.md) |
| React to patterns | `register_pattern()` + `on_pattern_matched()` | [Bot SDK](bot/index.md) |

### The bot-author contract

A working bot is four things:

1. `BOT_NAME` — your bot's identity
2. `should_handle(command, args)` — decide if you handle this command
3. `handle(command, args, raw_args, message, thread_context)` — produce a response
4. `connect()` — start

Everything else — auth, reconnect, routing, labels, RPC — is handled by the SDK.

---

## 5. Data investigation

You want to explore the data: who talked to which bot, what forms were submitted, how labels flow through the system. The data lives in JSONL files on the server.

### Where the data is

Messages are stored in `meadows-server/messages/<group>.jsonl`. Each line is a JSON object representing one message, reaction, label assignment, or form submission.

```bash
cd meadows-server/messages

# List all groups
ls *.jsonl

# See recent messages in a group
tail -5 general.jsonl | python -m json.tool

# Count messages per group
wc -l *.jsonl
```

### Message structure

Each line in a JSONL file is a wire-format message:

```json
{
  "id": "1783709286616-39cbbf9d2614",
  "type": "user",
  "user_id": "user-alice",
  "group_id": "general",
  "content": "Hello everyone!",
  "timestamp": "2026-07-10T18:42:00Z",
  "labels": [["meadows", "room:general", "1.0.0"]]
}
```

Bot messages have `"type": "bot"` and a `"bot_name"` field. Form submissions have `"type": "form_submission"` with response data in `metadata.meadows.form_handling.response`.

### Exploring with jq

[jq](https://jqlang.github.io/jq/) is your best friend for JSONL exploration:

```bash
# All messages from a specific user
cat general.jsonl | jq 'select(.user_id == "user-alice")'

# All bot messages
cat general.jsonl | jq 'select(.type == "bot")'

# All form submissions
cat general.jsonl | jq 'select(.type == "form_submission")'

# All messages with labels
cat general.jsonl | jq 'select(.labels | length > 0)'

# Messages from a specific bot
cat general.jsonl | jq 'select(.bot_name == "todo")'

# Extract form response data
cat general.jsonl | jq 'select(.type == "form_submission") | .metadata.meadows.form_handling.response'

# Count messages per user
cat general.jsonl | jq -r '.user_id // .bot_name // "unknown"' | sort | uniq -c | sort -rn

# Timeline of a conversation
cat general.jsonl | jq '{time: .timestamp, user: (.user_id // .bot_name), content: .content[:80]}'
```

### Label analysis

Labels are stored on messages and also as separate `LABEL_ASSIGNED` records:

```bash
# All label assignments
cat general.jsonl | jq 'select(.event == "label_assigned")'

# Which bots produce which labels
cat general.jsonl | jq 'select(.event == "label_assigned") | {by: .applied_by, labels: [.labels[] | .label]}'

# Messages with the interactive-form label
cat general.jsonl | jq 'select(.labels? // [] | map(select(.[1] == "interactive-form")) | length > 0)'
```

### Programmatic access

For more complex analysis, use Python:

```python
import json

with open("messages/general.jsonl") as f:
    messages = [json.loads(line) for line in f if line.strip()]

# All form submissions
submissions = [m for m in messages if m.get("type") == "form_submission"]

# All bot responses
bot_msgs = [m for m in messages if m.get("type") == "bot"]

# Messages with labels
labeled = [m for m in messages if m.get("labels")]
```

### Dedup index

The server maintains a SQLite-backed dedup index at `messages/.label_dedup/`. This tracks which `(origin, label, semver, message_id)` combinations have been seen, preventing duplicate label delivery.

---

## Next steps

- [Architecture Overview](architecture/overview.md) — understand the design
- [Labeling System](architecture/labeling.md) — how labels, subscriptions, and routing work
- [Interactive Forms](reference/forms.md) — send forms, receive submissions
- [Bot SDK](bot/index.md) — the full bot-author surface
- [Socket.IO API](reference/socketio-api.md) — the complete event reference
- [Docker Deployment](development/docker.md) — production setup with Traefik
