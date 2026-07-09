---
title: Testing
description: How to test MEADOWS packages
---

# Testing

## Test framework

All packages use:

- **pytest** — test runner
- **pytest-asyncio** — async test support (`asyncio_mode = auto`)

No markers needed for async tests — they're auto-detected.

## Running tests

### Per package (required)

```bash
cd meadows-protocol && uv run pytest -q
cd meadows-client && uv run pytest -q
cd meadows-bot && uv run pytest -q
cd meadows-server && uv run pytest -q
cd meadows-web && uv run pytest -q
cd meadows-tui && uv run pytest -q
```

### Via edwh

```bash
cd meadows-server
uv run edwh local.test    # uv run pytest -q
```

### With coverage

```bash
uv run pytest --cov=src --cov-report=term-missing
```

## Integration tests

The server has integration tests that need extra dependencies:

```bash
cd meadows-server
uv pip install -e ".[integration]"
uv run pytest -q
```

## Test conventions

- Tests live in `tests/` alongside `src/`
- Test files are named `test_*.py`
- Fixtures are in `conftest.py` at each package level
- Async tests use `asyncio_mode = auto` (no markers needed)
- A test is also documentation — if the behavior changes, update both

## Writing tests

```python
import pytest
from meadows.protocol import Message, MessageType


def test_message_creation():
    """Messages are created with correct defaults."""
    msg = Message(
        content="hello",
        group_id="general",
        type=MessageType.USER,
        user_id="user-alice",
        username="alice",
    )
    assert msg.content == "hello"
    assert msg.group_id == "general"
```
