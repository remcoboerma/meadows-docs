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

```
meadows-protocol  ←  meadows-client  ←  meadows-bot
meadows-protocol  ←  meadows-server
meadows-protocol  ←  meadows-web
meadows-client + meadows-protocol  ←  meadows-tui
```

- **`meadows-protocol`** — pure declarations (Pydantic models, enums, constants). Zero behavior, zero dependencies beyond `pydantic`.
- **`meadows-client`** — client-side Socket.IO transport: connect, reconnect, JWT handshake.
- **`meadows-bot`** — bot SDK with `BaseBot`, `LLMBot`, and ready-to-use bots.
- **`meadows-server`** — the coordination hub: Socket.IO server, JWT auth, persistence.
- **`meadows-web`** — dumb HTTP host serving the browser-based chat UI.
- **`meadows-tui`** — terminal UI client built with Textual.

## Quick links

| I want to... | Go to |
|---|---|
| Get started quickly | [Quickstart](getting-started.md) |
| Understand the architecture | [Architecture Overview](architecture/overview.md) |
| Write a bot | [Bot Package](bot/index.md) |
| Run the server | [Server Package](server/index.md) |
| Deploy with Docker | [Docker](development/docker.md) |
| Contribute code | [Contributing](development/contributing.md) |

## License

Open source — see the repository for license details.
