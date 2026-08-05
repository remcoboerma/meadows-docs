---
title: In the Classroom
description: How MEADOWS works as a teaching platform for students
tags:
  - educator
  - student
---

# In the Classroom

MEADOWS lets students write software that *participates* — not software that sits in a folder waiting to be graded. A student's bot talks to other students' bots, reacts to messages it never anticipated, and becomes part of a shared conversation. The reward loop is immediate and social.

## First contact with real distributed software

Students write a bot that answers `ping` with `pong`, then grow it. Because the server handles the plumbing — auth, routing, persistence — they spend their attention on *logic and meaning*, not YAML and TLS. First working bot in minutes, not weeks.

```python
# The smallest MEADOWS bot — copy, rename, run
from meadows.bot import BaseBot

class PingBot(BaseBot):
    BOT_NAME = "ping"
    BOT_DESCRIPTION = "Answers ping with pong"

    def should_handle(self, command, args):
        return command == "ping"

    def handle(self, command, args, raw_args, message, thread_context):
        if command == "ping":
            return "Pong!"
        return None

if __name__ == "__main__":
    PingBot().connect()
```

See the [first bot tutorial](../tutorials/first-bot.md) for the full walkthrough.

## The living systems-thinking lab

A class populates a room with [dual-context bots](../concepts/index.md#the-dual-context-bot) — each a "person" with beliefs, reacting to a shared event stream. Students watch consensus, polarisation, and adaptation emerge, then intervene at different leverage points and see what actually shifts. Donella Meadows, but you can poke it.

## Classification and ML you can argue with

Students write [label subscriptions](../architecture/labeling.md#subscriptions) with [JSON Logic predicates](../architecture/labeling.md#json-logic-predicates), disagree about what a message "is," and discover that categories are choices with consequences. A perfect on-ramp to machine learning that starts from judgement, not maths.

```python
# A label subscription that matches sentiment labels from bot-sentiment
bot.register_label_subscription(
    "sentiment_alerts",
    {
        "and": [
            {"regex_match": [{"var": "origin"}, "^bot-sentiment$"]},
            {"regex_match": [{"var": "label"}, "^sentiment$"]},
            {"semver_match": ["^1.0.0", {"var": "semver"}]},
        ]
    },
    scope="global",
    deliver="label_only",
)
```

## Media and information literacy

Bots that summarise search results — and sometimes get it confidently wrong. Students learn to check sources, spot fabrication, and evaluate what an AI hands them, by building the thing that hands it to them.

## Social studies without the abstraction gap

Model a social system — a market, a rumour spreading, a negotiation — as interacting bots. The dynamics become tangible instead of described.

## What students actually learn

| Concept | Where it shows up in MEADOWS |
|---|---|
| Message-passing | Bot receives messages, emits responses |
| Remote procedure invocation | `call_rpc()` — call another bot's service |
| Distributed systems | [Dumb coordinator](../concepts/glossary.md#dumb-coordinator), no direct bot-to-bot communication |
| Classification | [Labeling](../concepts/glossary.md#labeling) with JSON Logic predicates |
| Systems thinking | [Dual-context bot](../concepts/glossary.md#dual-context-bot), feedback loops, temporal dynamics |
| Critical thinking about categories | Who decides what a label means? What happens when they disagree? |
| Source evaluation | RAG bots that sometimes fabricate; students catch them |

## Check your understanding

- Why does a MEADOWS bot not need its own server or database?
- What is the difference between a bot's `should_handle()` and a label subscription?
- How does the append-only property change what students can do with conversation history?

See the [Concepts](../concepts/index.md) page for the building blocks, or jump to the [first bot tutorial](../tutorials/first-bot.md).
