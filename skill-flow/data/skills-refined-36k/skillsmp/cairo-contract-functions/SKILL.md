---
name: cairo-contract-functions
description: Explain Starknet contract entry points (external, view, constructor, l1 handler) and ABI configuration; use when a request involves defining or exposing contract functions in Cairo.
---

# Cairo Contract Functions

## Overview
Guide how to define contract entry points and control ABI exposure in Cairo.

## Quick Use
- Read `references/contract-functions.md` before answering.
- Use `#[starknet::interface]` with `#[abi(embed_v0)]` for standard ABI definitions.
- Use `self: ContractState` for view, `ref self: ContractState` for state-mutating entry points.

## Response Checklist
- Mark constructors with `#[constructor]` and L1 handlers with `#[l1_handler]`.
- Use `#[external(v0)]` for public entry points if using per-item ABI.
- Explain that view functions are not enforced by the protocol.

## Example Requests
- "How do I define a view function vs external function?"
- "Where do I put a constructor in a Cairo contract?"
- "How do I expose a function in the ABI?"
