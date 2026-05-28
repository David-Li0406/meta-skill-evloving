---
name: retry-ollama-call
description: Retry pattern with exponential backoff for Ollama LLM failures. Wraps any command execution to ensure reliability.
---

# Retry Ollama Call

## Overview

This skill provides a wrapper script to retry commands that fail. It is specifically designed to handle transient failures in LLM calls (e.g., Ollama/network timeouts) using exponential backoff.

## Usage

### Retry Script

**Syntax:**

```bash
python3 .agent/skills/retry-ollama-call/scripts/retry_call.py <command> [args...]
```

**Example:**

```bash
# Retry a python script
python3 .agent/skills/retry-ollama-call/scripts/retry_call.py python3 my_script.py arg1

# Retry a curl command
python3 .agent/skills/retry-ollama-call/scripts/retry_call.py curl http://localhost:11434/api/tags
```
