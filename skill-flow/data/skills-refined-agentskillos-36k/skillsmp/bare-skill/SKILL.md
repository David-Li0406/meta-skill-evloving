---
name: bare-skill
description: A skill from a bare directory with no manifest
---

# Bare Skill

FIXTURE_MARKER:BARE_SKILL

This skill demonstrates auto-wrapping of directories that have no `capability.toml` or `.claude-plugin/plugin.json`. OmniDev detects the `skills/` directory and automatically wraps it as a capability.

When you see this content, it means:
1. The directory was detected as wrappable
2. A capability.toml was auto-generated
3. The skill was synced successfully
