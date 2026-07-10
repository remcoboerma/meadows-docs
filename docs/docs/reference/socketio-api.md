---
title: Socket.IO API
description: Socket.IO event reference
---

# Socket.IO API

All application events are on the **`/chat`** namespace. The client connects, emits `authenticate` with a JWT, then interacts via events.

## Connection lifecycle

| Event | Direction | Description |
|---|---|---|
| `connect` | client → server | Establishes WebSocket connection |
| `authenticate` | client → server | JWT handshake. Server responds with `authenticated` (user) or `bot_authenticated` (bot), then sends `group_list`, `bot_list`, `my_permissions`, and auto-joins `general`. |
| `disconnect` | client → server | Server cleans up session. If bot, removes from registry and broadcasts `bot_unregistered`. |

## Chat events

| Event | Direction | Auth | Description |
|---|---|---|---|
| `message` | client → server | yes | Send a message. Server broadcasts to group, persists to JSONL, routes `@bot` mentions, evaluates patterns, evaluates label subscriptions. |
| `typing` | client → server | yes | Typing indicator (rate-limited to 1/sec). |
| `remove_message` | client → server | yes | Mark a message as removed (strikethrough). |
| `fetch_messages` | client → server | yes | Fetch specific messages by ID. Server responds with `fetch_messages_result`. |
| `bot_response` | client → server | bot only | **(deprecated — use `message` with bot auth)** Bot sends a response. |
| `link_click` | client → server | yes | Track that a user clicked a link in a message. |

## RPC (via `message` event)

RPC uses the existing `message` event with `type` set to `rpc_request` or `rpc_response`. There are no separate RPC Socket.IO events. The server routes RPC messages exclusively via label subscriptions — no room broadcast, no pattern evaluation, no `@bot` routing.

### Sending an RPC request

```json
{
  "content": "add 2 3",
  "type": "rpc_request",
  "group_id": "general",
  "labels": [["bot-math-svc", "service:math", "1.0.0", {"request_id": "a1b2c3"}]]
}
```

### Sending an RPC response

```json
{
  "content": "5",
  "type": "rpc_response",
  "group_id": "general",
  "labels": [["bot-math-svc", "service:math-response", "1.0.0", {"request_id": "a1b2c3"}]]
}
```

### Behaviour

- **No room broadcast.** RPC messages skip `emit_frame(EventName.MESSAGE, room=...)`. They reach subscribers exclusively via label routing.
- **No auto-room-label.** The `meadows:room:<group_id>` label is not applied to RPC messages.
- **Persisted.** Both request and response are stored in the group's JSONL file.
- **Correlation.** The `request_id` in label metadata ties response to request. The caller's `call_rpc()` future resolves when a matching `RPC_RESPONSE` arrives.
- **Deliver modes.** Service bots subscribe with `deliver="message_only"` to receive the full message content. The server loads the message from persistence and emits it as a `MESSAGE` event to the subscriber.

## Message types

Every `message` event carries a `type` field that determines how the server and clients handle it:

| Type | Value | Description |
|---|---|---|
| `user` | `user` | Human-authored message |
| `bot` | `bot` | Bot-authored message |
| `reaction` | `reaction` | Reaction to another message (carries `emoji` + `target_message_id`) |
| `form_submission` | `form_submission` | Interactive form response (reserved, not yet implemented) |
| `webhook` | `webhook` | Message received via HTTP webhook |
| `system` | `system` | System-generated message |
| `rpc_request` | `rpc_request` | RPC request to a service bot (routes via labels only) |
| `rpc_response` | `rpc_response` | RPC response from a service bot (routes via labels only) |

GUI/TUI clients typically filter on `user` and `bot` types. RPC and system messages are invisible to chat rendering unless the client explicitly subscribes to them.

## Group events

| Event | Direction | Auth | Description |
|---|---|---|---|
| `create_group` | client → server | yes | Create a group (`^[a-z0-9_-]{1,32}$`). Bots auto-join. |
| `list_groups` | client → server | yes | Returns `group_list`. |
| `join_group` | client → server | yes | Join a group. Server sends `joined_group` with history. |
| `leave_group` | client → server | yes | Leave a group. |
| `delete_group` | client → server | yes | Delete a group (not `general`). Archives JSONL. |

## Reaction events

| Event | Direction | Auth | Description |
|---|---|---|---|
| `add_reaction` | client → server | yes | Toggle a reaction (emoji) on a message. If the same emoji exists from the same user, it is removed (toggle). |
| `remove_reaction` | client → server | yes | Explicitly remove a reaction. |

## Bot events

| Event | Direction | Auth | Description |
|---|---|---|---|
| `register_bot` | client → server | bot only | Register bot metadata. Server broadcasts `bot_list`. |
| `bot_list_bots` | client → server | yes | Returns `bot_list`. |
| `register_pattern` | client → server | bot only | Register a regex pattern (max 50/scope, 512 chars). |
| `unregister_pattern` | client → server | bot only | Remove a pattern by name. |
| `register_label_subscription` | client → server | bot only | Register a JSON Logic predicate against label data. |
| `unregister_label_subscription` | client → server | bot only | Remove a label subscription by name. |
| `label_assigned` | client → server | bot only | Bot emits a label on a message (dedup + cascade). |

## Ntfy events

| Event | Direction | Auth | Description |
|---|---|---|---|
| `get_ntfy_prefs` | client → server | yes | Request the user's ntfy notification preferences. |
| `save_ntfy_prefs` | client → server | yes | Save ntfy notification preferences. |

## JWT invite events

| Event | Direction | Auth | Description |
|---|---|---|---|
| `request_user_jwt` | client → server | `user-invite` | Mint a JWT for a new user. |
| `request_bot_jwt` | client → server | `bot-invite` | Mint a JWT for a new bot. |

## Server-to-client events

| Event | Trigger | Payload |
|---|---|---|
| `authenticated` | User auth success | — |
| `bot_authenticated` | Bot auth success | — |
| `auth_error` | Auth failure | `{error}` |
| `my_permissions` | Sent after auth | `{permissions, available_permissions}` |
| `message` | Message broadcast | Full message envelope |
| `message_removed` | Message marked as removed | `{message_id, group_id}` |
| `user_typing` | Typing indicator | `{user_id, group_id}` |
| `joined_group` | Group joined (includes history) | `{group_id, messages, members}` |
| `left_group` | Group left | `{group_id}` |
| `user_joined` | Someone joined a group (room broadcast, skip_sid) | `{user_id, group_id}` |
| `user_left` | Someone left a group (room broadcast, skip_sid) | `{user_id, group_id}` |
| `group_list` | Full list of groups | `{groups}` |
| `group_created` | New group created | Group state |
| `group_deleted` | Group deleted | `{group_id}` |
| `members_updated` | Group membership changed | `{group_id, members}` |
| `bot_list` | List of registered bots | `{bots}` |
| `bot_registered` | Bot successfully registered | `{bot_name}` |
| `bot_unregistered` | Bot disconnected | `{bot_name}` |
| `bot_command` | @bot mention routed to bot | Full message envelope |
| `bot_not_found` | @mention targets nothing | `{name}` |
| `rate_limited` | Bot exceeded 30 msg/min | `{bot_name}` |
| `pattern_registered` | Pattern registration ack | `{name}` |
| `pattern_unregistered` | Pattern removal ack | `{name}` |
| `pattern_matched` | Regex pattern matched a message | `{name, message_id, group_id}` |
| `label_subscription_registered` | Label subscription registered | `{name}` |
| `label_subscription_unregistered` | Label subscription removed | `{name}` |
| `label_assigned` | Label matched a subscription | `{labels, target_msg_id, applied_by, subscription_name}` |
| `reaction_added` | Reaction added to a message | `{emoji, target_message_id, user_id, group_id}` |
| `reaction_toggled` | Same emoji toggled off | `{emoji, target_message_id, user_id, group_id}` |
| `reaction_removed` | Reaction explicitly removed | `{emoji, target_message_id, user_id, group_id}` |
| `fetch_messages_result` | Response to fetch_messages | `{request_id, messages}` |
| `ntfy_prefs` | Ntfy notification preferences | Preferences data |
| `ntfy_prefs_saved` | Ntfy preferences save ack | `{success}` |
| `user_jwt_generated` | JWT minted for a user | `{token, username}` |
| `bot_jwt_generated` | JWT minted for a bot | `{token, bot_name}` |
| `error` | Generic error | `{error}` |

## Rate limiting

| Limit | Value | Scope |
|---|---|---|
| Max messages per window | 30 | per bot (sliding 60s window) |
| Cooldown on violation | 60 seconds | per bot |
| Max patterns per scope | 50 | per scope-key |
| Max pattern length | 512 chars | — |
