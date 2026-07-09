---
title: Installation
description: How to install MEADOWS packages
---

# Installation

## Requirements

| Requirement | Version |
|---|---|
| Python | >= 3.12 |
| uv | latest |
| Docker | optional, for production |

## Install individual packages

Each package is installed independently. Use editable mode for development.

### meadows-protocol (pure declarations, no dependencies)

```bash
cd meadows-protocol
uv pip install -e .
```

### meadows-client (depends on protocol)

```bash
cd meadows-client
uv pip install -e .
```

### meadows-bot (depends on client + protocol)

```bash
cd meadows-bot
uv pip install -e .

# With optional bot dependencies
uv pip install -e ".[examples,dependency-heavy,llm]"
```

### meadows-server (depends on protocol)

```bash
cd meadows-server
uv pip install -e ".[dev]"
```

### meadows-web (depends on protocol)

```bash
cd meadows-web
uv pip install -e ".[dev]"
```

### meadows-tui (depends on client + protocol)

```bash
cd meadows-tui
uv pip install -e ".[dev]"
```

## Development tools

All packages use `edwh` as the task runner:

```bash
uv pip install edwh
```

Standard commands per package:

```bash
uv run edwh local.setup   # check/create env vars
uv run edwh local.test    # run tests
uv run edwh local.lint    # lint with ruff
uv run edwh local.fmt     # format with ruff
```

## Docker (production)

Each package has its own `Dockerfile` and `docker-compose.yml`. See the [Docker](development/docker.md) guide.
