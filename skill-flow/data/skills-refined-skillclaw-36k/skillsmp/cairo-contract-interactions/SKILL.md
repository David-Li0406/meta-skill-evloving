---
name: cairo-contract-interactions
description: Explain how to call another Starknet contract using dispatcher patterns and interfaces; use when a request involves cross-contract calls, dispatchers, or contract_call_syscall.
---

# Cairo Contract Interactions

## Overview
Guide contract to contract calls using interfaces, dispatchers, and low-level syscalls.

## Quick Use
- Read `references/contract-interactions.md` before answering.
- Prefer generated dispatchers over raw syscalls.
- Mention safe dispatchers for error handling.

## Response Checklist
- Define an interface trait for the target contract.
- Use a ContractDispatcher with a contract address.
- Use SafeDispatcher when return errors must be handled explicitly.
- Use contract_call_syscall only for low-level control.

## Example Requests
- "How do I call another contract from Cairo?"
- "What is the difference between safe and unsafe dispatchers?"
- "How do I use contract_call_syscall directly?"
