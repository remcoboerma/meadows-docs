---
title: meadows-bot
description: Bot SDK for MEADOWS
---

# meadows-bot

> MEADOWS bot SDK: `BaseBot`, `LLMBot`, and ready-to-use bots. Bot-author-facing package with a fast quick-start.
> Depends on `meadows-client` (transport) and `meadows-protocol` (shapes). Never imports from `meadows-server`.

**Repository:** [github.com/remcoboerma/meadows-bot](https://github.com/remcoboerma/meadows-bot)

## Overview

The bot package is what bot authors interact with. The whole contract is: `BOT_NAME` + `should_handle` + `handle` + `connect()`.

## Quick start

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

## Install

```bash
cd meadows-bot
uv pip install -e .

# With optional bot dependencies
uv pip install -e ".[examples,dependency-heavy,llm]"
```

## Included bots

| Bot | Commands | Description |
|---|---|---|
| `HelpBot` | `help`, `bots`, `commands`, `groups`, `guide` | Static help text |
| `StatsBot` | `@stats`, `@stats reset` | Passive monitoring dashboard |
| `ChatBot` | `chat`, `ask`, `vraag`, `praat` | LLM assistant via Ollama |
| `FetchBot` | `fetch`, `haal` | Fetches URLs → Markdown |
| `ExportBot` | `export`, `exporteer` | Exports a thread to Markdown |
| `RagBot` | `rag`, `zoek` | Video/audio fragment search |
| `SLOBot` | `slo`, `leerdoel` | Dutch SLO curriculum search |
| `SentimentBot` | — | Label producer: sentiment analysis on all messages |
| `LabelListenerBot` | — | Label consumer: alerts on angry sentiment |
| `EchoServiceBot` | `help` | Minimal RPC service (echo) |
| `MathServiceBot` | `help`, `stats` | RPC service (arithmetic) |
| `RPCCallerBot` | `echo`, `math` | Demonstrates RPC via labels |
| `TodoBot` | `add`, `list`, `edit`, `toggle`, `delete` | CRUD demo using interactive forms |

## Bot-author surface

| What | How |
|---|---|
| Identity | `BOT_NAME`, `BOT_DESCRIPTION`, `BOT_COMMANDS`, `BOT_CONTEXT_LIMIT` |
| Decide | `should_handle(command, args) -> bool` |
| Respond | `handle(command, args, raw_args, message, thread_context) -> str | None` |
| Start | `connect()` — waits 3s for server, then connects |
| Helpers | `log()`, `get_sender_info()`, `format_help_response()` |
| Patterns | `register_pattern()`, `unregister_pattern()`, `on_pattern_matched()` |
| Labels | `register_label_subscription()`, `unregister_label_subscription()`, `on_label_assigned()`, `emit_label()` |
| Forms | `send_form()` — send interactive HTML forms, receive submissions via label subscriptions |
| RPC | `emit_rpc_request()`, `emit_rpc_response()`, `on_rpc_response()`, `call_rpc()` |
| History | `fetch_messages()` |
| Lifecycle | `on_connect()`, `on_disconnect()` |

## The protocol boundary

This package imports from `meadows.client` (transport) and `meadows.protocol` (shapes), never from `meadows.server`. Server and bot meet only via the protocol declaration.

## Defaults and errors are pedagogy

The target user is not a standard Python developer — it's a Dutch teacher (groep 6) working with an AI during a hackathon. Defaults that "just work" and errors in human language matter more than elegance.
