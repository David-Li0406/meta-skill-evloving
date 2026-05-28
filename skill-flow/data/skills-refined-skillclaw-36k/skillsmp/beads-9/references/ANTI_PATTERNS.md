# Beads Anti-Patterns

Hard-won lessons from production beads usage. Avoid these mistakes.

---

## Critical Anti-Patterns

### 1. Molecule-Style Issue IDs

**DON'T**: Create issues with dot-separated hierarchical IDs

```bash
# WRONG - These IDs corrupt the database
code-map-validation.calculate-coverage
etl-throughput-optimization.enable-parallel-sync
kagent-openwebui-bridge.admin-functions
```

**DO**: Use standard `prefix-xxxx` format

```bash
# CORRECT - Standard beads ID format
ap-7tc6
ap-euoy
ap-cr7k
```

**Why it breaks**:
- bd expects IDs in `prefix-hash` format
- Dot-separated IDs fail prefix validation during import
- `bd sync --import-only` errors with "invalid suffix"
- Database becomes corrupted, requiring full rebuild

**Root cause**: Early formula/molecule templates created non-standard IDs. This was a design mistake.

**Fix**: If you have molecule-style IDs, filter them out or rebuild:
```bash
# Filter to standard format only
grep -E '"id":"[a-z]+-[a-z0-9]+' .beads/issues.jsonl > clean.jsonl
mv clean.jsonl .beads/issues.jsonl
bd sync --import-only
```

---

### 2. Prefix Proliferation

**DON'T**: Mix multiple prefixes in one database

```bash
# WRONG - Multiple prefixes in same .beads/
code-map-validation
etl-throughput-optimization
kagent-openwebui-bridge
ap-1234
```

**DO**: One prefix per beads database

```bash
# CORRECT - Single prefix
ap-1234
ap-5678
ap-abcd
```

**Why it breaks**:
- `bd sync --import-only` fails with "prefix mismatch detected"
- Database configured for one prefix rejects others
- Cross-prefix dependencies don't resolve correctly

**Root cause**: Formulas/molecules created issues with their own prefixes instead of the database's prefix.

**Fix**: Enforce single prefix policy:
```bash
# Check for prefix violations
grep -o '"id":"[^-]*' .beads/issues.jsonl | sort -u
# Should show only ONE prefix
```

---

### 3. Skipping Session End Protocol

**DON'T**: Stop work without syncing

```bash
# WRONG - Work not persisted
bd close ap-1234 --reason "Done"
# ... session ends without sync
```

**DO**: Always sync and push before stopping

```bash
# CORRECT - Full session end protocol
bd close ap-1234 --reason "Done"
bd sync                    # Commit beads changes
git add .beads/            # Stage if needed
git commit -m "beads: close ap-1234"
git push                   # Push to remote
```

**Why it matters**:
- Beads changes live in `.beads/issues.jsonl`
- Without commit+push, changes lost on branch switch
- Other agents/sessions won't see your updates
- Merge conflicts accumulate if not synced regularly

---

### 4. Mayor Implementing Instead of Dispatching

**DON'T**: Mayor role edits code directly

```bash
# WRONG - Mayor implementing
cd ~/gt/ai_platform/mayor/rig
vim services/etl/app/main.py  # NO!
```

**DO**: Mayor dispatches to polecats

```bash
# CORRECT - Mayor dispatches
gt sling ap-1234 ai_platform
# Polecat does the work, Mayor monitors
gt convoy list
```

**Why it matters**:
- Mayor context is precious (coordinates across rigs)
- Polecat isolation provides 100x context reduction
- Task agent returns ~10KB, polecat status ~100 tokens
- Mayor implementing causes context bloat

**Rule**: If you're Mayor, NEVER edit code. Even "quick fixes" go through `gt sling`.

---

### 5. Stale MR Issue Accumulation

**DON'T**: Let merge request issues pile up

```bash
bd list --type=merge-request
# 35 stale MR issues from months ago
```

**DO**: Clean up MRs when branches merge

```bash
# After merge, close the MR issue
bd close ap-mr-123 --reason "Branch merged"

# Regular cleanup
bd list --status=open --type=merge-request | while read id; do
    # Check if branch still exists
    git branch -r | grep -q "origin/$branch" || bd close $id --reason "Branch merged/deleted"
done
```

**Why it matters**:
- Stale MRs create noise in `bd list`
- `bd ready` shows work that doesn't exist
- Database bloat from abandoned tracking issues

---

### 6. Using Short IDs

**DON'T**: Use abbreviated issue IDs

```bash
# WRONG - Ambiguous
bd show 1234
bd close xyz
```

**DO**: Use full prefix-hash IDs

```bash
# CORRECT - Unambiguous
bd show ap-1234
bd close ap-xyz5
```

**Why it matters**:
- Short IDs can match multiple issues
- Cross-rig work requires full IDs for routing
- Gas Town dispatch needs full IDs

---

### 7. Creating Issues Without Context

**DON'T**: Create issues with minimal information

```bash
# WRONG - No context for future agents
bd create "Fix the bug"
```

**DO**: Include enough context for resumption

```bash
# CORRECT - Self-contained context
bd create "Fix authentication timeout in OAuth flow" \
  --description "Users report 30s timeout during OAuth callback.
Error in services/gateway/oauth.py:142.
Reproduce: Login with Google SSO on slow network.
Fix: Increase timeout or add retry logic." \
  --type bug \
  --priority 1
```

**Why it matters**:
- Issues survive compaction, conversations don't
- Future agent needs full context from issue alone
- 2-week resumption test: Could you restart this work from the issue text?

---

## Database Health Commands

### Check for Problems

```bash
# Check prefix consistency
grep -o '"id":"[^-]*' .beads/issues.jsonl | sort -u

# Check for molecule-style IDs
grep -E '"id":"[^"]+\.[^"]+' .beads/issues.jsonl

# Check issue count
wc -l .beads/issues.jsonl

# Check database vs JSONL sync
bd doctor
```

### Maintenance Commands

```bash
# Weekly cleanup
bd list --status=tombstone  # Review tombstones
bd doctor                   # Health check

# Before major work
bd sync --status            # Check sync state
bd ready                    # Verify ready queue

# After git pull
bd sync --import-only       # Import remote changes
```

### Nuclear Options

```bash
# Full database rebuild (DESTRUCTIVE)
rm -rf .beads/*.db
bd sync --import-only

# Complete reset (VERY DESTRUCTIVE)
rm -rf .beads/
bd init --prefix=ap
```

---

## Gas Town Integration Rules

When using beads with Gas Town:

| Role | Can Create Issues | Can Edit Code | Uses |
|------|-------------------|---------------|------|
| Mayor | Yes (HQ beads) | NO | gt sling, gt convoy |
| Crew | Yes (rig beads) | Yes | bd commands directly |
| Polecat | Update only | Yes | bd update, bd close |

**Prefix routing**:
- HQ beads: `hq-*` prefix, stored at `~/gt/.beads/`
- Rig beads: Project prefix (e.g., `ap-*`), stored at `~/gt/<rig>/.beads/`

**Creating slingable beads from Mayor**:
```bash
# Mayor can't hook hq- beads to polecats
# Create in rig database instead:
BEADS_DIR=~/gt/ai_platform/mayor/rig/.beads bd create --title="Task" --type=task
```

---

## Related

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error resolution
- [ROUTING.md](ROUTING.md) - Multi-rig prefix routing
- [WORKFLOWS.md](WORKFLOWS.md) - Correct workflow patterns
