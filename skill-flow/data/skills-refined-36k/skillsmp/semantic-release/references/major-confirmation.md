**Skill**: [semantic-release](../SKILL.md)

# MAJOR Version Breaking Change Confirmation

## When This Applies

**Trigger**: When commits contain `BREAKING CHANGE:` footer or `feat!:` / `fix!:` prefix.

**Why extra confirmation**: MAJOR version bumps signal breaking changes that require consumers to update their code. False positives (accidental breaking change marker) or unnecessary breaking changes can fragment the user base.

---

## Phase 1: Detection (Automatic)

```bash
/usr/bin/env bash << 'MAJOR_CHECK_EOF'
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
MAJOR_COMMITS=$(git log "${LAST_TAG}..HEAD" --oneline | grep -E "(BREAKING CHANGE|^[a-f0-9]+ (feat|fix)!:)")
if [[ -n "$MAJOR_COMMITS" ]]; then
    echo "MAJOR_DETECTED"
    echo "$MAJOR_COMMITS"
fi
MAJOR_CHECK_EOF
```

---

## Phase 2: Multi-Perspective Analysis (Claude Task Subagents)

When MAJOR is detected, spawn **three parallel Task subagents** for independent analysis:

```
                      MAJOR Version Confirmation

+-----------+      -----------------   spawn 3 agents   +-------------+
| Migration | <-- | MAJOR Detected  | ----------------> | User Impact |
+-----------+      -----------------                    +-------------+
  |                 |                                     |
  |                 |                                     |
  |                 v                                     |
  |               +-----------------+                     |
  |               |   API Compat    |                     |
  |               +-----------------+                     |
  |                 |                                     |
  |                 |                                     |
  |                 v                                     |
  |               +-----------------+                     |
  +-------------> | Collect Results | <-------------------+
                  +-----------------+
                    |
                    |
                    v
                  #=================#
                  H AskUserQuestion H
                  #=================#
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "MAJOR Version Confirmation"; flow: south; }

[ MAJOR Detected ] { shape: rounded; }
[ User Impact ] -> [ Collect Results ]
[ API Compat ] -> [ Collect Results ]
[ Migration ] -> [ Collect Results ]
[ MAJOR Detected ] -- spawn 3 agents --> [ User Impact ]
[ MAJOR Detected ] --> [ API Compat ]
[ MAJOR Detected ] --> [ Migration ]
[ Collect Results ] -> [ AskUserQuestion ] { border: double; }
```

</details>

### Task Subagent Prompts (spawn in parallel)

1. **User Impact Analyst** (`subagent_type: "Explore"`):
   ```
   Analyze the breaking changes in commits since last tag. Identify:
   - Which user personas are affected (library consumers, CLI users, API clients)
   - Approximate usage scope (core feature vs edge case)
   - Available workarounds before upgrading
   Return a 2-3 sentence impact assessment.
   ```

2. **API Compatibility Analyst** (`subagent_type: "Explore"`):
   ```
   Review the breaking changes for API compatibility:
   - What specific signatures, behaviors, or contracts are changing
   - Whether the change could be made backwards-compatible with feature flags
   - If deprecation warnings could have preceded this break
   Return a 2-3 sentence compatibility assessment.
   ```

3. **Migration Strategist** (`subagent_type: "Explore"`):
   ```
   Assess the migration path for this breaking change:
   - Effort level for consumers to update (trivial/moderate/significant)
   - Whether a migration guide is needed in release notes
   - Suggested deprecation timeline if change could be phased
   Return a 2-3 sentence migration assessment.
   ```

---

## Phase 3: User Confirmation (AskUserQuestion with multiSelect)

After collecting subagent analyses, present consolidated findings:

```yaml
AskUserQuestion:
  questions:
    - question: "MAJOR version bump (X.0.0) detected. How should we proceed?"
      header: "Breaking"
      multiSelect: false
      options:
        - label: "Proceed with MAJOR (Recommended)"
          description: "Release as X.0.0 - breaking change is intentional and necessary"
        - label: "Downgrade to MINOR"
          description: "Amend commits to remove BREAKING CHANGE - change can be backwards-compatible"
        - label: "Abort release"
          description: "Review commits before releasing - need to reconsider approach"
    - question: "Which mitigations should be included in release notes?"
      header: "Mitigations"
      multiSelect: true
      options:
        - label: "Migration guide"
          description: "Step-by-step instructions for updating consumer code"
        - label: "Deprecation notice"
          description: "Warning that old behavior will be removed in future version"
        - label: "Compatibility shim"
          description: "Temporary backwards-compat layer with deprecation warning"
```

---

## Decision Tree

```
                           MAJOR Release Decision Tree

 ---------------------   NO       -------------------
| Proceed MINOR/PATCH | <------- |  MAJOR detected?  |
 ---------------------            -------------------
                                   |
                                   | YES
                                   v
                                 +-------------------+
                                 | Spawn 3 Subagents |
                                 +-------------------+
                                   |
                                   |
                                   v
 ---------------------   abort   +-------------------+  proceed    ---------------
|    Abort Release    | <------- |  AskUserQuestion  | ---------> | Proceed MAJOR |
 ---------------------           +-------------------+             ---------------
                                   |
                                   | downgrade
                                   v
                                 +-------------------+
                                 |  Downgrade MINOR  |
                                 +-------------------+
                                   |
                                   |
                                   v
                                 +-------------------+
                                 |   Amend Commits   |
                                 +-------------------+
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "MAJOR Release Decision Tree"; flow: south; }

[ MAJOR detected? ] { shape: rounded; }
[ Proceed MINOR/PATCH ] { shape: rounded; }
[ Spawn 3 Subagents ]
[ AskUserQuestion ]
[ Proceed MAJOR ] { shape: rounded; }
[ Downgrade MINOR ]
[ Abort Release ] { shape: rounded; }
[ Amend Commits ]

[ MAJOR detected? ] -- NO --> [ Proceed MINOR/PATCH ]
[ MAJOR detected? ] -- YES --> [ Spawn 3 Subagents ]
[ Spawn 3 Subagents ] -> [ AskUserQuestion ]
[ AskUserQuestion ] -- proceed --> [ Proceed MAJOR ]
[ AskUserQuestion ] -- downgrade --> [ Downgrade MINOR ]
[ AskUserQuestion ] -- abort --> [ Abort Release ]
[ Downgrade MINOR ] -> [ Amend Commits ]
```

</details>

---

## Example Output

```
╔══════════════════════════════════════════════════════════════════╗
║  🔴 MAJOR VERSION BUMP DETECTED                                   ║
╠══════════════════════════════════════════════════════════════════╣
║  Commits triggering MAJOR:                                        ║
║  • a1b2c3d feat!: change API to require authentication           ║
║  • e4f5g6h fix!: rename config option from 'timeout' to 'ttl'    ║
╠══════════════════════════════════════════════════════════════════╣
║  📊 MULTI-PERSPECTIVE ANALYSIS                                    ║
╠──────────────────────────────────────────────────────────────────╣
║  👥 User Impact: All API consumers affected. Core authentication ║
║     flow changes. No workaround - update required.               ║
║                                                                   ║
║  🔌 API Compat: Authorization header now mandatory. Could add    ║
║     optional fallback with deprecation warning for 1-2 releases. ║
║                                                                   ║
║  📋 Migration: Moderate effort - add API key to all calls.       ║
║     Migration guide recommended. 2-week notice suggested.        ║
╠══════════════════════════════════════════════════════════════════╣
║  Current: v2.4.1 → Proposed: v3.0.0                              ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Configuration

To skip MAJOR confirmation (not recommended):

```yaml
# .releaserc.yml
# WARNING: Disables safety check - use only for automated pipelines
skipMajorConfirmation: true
```

**Default**: MAJOR confirmation is ENABLED. This skill will always prompt for breaking changes unless explicitly disabled.
