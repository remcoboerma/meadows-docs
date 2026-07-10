---
title: Webhook API
description: HTTP webhook endpoint reference
---

# Webhook API

## `POST /r/{group_id}`

Send a message to a group over HTTP. The message goes through the same pipeline as Socket.IO messages: broadcast, persistence, @bot routing, and regex pattern evaluation.

### Request

```
POST /r/general
Authorization: Bearer <jwt>
Content-Type: application/json

{"content": "Build passed"}
```

### Auth

Any valid JWT (user or bot). No specific permission required.

### Body

| Field | Type | Required | Description |
|---|---|---|---|
| `content` | string | yes | Message content (markdown, max 100k chars) |
| `type` | string | no | Message type. Defaults to `"webhook"`. Set to `"rpc_request"` or `"rpc_response"` for RPC. |
| `labels` | array | no | Labels for RPC routing. Each label is `[origin, label, semver, metadata?]`. |

### Response

```json
{"status": "ok", "message_id": "01923a4f5e6c-3a2f4b8c0d1e"}
```

### Error responses

| Status | Body | Condition |
|---|---|---|
| 401 | `{"error": "missing bearer token"}` | No Authorization header |
| 401 | `{"error": "invalid token"}` | Bad or expired JWT |
| 404 | `{"error": "group not found"}` | Unknown group_id |
| 400 | `{"error": "invalid JSON body"}` | Malformed request body |
| 400 | `{"error": "content is required"}` | Empty or missing content |
| 400 | `{"error": "content too large"}` | Content exceeds 100k chars |

### Behaviour

- Messages are typed as `webhook` (distinct from `user` / `bot`)
- `@botname command` in content triggers bot routing
- `@everyone` / `@all` sets `is_everyone=true` if JWT has `mention-all`
- Registered regex patterns are evaluated against the content
- Sender identity is derived from the JWT (not the request body)
- When `type` is `rpc_request` or `rpc_response`, the message skips room broadcast and routes exclusively via label subscriptions

### Examples

=== "cURL"

    ```bash
    curl -X POST http://localhost:8080/r/general \
      -H "Authorization: Bearer $JWT" \
      -H "Content-Type: application/json" \
      -d '{"content":"Deploy #42 complete"}'
    ```

=== "Python"

    ```python
    import httpx

    resp = httpx.post(
        "http://localhost:8080/r/general",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"content": "Build passed"},
    )
    print(resp.json())  # {"status": "ok", "message_id": "..."}
    ```

### RPC via webhook

Set `type` and `labels` to send RPC requests over HTTP:

```bash
curl -X POST http://localhost:8080/r/general \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{"content":"add 2 3","type":"rpc_request","labels":[["bot-math-svc","service:math","1.0.0",{"request_id":"req-001"}]]}'
```

The `labels` field is an array of `[origin, label, semver, metadata?]` tuples. The metadata dict should include `request_id` for correlation. Both request and response are persisted to the group's JSONL file.
