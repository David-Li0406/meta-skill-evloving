---
name: doggo
description: DNS command-line client
---

# Doggo DNS lookup

## When to use this skill

Use this skill whenever the user asks for a DNS lookup.

## Install

- If the `doggo` tool is already in the user's PATH, don't install it.
- If the tool is already available via `go tool doggo`, don't install it.
- Otherwise, if needed, install doggo via `go install github.com/mr-karan/doggo/cmd/doggo@latest`

## DNS lookup

```bash
doggo example.com  # or whatever query
```
