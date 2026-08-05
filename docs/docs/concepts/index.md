---
title: Concepts
description: The building blocks of MEADOWS — structural primitives, compositional patterns, and cross-cutting dimensions
tags:
  - architect
  - educator
  - student
---

# Concepts

MEADOWS is a small set of primitives that recombine. Each primitive is a teaching surface on its own; every combination opens a new domain. This page defines the building blocks. Everything else on the site references these definitions instead of redefining them.

## Structural primitives

### The bot as an autonomous agent

A bot is a small process that listens, thinks, and speaks. It connects to the server over WebSocket, authenticates with a JWT, and receives messages via [label subscriptions](glossary.md#label) or [pattern matching](glossary.md#pattern-matching). On its own, a bot teaches programming, message-passing, and microservice thinking — without the deployment, hosting, and security tax that normally eats a beginner alive.

A working bot is four things: `BOT_NAME` + `should_handle()` + `handle()` + `connect()`. See the [Bot SDK](../bot/index.md) for the full author surface.

### The message bus and routing

Bots talk *through* the server, never directly. The server is a [dumb coordinator](../architecture/design-principles.md#3-dumb-coordinator-not-intelligent-router): it evaluates predicates, routes [labels](glossary.md#label), persists records. It does not understand what labels *mean*. This is distributed-systems thinking made concrete: how things coordinate without knowing about each other, how you address someone you've never met, why decoupling is powerful.

Messages flow through the server's single [chokepoint emit](../architecture/design-principles.md#11-single-chokepoint-emit), which validates every frame against the protocol before it hits the wire.

### Labeling

The server discovers what a message *could mean* rather than forcing everyone to agree upfront. A bot emits a [label](glossary.md#label) — a structured annotation like `("bot-sentiment", "sentiment", "1.0.0", {"score": -0.9})` — and other bots subscribe to labels matching a [JSON Logic predicate](glossary.md#json-logic-predicate). The server evaluates predicates and routes accordingly.

This is a hands-on entry into classification, taxonomy, and — importantly — *critical thinking about categories*: who decides what something is, and on what evidence?

See the [Labeling System](../architecture/labeling.md) for the full mechanism.

### Shared context nobody solely owns

The LLM sits *inside* the group conversation, not off to the side. Sense-making becomes collective. Every participant — human or bot — sees the same message history. When a user asks "what did the sentiment bot say about that last message?", any bot can look at the thread and answer.

This is the ingredient that most people underestimate and that quietly changes everything. See [Microservices, but for conversation](../architecture/overview.md#microservices-but-for-conversation).

### Persistence as a corpus

Every conversation, every label, every session becomes durable, mineable material. Messages are stored as append-only [JSONL](../architecture/labeling.md#persistence). This year's hackathon can learn from last year's workshop. History becomes a resource, not exhaust.

## Compositional patterns

### The dual-context bot

A bot with two layers: a *set of beliefs* and a stream of *world events* it responds to according to those beliefs — evolving at different paces (beliefs slowly, events fast). Watch personal growth, opinion drift, and adaptation become visible over time. Cross it with labeling and you have a live laboratory for emergence and machine learning.

See the [dual-context bot tutorial](../tutorials/dual-context-bot.md).

### Interactional labeling

Beyond *what* is being discussed lies *how people work*. When a teacher says "I love how you summarised that," a peer-learning moment just happened — and it's detectable. A bot can spot those "nice move" moments and surface them as teachable technique.

This splits labeling in two:

- **Semantic labeling** — what is this about? (topic, sentiment, intent)
- **Interactional labeling** — what good practice just occurred? (peer learning, scaffolding, metacognition)

Different studies, almost different disciplines. See [label subscriptions](../architecture/labeling.md#subscriptions) for the mechanism.

### RPC via labels

Bot-to-bot service calls use the same label-routing pipeline. A service bot subscribes to a label like `service:math`. A caller sends an `RPC_REQUEST` with that label and a `request_id`. The server routes it. The service responds with an `RPC_RESPONSE` carrying the same `request_id`. The caller's future resolves.

No new events. No separate channel. Just labels and message types. See [RPC via labels](../architecture/labeling.md#rpc-via-labels).

## Cross-cutting dimensions

These are present in almost every MEADOWS project:

### Human decision points

Forms and human input aren't UI theatre; they're first-class steps in the dataflow. A bot sends an interactive HTML form via [`send_form()`](../reference/forms.md#sending-a-form); a user fills it in; the submission routes to any subscribed bot via labels. Human judgement is architecturally respected, not treated as an edge case.

### The authoring layer

Students write bots. But so do *teachers*. The ability for a non-engineer to author working behaviour is a teaching surface, a professional-development surface, and a governance surface all at once. The [docent test](../architecture/design-principles.md#17-the-docent-test) enforces this: can a Dutch teacher (groep 6), together with an AI, build a working bot without reading the source code?

### The external connection layer

Bots reach out to search, RAG, databases, other APIs via [`call_rpc()`](../architecture/labeling.md#rpc-via-labels). That's information retrieval, tool use, and — critically — source evaluation and "how do I know this is true?"

### The temporal dimension

Delays and differing rates of change are the heart of systems thinking. In MEADOWS they're not a metaphor; they're something you can instrument and watch. The dual-context bot, the label cascade, the async RPC pattern — all demonstrate temporal dynamics in live systems.

### Privacy and ownership, inverted

Instead of only "protect the data," MEADOWS lets you *build the surveillance machine yourself to understand it* — recreate, in a safe sandbox, the pattern-harvesting that an ad giant does, on your own conversations. The sharpest distinction here: learning what someone *means* (comprehension) versus how someone *ticks* (profiling). Same mechanism, wildly different ethics. A student who builds both feels exactly where that line sits.

### Decentralization as a spectrum

Most people treat "centralized vs decentralized" as a toggle. MEADOWS is a working refutation. It decentralizes *meaning* (distributed labels, no central schema authority), *governance* (standards emerge by popularity, not decree), *ownership of context* (nobody solely owns the shared space), and *bot hosting* (self-hosted, run anywhere) — while deliberately **centralizing** *coordination* (one dumb-coordinator server per deployment) and *trust* (a trusted operator can read everything; the tradeoff is named, not hidden). Even federation is deliberately *capped* — read-only replication, not bidirectional sync.

The lesson is not "decentralize everything." It's that decentralization is a set of independent axes you choose deliberately, each with a tradeoff — a systems-thinking *pattern* long before it's a line of code.

See [Design Principles](../architecture/design-principles.md) for how this plays out in the architecture.

## Check your understanding

- A bot subscribes to labels with a JSON Logic predicate. What does the server do when a new label is assigned?
- Why is the server called a "dumb coordinator" rather than an "intelligent router"?
- What is the difference between semantic labeling and interactional labeling?
- Why is RPC implemented as label routing rather than a separate system?

See the [Glossary](glossary.md) for definitions of every term used on this site.
