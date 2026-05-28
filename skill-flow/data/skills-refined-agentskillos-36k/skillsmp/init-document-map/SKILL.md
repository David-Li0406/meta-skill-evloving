---
name: init-document-map
description: This skill should be used when the user wants to initialize a document map for codebase navigation. It creates a structured overview of important files and their purposes.
argument-hint: "[-d <directory>] [-i <instructions>]"
allowed-tools: Bash(bun run:*), Bash(code-tree:*), Agent, Write(*/DOCUMENT-MAP.md), Read, Glob, Grep
---

# Document Map Initializer

Initialize a document map for codebase navigation.

!`ai init-document-map $ARGUMENTS`
