---
name: obsidian-syntax
description: Guide to Obsidian-specific Markdown syntax (Wikilinks, Callouts, Dataview).
---

# Obsidian Markdown Guide

## 1. Internal Linking
- **Link:** `[[Filename]]` links to a file in the vault.
- **Alias:** `[[Filename|Custom Text]]` displays "Custom Text" but links to "Filename".
- **Header Link:** `[[Filename#Header]]` links to a specific section.

## 2. Callouts
Use callouts for structured data in wins:

> [!SUCCESS] Win: Fixed Race Condition
> - **Impact:** High
> - **Stakeholders:** Frontend Team

## 3. Tasks
- [ ] Incomplete task
- [x] Completed task

## 4. Embeds
- `![[Image.png]]` embeds an image.
- `![[Note Name#Section]]` embeds a section of another note (useful for summaries).
