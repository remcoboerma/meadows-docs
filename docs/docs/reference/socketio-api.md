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
| `fetch_messages` | client → server | yes | Fetch specific messages by ID. |
| `bot_response` | client → server | bot only | Bot sends a response. |
| `link_click` | client → server | yes | Track that a user clicked a link in a message. |

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
| `add_reaction` | client → server | yes | Toggle a reaction (emoji) on a message. |
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

| Event | Trigger |
|---|---|
| `authenticated` | User auth success |
| `bot_authenticated` | Bot auth success |
| `auth_error` | Auth failure |
| `message` | Message broadcast |
| `message_removed` | Message marked as removed |
| `user_typing` | Typing indicator |
| `joined_group` | Group joined (includes history) |
| `left_group` | Group left |
| `group_list` | Full list of groups |
| `group_created` | New group created |
| `group_deleted` | Group deleted |
| `members_updated` | Group membership changed |
| `bot_list` | List of registered bots |
| `bot_registered` | Bot successfully registered |
| `bot_unregistered` | Bot disconnected |
| `bot_command` | @bot mention routed to bot |
| `bot_not_found` | @mention targets nothing |
| `rate_limited` | Bot exceeded 30 msg/min |
| `pattern_registered` | Pattern registration ack |
| `pattern_unregistered` | Pattern removal ack |
| `pattern_matched` | Regex pattern matched a message |
| `label_subscription_registered` | Label subscription registered |
| `label_subscription_unregistered` | Label subscription removed |
| `label_assigned` | Label matched a subscription |
| `reaction_added` | Reaction added to a message |
| `ntfy_prefs` | Ntfy notification preferences |
| `ntfy_prefs_saved` | Ntfy preferences save ack |
| `error` | Generic error |

## Rate limiting

| Limit | Value | Scope |
|---|---|---|
| Max messages per window | 30 | per bot (sliding 60s window) |
| Cooldown on violation | 60 seconds | per bot |
| Max patterns per scope | 50 | per scope-key |
| Max pattern length | 512 chars | — |
