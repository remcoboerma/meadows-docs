---
title: Labeling Walkthrough
description: Write a JSON Logic predicate, watch labels flow, understand the routing pipeline
tags:
  - educator
  - student
---

# Labeling Walkthrough

This tutorial walks through the full label lifecycle: a bot produces a label, the server evaluates predicates, and a subscribing bot receives it. You'll write the code for both sides and watch the pipeline work.

## Prerequisites

- A working MEADOWS server and two bot JWTs (see [First Bot](first-bot.md))
- The bot SDK installed (`uv pip install -e .` in `meadows-bot`)

## The pipeline in 30 seconds

1. **Bot A** emits a label on a message: `("bot-sentiment", "sentiment", "1.0.0", {"score": -0.9})`
2. **Server** evaluates all label subscriptions against this label
3. **Bot B** subscribed with predicate `{"regex_match": [{"var": "label"}, "^sentiment$"]}` — it matches
4. **Server** delivers the `LABEL_ASSIGNED` event to Bot B
5. Bot B reacts

See [Labeling System](../architecture/labeling.md) for the full mechanism.

## 1. Write the label producer

Create `sentiment_producer.py`:

```python
from __future__ import annotations

from typing import Any, ClassVar

from meadows.bot import BaseBot
from meadows.protocol import Label


def analyze(text: str) -> dict[str, Any]:
    """Simple keyword sentiment — real systems use NLP."""
    happy = {"great", "love", "amazing", "awesome", "good", "wonderful"}
    angry = {"terrible", "hate", "awful", "horrible", "bad", "worst"}
    words = set(text.lower().split())

    h = len(words & happy)
    a = len(words & angry)
    total = h + a

    if total == 0:
        return {"score": 0.0, "tone": "neutral"}

    score = round((h - a) / total, 2)
    tone = "happy" if score > 0 else "angry" if score < 0 else "neutral"
    return {"score": score, "tone": tone}


class SentimentProducer(BaseBot):
    BOT_NAME = "sentiment"
    BOT_DESCRIPTION = "Produces sentiment labels on messages"
    BOT_COMMANDS: ClassVar[list[dict[str, str]]] = [
        {"name": "help", "description": "Show available commands"},
    ]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._seen: set[str] = set()
        from meadows.protocol import EventName
        self.client.on(EventName.MESSAGE, self._on_message)

    def should_handle(self, command: str, args: list[str]) -> bool:
        return command == "help"

    def handle(self, command, args, raw_args, message, thread_context):
        if command == "help":
            return self.format_help_response()
        return None

    def _on_message(self, data: dict[str, Any]) -> None:
        content = data.get("content", "")
        msg_id = data.get("id", "")

        if data.get("bot_name") == self.BOT_NAME:
            return
        if not content or msg_id in self._seen:
            return
        self._seen.add(msg_id)

        sentiment = analyze(content)
        label = Label("bot-sentiment", "sentiment", "1.0.0", sentiment)
        self.emit_label(msg_id, [label])
        self.log(f"Label: {sentiment}")


if __name__ == "__main__":
    bot = SentimentProducer()
    # Subscribe to ALL messages — we analyze everything
    bot.register_label_subscription("all", {}, scope="global", deliver="message_only")
    bot.connect()
```

### Key points

- **`emit_label(msg_id, [label])`** — attaches a label to an existing message
- **`register_label_subscription("all", {}, ...)`** — empty predicate matches all messages
- **`deliver="message_only"`** — we need the message content to analyze it

## 2. Write the label consumer

Create `sentiment_consumer.py`:

```python
from __future__ import annotations

from typing import Any, ClassVar

from meadows.bot import BaseBot


class SentimentConsumer(BaseBot):
    BOT_NAME = "alert"
    BOT_DESCRIPTION = "Alerts on angry sentiment labels"
    BOT_COMMANDS: ClassVar[list[dict[str, str]]] = [
        {"name": "stats", "description": "Show alert statistics"},
        {"name": "help", "description": "Show available commands"},
    ]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.alerts = 0
        self.total = 0

    def should_handle(self, command: str, args: list[str]) -> bool:
        return command in {"stats", "help"}

    def handle(self, command, args, raw_args, message, thread_context):
        if command == "stats":
            return f"Labels received: {self.total}\nAngry alerts: {self.alerts}"
        if command == "help":
            return self.format_help_response()
        return None

    def _on_sentiment(self, data: dict[str, Any]) -> None:
        """Called when a sentiment label matches our predicate."""
        labels = data.get("labels", [])
        for lbl in labels:
            self.total += 1
            meta = lbl.get("metadata", {})
            tone = meta.get("tone", "unknown")
            score = meta.get("score", 0)

            if tone == "angry" and score < -0.3:
                self.alerts += 1
                msg_id = data.get("target_msg_id", "")
                self.log(f"ANGER ALERT on {msg_id}: score={score}")


if __name__ == "__main__":
    bot = SentimentConsumer()

    # Subscribe to sentiment labels from bot-sentiment
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

    # Register the callback
    bot.on_label_assigned("sentiment_alerts")(bot._on_sentiment)

    bot.connect()
```

### The predicate explained

```json
{
  "and": [
    {"regex_match": [{"var": "origin"}, "^bot-sentiment$"]},
    {"regex_match": [{"var": "label"}, "^sentiment$"]},
    {"semver_match": ["^1.0.0", {"var": "semver"}]}
  ]
}
```

| Clause | What it matches |
|---|---|
| `origin` = `^bot-sentiment$` | Labels produced by the sentiment bot |
| `label` = `^sentiment$` | Labels with kind "sentiment" |
| `semver` satisfies `^1.0.0` | Version 1.x.x (compatible) |

All three must be true (the `and` combinator). See [JSON Logic predicates](../architecture/labeling.md#json-logic-predicates) for the full operator reference.

## 3. Run both bots

Terminal 1:

```bash
MEADOWS_JWT_TOKEN=<token-a> uv run python sentiment_producer.py
```

Terminal 2:

```bash
MEADOWS_JWT_TOKEN=<token-b> uv run python sentiment_consumer.py
```

## 4. Watch the pipeline work

Open the web UI or TUI and send messages:

1. Type `hello everyone` — neutral sentiment, no alert
2. Type `this is terrible and awful` — angry sentiment, alert fires
3. Type `@alert stats` — see the label count

Watch the producer's log output: it prints the sentiment score and tone for every message it analyzes. Watch the consumer's log output: it prints alerts when anger exceeds the threshold.

## What you just learned

- **Label production**: `emit_label(msg_id, [label])` attaches structured metadata to messages
- **JSON Logic predicates**: filter which labels a bot receives
- **The cascade**: producer emits → server evaluates → consumer receives
- **Delivery modes**: `label_only` (just the label event) vs `message_only` (full message)
- **Dedup**: the server prevents duplicate label delivery via `(origin, label, semver, message_id)`

## Next steps

- [RPC via labels](../architecture/labeling.md#rpc-via-labels) — make your label consumer call back to the producer
- [Interactive forms](../reference/forms.md) — let users configure sentiment thresholds via forms
- [Dual-context bot](dual-context-bot.md) — combine beliefs with labeling

## Check your understanding

- Why does the producer subscribe with `deliver="message_only"` but the consumer uses `deliver="label_only"`?
- What happens if two bots emit the same label on the same message?
- How would you change the predicate to match all labels from any bot?
