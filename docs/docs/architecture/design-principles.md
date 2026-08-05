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

---

## Architecture as deliberate tradeoff

The principles above are not abstract ideals. Each one resolves a specific tension between competing goods. Naming the tradeoff is as important as making the choice.

### Decentralization is a spectrum, not a switch

Most people treat "centralized vs. decentralized" as a toggle. MEADOWS treats it as a set of independent axes, each tuned deliberately:

| Axis | MEADOWS choice | What it centralizes | What it decentralizes |
|------|----------------|---------------------|----------------------|
| **Meaning** | Distributed labels, no central schema authority | — | Bots define their own label vocabularies; no registry, no approval gate |
| **Governance** | Standards emerge by popularity, not decree | — | Which labels become de facto standard is decided by usage, not by a committee |
| **Ownership of context** | Nobody solely owns the shared space | Coordination (one server per deployment) | The conversation belongs to all participants; the server routes but does not curate |
| **Bot hosting** | Self-hosted, run anywhere | Trust (a trusted operator can read everything) | A bot is a process with a JWT; it can run on a laptop, a Pi, or a cloud function |
| **Federation** | Capped — read-only replication, not bidirectional sync | Coordination topology | A second server can replicate a room's history; it cannot write back |

The lesson is not "decentralize everything." Each axis has a tradeoff. Centralizing coordination gives you simplicity and low latency. Centralizing trust gives you an accountability model without Byzantine-fault complexity. Decentralizing meaning gives you emergence. Decentralizing hosting gives you resilience.

The phrase that captures the whole design: **decentralized governance within a centralized coordination hub.**

### Why dumb-coordinator beats smart-router

A smart router would understand message semantics, make routing decisions based on content, and offer features like priority queues, content transformation, or AI-powered triage. This would make the server a *product* — and every bot would depend on its intelligence.

The dumb coordinator does less, and that's the point. Because the server doesn't understand meaning:

- Bots can invent new label vocabularies without server changes
- A second server can be built that speaks the same protocol
- Federation is trivial (replicate the log, not the intelligence)
- The operator's trust boundary is clean (route, don't interpret)
- No single AI vendor is baked into the infrastructure

The tradeoff: bot authors must handle their own meaning-making. The platform provides routing; bots provide intelligence. This is the [substrate, not a framework](../concepts/glossary.md#substrate) principle in action.

### Why RPC is labels, not a separate system

An alternative would be a dedicated RPC channel with its own auth, its own routing, and its own protocol events. This would be more "powerful" — but also more complex, harder to debug, and opaque to other participants.

By making RPC a label subscription with a `request_id` in metadata:

- Any bot can observe RPC traffic by subscribing to the right labels
- The same dedup, persistence, and cascade mechanisms apply
- A GUI client can display "which bots are calling which services"
- There is exactly one routing mechanism to learn

The tradeoff: RPC is less flexible than a bespoke system. It cannot do streaming, bidirectional callbacks, or type-safe contracts. But it is transparent, composable, and simple — which matters more in a system where bots are written by non-engineers.

### Why append-only

Labels could be mutable. A bot could "correct" a sentiment score, or a governance label could be updated when consensus changes. This would be more "accurate" — but it would break the guarantee that a subscriber who saw a label can rely on it existing.

Append-only means:

- No depth limits or timeouts needed to prevent infinite cascades
- Subscribers can trust that what they saw is what happened
- The JSONL log is a faithful history, not a materialized view
- Debugging is straightforward: what happened, happened

The tradeoff: you accumulate stale labels. If a semver is wrong, you bump it rather than fix it. This is intentional — it trades storage simplicity for correctness guarantees.

### Why the docent test is principle #17, not #1

Every principle above serves the docent test. The dumb coordinator serves it (simpler mental model). The trusted operator serves it (no federation complexity). The append-only labels serve it (no surprising state). The docent test is not a separate concern — it is the *purpose* that the other principles serve.

The order matters: principles 1–16 are the *how*. Principle 17 is the *why*.
