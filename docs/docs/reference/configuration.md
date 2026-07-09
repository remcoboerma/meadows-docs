---
title: Configuration
description: Configuration reference for MEADOWS
---

# Configuration

## Server configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_HOST` | `0.0.0.0` | Bind address |
| `MEADOWS_PORT` | `8080` | Bind port |
| `MEADOWS_JWT_SECRET` | `./shared_keys/jwt.key` | JWT secret (file path or literal string, 32+ bytes) |
| `MEADOWS_MESSAGES_DIR` | `./messages` | JSONL message storage directory |
| `MEADOWS_CORS_ORIGINS` | `*` | CORS allowed origins |

## Client configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_SERVER_URL` | `http://localhost:8080` | Server URL for Socket.IO |

## Web configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_WEB_HOST` | `0.0.0.0` | Bind address |
| `MEADOWS_WEB_PORT` | `8081` | Bind port |
| `MEADOWS_SERVER_URL` | `http://localhost:8080` | Server URL (injected into page) |
| `MEADOWS_SYSTEM_NAME` | `MEADOWS Chat` | Display name |
| `PROJECT` | `meadows` | Traefik router prefix |
| `HOSTINGDOMAIN` | `localhost` | Traefik host domain |

## TUI configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_SERVER_URL` | `http://localhost:8080` | Server URL |
| `MEADOWS_JWT` | — | Pre-encoded JWT token |
| `MEADOWS_JWT_SECRET` | — | JWT secret for local token generation |
| `MEADOWS_USERNAME` | — | Username when using JWT secret |
| `MEADOWS_THEME` | `auto` | Color theme choice |
| `MEADOWS_LOG_LEVEL` | `WARNING` | Logging verbosity |
| `MEADOWS_SYSTEM_NAME` | `MEADOWS Chat` | Display name |

## Bot configuration

| Env var | Default | Description |
|---|---|---|
| `MEADOWS_JWT_TOKEN` | — | Pre-signed JWT token for bot identity |
| `MEADOWS_SERVER_URL` | `http://localhost:8080` | Server URL |

## Docker configuration

| Env var | Default | Description |
|---|---|---|
| `PROJECT` | — | Project name for Traefik routing |
| `NAME_SERVICE` | — | Service name for Traefik routing |
| `HOSTINGDOMAIN` | — | Domain for Traefik TLS |
