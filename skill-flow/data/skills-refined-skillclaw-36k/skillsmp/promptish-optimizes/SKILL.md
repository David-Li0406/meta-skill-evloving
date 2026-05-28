---
name: promptish-optimizes
description: analyzes and optimizes prompts/agents using best practices
argument-hint: <file-path|agent-name> [reference-url]
allowed-tools: Read, Grep, Glob, WebFetch
context: fork
agent: swe-master-prompter
---

# /promptish-optimizes

Analyze and optimize the target specified in `$ARGUMENTS`.

Arguments format: `<target> [reference-url]`

- target: File path or agent name to analyze
- reference-url (optional): URL to fetch best practices from

If a reference URL is provided, fetch it and use those guidelines for the analysis.
