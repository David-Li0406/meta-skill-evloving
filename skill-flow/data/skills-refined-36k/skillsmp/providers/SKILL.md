---
name: providers
description: Use when integrating multiple LLM providers. Keep provider-specific code isolated behind a small interface.
---

## Guidelines

- Use an adapter/interface per provider.
- Normalize request/response shapes at the boundary.
- Keep secrets out of repo; use environment variables.
