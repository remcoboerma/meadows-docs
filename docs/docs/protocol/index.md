---
title: meadows-protocol
description: Pure declarations for the MEADOWS protocol
---

# meadows-protocol

> Pure declaration of the MEADOWS protocol: envelope, event names, JWT claims, permissions, labels.
> **No behavior.**

## Overview

`meadows-protocol` is the foundation package. Every other package depends on it. It contains only Pydantic models, enums, and constants — zero behavior, zero I/O.

| File | Purpose |
|---|---|
| `envelope.py` | `Message` model, `MessageType` enum, `QuotedMessage`, mention/everyone parsing |
| `events.py` | `EventName` constants (the closed set of Socket.IO events) |
| `jwt.py` | `JWTClaims` model, `JWTRole`, `build_claims()` helper |
| `permissions.py` | `AVAILABLE_PERMISSIONS` (single source of truth) |
| `labels.py` | `Label` triplet `(origin, label, semver)`; reserved origins: `meadows`, `system` |
| `codec.py` | Reference encoder/decoder, **subordinated** to the models |

## Install

```bash
cd meadows-protocol
uv pip install -e .
```

## Test

```bash
uv run pytest -q
```

## Usage

```python
from meadows.protocol import (
    Message,
    MessageType,
    EventName,
    JWTClaims,
    JWTRole,
    build_claims,
    Label,
    AVAILABLE_PERMISSIONS,
)
```

## The protocol boundary

**In protocol:** envelope fields, event names, JWT claims, system-message bodies, the label signaling mechanism.

**Not in protocol:** the `content` payload of ordinary messages (opaque Markdown), domain schemas, form field semantics.

See [Protocol Boundary](../architecture/protocol-boundary.md) for details.
