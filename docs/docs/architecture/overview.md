---
title: Architecture Overview
description: Why MEADOWS exists and how it is structured
---

# Architecture Overview

MEADOWS follows a **protocol-first architecture** with strict dependency boundaries. This is not accidental — it is the result of a specific philosophy about what a platform should be.

## Philosophy

### The platform is a substrate, not a framework

MEADOWS does not tell bots what to do. It provides mechanisms — labels for routing, RPC for service calls, patterns for content matching — and lets bots compose them. A "sentiment service" is not a server feature; it is a bot that subscribes to messages and emits sentiment labels. A "math service" is not a server feature; it is a bot that responds to RPC requests. The vocabulary is emergent. The mechanism is protocol.

This is the deepest design principle: the platform provides the *how* (routing, persistence, auth), and bots provide the *what* (sentiment analysis, math, LLM queries). The separation is what makes a second frontend, an alternative server, or a federating layer possible without reading the whole codebase.

### Mechanism is protocol, vocabulary is domain

The test for what belongs in `meadows-protocol`: does the server need this fact for its structural job (routing, storing, generating, notifying)? If yes, and the meaning is irrelevant to the mechanism — it belongs in protocol. If the server only relays it untouched — it belongs in domain.

**Labels** are mechanism: the server routes on `(origin, label, semver)`. What `sentiment` or `service:math` *means* is emergent between bots and users. **RPC** is mechanism: the server routes `RPC_REQUEST` to label subscribers. What a "math service" or "LLM query" *does* is domain. **Message types** are mechanism: `USER`, `BOT`, `RPC_REQUEST`, `RPC_RESPONSE`. The content of those messages is opaque.

### Emergence over prescription

The platform does not prescribe what bots do. It provides mechanisms and lets bots compose them. A bot that calls the math service, then the LLM service, then the sentiment service — that composition is not a platform feature. It is a bot author's decision. The platform enables it; the bot defines it.

This is why `call_rpc` is on `MeadowClient`, not `BaseBot`. Any client — bot, TUI, GUI — can call any service. The service vocabulary is emergent; the routing mechanism is protocol.

### The docent test

Every piece of documentation, every SDK surface, every error message must pass the docent test: can a Dutch teacher (groep 6), together with an AI, use this to build a working bot without reading the source code? If the answer is no, the documentation is not done.

## Dependency graph

```
meadows-protocol  ←  meadows-client  ←  meadows-bot
meadows-protocol  ←  meadows-server
meadows-protocol  ←  meadows-web
meadows-protocol  ←  meadows-jsonlogic  ←  meadows-server
meadows-protocol  ←  meadows-jsonlogic  ←  meadows-client
meadows-client + meadows-protocol  ←  meadows-tui
```

## The six packages

### meadows-protocol

Pure declarations. Pydantic models, enums, constants. **Zero behavior.** This is the single source of truth for all shared types.

- `envelope.py` — `Message` model, `MessageType` enum
- `events.py` — `EventName` constants (closed set of Socket.IO events)
- `jwt.py` — `JWTClaims` model, `JWTRole`, `build_claims()` helper
- `permissions.py` — `AVAILABLE_PERMISSIONS`
- `labels.py` — `Label` model `(origin, name, version, metadata?)`
- `codec.py` — reference encoder/decoder

### meadows-jsonlogic

JSON Logic evaluator with custom operators (`regex_match`, `semver_match`, `semver_eq`). Single implementation shared by server and client — DRY.

### meadows-client

Client-side Socket.IO transport. Connect, reconnect, JWT handshake, label subscriptions, `call_rpc()`. Used by both `meadows-bot` and `meadows-tui`.

### meadows-bot

Bot SDK with `BaseBot`, `LLMBot`, and ready-to-use bots. The bot-author-facing package.

### meadows-server

The coordination hub. Socket.IO server, JWT authentication, message persistence, group management, pattern matching, label subscription evaluation, dedup index, RPC routing, rate limiting.

### meadows-web

Dumb HTTP host. Serves `index.html` and static assets. No Socket.IO, no auth, no domain logic. The browser is the real client.

### meadows-tui

Terminal UI client built with Textual. Connects via `meadows-client`.

## Key design decisions

1. **Hub is an object** — no module-level `sio` or state. `Hub()` is instantiated, wrapped, testable.
2. **Single chokepoint emit** — all client-bound frames pass through `hub.emit_frame()` which validates against protocol.
3. **Protocol is the only sibling dependency** — server never imports from bot/client, and vice versa.
4. **PEP 420 namespace** — no `src/meadows/__init__.py` anywhere.

See [Design Principles](design-principles.md) for the full set of architectural invariants.
