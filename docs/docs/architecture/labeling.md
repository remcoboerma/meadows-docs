---
title: Labeling System
description: How MEADOWS labels route messages between bots
---

# The Labeling System

MEADOWS has a labeling mechanism that lets bots annotate messages and subscribe to annotations from other bots. Labels are the primary routing structure for bot-to-bot communication — they replace brittle regex patterns with a structured, composable system.

## The simplest case

Every message in MEADOWS gets a label automatically:

```
Label("meadows", "room:general", "1.0.0")
```

This is the **auto-room-label**. It says: "this message is in the `general` room." A bot that wants all messages in a room subscribes to this label. A bot that wants all messages everywhere subscribes with an empty predicate.

That's the whole idea. Labels are facts about messages. Bots subscribe to facts.

## What is a label?

A label is a four-part tuple:

| Field | Purpose | Example |
|-------|---------|---------|
| `origin` | Who produced it | `"bot-sentiment"`, `"meadows"` |
| `label` | What kind of fact | `"sentiment"`, `"room:general"` |
| `semver` | Version of the contract | `"1.0.0"` |
| `metadata` | Optional enrichment | `{"score": -0.9, "tone": "angry"}` |

```python
Label("bot-sentiment", "sentiment", "1.0.0", {"score": -0.9, "tone": "angry"})
```

The first three fields are the **identity**. Metadata is enrichment — two labels with the same `(origin, label, semver)` but different metadata are duplicates. If you want different metadata, bump the semver.

## How routing works

```mermaid
sequenceDiagram
    participant User
    participant Server
    participant SentimentBot
    participant ListenerBot

    User->>Server: "I am furious!"
    Server->>Server: Auto-label: meadows:room:general
    Server->>Server: Evaluate subscriptions
    Server->>SentimentBot: MESSAGE (via message_only subscription)
    SentimentBot->>Server: LABEL_ASSIGNED: sentiment=-0.9
    Server->>Server: Evaluate subscriptions against new label
    Server->>ListenerBot: LABEL_ASSIGNED (matches sentiment_alerts)
    ListenerBot->>ListenerBot: ANGER ALERT triggered!
```

The server is the coordinator. It doesn't know what labels *mean* — it only evaluates predicates against label data and routes to matching subscribers.

## Subscriptions

A subscription is a name + a JSON Logic predicate + a delivery mode:

```json
{
  "name": "sentiment-alerts",
  "predicate": {
    "and": [
      {"regex_match": [{"var": "origin"}, "^bot-sentiment$"]},
      {"regex_match": [{"var": "label"}, "^sentiment$"]},
      {"semver_match": [">=1.0.0", {"var": "semver"}]}
    ]
  },
  "scope": "global",
  "deliver": "label_only"
}
```

### Delivery modes

| Mode | What the subscriber receives |
|------|------------------------------|
| `label_only` | Just the `LABEL_ASSIGNED` event (default, least noise) |
| `message_only` | The full `MESSAGE` event (for bots that need content) |
| `both` | Both events |

### Empty predicate = match everything

```python
bot.register_label_subscription("all_msgs", {}, scope="global", deliver="message_only")
```

This is how a bot that wants to see every message subscribes. The `sentiment_bot` uses this to analyze all messages.

## The cascade

Labels can produce more labels. When a bot emits a `LABEL_ASSIGNED`, the server:

1. Deduplicates against the key `(origin, label, semver, message_id)`
2. Persists the new label in JSONL
3. Evaluates all subscriptions against the new labels
4. Delivers to matched subscribers
5. Those subscribers can produce more labels
6. Repeat until no new labels (fixed point)

```mermaid
flowchart TD
    A[Message arrives] --> B[Server assigns auto-room-label]
    B --> C[Evaluate subscriptions]
    C --> D[Deliver to matching subscribers]
    D --> E[Subscriber produces new labels]
    E --> F{Dedup: already seen?}
    F -->|No| G[Persist + Evaluate subscriptions]
    G --> D
    F -->|Yes| H[Drop — cascade terminates]
```

The dedup key prevents cycles. There are no depth limits or timeouts — the cascade runs until no new labels appear.

## The dedup key

```
(origin, label, semver, message_id)
```

Metadata is **not** part of the key. Two labels with the same key but different metadata are duplicates. If you need different metadata, bump the semver.

```mermaid
graph LR
    A["bot-sentiment:sentiment@1.0.0 on msg-1"] -->|dedup check| B{Same key exists?}
    B -->|No| C[Store + evaluate]
    B -->|Yes| D[Drop silently]
    E["bot-sentiment:sentiment@1.0.1 on msg-1"] -->|dedup check| F{Same key exists?}
    F -->|No| G[Store + evaluate — different semver]
```

## JSON Logic predicates

Subscriptions use [JSON Logic](https://jsonlogic.com/) with three custom operators:

| Operator | Purpose | Example |
|----------|---------|---------|
| `regex_match(a, b)` | `re.search(b, a)` with case-insensitive | `{"regex_match": [{"var": "origin"}, "^bot-sentiment$"]}` |
| `semver_match(a, b)` | Version b satisfies range a | `{"semver_match": [">=1.0.0", {"var": "semver"}]}` |
| `semver_eq(a, b)` | Exact semver equality | `{"semver_eq": [{"var": "semver"}, "1.0.0"]}` |

All standard JSON Logic operators work too: `==`, `!=`, `>`, `>=`, `<`, `<=`, `and`, `or`, `!`, `var`, `in`, `cat`, `+`, `-`, `*`, `/`, `?:`, `min`, `max`, `count`, `log`.

### Example predicates

Match any label from the sentiment bot:

```json
{"regex_match": [{"var": "origin"}, "^bot-sentiment$"]}
```

Match room labels for a specific group:

```json
{"regex_match": [{"var": "label"}, "^room:ops$"]}
```

Match sentiment labels with semver >= 2.0:

```json
{
  "and": [
    {"regex_match": [{"var": "label"}, "^sentiment$"]},
    {"semver_match": [">=2.0.0", {"var": "semver"}]}
  ]
}
```

Access metadata fields:

```json
{"<": [{"var": "metadata.score"}, -0.5]}
```

## Persistence

Labels are stored as separate JSONL records alongside messages:

```
{"type":"user","user_id":"user-1","group_id":"general","content":"I am furious!",...}
{"event":"label_assigned","labels":[{"origin":"bot-sentiment","label":"sentiment","semver":"1.0.0","metadata":{"score":-1.0,"tone":"angry"}}],"target_msg_id":"1783...","applied_by":"bot-sentiment"}
```

The server never merges `MESSAGE` and `LABEL_ASSIGNED` records — they are distinct. `FETCH_MESSAGES` returns both.

Auto-room-labels are **not** persisted. The room is already in the filename.

## Patterns vs. label subscriptions

MEADOWS has two routing mechanisms. They coexist:

| | Pattern | Label subscription |
|---|---------|-------------------|
| **Matches on** | Message content (regex) | Label fields (JSON Logic) |
| **Input** | Raw text | Structured label data |
| **Use case** | "Messages containing 'urgent'" | "Messages labeled as sentiment by bot-sentiment" |
| **Who registers** | Bots only | Bots and UI clients |
| **Limit** | 50 per bot | Unlimited |
| **Event** | `PATTERN_MATCHED` | `LABEL_ASSIGNED` |

Patterns are the simple path for content matching. Label subscriptions are the structured path for annotation-based routing. A bot can use both.

## RPC via labels

Bots can offer services to other bots using `RPC_REQUEST` and `RPC_RESPONSE` message types. These flow through the same label-routing pipeline:

```mermaid
sequenceDiagram
    participant BotA as Bot A (caller)
    participant Server
    participant BotB as Bot B (service)

    BotA->>Server: MESSAGE (type=RPC_REQUEST)<br>labels: [("bot-llm", "service:llm-query", "1.0.0")]
    Server->>Server: Skip room broadcast (RPC only routes via labels)
    Server->>BotB: LABEL_ASSIGNED (subscription matches service:llm-query)
    BotB->>Server: MESSAGE (type=RPC_RESPONSE)<br>labels: [("bot-llm", "service:llm-response", "1.0.0")]
    Server->>BotA: LABEL_ASSIGNED (subscription matches service:llm-response)
```

RPC messages are **not** room-broadcast. They reach subscribers exclusively via label routing. The auto-room-label is not applied to RPC messages.

Correlation uses `request_id` in label metadata — the caller includes a UUID in the request, and the service echoes it back in the response.

## The package structure

```mermaid
graph TD
    JL[meadows-jsonlogic] --> S[meadows-server]
    JL --> C[meadows-client]
    P[meadows-protocol] --> JL
    P --> S
    P --> C
    C --> B[meadows-bot]
    S -.->|labels route| B
    B -.->|LABEL_ASSIGNED| S
```

| Package | What it does for labels |
|---------|------------------------|
| `meadows-jsonlogic` | Evaluates JSON Logic predicates with custom operators |
| `meadows-protocol` | Declares `Label` model, `EventName` constants, `MessageType` values |
| `meadows-server` | Subscription registry, label evaluation, dedup index, cascade, persistence |
| `meadows-client` | `register_label_subscription()`, `on_label_assigned()`, reconnect replay |
| `meadows-bot` | Thin wrappers + `emit_label()` for the author surface |

## Example bots

### sentiment_bot — a label producer

This bot subscribes to all messages, analyzes sentiment, and produces labels:

```python
class SentimentBot(BaseBot):
    BOT_NAME = "sentiment"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client.on(EventName.MESSAGE, self._on_message)

    def _on_message(self, data):
        content = data.get("content", "")
        sentiment = analyze_sentiment(content)
        lbl = Label("bot-sentiment", "sentiment", "1.0.0", sentiment)
        self.emit_label(data["id"], [lbl])

if __name__ == "__main__":
    bot = SentimentBot()
    bot.register_label_subscription("all_msgs", {}, scope="global", deliver="message_only")
    bot.connect()
```

### label_listener_bot — a label consumer

This bot subscribes to sentiment labels and alerts on angry messages:

```python
class LabelListenerBot(BaseBot):
    BOT_NAME = "listener"

    def _on_angry_sentiment(self, data):
        for lbl in data.get("labels", []):
            if lbl["metadata"]["tone"] == "angry":
                self.log(f"ANGER ALERT! score={lbl['metadata']['score']}")

if __name__ == "__main__":
    bot = LabelListenerBot()
    bot.register_label_subscription(
        "sentiment_alerts",
        {
            "and": [
                {"regex_match": [{"var": "origin"}, "^bot-sentiment$"]},
                {"regex_match": [{"var": "label"}, "^sentiment$"]},
                {"semver_match": [">=1.0.0", {"var": "semver"}]},
            ]
        },
        scope="global",
        deliver="label_only",
    )
    bot.on_label_assigned("sentiment_alerts")(bot._on_angry_sentiment)
    bot.connect()
```

### Running them together

```bash
# Terminal 1 — server
cd meadows-server && uv run python -m meadows.server

# Terminal 2 — sentiment bot
cd meadows-bot && MEADOWS_SERVER_URL=http://localhost:8080 \
  MEADOWS_JWT_TOKEN=<token> uv run python -m meadows.bot.examples.sentiment_bot

# Terminal 3 — listener bot
cd meadows-bot && MEADOWS_SERVER_URL=http://localhost:8080 \
  MEADOWS_JWT_TOKEN=<token> uv run python -m meadows.bot.examples.label_listener_bot

# Send a message
curl -X POST http://localhost:8080/r/general \
  -H "Authorization: Bearer <user-token>" \
  -H "Content-Type: application/json" \
  -d '{"content":"I am furious about this!"}'
```

Listener output:

```
[INFO] [listener] RECEIVED LABEL_ASSIGNED: 1 labels for msg 1783...
[INFO] [listener] ANGER ALERT on msg 1783...: score=-1.0, tone=angry
```

## Design intent

### Why labels exist

MEADOWS had a routing problem. Pattern matching (regex on content) is flat — every bot gets what the regex finds, without context, without shared taxonomy. The stats bot registers `".*"` and sees everything. A bot that wants only urgent messages must write its own regex and hope nobody else defines "urgent" differently.

Labels solve this by making annotations first-class routing objects. A bot declares "this message is of kind X" via a label. Other bots subscribe to kind X. The server routes based on labels, not content.

### Why a separate package for JSON Logic

Both server and clients need to evaluate predicates. DRY is not optional — duplicating the custom operators in server and client would guarantee they diverge. The `meadows-jsonlogic` package is the single implementation.

### Why the dedup key excludes metadata

Metadata is enrichment, not identity. If metadata were part of the key, a bot producing labels with evolving metadata (`{"score": -0.9}`, then `{"score": -0.9, "tone": "angry"}`) would create new keys each time. The cascade would never converge. Bumping the semver is the explicit contract for "this is a different fact."

### Why append-only

Labels are facts about messages. Facts don't un-happen. If a label's semver is wrong, bump the semver. Deletion adds complexity and breaks the guarantee that a subscriber who saw a label can rely on it existing forever.

## Future possibilities

### Rich NLP pipelines

A bot chain where each bot adds a layer of analysis:

```mermaid
flowchart LR
    M[Message] --> L1[Language detection bot]
    L1 -->|Label: lang=en| L2[Translation bot]
    L2 -->|Label: translated| L3[Sentiment bot]
    L3 -->|Label: sentiment| L4[Summary bot]
    L4 -->|Label: summary| UI[GUI/TUI displays all labels]
```

Each bot subscribes to the previous bot's labels and produces its own. The cascade handles the pipeline automatically.

### Federated services

A bot offers LLM access as a service via RPC:

```mermaid
sequenceDiagram
    participant ChatBot
    participant Server
    participant LLMService

    ChatBot->>Server: RPC_REQUEST to llm-service
    Server->>LLMService: Label-routed delivery
    LLMService->>Server: RPC_RESPONSE with generated text
    Server->>ChatBot: Label-routed delivery
```

The service bot runs on fast hardware. The chat bot runs anywhere. They communicate through labels, never directly.

### UI transparency

A GUI client that subscribes to all labels in its rooms can show humans what the bots see:

```
[alice] I am furious about this!
  └─ [bot-sentiment:sentiment@1.0.0] score=-1.0, tone=angry
  └─ [bot-urgency:urgent@1.0.0] level=high
```

The labeling mechanism is protocol. Transparancy is a UI responsibility. The server doesn't force it — the client chooses what to show.

### Form submissions

The existing forms mechanism (bots send HTML in markdown fences) will be formalized via labels. The label `("meadows", "interactive-form", "1.0.0")` declares "this message contains an interactive element." The payload stays opaque. This resolves the current gap where forms are detected by regex-sniffing markdown fences.

### Temporal analysis

Labels can be produced on old messages. A bot processing months of history can label old messages with sentiment scores. Subscribers that care about historical analysis receive those labels. The dedup key uses `message_id`, so re-processing the same message with the same label is idempotent.
