---
title: Architecture Overview
description: How MEADOWS is structured
---

# Architecture Overview

MEADOWS follows a **protocol-first architecture** with strict dependency boundaries.

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
