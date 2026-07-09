---
title: Environment Variables
description: All MEADOWS environment variables
---

# Environment Variables

MEADOWS applications read configuration from environment variables, not from `.env` files. All env management goes through `edwh.check_env()` in `tasks.py:setup` tasks.

## Server

| Variable | Default | Package |
|---|---|---|
| `MEADOWS_HOST` | `0.0.0.0` | server |
| `MEADOWS_PORT` | `8080` | server |
| `MEADOWS_JWT_SECRET` | `./shared_keys/jwt.key` | server, client |
| `MEADOWS_MESSAGES_DIR` | `./messages` | server |
| `MEADOWS_CORS_ORIGINS` | `*` | server |

## Client / Transport

| Variable | Default | Package |
|---|---|---|
| `MEADOWS_SERVER_URL` | `http://localhost:8080` | client, bot, web, tui |

## Authentication

| Variable | Default | Package |
|---|---|---|
| `MEADOWS_JWT` | — | tui (pre-signed token) |
| `MEADOWS_JWT_TOKEN` | — | bot (pre-signed token) |
| `MEADOWS_JWT_SECRET` | — | tui (local signing for dev) |
| `MEADOWS_USERNAME` | — | tui (local signing) |

## Web

| Variable | Default | Package |
|---|---|---|
| `MEADOWS_WEB_HOST` | `0.0.0.0` | web |
| `MEADOWS_WEB_PORT` | `8081` | web |
| `MEADOWS_SYSTEM_NAME` | `MEADOWS Chat` | web, tui |

## TUI

| Variable | Default | Package |
|---|---|---|
| `MEADOWS_THEME` | `auto` | tui |
| `MEADOWS_LOG_LEVEL` | `WARNING` | tui |

## Docker / Traefik

| Variable | Default | Package |
|---|---|---|
| `PROJECT` | — | all (Traefik routing) |
| `NAME_SERVICE` | — | all (Traefik routing) |
| `HOSTINGDOMAIN` | — | all (Traefik TLS) |
