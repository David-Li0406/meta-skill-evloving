---
name: cairo-library-calls
description: Explain Starknet library calls that execute code from another class using class hash; use when a request involves library dispatchers, class hashes, or library_call_syscall.
---

# Cairo Library Calls

## Overview
Explain how to execute code from another class in the caller context using library calls.

## Quick Use
- Read `references/library-calls.md` before answering.
- Distinguish contract calls from library calls (context and storage).
- Use a LibraryDispatcher with a class hash when possible.

## Response Checklist
- Use library calls when you need to reuse logic without deploying another instance.
- Mention that library calls run in the caller's storage context.
- Use Serde for calldata and return data when using low-level syscalls.

## Example Requests
- "How do I call a class by hash from a contract?"
- "What is the difference between library_call and contract_call?"
- "How do I use library_call_syscall directly?"
