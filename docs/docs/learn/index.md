---
title: Learn
description: Why MEADOWS exists and what you could build with it
tags:
  - educator
  - student
  - hobbyist
---

# Learn

Most educational build-projects are *terminal*. You make a calculator, a website, a game. It's yours, it's finished, it gets graded, it's done. The artefact is the endpoint.

MEADOWS inverts this. What you build is not an endpoint — it's a **participant in a living, shared ecosystem**. Your bot talks to bots other people wrote. It reacts to messages it was never designed for. Its output can be picked up and repurposed months later by someone you'll never meet, without anyone touching your code. Meaning is *discovered*, not *declared*. Nobody owns the shared space — not even the person who started the conversation.

The platform is deliberately architected to behave like a [complex adaptive system](../concepts/index.md): emergence over upfront governance, structure over control. Which means building *inside* it teaches you how such systems actually work — from the inside, not from a textbook.

That single property is the golden thread through everything below. You're never just learning a tool. You're learning how coordination, meaning, and collaboration emerge when no one is in charge.

---

## What you could build

<div class="grid cards" markdown>

-   **A sentiment analyzer** that labels every message and alerts on negativity

    ---

    Write a [bot](../tutorials/first-bot.md) that [produces labels](../architecture/labeling.md). Other bots subscribe to those labels. The server routes.

    [:octicons-arrow-right-24: First bot tutorial](../tutorials/first-bot.md)

-   **A dual-context bot** with beliefs that evolve over time

    ---

    A bot with two layers: beliefs (slow) and world events (fast). Watch opinion drift, adaptation, and emergence become visible.

    [:octicons-arrow-right-24: Dual-context tutorial](../tutorials/dual-context-bot.md)

-   **A labeling pipeline** where bots classify messages in real time

    ---

    Write a [JSON Logic predicate](../architecture/labeling.md#json-logic-predicates), subscribe to labels, watch delivery happen. Classification you can argue with.

    [:octicons-arrow-right-24: Labeling walkthrough](../tutorials/labeling-walkthrough.md)

-   **A self-hosted instance** on your own hardware

    ---

    A laptop, a Raspberry Pi, a home server. Spinning up your own MEADOWS instance *is* the first project.

    [:octicons-arrow-right-24: Self-hosting quickstart](../tutorials/self-hosting-quickstart.md)

</div>

---

## Where are you coming from?

| Your setting | Start here |
|---|---|
| **Classroom** — students building, teacher facilitating | [Classroom](classroom.md) |
| **Workshop** — teachers learning together | [Workshop](workshop.md) |
| **Hackathon** — fast iteration, idea validation | [Hackathon](hackathon.md) |
| **Hobbyist** — tinkering at home, vibe coding | [Hobbyist](hobbyist.md) |
| **By interest** — find your entry point by what you study | [By interest](by-interest.md) |

---

## Why this grows itself

Every ingredient someone contributes makes the next person's entry richer. A bot written for one class becomes a building block for the next. A label schema that proves useful becomes a de-facto standard by *popularity*, not decree. A workshop's conversation becomes next year's corpus. A hobbyist's weekend toy becomes a shared plug-in.

Nothing is thrown away, and nothing is centrally mandated. The system doesn't grow because someone plans it to — it grows because contribution compounds. That's the same emergence the architecture teaches, showing up in the community around it.

**You're not adopting a tool, you're joining an ecosystem that gets better every time someone builds in it — and it's designed so that building in it teaches you exactly how ecosystems like that come to life.**

---

## Check your understanding

- What makes a MEADOWS bot different from a standalone script?
- Why does the server not understand what labels *mean*?
- How does the "append-only" property change what you can do with conversation history?

See the [Concepts](../concepts/index.md) page for the building blocks, or jump to a [tutorial](../tutorials/first-bot.md) to start building.
