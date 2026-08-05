---
title: Dual-Context Bot
description: Build a bot with beliefs that evolve and events it reacts to
tags:
  - educator
  - student
---

# Dual-Context Bot

A dual-context bot has two layers: a *set of beliefs* and a stream of *world events* it responds to according to those beliefs. Beliefs evolve slowly. Events arrive fast. This separation makes personal growth, opinion drift, and adaptation visible over time.

## Why this pattern matters

In most AI applications, the model has no persistent state between conversations. A dual-context bot flips this: it carries beliefs that persist across sessions and reacts to new events through the lens of those beliefs. When you cross this with [labeling](../architecture/labeling.md), you get a live laboratory for emergence and machine learning.

## Prerequisites

- A working MEADOWS server and bot JWT (see [First Bot](first-bot.md))
- The bot SDK installed (`uv pip install -e .` in `meadows-bot`)

## 1. Define the bot

Create `belief_bot.py`:

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar

from meadows.bot import BaseBot


class BeliefBot(BaseBot):
    """A bot with persistent beliefs that evolve based on world events."""

    BOT_NAME = "belief"
    BOT_DESCRIPTION = "Holds beliefs and reacts to events that challenge or confirm them"
    BOT_COMMANDS: ClassVar[list[dict[str, str]]] = [
        {"name": "belief", "description": "Show current beliefs"},
        {"name": "set", "description": "Set a belief: @belief set <topic> <stance>"},
        {"name": "help", "description": "Show available commands"},
    ]

    BELIEFS_FILE = Path("belief_state.json")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.beliefs: dict[str, float] = self._load_beliefs()

    def _load_beliefs(self) -> dict[str, float]:
        if self.BELIEFS_FILE.exists():
            return json.loads(self.BELIEFS_FILE.read_text())
        return {"ai": 0.5, "privacy": 0.3, "education": 0.7}

    def _save_beliefs(self) -> None:
        self.BELIEFS_FILE.write_text(json.dumps(self.beliefs, indent=2))

    def should_handle(self, command: str, args: list[str]) -> bool:
        return command in {"belief", "set", "help"}

    def handle(
        self,
        command: str,
        args: list[str],
        raw_args: list[str],
        message: dict[str, Any],
        thread_context: list[dict[str, Any]],
    ) -> str | None:
        if command == "belief":
            if not self.beliefs:
                return "No beliefs set yet."
            lines = ["Current beliefs:"]
            for topic, stance in self.beliefs.items():
                bar = "+" * int(stance * 10) + "-" * (10 - int(stance * 10))
                lines.append(f"  {topic}: [{bar}] {stance:.1f}")
            return "\n".join(lines)

        if command == "set":
            if len(args) < 2:
                return "Usage: @belief set <topic> <0.0 to 1.0>"
            topic = args[0]
            try:
                stance = float(args[1])
                stance = max(0.0, min(1.0, stance))
            except ValueError:
                return "Stance must be a number between 0.0 and 1.0."
            self.beliefs[topic] = stance
            self._save_beliefs()
            return f"Belief updated: {topic} = {stance:.1f}"

        if command == "help":
            return self.format_help_response()

        return None
```

### The two layers

| Layer | What it is | Pace |
|---|---|---|
| **Beliefs** | Persistent state (JSON file) — stances on topics from 0.0 to 1.0 | Slow — changed only by explicit `set` commands or event reactions |
| **World events** | Messages arriving via label subscriptions | Fast — every message triggers evaluation |

## 2. React to world events

Add an event handler that adjusts beliefs based on incoming messages. Register it in `__init__`:

```python
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.beliefs: dict[str, float] = self._load_beliefs()
        from meadows.protocol import EventName
        self.client.on(EventName.MESSAGE, self._on_world_event)

    def _on_world_event(self, data: dict[str, Any]) -> None:
        """React to messages by adjusting beliefs."""
        content = data.get("content", "").lower()

        # Skip bot's own messages
        if data.get("bot_name") == self.BOT_NAME:
            return
        if not content:
            return

        # Simple belief adjustment based on keywords
        adjustments = {
            "ai": {"positive": 0.05, "negative": -0.05},
            "privacy": {"positive": 0.03, "negative": -0.03},
        }

        for topic, rules in adjustments.items():
            if any(w in content for w in ["great", "amazing", "love", "good"]):
                old = self.beliefs.get(topic, 0.5)
                self.beliefs[topic] = min(1.0, old + rules["positive"])
            elif any(w in content for w in ["terrible", "hate", "scary", "bad"]):
                old = self.beliefs.get(topic, 0.5)
                self.beliefs[topic] = max(0.0, old + rules["negative"])

        self._save_beliefs()
```

## 3. Run it

```bash
# Start the bot with a label subscription for all messages
MEADOWS_JWT_TOKEN=<token> uv run python belief_bot.py
```

To subscribe to all messages (not just `@belief` mentions), add this before `connect()`:

```python
if __name__ == "__main__":
    bot = BeliefBot()
    bot.register_label_subscription(
        "all_messages",
        {},  # empty predicate = match everything
        scope="global",
        deliver="message_only",
    )
    bot.connect()
```

## 4. Watch it evolve

1. Open the web UI or TUI
2. Type `@belief belief` — see the initial stances
3. Send messages like "AI is amazing" or "privacy is terrible"
4. Type `@belief belief` again — watch the stances shift

The beliefs file (`belief_state.json`) persists across restarts. Leave the bot running for a day and watch drift accumulate.

## What you just learned

- **Persistent state**: beliefs survive restarts (JSON file, not in-memory)
- **Event-driven adaptation**: world events adjust beliefs automatically
- **Two time scales**: beliefs change slowly, events arrive fast
- **Observability**: you can watch the bot's internal state change over time

## Crossing with labeling

The real power comes when you add [labels](../architecture/labeling.md). Emit a label whenever a belief changes, so other bots can track opinion drift:

```python
from meadows.protocol import Label

    def _on_world_event(self, data: dict[str, Any]) -> None:
        """React to messages by adjusting beliefs and emitting labels."""
        content = data.get("content", "").lower()
        msg_id = data.get("id", "")

        if data.get("bot_name") == self.BOT_NAME:
            return
        if not content:
            return

        adjustments = {
            "ai": {"positive": 0.05, "negative": -0.05},
            "privacy": {"positive": 0.03, "negative": -0.03},
        }

        for topic, rules in adjustments.items():
            old = self.beliefs.get(topic, 0.5)
            if any(w in content for w in ["great", "amazing", "love", "good"]):
                self.beliefs[topic] = min(1.0, old + rules["positive"])
            elif any(w in content for w in ["terrible", "hate", "scary", "bad"]):
                self.beliefs[topic] = max(0.0, old + rules["negative"])

            delta = self.beliefs[topic] - old
            if delta != 0:
                label = Label("belief-bot", "opinion-shift", "1.0.0",
                              {"topic": topic, "delta": round(delta, 2)})
                self.emit_label(msg_id, [label])

        self._save_beliefs()
```

Other bots can subscribe to opinion-shift labels:

```python
bot.register_label_subscription(
    "opinion_watcher",
    {
        "and": [
            {"regex_match": [{"var": "origin"}, "^belief-bot$"]},
            {"regex_match": [{"var": "label"}, "^opinion-shift$"]},
        ]
    },
    scope="global",
    deliver="label_only",
)
```

See the [labeling walkthrough](labeling-walkthrough.md) for the full pipeline.

## Next steps

- [Labeling walkthrough](labeling-walkthrough.md) — add label production to your bot
- [Interactive forms](../reference/forms.md) — let users set beliefs via forms instead of commands
- [Architecture overview](../architecture/overview.md) — understand the message bus

## Check your understanding

- Why separate beliefs from event handlers instead of combining them in one function?
- What would happen if beliefs were not persisted to a file?
- How does the append-only property affect the belief history?
