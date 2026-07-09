# meadows-docs

> MEADOWS documentation site built with MkDocs Material.
> Deployed to [meadows.chat](https://meadows.chat).

## Quick start

```bash
# Set up environment
uv pip install -e ".[dev]"
uv pip install edwh
uv run edwh local.setup

# Development server (localhost:8000)
uv run edwh local.serve

# Build static site
uv run edwh local.build

# Production deployment
docker compose up -d server
```

## Structure

```
docs/
├── mkdocs.yml          # MkDocs configuration
└── docs/
    ├── index.md        # Homepage
    ├── getting-started.md
    ├── installation.md
    ├── architecture/   # Architecture docs
    ├── protocol/       # meadows-protocol package docs
    ├── server/         # meadows-server package docs
    ├── client/         # meadows-client package docs
    ├── bot/            # meadows-bot package docs
    ├── web/            # meadows-web package docs
    ├── tui/            # meadows-tui package docs
    ├── reference/      # API reference
    ├── development/    # Development guides
    └── images/         # Static assets
```

## Commands

| Command | Description |
|---|---|
| `uv run edwh local.setup` | Check environment variables |
| `uv run edwh local.build` | Build static site via Docker |
| `uv run edwh local.update` | Build + restart server |
| `uv run edwh local.serve` | Dev server (localhost:8000) |
| `uv run edwh local.clean` | Remove built site/ |

## Docker

Three Dockerfiles:

- `Dockerfile` — development (mkdocs serve)
- `Dockerfile.builder` — build static files
- `Dockerfile.server` — production (gunicorn)
