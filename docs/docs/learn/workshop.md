---
title: In the Workshop
description: How MEADOWS supports teacher professional development
tags:
  - educator
---

# In the Workshop

A workshop with MEADOWS is not a lecture about AI tools. It's a shared space where teachers *use* AI tools together, in real time, and learn from watching each other work.

## Peer learning in a shared space

Teachers collaborate around the same bots, in the same conversation. When one does something clever with an AI — a prompt, a workflow, a summarisation move — the others *see it happen* and adopt it. AI facilitation skill spreads horizontally, by demonstration, not by course.

This is the [interactional labeling](../concepts/index.md#interactional-labeling) principle applied to professional development: the "nice move" moments are visible and shareable, not buried in individual practice.

## Teachers as authors

Educators build their own small bots tailored to their subject — a Socratic questioner, a rubric-checker, a debate partner — without needing to be engineers. Ownership of tooling stays with the teacher. The [docent test](../architecture/design-principles.md#17-the-docent-test) enforces this: every SDK surface must be usable by a teacher working with an AI during a hackathon.

```python
# A Socratic questioner — teacher-authored, no engineering degree required
from meadows.bot import BaseBot

class SocratesBot(BaseBot):
    BOT_NAME = "socrates"
    BOT_DESCRIPTION = "Asks probing questions about whatever you discuss"

    def should_handle(self, command, args):
        return command == "ask"

    def handle(self, command, args, raw_args, message, thread_context):
        topic = " ".join(args) if args else "that"
        return f"What do you mean by {topic}? Why do you think that?"

if __name__ == "__main__":
    SocratesBot().connect()
```

## Mining the archive

Because sessions persist as append-only [JSONL](../concepts/glossary.md#persistence-as-a-corpus), a workshop can look back at what previous groups discovered, reuse patterns, and stand on prior work rather than restarting from zero.

## What teachers actually learn

| Concept | Where it shows up |
|---|---|
| Bot authoring | `BaseBot` contract: `BOT_NAME` + `should_handle` + `handle` + `connect` |
| AI facilitation | Watching peers use LLM bots, prompts, and forms in the shared conversation |
| Label-based routing | Subscribing to labels to filter what a bot sees |
| Interactive forms | [`send_form()`](../reference/forms.md) for structured input |
| Systems thinking | Observing how bots interact, cascade, and produce emergent behavior |

## Check your understanding

- How does a teacher author a bot without being an engineer?
- What does "append-only persistence" mean for workshop archives?
- Why is the shared conversation more effective than individual practice for learning AI facilitation?

See the [Concepts](../concepts/index.md) page or jump to the [first bot tutorial](../tutorials/first-bot.md).
