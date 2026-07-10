---
title: MEADOWS Documentation
description: MEADOWS Enables Agentic Dialogue, Orchestrating a Web of Sense
---

# MEADOWS Documentation

**MEADOWS** = *MEADOWS Enables Agentic Dialogue, Orchestrating a Web of Sense*

Named after Donella Meadows (systems thinking). An open-source Socket.IO orchestration server for AI-facilitated group conversations, hackathon education, and multi-bot simulations.

## What is MEADOWS?

MEADOWS is a modular chat platform built around a **protocol-first architecture**. Six independent Python packages share a common namespace (`meadows.*`) but are developed, tested, and deployed separately.

**Key features:**

- **Group chat** with Socket.IO real-time messaging
- **Bot SDK** — build working bots in minutes, not hours
- **Protocol-driven** — the protocol is explicit, not implicit
- **Multi-client** — web UI, terminal TUI, and bot clients
- **Hackathon-friendly** — designed for rapid iteration and education

## Architecture at a glance

```mermaid
graph TD
    J[meadows-jsonlogic<br><i>JSON Logic evaluator</i>]
    C[meadows-client<br><i>Socket.IO transport</i>]
    B[meadows-bot<br><i>BaseBot SDK</i>]
    S[meadows-server<br><i>coordination hub</i>]
    W[meadows-web<br><i>dumb HTTP host</i>]
    T[meadows-tui<br><i>terminal UI</i>]
    P[meadows-protocol<br><i>pure declarations</i>]
    Browser[Browser JS<br><i>real client</i>]

    J --> P
    C --> P
    C --> J
    S --> P
    S --> J
    W --> P
    T --> P
    T --> C
    B --> C
    B --> P
    W -.->|static files| Browser
    Browser -->|Socket.IO| S
    B -->|Socket.IO| S
```

- **`meadows-protocol`** — pure declarations (Pydantic models, enums, constants). Zero behavior, zero dependencies beyond `pydantic`.
- **`meadows-jsonlogic`** — JSON Logic evaluator with custom operators (`regex_match`, `semver_match`, `semver_eq`). Shared by server and client.
- **`meadows-client`** — client-side Socket.IO transport: connect, reconnect, JWT handshake, label subscriptions.
- **`meadows-bot`** — bot SDK with `BaseBot`, `LLMBot`, `send_form()`, `call_rpc()`, and ready-to-use bots.
- **`meadows-server`** — the coordination hub: Socket.IO server, JWT auth, persistence, label evaluation, RPC routing.
- **`meadows-web`** — dumb HTTP host serving the browser-based chat UI. No Socket.IO, no auth.
- **`meadows-tui`** — terminal UI client built with Textual.

## How it works

- **[Labels](architecture/labeling.md)** — the routing mechanism. Bots subscribe to label patterns via [JSON Logic predicates](architecture/labeling.md#json-logic-predicates); the server evaluates and delivers.
- **[RPC via labels](architecture/labeling.md#rpc-via-labels)** — bot-to-bot service calls. A math service, an LLM proxy, a database — any bot can expose functionality.
- **[Forms](reference/forms.md)** — interactive HTML sent by bots, submitted by users, routed to any subscribed bot via labels.
- **[Microservices](architecture/overview.md#microservices-but-for-conversation)** — each bot is an independent service. The conversation is the message bus. Humans and bots are peers.

## Quick links

| I want to... | Go to |
|---|---|
| Get started quickly | [Quickstart](getting-started.md) |
| Understand the architecture | [Architecture Overview](architecture/overview.md) |
| Write a bot | [Bot Package](bot/index.md) |
| Send interactive forms | [Interactive Forms](reference/forms.md) |
| Run the server | [Server Package](server/index.md) |
| Deploy with Docker | [Docker](development/docker.md) |
| Contribute code | [Contributing](development/contributing.md) |

## License

Open source — see the repository for license details.
