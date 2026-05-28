---
name: cairo-contract-events
description: Explain Starknet contract events, event enums, and emitting events; use when a request involves defining or emitting events in Cairo.
---

# Cairo Contract Events

## Overview
Explain how to define events and emit them from Cairo contracts.

## Quick Use
- Read `references/contract-events.md` before answering.
- Define an `Event` enum with `#[event]` and `#[derive(starknet::Event)]`.
- Mark indexed fields with `#[key]`.

## Response Checklist
- Emit events with `self.emit(Event::Variant(...))`.
- Use struct variants to keep event fields clear and typed.
- Use `#[key]` for fields that should be indexed.

## Example Requests
- "How do I emit an event from a contract?"
- "What does #[key] do on an event field?"
- "How do I define multiple event types?"
