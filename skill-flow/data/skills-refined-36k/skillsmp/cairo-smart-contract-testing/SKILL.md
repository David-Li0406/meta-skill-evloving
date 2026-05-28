---
name: cairo-smart-contract-testing
description: Explain how to test Starknet contracts with Foundry tools, deploy and call contracts, and use cheatcodes; use when a request involves contract test setup or testing patterns.
---

# Cairo Smart Contract Testing

## Overview
Explain common testing workflows for Starknet contracts, including deployment, dispatchers, and cheatcodes.

## Quick Use
- Read `references/smart-contract-testing.md` before answering.
- Use snforge standard library helpers for declare and deploy.
- Use dispatchers to call contract entry points in tests.

## Response Checklist
- Deploy test contracts and use their dispatchers for calls.
- Use cheatcodes to set caller, block info, or spoof events.
- Validate events and storage state after calls.

## Example Requests
- "How do I write a contract test with snforge?"
- "How do I call a contract from a test?"
- "What cheatcodes are available for Starknet tests?"
