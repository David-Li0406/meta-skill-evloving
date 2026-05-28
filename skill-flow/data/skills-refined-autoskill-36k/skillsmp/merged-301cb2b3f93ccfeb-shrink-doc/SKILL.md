---
name: shrink-doc
description: Compress documentation while preserving execution equivalence using a validation-driven approach.
---

# Validation-Driven Document Compression

**Task**: Compress the documentation file: `{{arg}}`

**Goal**: Reduce document size while preserving execution equivalence using objective validation instead of prescriptive rules.

---

## Workflow

### Step 1: Validate Document Type

**BEFORE compression**, verify this is a Claude-facing document:

**ALLOWED** (Claude-facing):
- `.claude/` configuration files:
  - `.claude/agents/` - Agent definitions (prompts for sub-agents)
  - `.claude/commands/` - **Slash commands** (prompts that expand when invoked)
  - `.claude/hooks/` - Hook scripts (execute on events)
  - `.claude/settings.json` - Claude Code settings
- `CLAUDE.md` and project instructions
- `docs/project/` development protocol documentation
- `docs/code-style/*-claude.md` style detection patterns

**FORBIDDEN** (Human-facing):
- `README.md`, `changelog.md`, `CHANGELOG.md`
- `docs/studies/`, `docs/decisions/`, `docs/performance/`
- `docs/optional-modules/` (potentially user-facing)
- `todo.md`, `docs/code-style/*-human.md`

**⚠️ SPECIAL HANDLING: CLAUDE.md**

When compressing `CLAUDE.md`, use **content reorganization** instead of standard compression:

**Step 1: Analyze Content Location**
Before compressing, categorize ALL content into:

| Category | Action |
|----------|--------|
| **Duplicates skills** | REMOVE - reference skill instead |
| **Main-agent-specific** | MOVE to main-agent-specific file |
| **Sub-agent-specific** | MOVE to sub-agent-specific file |
| **Universal (all agents)** | KEEP in CLAUDE.md |

**Step 2: Check for Duplication**
```bash
# Check if content already exists in skills
ls .claude/skills/

# Check if procedural content duplicates a skill
grep -l "pattern" .claude/skills/*/SKILL.md
```

**Step 3: Content Categories**

*Examples are illustrative; specific categories vary by project.*

**REMOVE (duplicates existing):**
- Procedural content that exists in skills
- Content already documented in agent-specific files

**MOVE (agent-specific):**
- Main-agent-only content (e.g., multi-agent coordination, repository structure)
- Sub-agent-only content (e.g., specific workflow steps only they perform)

**KEEP (universal guidance):**
- Tone/style, error handling, security policies
- Content that applies equally to ALL agent types

**Step 4: Result Structure**

CLAUDE.md should be a **slim reference document** (~200 lines) that:
- Contains ONLY universal guidance for ALL agents
- **Instructs agents to read their agent-specific files** (e.g., "MAIN AGENT: Read {file}.md")
- References skills for procedural content (not duplicate them)

**Hub-and-Spoke Pattern**:
```
CLAUDE.md (universal, ~200 lines)
  ├── "MAIN AGENT: Read {main-agent-file}.md"
  └── "SUB-AGENTS: Read {sub-agent-file}.md"
```

Agent-specific files contain the detailed content moved out of CLAUDE.md. Create these files if they don't exist. CLAUDE.md becomes a routing document that directs agents to their specialized guidance.

**Why This Approach**: Standard compression preserves all content in place. CLAUDE.md benefits from **reorganization** because much content is duplicated elsewhere or is agent-specific. Moving content to appropriate locations reduces redundancy across the entire documentation system.

**Validation**: After reorganization, verify:
```bash
# CLAUDE.md should be ~200-250 lines (not 800+)
wc -l CLAUDE.md

# No procedural duplication with skills
grep -c "Step 1:" CLAUDE.md  # Should be minimal
```

---

**⚠️ SPECIAL HANDLING: Style Documentation Files**

When compressing `.claude/rules/*.md` or `docs/code-style/*-claude.md`:

**Preserve style rule sections** (lines starting with `### `). These are intentionally-added detection patterns and rules. Compression can:
- ✅ Condense explanatory text within sections
- ✅ Shorten verbose rationale paragraphs
- ✅ Combine redundant examples
- ❌ Deleting entire `### Section Name` blocks breaks detection
- ❌ Removing detection patterns or code examples breaks detection

**Verification Required**: After compression, count section headers:
```bash
ORIGINAL_SECTIONS=$(grep -c "^### " /tmp/original-{filename})
COMPRESSED_SECTIONS=$(grep -c "^### " /tmp/compressed-{filename}-v${VERSION}.md)
if [ "$COMPRESSED_SECTIONS" -lt "$ORIGINAL_SECTIONS" ]; then
  echo "❌ ERROR: Section(s) removed! Original: $ORIGINAL_SECTIONS, Compressed: $COMPRESSED_SECTIONS"
  echo "   Style rule sections must be preserved. Iterate to restore missing sections."
fi
```

**If forbidden**, respond:
```
This compression process only applies to Claude-facing documentation.
The file `{{arg}}` appears to be human-facing documentation.
```

---

### Step 2: Check for Existing Baseline

**Check if baseline exists from prior iteration**:

```bash
BASELINE="/tmp/original-{{filename}}"
if [ -f "$BASELINE" ]; then
  BASELINE_LINES=$(wc -l < "$BASELINE")
  CURRENT_LINES=$(wc -l < "{{arg}}")
  echo "✅ Found existing baseline: $BASELINE ($BASELINE_LINES lines)"
  echo "   Current file: $CURRENT_LINES lines"
  echo "   Scores will compare against original baseline."
fi
```

**If NO baseline exists**, optionally check git history for prior compression:

```bash
if [ ! -f "$BASELINE" ]; then
  RECENT_SHRINK=$(git log --oneline -5 -- {{arg}} 2>/dev/null | grep -iE "compress|shrink|reduction" | head -1)
  if [ -n "$RECENT_SHRINK" ]; then
    echo "ℹ️ Note: File was previously compressed (commit: $RECENT_SHRINK)"
    echo "   No baseline preserved. Starting fresh with current version as baseline."
  fi
fi
```

---

### Step 3: Invoke Compression Agent

Use Task tool with `subagent_type: "general-purpose"` and simple outcome-based prompt:

**Agent Prompt Template**:
```
**Document Compression Task**

**File**: {{arg}}

**Goal**: Compress while preserving **perfect execution equivalence** (score = 1.0).

**Compression Target**: ~50% reduction is ideal, but lesser compression is acceptable. Perfect equivalence (1.0) is mandatory; compression amount is secondary.

---

## What is Execution Equivalence?

**Execution Equivalence** means: A reader following the compressed version will achieve the same results as someone following the original.

**Preserve**:
- **YAML frontmatter** (between `---` delimiters) - REQUIRED for slash commands
- **Decision-affecting information**: Claims, requirements, constraints that affect what to do
- **Relationship structure**: Temporal ordering (A before B), conditionals (IF-THEN), prerequisites, exclusions (A ⊥ B), escalations
- **Control flow**: Explicit sequences, blocking checkpoints (STOP, WAIT), branching logic
- **Executable details**: Commands, file paths, thresholds, specific values

**Safe to remove**:
- **Redundancy**: Repeated explanations of same concept
- **Verbose explanations**: Long-winded descriptions that can be condensed
- **Meta-commentary**: Explanatory comments about the document (NOT structural metadata like YAML frontmatter)
- **Non-essential examples**: Examples that don't add new information
- **Elaboration**: Extended justifications or background that don't affect decisions

---

## Compression Approach

**Focus on relationships**:
- Keep explicit relationship statements (Prerequisites, Dependencies, Exclusions, Escalations)
- Preserve temporal ordering (Step A→B)
- Maintain conditional logic (IF-THEN-ELSE)
- Keep constraint declarations (CANNOT coexist, MUST occur after)

**Condense explanations**:
- Remove "Why This Ordering Matters" verbose sections → keep ordering statement
- Remove "Definition" sections that explain obvious terms
- Combine related claims into single statements where possible
- Use high-level principle statements instead of exhaustive enumeration (when appropriate)

---

## Output

Read `{{arg}}`, compress it, and **USE THE WRITE TOOL** to save the compressed version.

**⚠️ CRITICAL**: You MUST actually write the file using the Write tool. Do NOT just describe or summarize the compressed content - physically create the file.

**Target**: ~50% word reduction while maintaining execution equivalence.
```

**Execute compression**:
```bash
# Invoke agent
Task tool: general-purpose agent with above prompt
```

---

### Step 4: Validate with /compare-docs

**⚠️ CRITICAL**: Before saving compressed version, read and save the ORIGINAL document state to use as baseline for validation.

After agent completes:

1. **Save original document** (ONLY if baseline doesn't exist):
   ```bash
   BASELINE="/tmp/original-{{filename}}"
   if [ ! -f "$BASELINE" ]; then
     cp {{arg}} "$BASELINE"
     echo "✅ Saved baseline: $BASELINE ($(wc -l < "$BASELINE") lines)"
   else
     echo "✅ Reusing existing baseline: $BASELINE"
   fi
   ```

   **Why baseline is preserved**: Baseline is kept until user explicitly confirms they're done iterating (see Step 5). This ensures scores always compare against the TRUE original, not intermediate compressed versions.

2. **Determine version number and save compressed version**:
   ```bash
   VERSION_FILE="/tmp/shrink-doc-{{filename}}-version.txt"

   # Get next version number from persistent counter (survives across sessions)
   if [ -f "$VERSION_FILE" ]; then
     LAST_VERSION=$(cat "$VERSION_FILE")
     VERSION=$((LAST_VERSION + 1))
   else
     # First time: check for existing version files to continue numbering
     HIGHEST=$(ls /tmp/compressed-{{filename}}-v*.md 2>/dev/null | sed 's/.*-v\([0-9]*\)\.md/\1/' | sort -n | tail -1)
     if [ -n "$HIGHEST" ]; then
       VERSION=$((HIGHEST + 1))
     else
       VERSION=1
     fi
   fi

   # Save version counter for next iteration
   echo "$VERSION" > "$VERSION_FILE"

   # Save with version number for rollback capability
   # Agent output → /tmp/compressed-{{filename}}-v${VERSION}.md
   echo "📝 Saved as version ${VERSION}: /tmp/compressed-{{filename}}-v${VERSION}.md"
   ```

   **Why persistent versioning**: Version numbers continue across sessions (v1, v2 in session 1 → v3, v4 in session 2) so older revisions are never overwritten. This enables rollback to any previous version and maintains complete compression history.

3. **Verify YAML frontmatter preserved** (if compressing slash command):
   ```bash
   head -5 /tmp/compressed-{{filename}}-v${VERSION}.md | grep -q "^---$" || echo "⚠️ WARNING: YAML frontmatter missing!"
   ```

4. **Run validation AGAINST ORIGINAL**:
   ```bash
   # ALWAYS compare against original baseline, NOT current file state
   /compare-docs /tmp/original-{{filename}} /tmp/compressed-{{filename}}-v${VERSION}.md
   ```

   **⚠️ IMPORTANT**: The validation score reflects execution equivalence between:
   - **Document A**: Original document state BEFORE /shrink-doc was invoked in this session
   - **Document B**: Newly compressed candidate version

   **NOT** a comparison against any intermediate compressed versions.

5. **Parse validation result**:
   - Extract execution_equivalence_score
   - Extract warnings and lost_relationships
   - Extract structural_changes

**Scoring Context**: When reporting the score to the user, explicitly state:
```
Score {score}/1.0 compares the compressed version against the ORIGINAL document state from before /shrink-doc was invoked (not against any intermediate versions).
```

**⚠️ CRITICAL REMINDER**: On second, third, etc. invocations:
- ✅ **REUSE** `/tmp/original-{{filename}}` from first invocation
- ✅ Always compare against original baseline (not intermediate versions)
- The baseline is set ONCE on first invocation and REUSED for all subsequent invocations

---

### Step 5: Decision Logic

**Threshold**: 1.0

**Report Format** (for approval):
1. What was preserved
2. What was removed
3. Validation Details (claim/relationship/graph scores)
4. **Results** (original size, compressed size, reduction %, **execution equivalence score**)
5. **Version Comparison Table** (showing all versions generated in this session)

**⚠️ CRITICAL**: List execution equivalence score at bottom for easy visibility.

**Version Comparison Table Format**:

After presenting validation results for ANY version, show comparison table.

**Table format:**

| Version      | Lines | Size | Reduction | Score | Status     |
|--------------|-------|------|-----------|-------|------------|
| **Original** | {n}   | {n}K | baseline  | N/A   | Reference  |
| **V{n}**     | {n}   | {n}K | {n}%      | {n}   | {status}   |

**Expected output format:**

| Version      | Lines | Size | Reduction | Score | Status      |
|--------------|-------|------|-----------|-------|-------------|
| **Original** | {n}   | {n}K | baseline  | N/A   | Reference   |
| **V1**       | {n}   | {n}K | {n}%      | {n}   | Rejected    |
| **V2**       | {n}   | {n}K | {n}%      | {n}   | Applied     |

---

**If score = 1.0**: ✅ **APPROVE**
```
Validation passed! Execution equivalence: {score}/1.0

✅ Approved version: /tmp/compressed-{{filename}}-v${VERSION}.md

Writing compressed version to {{arg}}...
```
→ Overwrite original with approved version
→ Clean up versioned compressions: `rm /tmp/compressed-{{filename}}-v*.md`
→ **KEEP baseline**: `/tmp/original-{{filename}}` preserved for potential future iterations

**After applying changes, ASK user**:
```
Changes applied successfully!

Would you like to try again to generate an even better version?
- YES → I'll keep the baseline and iterate with new compression targets
- NO → I'll clean up the baseline (compression complete)
```

**If user says YES** (wants to try again):
→ Keep `/tmp/original-{{filename}}`
→ Future /shrink-doc invocations will reuse this baseline
→ Scores will reflect cumulative compression from true original
→ Go back to Step 3 with user's feedback

**If user says NO** (done iterating):
→ `rm /tmp/original-{{filename}}`
→ `rm /tmp/shrink-doc-{{filename}}-version.txt`
→ Note: Future /shrink-doc on this file will use compressed version as new baseline

**If score < 1.0**: ❌ **ITERATE**
```
Validation requires improvement. Score: {score}/1.0 (threshold: 1.0)

Components:
- Claim preservation: {claim_score}
- Relationship preservation: {relationship_score}
- Graph structure: {graph_score}

**Why < 1.0 requires iteration**:
Scores below 1.0 indicate relationship abstraction or loss that creates interpretation vulnerabilities. See /compare-docs § Score Interpretation for