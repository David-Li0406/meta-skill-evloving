---
name: nav-profile
description: Use this skill when you want to manage user preferences and corrections for bilateral modeling, allowing the AI to adapt to your working style and preferences.
---

# Navigator Profile Skill

Manage user preferences for bilateral modeling, enabling Claude to understand and adapt to your working style, technical preferences, and past corrections.

## Why This Exists (Theory of Mind)

Based on Riedl & Weidmann 2025 research on Human-AI Synergy:
- Theory of Mind (ToM) is the key differentiator in human-AI collaboration success.
- Users with higher ToM achieve a 23-29% performance boost.
- **Bilateral modeling** completes the ToM loop: Claude models you, you model Claude.

This skill enables Claude to:
- Remember your preferences across sessions.
- Learn from corrections without you repeating them.
- Adapt communication style to your level.
- Build a persistent mental model of YOU.

## When to Invoke

**Auto-invoke when**:
- User says "save my preferences", "remember I like..."
- User says "update my profile", "change my preference for..."
- After detecting a correction pattern (auto-learn mode).
- User says "show my profile", "what do you know about me?"

**DO NOT invoke if**:
- User is creating a context marker (use nav-marker).
- User wants session-specific preferences only.
- User explicitly says "just for this session".

## Profile Location

`.agent/.user-profile.json` (git-ignored, session-persistent).

## Execution Steps

### Step 1: Determine Action

**SHOW** (viewing profile):
```
User: "Show my profile", "What do you remember about me?"
→ Display current profile.
```

**UPDATE** (explicit preference):
```
User: "Remember I prefer functional style", "Save that I like concise explanations."
→ Update specific preference.
```

**LEARN** (auto-detect correction):
```
[Internal trigger after correction detected]
→ Extract and save correction pattern.
```

**RESET** (clear profile):
```
User: "Reset my profile", "Clear my preferences."
→ Confirm and delete profile.
```

### Step 2: Load or Initialize Profile

**Check if profile exists**:
```bash
if [ -f ".agent/.user-profile.json" ]; then
  echo "Profile exists."
else
  echo "No profile found, will create new."
fi
```

**Initialize new profile** (if not exists):
```json
{
  "version": "1.0",
  "created": "{YYYY-MM-DD}",
  "last_updated": "{YYYY-MM-DD}",
  "preferences": {
    "communication": {}
  }
}
```