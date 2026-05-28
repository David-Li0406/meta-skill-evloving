# Bracket System Deep Dive

The bracket system prevents version thrashing by freezing at scope level until commit.

## Core Principle

**Version freezes at its bracket level until commit. Can only jump to higher bracket if scope demands it. After commit, reset for next cycle.**

## Three Brackets Explained

### PATCH Bracket (Z)

**When active:** Working on bug fixes, documentation, wording improvements, or other patch-level changes.

**What you can do:**
- Fix bugs in code
- Update documentation
- Correct typos and wording
- Improve performance (no API change)
- No new features

**Version pattern:** X.Y.Z where Z increments (1.0.0 → 1.0.1 → 1.0.2)

**Frozen behavior:** If in patch bracket and discover you need new features or breaking changes, jump to MINOR or MAJOR respectively.

### MINOR Bracket (Y)

**When active:** Working on new features or capabilities that are backward compatible.

**What you can do:**
- Add new commands/features
- Expand tool access
- Add new capabilities
- Add new reference materials
- No breaking changes
- Patch fixes can still be applied

**Version pattern:** X.Y.Z where Y increments and Z resets (1.0.5 → 1.1.0)

**Frozen behavior:** If in minor bracket and discover breaking changes needed, jump to MAJOR. If discovering only patch work, stay in minor (don't drop back).

### MAJOR Bracket (X)

**When active:** Working on breaking changes, incompatible API changes, or structural changes.

**What you can do:**
- Remove or rename commands
- Change API behavior incompatibly
- Change output formats
- Change configuration structures
- Requires migration guide
- Any patch or minor fixes can still be applied

**Version pattern:** X.Y.Z where X increments and Y, Z reset (1.5.2 → 2.0.0)

**Frozen behavior:** Once in major bracket, stay frozen. Don't bump further even if more work discovered. All changes accumulate under the same major version bump.

## State Transitions

### Starting Fresh After Last Commit

Version is currently at last committed state. Starting new work:

```
Last commit: 1.0.1
↓
Assess new scope → Patch? → Bump to 1.0.2 (patch frozen)
                → Minor? → Bump to 1.1.0 (minor frozen)
                → Major? → Bump to 2.0.0 (major frozen)
```

### Scope Creep: Discovering Higher Bracket

You're in a bracket and discover work beyond that scope:

```
Current: 1.0.2 (patch frozen)
Discover: "New feature needed"
Action: Jump to 1.1.0 (minor frozen) — Z resets to 0

Current: 1.1.0 (minor frozen)
Discover: "This breaks existing API"
Action: Jump to 2.0.0 (major frozen) — Y and Z reset to 0

Current: 2.0.0 (major frozen)
Discover: "More work needed"
Action: Stay at 2.0.0 — Don't bump further
```

### Staying in Bracket

If all work discovered fits within current bracket:

```
Current: 1.0.2 (patch frozen)
Discover: "Another bug to fix"
Action: Stay at 1.0.2 — Don't bump yet

Discover: "Another doc typo"
Action: Still stay at 1.0.2

Commit when done: 1.0.2 includes all patch-level work
```

### Multiple Discoveries in One Cycle

It's normal to discover work across brackets:

```
Last commit: 1.2.0

Work discovered:
1. Bug fix (patch)         → Bump to 1.2.1
2. New feature (minor)     → Jump to 1.3.0
3. Breaking change (major) → Jump to 2.0.0

Final state: 2.0.0
All changes documented in one CHANGELOG entry for 2.0.0
Commit records transition from 1.2.0 → 2.0.0
```

## Why Bracket System Matters

**Problem without brackets:**
- Version bump to 1.0.1 for a fix
- Discover new feature needed
- Version bump to 1.1.0
- Discover breaking change
- Version bump to 2.0.0
- Find another bug
- Version bump to 2.0.1
- Result: 5 version bumps for loosely related work = confusing history

**Solution with brackets:**
- Start patch work → bump to 1.0.1 (frozen)
- Discover feature → jump to 1.1.0 (frozen)
- Discover breaking change → jump to 2.0.0 (frozen)
- Find another bug → stay at 2.0.0 (frozen, don't bump)
- Commit once: 2.0.0 captures all work in single version
- Result: Clean history, clear scope, no thrashing

## Multi-Component Behavior

In projects with multiple components, each component has its own bracket:

```
Plugin: 1.2.0 (no active work)
Skill-A: 1.0.0 (no active work)
Skill-B: 1.0.0 (no active work)

Start work:
- Plugin: Discover bug fix → bump to 1.2.1 (patch frozen)
- Skill-A: Discover new feature → bump to 1.1.0 (minor frozen)
- Skill-B: No work yet → stays at 1.0.0

Skill-B later: Discover bug fix → bump to 1.0.1 (patch frozen)

At commit time:
- Plugin: 1.2.1
- Skill-A: 1.1.0
- Skill-B: 1.0.1
- Parent version: ≥ 1.1.0 (bump to 1.3.0 if it was 1.2.1)

Result: Only the components that changed got version bumps
```

## Frozen Concept

"Frozen" means the version doesn't change again until commit, even if more work is discovered **within the same bracket**:

```
Patch frozen at 1.0.2:
- Fix bug #1        → Stay at 1.0.2
- Fix bug #2        → Stay at 1.0.2
- Fix bug #3        → Stay at 1.0.2
Commit: 1.0.2 with all 3 fixes in changelog

But if you discover major work:
- Fix bug #1        → 1.0.2 (patch frozen)
- Fix bug #2        → 1.0.2 (patch frozen)
- Discover breaking API change → 2.0.0 (jump to major, no longer frozen)
- Discover bug #3   → Stay at 2.0.0
- Discover feature → Stay at 2.0.0
Commit: 2.0.0 with bugs + feature + breaking change in changelog
```

## Decision Tree

When work is discovered:

```
Is this work at current bracket level?
├─ YES → Stay frozen, don't bump
└─ NO (higher bracket needed)
   ├─ At PATCH, need MINOR? → Jump to MINOR (Y++, Z=0)
   ├─ At PATCH, need MAJOR? → Jump to MAJOR (X++, Y=0, Z=0)
   ├─ At MINOR, need MAJOR? → Jump to MAJOR (X++, Y=0, Z=0)
   └─ At MAJOR, need anything? → Stay frozen (X same)
```

## Examples from Real Projects

### Example 1: Typical Patch Release

```
Last commit: 2.1.0
Work discovered:
- Fixed typo in README
- Fixed timeout in API calls
- Updated documentation

Scope: All patch-level
Process: 2.1.0 → 2.1.1 (bump Z)
Changelog:
  - Fix timeout in API calls
  - Fix typo in README
  - Update API documentation
```

### Example 2: Scope Creep Across Brackets

```
Last commit: 1.2.3
Work discovered in sequence:
1. Found performance issue → 1.2.4 (patch frozen)
2. Need new export format → 1.3.0 (minor frozen)
3. Export format incompatible with old API → 2.0.0 (major frozen)
4. Found another bug → 2.0.0 (major, frozen, no bump)

Final commit: 2.0.0
Changelog documents:
- Fixed performance issue
- Added new export formats
- **BREAKING**: Export format no longer compatible with API v1
- Fixed additional bug
- Migration guide provided
```

### Example 3: Multi-Component Plugin Release

```
Last commits:
- Plugin: 1.5.0
- Skill-A: 1.2.0
- Skill-B: 1.1.0

Work discovered:
- Skill-A: Bug fix → 1.2.1 (patch)
- Skill-B: New feature → 1.2.0 (minor, was 1.1.0)
- Plugin: Coordinate with skills → 1.6.0 (minor, to match skill-b's capability)

Final state:
- Plugin: 1.6.0
- Skill-A: 1.2.1
- Skill-B: 1.2.0

Changelog:
## [1.6.0] - 2026-01-21
### Added (Skill-B)
- New processing capability
### Fixed (Skill-A)
- Fixed timeout in request handling
```
