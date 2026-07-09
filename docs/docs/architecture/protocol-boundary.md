---
title: Protocol Boundary
description: What belongs in protocol vs domain
---

# Protocol Boundary

> The system contracts what it itself must understand. What only bots and humans need to understand stays opaque.

## The test

Before adding anything to `meadows-protocol`, ask: **does the server need this fact to do its structural job (route, store, generate, notify) — regardless of what the fact means?**

| Answer | Placement | Example |
|---|---|---|
| Yes, and meaning is irrelevant | Protocol | "This message reacts to message X" |
| Server only relays it untouched | Domain (bot/client code) | What a reaction emoji *means* |
| Only changes human perception | UI | Display formatting |

## In protocol

- Envelope fields (`Message` model)
- Event names (`EventName` constants)
- JWT claims (`JWTClaims` model)
- System-message bodies
- The label signaling mechanism
- Permissions list

## Not in protocol

- The `content` payload of ordinary messages (opaque Markdown)
- Domain schemas (SLO results, export formats, todo shapes)
- What reaction emoji *mean*
- Form field semantics
- Which label schemas exist

## Worked examples

### Reactions

**Protocol** owns "this message reacts to message X" — the shape of the reaction event, the `target_message_id` field, the `emoji` field.

**Domain** owns what the reaction symbol means — whether it's a vote, a sentiment, or a status indicator.

### Forms

**Protocol** owns "this message contains an interactive element requiring a server-generated endpoint" — the `labels` mechanism and form submission event shape.

**Domain** owns field semantics — what fields exist, what they're called, what validation rules apply.

### Labels

**Protocol** owns the JSON Logic predicate mechanism and the `(origin, name, version)` tuple shape.

**Domain** owns which schemas exist and what they're called.

## The boundary rule

If you find yourself declaring a *set of valid values* (reaction emoji, form field types, schema names) in protocol, stop — that's vocabulary leaking upward. Protocol declares shapes; domain declares vocabulary.
