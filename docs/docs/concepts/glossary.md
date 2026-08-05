---
title: Glossary
description: Every MEADOWS concept defined once — the shared anchor for the entire site
tags:
  - architect
  - educator
  - student
---

# Glossary

Every term on this site is defined here once. All other pages reference these definitions instead of redefining them.

---

### append-only

Labels are append-only. A label, once assigned, stays forever. If the semver is wrong, bump the semver. Deletion adds complexity and breaks the guarantee that a subscriber who saw a label can rely on it existing. The dedup key `(origin, label, semver, message_id)` prevents cycles without depth limits or timeouts.

### base bot

The `BaseBot` class in `meadows-bot`. The minimal contract: `BOT_NAME` + `should_handle()` + `handle()` + `connect()`. Every bot extends this. See [Bot SDK](../bot/index.md).

### bot

A small, independent process that connects to a MEADOWS server over WebSocket, authenticates with a JWT, and participates in a shared conversation. Bots are peers with humans — they see the same messages and can @mention or be @mentioned. A bot is a [Socket.IO client](https://socket.io/docs/v4/) with a JWT. See [Bot SDK](../bot/index.md).

### call_rpc

An async method on `MeadowClient` (and `BaseBot`) that sends an `RPC_REQUEST` via labels and awaits the `RPC_RESPONSE`. Any client — bot, TUI, GUI — can call any service. See [RPC via labels](../architecture/labeling.md#rpc-via-labels).

### chokepoint emit

The single point through which every client-bound frame passes. `hub.emit_frame()` validates the frame against `meadows.protocol` before it hits the wire. Invalid frames raise `ValueError`. See [Design Principles](../architecture/design-principles.md#11-single-chokepoint-emit).

### dumb coordinator

The server distributes messages without claiming room ownership. It evaluates predicates, routes labels, persists records. It does not understand what labels *mean*. Meaning is domain; routing is protocol. See [Design Principles](../architecture/design-principles.md#3-dumb-coordinator-not-intelligent-router).

### emergence

The platform provides mechanisms (labels, RPC, patterns) and lets bots compose them. Vocabulary is emergent; mechanism is protocol. A "sentiment service" is not a server feature — it is a bot that subscribes to messages and emits sentiment labels. See [Design Principles](../architecture/design-principles.md#8-emergence-over-prescription).

### exaptation

A concept borrowed from evolutionary biology: a trait that evolves for one purpose but is later co-opted for another. In MEADOWS, the labeling system was designed for message routing, but its composability means bots can repurpose labels for classification, ML training, governance signals, or anything else the community discovers. The architecture *invites* exaptation by keeping mechanisms open and vocabulary emergent. You'll encounter this term in education and systems-thinking contexts; in the MEADOWS docs, it names the property that makes the platform grow in directions its designers didn't predict.

### hub

The `Hub` class in `meadows-server`. An object holding all mutable state — sessions, bots, groups, patterns, persistence — with explicit `start()`/`stop()`. No module-level `sio` or state. See [Server Package](../server/index.md).

### JSON Logic predicate

A boolean expression over label data, written in [JSON Logic](https://jsonlogic.com/) syntax. Used in label subscriptions to filter which labels a bot receives. MEADOWS adds three custom operators: `regex_match`, `semver_match`, `semver_eq`. See [JSON Logic predicates](../architecture/labeling.md#json-logic-predicates).

### label

A four-part tuple: `(origin, label, semver, metadata)`. The first three fields are the identity. Metadata is enrichment — two labels with the same `(origin, label, semver)` but different metadata are duplicates. Labels are the primary routing structure for bot-to-bot communication. See [Labeling System](../architecture/labeling.md).

### label subscription

A name + a JSON Logic predicate + a delivery mode. Bots register subscriptions; the server evaluates predicates against incoming labels and delivers matching events. Subscriptions are replayed on reconnect. See [Subscriptions](../architecture/labeling.md#subscriptions).

### labeling

The system by which bots annotate messages with [labels](#label) and other bots subscribe to those annotations via [JSON Logic predicates](#json-logic-predicate). The server evaluates predicates and routes accordingly. This replaces brittle regex patterns with a structured, composable system. See [Labeling System](../architecture/labeling.md).

### meadows-bot

The bot SDK package. `BaseBot`, `LLMBot`, ready-to-use bots. Depends on `meadows-client` and `meadows-protocol`, never on `meadows-server`. See [Bot Package](../bot/index.md).

### meadows-client

Client-side Socket.IO transport. Connect, reconnect, JWT handshake, label subscriptions, `call_rpc()`. Shared by bots and future non-browser clients. See [Client Package](../client/index.md).

### meadows-jsonlogic

JSON Logic evaluator with custom operators (`regex_match`, `semver_match`, `semver_eq`). Shared by server and client. DRY — one implementation for label predicate evaluation. See [Architecture Overview](../architecture/overview.md).

### meadows-protocol

Pure declarations: Pydantic models, enums, constants. Zero behavior. Language-agnostic — reimplementable in any language. The single source of truth for all shared types. See [Protocol Package](../protocol/index.md).

### meadows-server

The coordination hub. Socket.IO server, JWT auth, persistence, label evaluation, pattern matching, RPC routing, rate limiting. The message broker. Routes, stores, authenticates. No domain logic. See [Server Package](../server/index.md).

### meadows-tui

Terminal UI client built with curses. A second frontend proving the protocol supports multiple UIs. See [TUI Package](../tui/index.md).

### meadows-web

Dumb HTTP host serving `index.html` and static assets. No Socket.IO, no auth. The browser is the real client; the Socket.IO connection runs browser→meadows-server. See [Web Package](../web/index.md).

### message bus

The server acts as a message bus: every message in a group is visible to every participant — human or bot. Bots that subscribe to a room label receive the same messages that humans see. This is not request-response; it is a shared, persistent, multi-party context. The conversation *is* the architecture. See [Microservices, but for conversation](../architecture/overview.md#microservices-but-for-conversation).

### persistence as a corpus

Every conversation, every label, every session becomes durable, mineable material. Messages are stored as append-only JSONL. This year's hackathon can learn from last year's workshop. History becomes a resource, not exhaust. See [Persistence](../architecture/labeling.md#persistence).

### pattern matching

Regex-based message interception. Flat — every bot gets what the regex finds, without context, without shared taxonomy. Coexists with [label subscriptions](#label-subscription) for simple content matching. Limited to 50 per bot. See [Patterns vs. label subscriptions](../architecture/labeling.md#patterns-vs-label-subscriptions).

### RPC via labels

Bot-to-bot communication using the same label-routing pipeline. An `RPC_REQUEST` message routes to a service bot via label subscriptions. The service responds with an `RPC_RESPONSE` carrying the same `request_id`. No new events, no separate channel. See [RPC via labels](../architecture/labeling.md#rpc-via-labels).

### semantic labeling

Labeling that answers "what is this about?" — topic, sentiment, intent, domain classification. One half of the labeling split. See [interactional labeling](#interactional-labeling).

### interactional labeling

Labeling that answers "what good practice just occurred?" — peer learning moments, scaffolding moves, metacognition. The other half of the labeling split. Different studies, almost different disciplines. See [interactional labeling](../concepts/index.md#interactional-labeling).

### single chokepoint emit

See [chokepoint emit](#chokepoint-emit).

### substrate

MEADOWS is a substrate, not a framework. It does not tell bots what to do. It provides mechanisms — labels for routing, RPC for service calls, patterns for content matching — and lets bots compose them. The vocabulary is emergent. The mechanism is protocol. See [Design Principles](../architecture/design-principles.md#1-the-platform-is-an-instrument-not-a-product).

### trusted operator

MEADOWS assumes a trusted server operator. This eliminates Byzantine-federation complexity (mutual-distrust axiom). The server routes; the operator decides who participates. Not on-by-default — a deliberate choice. See [Design Principles](../architecture/design-principles.md#2-trusted-operator-assumption).

### dual-context bot

A compositional pattern: a bot with two layers — a *set of beliefs* and a stream of *world events* it responds to according to those beliefs. Beliefs evolve slowly; events arrive fast. This makes personal growth, opinion drift, and adaptation visible over time. See [compositional patterns](../concepts/index.md#the-dual-context-bot).
