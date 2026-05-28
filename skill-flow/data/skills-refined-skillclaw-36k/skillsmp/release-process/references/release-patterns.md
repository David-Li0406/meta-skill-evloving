# Common Release Patterns

Real-world scenarios for bracket-based versioning.

## Pattern 1: Patch Release (Bug Fix + Docs)

**Scenario:** Small fix plus documentation cleanup.

```
Current: 1.2.3 → New: 1.2.4
Changes: Fix bug, update docs
Type: Patch (Z only)

CHANGELOG:
## [1.2.4] - 2026-01-21
### Fixed
- Fix timeout in database queries
- Fix typo in README
```

---

## Pattern 2: Feature Release (New Capability)

**Scenario:** New user-facing feature, backward compatible.

```
Current: 1.2.3 → New: 1.3.0
Changes: New encryption support
Type: Minor (Y+1, Z→0)

CHANGELOG:
## [1.3.0] - 2026-01-22
### Added
- Support for encrypted documents
```

---

## Pattern 3: Breaking Release (API Change)

**Scenario:** Incompatible change requiring user migration.

```
Current: 1.5.2 → New: 2.0.0
Changes: Rename command (breaking)
Type: Major (X+1, Y→0, Z→0)

CHANGELOG:
## [2.0.0] - 2026-01-23
### Changed
- **BREAKING**: Renamed 'validate' to 'verify'
### Removed
- Old 'validate' command (use 'verify')
```

---

## Pattern 4: Scope Creep (Multiple Jumps)

**Scenario:** Discovering work of different types during release planning.

```
Discoveries:
1. Bug fix detected → 1.2.1 (patch frozen)
2. Need new feature → 1.3.0 (jump to minor)
3. Need breaking change → 2.0.0 (jump to major)
4. Find another bug → 2.0.0 (stay major)

Final: 2.0.0 with all changes documented
```

**Key insight:** Once you jump to a higher bracket, you can only stay at that level or jump higher. You never descend. This prevents version chaos when scope expands.

See `bracket-system.md` for detailed state transitions and edge cases.
