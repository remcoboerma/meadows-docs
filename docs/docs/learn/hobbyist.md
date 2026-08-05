---
title: For the Hobbyist
description: How MEADOWS works for tinkerers and vibe coders at home
tags:
  - hobbyist
---

# For the Hobbyist

This is a real audience, not an afterthought. There's a large world of tinkerers who'd love to learn (vibe) coding but bounce off the setup wall.

## Self-hosting as a doorway, not a chore

MEADOWS is built to be run by a trusted operator on your own hardware — a laptop, a Raspberry Pi, a home server. Spinning up your own instance *is* the first project. No cloud account, no domain name, no TLS certificate required for local use.

```bash
# Clone, install, run — that's the whole setup
git clone https://github.com/remcoboerma/meadows-server.git
cd meadows-server
uv pip install -e ".[dev]"
uv pip install edwh
uv run edwh local.setup
uv run python -m meadows.server
```

See the [self-hosting quickstart](../tutorials/self-hosting-quickstart.md) for the full walkthrough.

## Vibe coding, safely

Describe what you want your bot to do, iterate fast, watch it actually talk to other bots. The reward loop is immediate and social, which is exactly what keeps a hobbyist hooked. The bot SDK is designed for this: `BOT_NAME` + `should_handle()` + `handle()` + `connect()`. No framework, no config files, no boilerplate beyond the class.

```python
# Describe what you want, watch it work
from meadows.bot import BaseBot

class JokeBot(BaseBot):
    BOT_NAME = "joke"
    BOT_DESCRIPTION = "Tells programming jokes"

    def should_handle(self, command, args):
        return command == "joke"

    def handle(self, command, args, raw_args, message, thread_context):
        return "Why do programmers prefer dark mode? Because light attracts bugs."

if __name__ == "__main__":
    JokeBot().connect()
```

## A community of tinkerers

Because bots are small, independent, and [language-agnostic](../architecture/overview.md#language-agnostic-by-design), the barrier to sharing one is tiny. "Here's a bot I made, plug it in." That's how ecosystems grow — one delighted hobbyist at a time.

## Grow it into something real

A bot that started as a weekend toy can be extended, connected to a real data source, and become genuinely useful — or the seed of a proper application. Nothing you learn is throwaway. The same `BaseBot` contract that powers your joke bot powers production-grade services.

## What hobbyists actually learn

| Concept | Where it shows up |
|---|---|
| Python basics | Class inheritance, methods, `if`/`return` |
| Client-server architecture | Bot connects to server, server routes messages |
| Event-driven programming | `should_handle()` decides, `handle()` responds |
| [JSON Logic predicates](../architecture/labeling.md#json-logic-predicates) | Subscribe to exactly the labels you care about |
| Docker basics | Optional: containerize your bot for easy sharing |

## Check your understanding

- What is the minimum code needed for a working MEADOWS bot?
- How does a bot connect to the server without a public IP address?
- What does "language-agnostic" mean for sharing bots?

See the [Concepts](../concepts/index.md) page or jump to the [first bot tutorial](../tutorials/first-bot.md).
