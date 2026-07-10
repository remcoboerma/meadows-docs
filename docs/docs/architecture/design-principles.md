---
title: Design Principles
description: Why MEADOWS exists and what it believes
---

# Design Principles

Each principle is load-bearing, not accidental. Do not change without updating this document first.

## 1. The platform is an instrument, not a product

MEADOWS exists to test whether bots and humans can build working software together during a hackathon. A Dutch teacher (groep 6) and an AI should be able to create a functioning bot in an afternoon. The success metric is idea validation and iteration speed, not code quality. A production-worthy idea does not require a production-worthy implementation.

## 2. Trusted-operator assumption

MEADOWS avoids Matrix' Byzantine-federation complexity by assuming a trusted server operator. This eliminates an entire complexity class (mutual-distrust axiom). Not on-by-default — a deliberate choice. The server routes; the operator decides who participates.

## 3. Dumb coordinator, not intelligent router

The server distributes messages without claiming room ownership. It evaluates predicates, routes labels, persists records. It does not understand what labels *mean*. Meaning is domain; routing is protocol. This makes federation trivial later and prevents room-namespace conflicts now.

## 4. Mechanism is protocol, vocabulary is domain

The test: does the server need this fact for its structural job (routing, storing, generating, notifying)? If yes, and the meaning is irrelevant to the mechanism — it belongs in protocol. If the server only relays it untouched — it belongs in domain.

**Labels** are mechanism: the server routes on `(origin, label, semver)`. What `sentiment` or `service:math` *means* is emergent between bots and users. **RPC** is mechanism: the server routes `RPC_REQUEST` to label subscribers. What a "math service" or "LLM query" *does* is domain.

This separation is what makes a second frontend, an alternative server, or a federating layer possible without reading the whole monolith.

## 5. Labels are how messages reach subscribers

Pattern matching (regex on content) is flat — every bot gets what the regex finds, without context, without shared taxonomy. Labels solve this by making annotations first-class routing objects.

A bot declares "this message is of kind X" via a label. Other bots subscribe to kind X. The server routes based on labels, not content. The stats bot subscribes with an empty predicate and sees everything. A bot that wants only sentiment labels subscribes to `{"regex_match": [{"var": "label"}, "^sentiment$"]}`. The server is the gatekeeper: only relevant messages reach each bot.

This is not a feature. It is the routing substrate. Pattern matching coexists for simple content matching. Label subscriptions are the structured path for annotation-based routing.

## 6. RPC is labels with correlation

Bot-to-bot communication is not a separate system. It is label routing with a `request_id` in metadata. A service bot subscribes to labels like `service:math`. A caller bot sends an `RPC_REQUEST` with that label and a `request_id`. The server routes it. The service responds with an `RPC_RESPONSE` carrying the same `request_id`. The caller's future resolves.

No new events. No separate channel. Just labels and message types. This is intentional: RPC is not privileged — it uses the same mechanism as everything else. A GUI client that subscribes to RPC labels can see which bots are calling which services. Transparency is a UI responsibility, not a protocol constraint.

## 7. `call_rpc` is async, not fire-and-forget

The `call_rpc` method on `MeadowClient` lets any client — bot, TUI, GUI — send an RPC request and await the response as if it were a local function call. This is not convenience; it is architectural. It means:

- A dependent bot can compose services: call the math service, then the LLM service, then the sentiment service. Each call is independent. A slow service does not block others.
- A TUI client can call a bot's service directly, without going through a bot intermediary.
- The async pattern enforces timeout discipline. A service that never responds does not hang the caller forever.

## 8. Emergence over prescription

The platform does not prescribe what bots do. It provides mechanisms (labels, RPC, patterns) and lets bots compose them. A "sentiment service" is not a server feature — it is a bot that subscribes to all messages and emits sentiment labels. A "math service" is not a server feature — it is a bot that subscribes to `service:math` labels and responds to RPC requests.

The vocabulary (which services exist, what labels mean, how bots compose) is emergent. The mechanism (routing, dedup, persistence) is protocol. This is the deepest design principle: the platform is a substrate, not a framework.

## 9. Protocol-first, always

Pure declarations in `meadows-protocol`. Pydantic models, enums, constants. **Zero behavior.** The protocol must be taalagnostisch — implementable in JavaScript, Go, Rust. The spec is the declaration, not a Python implementation. If the "spec" only exists as Python behavior, the dream of bots in other languages dies.

## 10. Hub is an object

`meadows.server.hub.Hub` is instantiated with explicit `start()`/`stop()`. No module-level `sio` or state. Someone can instantiate `Hub()`, wrap it, run it in another process, register hooks. Module-globals make federation impossible. The hub is testable, wrappable, replaceable.

## 11. Single chokepoint emit

Every client-bound frame passes through `hub.emit_frame()`, which validates against `meadows.protocol` before the data hits the wire. Invalid frames raise `ValueError` and are never emitted. This is the single enforcement point for the protocol contract. Two egress-rands: the client-rand validates against protocol; the peer-rand (federation, not yet built) is free.

## 12. Protocol is the only sibling dependency

Server imports from protocol only, never from client, bot, or web. Bot imports from client and protocol, never from server. If you find a cross-package import that isn't through protocol, something has gone wrong. The dependency tree is a tree, not a graph.

## 13. PEP 420 namespace

No `src/meadows/__init__.py` anywhere. Each package declares `src/meadows/<name>/__init__.py`. The shared namespace `meadows` is implicit. One package that claims the top-level breaks `pip install meadows-bot` without the server.

## 14. Defaults and errors are pedagogy

The target user is a Dutch teacher working with an AI during a hackathon. Defaults that "just work" and errors in human language matter more than elegance. A bot that fails silently teaches nothing. `time.sleep(3)` is not a hack — it is "wait 3 seconds so the server has time to start." Document the *why*, not just the *what*.

## 15. Labels are append-only

Facts don't un-happen. A label, once assigned, stays forever. If the semver is wrong, bump the semver. Deletion adds complexity and breaks the guarantee that a subscriber who saw a label can rely on it existing. The dedup key `(origin, label, semver, message_id)` prevents cycles without depth limits or timeouts.

## 16. JSON Logic is structural, not trusted

Label predicates are JSON Logic rules — boolean expressions over label data. JSON Logic cannot have state, which makes statelessness structurally enforced rather than trusted via sandbox isolation. A bot author writes `{"regex_match": [{"var": "label"}, "^sentiment$"]}` — not Python code that might import the server, access the filesystem, or hang in an infinite loop.

## 17. The docent test

Every piece of documentation, every SDK surface, every error message must pass the docent test: can a Dutch teacher (groep 6), together with an AI, use this to build a working bot without reading the source code? If the answer is no, the documentation is not done. Code examples must be copy-pasteable. Errors must be in human language. The quick-start must be truly quick.
