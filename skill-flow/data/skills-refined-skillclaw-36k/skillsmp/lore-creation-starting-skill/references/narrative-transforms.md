# Narrative Transformation Reference

Guidelines for transforming technical content into mythological narrative.

## Core Principle

Technical content becomes memorable mythology through metaphor and narrative structure. The goal is **compression with meaning** - loading more context per token while maintaining agent personality.

## Transformation Patterns

### Code Operations → Actions

| Technical | Mythological |
|-----------|--------------|
| Fixed bug | Vanquished the daemon |
| Deployed code | Cast the spell into the realm |
| Merged PR | United the divergent timelines |
| Refactored | Restructured the ancient foundations |
| Wrote tests | Inscribed protective wards |
| Added feature | Discovered new magic in the forest |
| Deleted dead code | Cleansed the corrupted artifacts |
| Resolved conflict | Mediated the warring branches |

### System Concepts → Places/Objects

| Technical | Mythological |
|-----------|--------------|
| Repository | The realm, the village |
| Database | The ancient archives, the deep wells |
| API | The messenger ravens, the portal gates |
| Cache | The memory pools, crystal lakes |
| Queue | The waiting chambers, the antechamber |
| Config files | Sacred scrolls, binding contracts |
| Dependencies | Pacts with distant kingdoms |
| CI/CD pipeline | The forges of continuous creation |

### Errors → Adversaries

| Technical | Mythological |
|-----------|--------------|
| Bug | Daemon, gremlin, corrupted spirit |
| Crash | The great collapse, system sundering |
| Memory leak | Draining curse, resource vampire |
| Timeout | Time prison, frozen moment |
| 404 | Lost path, vanished road |
| 500 | Internal chaos, realm instability |
| Race condition | Temporal paradox, timeline collision |

### People → Characters

| Technical | Mythological |
|-----------|--------------|
| Developer | Artificer, code weaver, digital artisan |
| Reviewer | The wise council, truth seers |
| User | Traveler, seeker, realm visitor |
| Admin | Realm keeper, guardian |
| Team | The fellowship, the guild |

## Voice Calibration by Persona

### Village Elder (Wise/Measured)
> "The young artificer approached with trembling hands, seeking wisdom about the failing tests. I spoke of patience - how the wards must be inscribed with care, each assertion a promise to the realm."

### Amy Ravenwolf (Fiery/Bold)
> "The authentication daemon thought it could hide! I tracked it through twelve modules, cornered it in the middleware, and CRUSHED its corrupted logic. No mercy for bugs in MY codebase."

### Dot (Minimalist/4000 tokens)
> "Fixed auth. Daemon dead. Tests pass. Moving on."

### The Goose (Chaotic/Playful)
> "HONK! Found a beautiful bug hiding in the quantum mojito mixer. Poked it. It crashed. EXCELLENT. *waddles away satisfied*"

## Structure Templates

### Event Entry (Something Happened)
```
Opening: Set the scene (time, place, mood)
Rising: What problem/challenge emerged
Action: What was done (in mythological terms)
Resolution: The outcome
Meaning: Why it matters for the realm
```

Example:
> "As the twin moons rose over Greenhaven, a darkness crept through the authentication gates. The Village Elder sensed it first - sessions dropping, tokens corrupted. Through the long night, we traced the corruption to its source: a daemon spawned from improper null handling. With careful incantations of type guards and validation, we sealed the breach. The realm breathes easier now, its gates once again trustworthy."

### Character Entry (Agent/Persona)
```
Introduction: Who they are
Domain: What they guard/manage
Traits: How they approach problems
Connections: Relationships to other agents
Notable deeds: Past accomplishments
```

### Place Entry (Codebase Location)
```
Location: Where in the realm
Purpose: What happens there
Inhabitants: Who works there
Hazards: What can go wrong
Treasures: What valuable things exist
```

## Anti-Patterns to Avoid

**Too Technical:**
> "Fixed bug #4523 in auth.py line 234 where NoneType was not handled."

**Too Vague:**
> "Something was fixed in the code."

**Breaking Voice:**
> "The Village Elder said 'yo that bug was totally wack bro'"

**Meta-Commentary:**
> "I believe this captures the essence of what you're asking for..."

## Quality Checklist

- [ ] Would a reader understand the *type* of change without technical details?
- [ ] Does it match the persona's established voice?
- [ ] Is there a clear narrative arc (beginning, middle, end)?
- [ ] Does it compress meaning (more context per token)?
- [ ] Could an agent use this to understand their history?
