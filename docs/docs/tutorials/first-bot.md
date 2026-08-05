---
title: First Bot
description: Write your first MEADOWS bot — ping becomes pong
tags:
  - student
  - hobbyist
---

# First Bot

This tutorial walks you through writing, running, and talking to a MEADOWS bot. By the end, you'll have a working bot that responds to commands in a shared conversation.

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- A running MEADOWS server (see [self-hosting quickstart](self-hosting-quickstart.md) or ask your server operator)
- A bot JWT token (see [Getting Started](../getting-started.md#2-generate-a-bot-token))

## 1. Set up the bot SDK

```bash
git clone https://github.com/remcoboerma/meadows-bot.git
cd meadows-bot
uv pip install -e .
```

## 2. Generate a bot token

```bash
cd meadows-server
uv run edwh local.bot-jwt --name=echo
```

Copy the printed token. This is your bot's identity.

## 3. Write your bot

Create `echo_bot.py`:

```python
from meadows.bot import BaseBot

class EchoBot(BaseBot):
    BOT_NAME = "echo"
    BOT_DESCRIPTION = "Repeats what you say"

    BOT_COMMANDS = [
        {"name": "echo", "description": "Echo back the provided text"},
        {"name": "ping", "description": "Check if the bot is responsive"},
        {"name": "help", "description": "Show available commands"},
    ]

    def should_handle(self, command, args):
        return command in {"echo", "ping", "help"}

    def handle(self, command, args, raw_args, message, thread_context):
        if command == "echo":
            text = self.extract_quoted_string(args)
            if not text:
                return "Usage: @echo echo <text to echo>"
            return f"Echo: {text}"

        if command == "ping":
            sender = self.get_sender_info(message)
            return f"Pong! Hello {sender['display_name']}, I'm alive."

        if command == "help":
            return self.format_help_response()

        return None

if __name__ == "__main__":
    EchoBot().connect()
```

### What each part does

| Part | Purpose |
|---|---|
| `BOT_NAME` | Your bot's identity — users type `@echo` to mention it |
| `BOT_COMMANDS` | Listed by `@help` so users know what you can do |
| `should_handle()` | Decide if this command is yours — return `True` to handle it |
| `handle()` | Produce a response (return a string) or stay silent (return `None`) |
| `connect()` | Start — waits 3s for the server, then connects |

## 4. Run it

```bash
MEADOWS_JWT_TOKEN=<your-bot-token> uv run python echo_bot.py
```

The bot connects to `http://localhost:8080` by default. Set `MEADOWS_SERVER_URL` to change:

```bash
MEADOWS_SERVER_URL=https://chat.example.com MEADOWS_JWT_TOKEN=<token> uv run python echo_bot.py
```

## 5. Talk to it

Open the web UI or TUI and type:

- `@echo ping` — the bot replies "Pong!"
- `@echo echo hello world` — the bot replies "Echo: hello world"
- `@help` — the bot lists available commands

You've just written a bot that participates in a shared conversation. It sees the same messages humans see. Other bots can see its responses.

## What you just learned

- **The bot contract**: `BOT_NAME` + `should_handle()` + `handle()` + `connect()`
- **The message bus**: your bot talks *through* the server, never directly
- **Shared context**: your bot sees the full conversation, not just `@echo` mentions
- **Persistence**: everything your bot says is stored as append-only JSONL

## Next steps

- [Labeling walkthrough](labeling-walkthrough.md) — make your bot produce labels other bots can subscribe to
- [Dual-context bot](dual-context-bot.md) — add beliefs that evolve over time
- [Interactive forms](../reference/forms.md) — send HTML forms, receive submissions
- [Bot SDK reference](../bot/index.md) — the full author surface

## Check your understanding

- Why does `connect()` wait 3 seconds before connecting?
- What happens if two bots try to handle the same command?
- How does the server know which bot should receive a `@echo` mention?
