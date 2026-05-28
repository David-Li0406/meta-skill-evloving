---
name: prove-your-worth
description: "Ruthlessly audit project features for justification. Challenge every feature to prove its value with evidence or face removal. Uses MCP tools for research."
---

# Prove Your Worth — Feature Justification Audit

## Philosophy

> "Every line of code is a liability. Every feature is technical debt until proven otherwise."

This skill embodies extreme pragmatism:
- **Existence is not justification** — Features must earn their place
- **External is often better** — Well-maintained OSS beats custom code
- **Simpler is superior** — Complexity requires compelling justification
- **Facts over feelings** — No "we might need this" or "it's cool"

## When to Use

- Before major architectural decisions
- When codebase feels bloated or unfocused
- When onboarding reveals "why do we have this?"
- Before starting new features (to clean first)
- Periodically (quarterly feature audit)

## MCP Tools Required

This skill leverages MCP tools for evidence-based research. If MCP is unavailable, findings will be limited to agent knowledge (clearly marked).

| Tool | Provider | Purpose |
|------|----------|---------|
| `brave_web_search` | brave-search | Find alternative solutions, compare tools |
| `get_library_docs` | context7 | Get documentation for potential replacements |
| `search_repositories` | github | Find similar OSS implementations |
| `get_readme` | github | Evaluate alternatives' capabilities |

## Procedure

### Phase 1: Feature Inventory

**Step 1: Generate or read context map**
- If `.agent/map.md` exists and is recent, use it
- Otherwise, invoke `agent-ops-context-map` first

**Step 2: Extract feature list**

Enumerate all features by category:

```markdown
## Feature Inventory

### CLI Commands
- `aoc issues list` — List and filter issues
- `aoc kg build` — Build knowledge graph
- ...

### Internal Modules
- `mcp/` — MCP integration module
- `kg/` — Knowledge graph module
- ...

### Skills/Agents
- `agent-ops-planning` — Multi-iteration planning
- ...

### API Endpoints (if any)
- `GET /api/issues` — List issues
- ...
```

**Step 3: Classify each feature**

| Classification | Meaning | Scrutiny Level |
|----------------|---------|----------------|
| **Core** | Essential to project identity | Low (but still verify) |
| **Supporting** | Enables core features | Medium |
| **Convenience** | Nice-to-have | High |
| **Legacy** | Historical, unclear purpose | Very High |

---

### Phase 2: Challenge Each Feature

For EACH feature, systematically investigate:

#### 2.1 Alternative Search [🌐 MCP: brave-search]

```
Query patterns:
- "{feature_name} open source alternatives"
- "best {category} tools 2025 2026"
- "{feature_name} vs {known_alternative}"
```

**Record findings:**
```markdown
#### Alternatives Found
| Tool | Stars/Users | Maintenance | Features | Verdict |
|------|-------------|-------------|----------|---------|
| {name} | {count} | {active/stale} | {comparison} | Better/Same/Worse |
```

#### 2.2 Library Documentation [📚 MCP: context7]

For potential replacements, fetch docs to verify:
- Feature parity
- API compatibility
- Migration effort

#### 2.3 Similar Implementations [🔍 MCP: github]

```
Query patterns:
- "topic:{category} language:{lang}"
- "{feature} implementation"
```

**Evaluate:**
- Stars and forks (popularity signal)
- Last commit date (maintenance signal)
- Issue count and response time (health signal)

#### 2.4 Code Analysis [💭 Agent Analysis]

Analyze without external tools:
- Lines of code (complexity proxy)
- Dependencies introduced
- Coupling to other modules
- Test coverage
- Recent bug history

#### 2.5 Usage Analysis [💭 Agent Analysis]

Determine actual usage:
- Call sites (grep for imports/usage)
- Configuration options used vs available
- User feedback (if available)

---

### Phase 3: Verdict Assignment

Each feature receives exactly ONE verdict:

| Verdict | Criteria | Required Evidence |
|---------|----------|-------------------|
| **KEEP** | Unique value, no better alternative | Documented search showing no alternatives |
| **REMOVE** | Better alternatives exist OR unused | Links to superior tools OR zero usage |
| **SIMPLIFY** | Overcomplicated for actual use | Usage analysis showing unused options |
| **EXTRACT** | Valuable but belongs in separate package | Clear boundaries, standalone value |
| **MERGE** | Duplicates another feature | Code overlap analysis |
| **DELEGATE** | External tool does it better | Feature comparison table |

### Evidence Standards

#### For KEEP Verdict (High Bar)
Must have ALL of:
- [ ] Active usage demonstrated
- [ ] Alternative search conducted (documented)
- [ ] No viable replacement found
- [ ] Unique value articulated

#### For REMOVE Verdict
Must have ANY of:
- [ ] Superior alternative exists (with evidence)
- [ ] Zero or near-zero usage
- [ ] Maintenance cost exceeds value
- [ ] Duplicates existing functionality

---

### Phase 4: Report Generation

Generate report at `.agent/docs/feature-audit-report.md`:

```markdown
# Feature Justification Audit Report

**Generated:** {date}
**Project:** {name}
**Scope:** {what was analyzed}

## Executive Summary

| Verdict | Count | % of Features |
|---------|-------|---------------|
| KEEP | N | X% |
| REMOVE | N | X% |
| SIMPLIFY | N | X% |
| EXTRACT | N | X% |
| MERGE | N | X% |
| DELEGATE | N | X% |

**Estimated impact:**
- Lines of code removable: ~N
- Dependencies removable: N
- Maintenance burden reduction: {estimate}

---

## Critical Findings

### 🗑️ Must Remove (Better Alternatives Exist)

#### 1. {Feature Name}
**Verdict:** REMOVE → DELEGATE to {alternative}

**Evidence:**
| Source | Finding |
|--------|---------|
| 🌐 brave-search | {alternative} has 10x stars, active maintenance |
| 📚 context7 | {alternative} docs show feature parity |
| 💭 Analysis | Our implementation: 500 LOC, 3 bugs/month |

**Recommendation:** Replace with {alternative}, delete {files}

---

#### 2. {Feature Name}
...

---

### ✂️ Must Simplify (Overcomplicated)

#### 1. {Feature Name}
**Verdict:** SIMPLIFY

**Evidence:**
| Aspect | Current | Actual Usage |
|--------|---------|--------------|
| Config options | 15 | 3 used |
| Modes | 4 | 1 used |
| LOC | 800 | ~200 needed |

**Recommendation:** Remove unused options, reduce to core functionality

---

### 📦 Extraction Candidates

#### 1. {Feature Name}
**Verdict:** EXTRACT as `{package-name}`

**Rationale:**
- Standalone value outside this project
- Clear API boundary
- Could benefit other projects

---

### ✅ Justified to Keep

#### 1. {Feature Name}
**Verdict:** KEEP

**Justification:**
- Unique functionality: {description}
- Alternatives evaluated: {list}
- Why alternatives don't work: {reasons}
- Usage: {metrics}

---

## Code Duplication Analysis

| Pattern | Locations | Action |
|---------|-----------|--------|
| {description} | file1.py, file2.py | Extract to {module} |

---

## Recommended Action Plan

### Immediate (This Week)
1. Remove {feature} — replace with {alternative}
2. Delete {unused files}

### Short-Term (2 Weeks)
1. Simplify {feature} — remove unused options
2. Extract {module} to shared package

### Medium-Term (1 Month)
1. Evaluate {feature} after usage tracking
2. Complete migration from {old} to {new}

---

## Appendix: Full Feature Analysis

[Detailed per-feature breakdown...]
```

---

## Anti-Patterns (What NOT to Do)

- ❌ **Assume value** — "We've always had this" is not justification
- ❌ **Fear removal** — Unused code is worse than missing code
- ❌ **Skip research** — Must check alternatives before KEEP verdict
- ❌ **Vague verdicts** — "Maybe keep" is not a verdict
- ❌ **Ignore evidence** — If data says REMOVE, don't override with opinion
- ❌ **Guess usage** — Measure or ask, don't assume
- ❌ **Research without MCP** — If MCP unavailable, clearly mark limitations

---

## MCP Fallback Behavior

If MCP tools are unavailable:

1. **Note limitation prominently:**
   ```markdown
   ⚠️ **Limited Analysis Mode**
   MCP tools unavailable. Research based on agent knowledge only.
   Findings marked with 💭 require external verification.
   ```

2. **Reduce confidence in verdicts:**
   - KEEP → "KEEP (pending external verification)"
   - REMOVE → "REMOVE (verify alternatives exist)"

3. **Recommend follow-up:**
   ```markdown
   ## Follow-Up Required
   
   Enable MCP tools and re-run for:
   - Alternative verification for {features}
   - Documentation comparison for {replacements}
   ```

---

## Integration with Issue Tracking

After generating report, invoke `agent-ops-tasks`:

```
📋 Audit found {N} actionable items:

REMOVE (create CHORE issues):
- Remove {feature} → CHORE "Remove {feature}, replace with {alt}"

SIMPLIFY (create REFAC issues):
- Simplify {feature} → REFAC "Reduce {feature} to core functionality"

EXTRACT (create FEAT issues):
- Extract {module} → FEAT "Extract {module} to standalone package"

Create issues for these? [A]ll / [S]elect / [N]one
```

---

### Phase 5: Issue Creation & Discussion Planning

After verdict assignment, convert findings to trackable issues with appropriate discussion flags.

#### 5.1 Issue Mapping

Map verdicts to issue types and discussion levels:

| Verdict | Issue Type | Discussion Level | Interview Needed? |
|---------|-----------|------------------|-------------------|
| **REMOVE** | CHORE | Minimal (clear action) | No |
| **SIMPLIFY** | REFAC | Normal (needs design) | Optional |
| **EXTRACT** | FEAT | Extensive (architecture) | **Yes** |
| **MERGE** | CHORE | Normal | Optional |
| **DELEGATE** | CHORE | Normal | No |

#### 5.2 Generate Issue Candidates

For each actionable verdict, prepare issue structure:

```markdown
## Issue Candidates

### From REMOVE Verdicts

#### CHORE: Remove {feature}, delegate to {alternative}
**Source:** Audit finding #{N}
**Confidence:** High (clear alternative exists)
**Discussion:** minimal
**Files affected:** {list}
**Estimated effort:** S/M/L

---

### From SIMPLIFY Verdicts

#### REFAC: Simplify {feature} to core functionality
**Source:** Audit finding #{N}
**Confidence:** Medium (requires design decisions)
**Discussion:** normal
**Questions to resolve:**
- Which options to keep?
- What's the minimal viable interface?
**Files affected:** {list}

---

### From EXTRACT Verdicts

#### FEAT: Extract {module} as standalone package
**Source:** Audit finding #{N}
**Confidence:** Low (major architectural change)
**Discussion:** extensive 🎤
**Requires interview to determine:**
- [ ] Package name and scope
- [ ] Public API boundaries
- [ ] Versioning strategy
- [ ] Distribution method (PyPI? npm?)
- [ ] Maintenance ownership
```

#### 5.3 User Confirmation

Present issue summary and request confirmation:

```
📋 Ready to create {N} issues from audit findings:

  🟢 Quick (minimal discussion):     {count} issues
  🟡 Design needed (normal):         {count} issues  
  🔴 Major decision (extensive 🎤):  {count} issues

Issues marked 🎤 will invoke agent-ops-interview for detailed discussion.

Options:
  [A]ll    — Create all issues
  [S]elect — Choose which to create
  [R]eview — Show issue details first
  [N]one   — Skip issue creation
```

#### 5.4 Create Issues

For each confirmed issue:

1. Invoke `agent-ops-tasks create` with:
   - Title and description from audit finding
   - Link back to audit report section
   - Priority based on:
     - REMOVE with security concerns → HIGH
     - REMOVE with bugs → HIGH
     - SIMPLIFY → MEDIUM
     - EXTRACT → LOW (long-term)

2. For issues with `discussion: extensive`:
   - Add `[🎤 Interview Required]` tag to title
   - Include interview questions in description
   - After creation, offer to invoke `agent-ops-interview`

#### 5.5 Interview Invocation

For extensive discussion items:

```
🎤 Issue {ID}: "{title}" requires detailed discussion.

This issue involves architectural decisions that benefit from 
structured interview to ensure requirements are captured.

Start interview now? [Y]es / [L]ater / [S]kip
```

If user accepts:
1. Invoke `agent-ops-interview` with prepared questions
2. Update issue with interview responses
3. Adjust confidence level based on discussion

#### 5.6 Update Focus

After issue creation, update `.agent/focus.md`:

```markdown
## Just Completed
- Feature audit report: `.agent/docs/feature-audit-report.md`
- Created {N} issues from audit findings

## Doing Now
- {Interview ID} if extensive discussion in progress

## Up Next
- Review created issues in priority order
- {First high-priority issue from audit}
```

---

## Example Output

### Feature: Custom YAML Config Parser

**Investigation:**

| Check | Tool | Finding |
|-------|------|---------|
| Alternatives | 🌐 brave-search | PyYAML (3.2k⭐), ruamel.yaml (1.1k⭐), strictyaml (1.4k⭐) |
| Docs comparison | 📚 context7 | ruamel.yaml handles all our syntax + YAML 1.2 |
| Similar projects | 🔍 github | No project builds custom YAML parser |
| Our code | 💭 Analysis | 450 LOC, 2 bugs last month, 3 call sites |

**Verdict: DELEGATE**

**Evidence Summary:**
- ruamel.yaml is better maintained (active, 1.1k stars)
- Handles 100% of our use cases (verified in docs)
- Our parser adds 450 lines of liability
- 2 bugs in one month = high maintenance cost

**Recommendation:**
1. Replace `config/parser.py` with `ruamel.yaml`
2. Delete 450 LOC
3. Remove 2 test files (180 LOC)
4. Net: -630 LOC, -0 dependencies (already have PyYAML)

---

## Success Criteria

After running this skill:
- [ ] All features have a verdict with evidence
- [ ] Alternatives researched for each feature (or limitation noted)
- [ ] Report generated at `.agent/docs/feature-audit-report.md`
- [ ] Action items converted to issues (with user consent)
- [ ] Focus.md updated with audit summary