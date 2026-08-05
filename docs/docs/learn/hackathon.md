---
title: In the Hackathon
description: How MEADOWS fits the hackathon philosophy
tags:
  - student
  - hobbyist
---

# In the Hackathon

A hackathon is for testing whether an *idea* works, not for shipping production software. MEADOWS fits this philosophy precisely: it abstracts the production-engineering tax so teams spend their hours on real iteration — more working bots, more cycles, less deploy-pain.

## Validation, not production

The output of the day is a *better-informed next decision*, not a fragile demo. MEADOWS handles auth, routing, persistence, and transport. Teams write logic. A bot that works at 2 PM is a bot that works at 2 AM — the server doesn't care how many times you rewrote it.

## Cross-pollination in real time

Teams' bots share a bus, so one team's output can become another team's input mid-event. Collaboration emerges instead of being organised. A sentiment analyzer from Team A becomes a filter for Team B's summarizer — without anyone coordinating.

## Retroactive reuse

A team joining late can write a [label subscription](../architecture/labeling.md#subscriptions) that recognizes patterns in bots built hours earlier — and start adding value without asking anyone to change their code.

```python
# A late-joining team's bot: subscribe to all sentiment labels produced today
bot.register_label_subscription(
    "all_sentiment",
    {"regex_match": [{"var": "label"}, "^sentiment$"]},
    scope="global",
    deliver="label_only",
)
```

## Inspiration from the corpus

A "find related work" bot searches past workshops and hackathons for similar patterns — not just similar topics, but similar *ways of working* — and offers them as sparks. The append-only [persistence layer](../concepts/glossary.md#persistence-as-a-corpus) makes this possible: every session is a resource, not a graveyard.

## What hackathon participants actually learn

| Concept | Where it shows up |
|---|---|
| Rapid prototyping | Write a bot in 10 minutes, iterate in real time |
| Microservice thinking | Each bot is an independent service with its own process |
| Label-based composition | Bots discover each other's output via [labels](../concepts/glossary.md#label) |
| [RPC via labels](../architecture/labeling.md#rpc-via-labels) | Bot-to-bot service calls without shared infrastructure |
| Systems thinking | Watching multiple bots interact produces emergent behavior |

## Check your understanding

- Why is MEADOWS better suited to hackathons than building from scratch?
- How does one team's bot consume another team's output without coordination?
- What does "append-only" mean for hackathon retrospectives?

See the [Concepts](../concepts/index.md) page or jump to the [first bot tutorial](../tutorials/first-bot.md).
