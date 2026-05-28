---
name: cairo-contract-class-abi
description: Explain the Starknet contract class ABI, entry points, selectors, and dispatcher usage; use when a request involves ABI JSON, entry point metadata, or how calldata is encoded for contracts.
---

# Cairo Contract Class ABI

## Overview
Explain what the contract class ABI contains and how entry points are represented and called.

## Quick Use
- Read `references/contract-class-abi.md` before answering.
- Distinguish ABI JSON (off-chain) from dispatcher patterns (on-chain).
- Include selector and entry point type when explaining invocation.

## Response Checklist
- Identify the entry point type: external, view, constructor, or L1 handler.
- Mention selectors are computed from function names.
- Explain calldata serialization per ABI when asked about argument encoding.

## Example Requests
- "What does the contract ABI include?"
- "How is an entry point selector computed?"
- "How do I encode arguments for a contract call?"
