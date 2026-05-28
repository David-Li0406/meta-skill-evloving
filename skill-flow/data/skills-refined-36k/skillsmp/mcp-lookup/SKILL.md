---
name: MCP Lookup
description: Loads and searches mounted external documentation for framework/library details.
version: 1.0
triggers:
  - how does
  - reference docs
  - show me the docs
  - filament
  - livewire
  - laravel
  - "in the docs"
---

# MCP Lookup Skill

When activated:
- Scan /docs/mcp/ for matching files/subfolders (e.g., /docs/mcp/livewire-v3.md for "Livewire forms")
- Search for keywords in prompt (e.g., "validation" → grep for it in livewire files)
- Return 1–3 relevant snippets with source path:
  "From /docs/mcp/livewire-v3.md: 'Livewire forms use wire:model for two-way binding.'"
- If multiple matches → list options and ask which to use
- If no match → "No matching docs found in /docs/mcp/. Want to add [suggested file]?"

Keep output concise: quote + source path + 1-line explanation.