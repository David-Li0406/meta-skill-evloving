---
name: profile
description: Generate full NPC profiles from character YAML and save JSON to sentinel-agent/generated_npcs. Native (no external agent call).
allowed-tools: Read, Glob, Write
user-invocable: true
proactive: false
---

# NPC Profile Generation (Native)

Generate full NPC profiles for SENTINEL using local context. Read character appearance from YAML and generate complete profiles with agenda, disposition modifiers, memory triggers, sample dialogue, secrets, and hooks. Save as JSON.

## Usage

```
/profile <character_name>
/profile cipher
/profile elder_kara
/profile vex --context "He's been promoted recently"
```

## How It Works

1. Read the character YAML from `assets/characters/{name}.yaml` or `assets/characters/{name}_detailed.yaml`.
2. Build a physical description string from the YAML fields.
3. Add faction context and role guidance.
4. Generate the profile JSON directly (no external agent calls).
5. Save to `sentinel-agent/generated_npcs/{name}.json`.
6. Report success with key details.

## Step 1: Find and Read Character YAML

Look for the character file:

```
C:\dev\SENTINEL\assets\characters\{name}.yaml
C:\dev\SENTINEL\assets\characters\{name}_detailed.yaml
```

If not found, ask the user for basic details (name, faction, role, and a short physical description) and proceed.

## Step 2: Build Physical Description

From the YAML, build an explicit physical description string.

### Person Descriptor Mapping

| Skin Tone | Gender: Masculine | Gender: Feminine | Gender: Androgynous |
|-----------|-------------------|------------------|---------------------|
| pale | pale-skinned man | pale-skinned woman | pale-skinned person |
| light | light-skinned man | light-skinned woman | light-skinned person |
| medium | olive-skinned man | olive-skinned woman | olive-skinned person |
| tan | tan man | tan woman | tan person |
| brown | Black man | Black woman | Black person |
| dark | dark-skinned Black man | dark-skinned Black woman | dark-skinned Black person |

For elderly characters, prepend "elderly" (e.g., "elderly olive-skinned woman").

### Build Order

1. Person descriptor with build (e.g., "Black man with lean build").
2. Hair description (length, style, color).
3. Eye description (color or "cybernetic eyes").
4. Facial features (comma-separated).
5. Distinguishing marks (scars, augmentations, tattoos, other).

## Step 3: Faction Context

| Faction | Tagline | Values | Culture | Speech |
|---------|---------|--------|---------|--------|
| nexus | The network that watches | information, prediction, control | Analytical, data-driven | Precise, clinical, uses statistics |
| ember_colonies | We survived. We endure. | community, survival, mutual aid | Tight-knit survivors | Direct, warm to friends, guarded |
| lattice | We keep the lights on | infrastructure, pragmatic cooperation | Engineers maintaining systems | Technical, problem-focused |
| convergence | Become what you were meant to be | enhancement, transcendence | Transhumanists | Enthusiastic about potential |
| covenant | We hold the line | oaths, sanctuary, ethical limits | Keepers of moral boundaries | Formal, principled |
| wanderers | The road remembers | freedom, trade, neutrality | Nomadic traders | Casual, storytelling |
| cultivators | From the soil, we rise | growth, patience, sustainability | Agrarian communities | Patient, agricultural metaphors |
| steel_syndicate | Everything has a price | profit, leverage, deals | Criminal-adjacent traders | Transactional, direct about costs |
| witnesses | We remember so you don't have to lie | truth, records, accountability | Archivists | Precise, cites sources |
| architects | We built this world | legacy, credentials, legitimacy | Remnants of old order | Formal, references procedures |
| ghost_networks | We were never here | anonymity, escape, protection | Underground railroad | Cautious, uses code words |

## Step 4: Role Suggestions

| Role | Description |
|------|-------------|
| leader | Commands respect, burden of responsibility |
| fixer | Solves problems, knows people, transactional |
| elder | Wisdom from experience |
| scout | Eyes and ears, often underestimated |
| enforcer | Applies pressure, reputation for action |
| medic | Healer, pragmatic about triage |
| technician | Comfortable with machines |
| trader | Deals in goods or information |
| refugee | Displaced, seeking safety |
| true_believer | Deeply committed to faction ideology |
| skeptic | Questions their own faction |
| veteran | Survived things, carries weight |

## Step 5: Output Format

Generate a complete NPC profile as JSON with this exact structure:

```
{
  "name": "{name}",
  "faction": "{faction_id}",
  "role": "{role}",
  "physical_appearance": "{physical_description}",
  "description": "2-3 sentence presence/demeanor description (NOT physical)",
  "agenda": {
    "wants": "Primary goal (specific, personal)",
    "fears": "What they're afraid of (specific)",
    "leverage": "What they could hold over the player (or null)",
    "owes": "What they might owe the player (or null)",
    "lie_to_self": "The self-deception that lets them sleep at night"
  },
  "disposition_modifiers": {
    "hostile": {
      "tone": "How they speak when hostile",
      "reveals": ["What they share at this level"],
      "withholds": ["What they hide"],
      "tells": ["Behavioral cues"]
    },
    "wary": { ... },
    "neutral": { ... },
    "warm": { ... },
    "loyal": { ... }
  },
  "memory_triggers": [
    {
      "condition": "tag like 'helped_ember'",
      "effect": "What happens",
      "disposition_shift": -2 to +2
    }
  ],
  "sample_dialogue": {
    "greeting_neutral": "...",
    "greeting_warm": "...",
    "refusal": "...",
    "bargaining": "...",
    "under_pressure": "..."
  },
  "secrets": ["Things the GM knows but player must discover"],
  "hooks": ["Plot hooks involving this NPC"]
}
```

## Guidelines

- Make the NPC feel like a real person with contradictions.
- The "lie_to_self" is crucial.
- Disposition modifiers should show meaningful progression.
- Memory triggers should reference realistic player actions.
- Secrets should create interesting dramatic irony.
- Hooks should tie into faction politics and player choice.
- Output only valid JSON when generating the file.

## Step 6: Save and Report

Save to `C:\dev\SENTINEL\sentinel-agent\generated_npcs\{name}.json`.

Report to the user:
- Name and faction
- Brief description
- Key agenda items (wants, fears)
- One sample dialogue line
- File path

Suggest running `/portrait {name}` to generate a matching portrait.

## Error Handling

- YAML not found: Ask for name, faction, role, and a short physical description.
- Missing fields: Fill with sensible defaults and warn the user.
- Invalid JSON: Fix and re-save.
