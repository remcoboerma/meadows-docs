---
title: Design Principles
description: Core architectural invariants
---

# Design Principles

Each principle is load-bearing, not accidental. Do not change without updating this document first.

## 1. Trusted-operator assumption

MEADOWS avoids Matrix' Byzantine-federation complexity by assuming a trusted server operator. This eliminates an entire complexity class (mutual-distrust axiom). Not on-by-default — a deliberate choice.

## 2. Dumb coordinator pattern

The server distributes messages without claiming room ownership. Makes federation trivial later; prevents room-namespace conflicts now.

## 3. Structural guarantee over convention (intended)

The design intention is that labeling lambdas will be JSON Logic rules (boolean predicates), not Python-sandboxed functions. JSON Logic cannot have state, which would make statelessness structurally enforced rather than trusted via sandbox isolation. **This is not yet implemented** — `labels.py` currently provides only the `(origin, label, semver)` triplet as a `NamedTuple`.

## 4. Mechanism is protocol, vocabulary is domain

The test: does the server need this fact for its structural job (routing, storing, generating, notifying)? If yes, and the meaning is irrelevant to the mechanism — it belongs in protocol. If the server only relays it untouched — it belongs in domain.

## 5. Hub is an object

`meadows.server.hub.Hub` is instantiated with explicit `start()`/`stop()`. No module-level `sio` or state. Someone can instantiate `Hub()`, wrap it, run it in another process.

## 6. Single chokepoint emit

Every client-bound frame passes through `hub.emit_frame()`, which validates against `meadows.protocol` before the data hits the wire. Invalid frames raise `ValueError` and are never emitted. This is the single enforcement point for the protocol contract.

## 7. Protocol is the only sibling dependency

Server imports from protocol only, never from client, bot, or web. Bot imports from client and protocol, never from server. If you find a cross-package import that isn't through protocol, something has gone wrong.

## 8. PEP 420 namespace

No `src/meadows/__init__.py` anywhere. Each package declares `src/meadows/<name>/__init__.py`. The shared namespace `meadows` is implicit.

## 9. Hackathon doctrine

The artifact is not a production system. It is an instrument to test the viability of an idea. Success metric is iteration speed and idea validation, not code quality. Production-worthy idea ≠ production-worthy implementation.

## 10. Defaults and errors are pedagogy

The target user is not a standard Python developer — it's a Dutch teacher (groep 6) working with an AI during a hackathon. Defaults that "just work" and errors in human language matter more than elegance. A bot that fails silently teaches nothing.
