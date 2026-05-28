---
name: voice-apply
description: Use this skill when you need to transform content to match a specific voice profile, tone, or style.
---

# Voice Apply Skill

## Purpose

Transform content to match a specified voice profile. This skill loads voice profiles and applies their characteristics (tone, vocabulary, structure, perspective) to new or existing content.

## When This Skill Applies

- User asks to "write in X voice" or "use Y tone"
- User wants to "make this sound more [casual/formal/technical/etc.]"
- User provides content and asks to transform its style
- User references a voice profile by name
- User wants content to match a specific audience or context

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Write this in technical voice" | Apply technical-authority profile |
| "Make it more casual" | Apply casual-conversational or calibrate toward casual |
| "This needs to sound executive" | Apply executive-brief profile |
| "Explain like I'm a beginner" | Apply friendly-explainer profile |
| "Use the [profile-name] voice" | Load and apply named profile |
| "Transform this to match [example]" | Analyze example, apply derived voice |

## Voice Profile Locations

Skill checks these locations (in order):
1. Project: `.aiwg/voices/`
2. User: `~/.config/aiwg/voices/`
3. Built-in: `voice-framework/voices/templates/`

## Built-in Voice Profiles

| Profile | Description | Best For |
|---------|-------------|----------|
| `technical-authority` | Direct, precise, confident | Docs, architecture, engineering |
| `friendly-explainer` | Approachable, encouraging | Tutorials, onboarding, education |
| `executive-brief` | Concise, outcome-focused | Business cases, stakeholder comms |
| `casual-conversational` | Relaxed, personal | Blog posts, social, newsletters |

## Application Process

### 1. Load Voice Profile

```python
# Load from YAML
profile = load_voice_profile("technical-authority")
```

### 2. Analyze Source Content (if transforming)

- Current tone characteristics
- Vocabulary patterns
- Structure patterns
- Gap analysis vs target voice

### 3. Apply Voice Characteristics

**Tone Calibration**:
- Adjust formality level (word choice, contractions)
- Calibrate confidence (hedging vs assertion)
- Set warmth (clinical vs personable)
- Tune energy (measured vs enthusiastic)

**Vocabulary Transformation**:
- Replace words per user preferences
- Adjust phrases to align with the target voice