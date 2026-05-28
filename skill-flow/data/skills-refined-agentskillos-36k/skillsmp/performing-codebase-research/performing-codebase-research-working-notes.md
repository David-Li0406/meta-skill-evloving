# Performing Codebase Research: Working Notes for Skill Discovery

Working notes from a discovery session exploring the `/Users/cyarie/Code/goals` testbed codebase.

---

## Skill Development Notes

### Insight 1: Start with "Fingerprint Files"

The most efficient first move was checking for fingerprint files that immediately reveal project type: `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, etc. These files tell you language, dependencies, and often build/test commands in one read.

**Skill implication**: The skill should prescribe checking fingerprint files first, with a prioritized list by ecosystem.

### Insight 2: Directory Structure Reveals Architecture

The directory layout (`api/`, `auth/`, `cli/`, `models/`, `storage/`) telegraphed a layered architecture before reading any code. Naming conventions are highly informative.

**Skill implication**: Include a "structural scan" step that maps directories to likely architectural roles.

### Insight 3: Entry Points Ground Everything

Finding the CLI entry point (`main.py`) immediately clarified how all the pieces connect. Without this, you're exploring in the dark.

**Skill implication**: Entry point discovery should be a required early step, not optional.

### Insight 4: Tests Reveal Expected Behavior

The test structure (`conftest.py`, fixtures, marker conventions) documented how the system is supposed to work better than comments would.

**Skill implication**: Include test examination as a primary investigation strategy, not just "look at source code."

### Insight 5: Specific Questions Drive Better Investigation

The second exploration was far more useful because it had a specific feature in mind. "Explore the codebase" produces surveys; "Where would X live?" produces actionable answers.

**Skill implication**: The skill should require the user to state a specific question or assumption to verify, not just "explore."

### Insight 6: Line Numbers Are Critical for Agent Consumers

The report included specific line numbers (`lines 16-19`, `lines 69-90`). These are essential for agents that will act on findings.

**Skill implication**: Findings format MUST include file paths + line numbers, not just file names.

### Insight 7: Pattern Matching Accelerates Investigation

Instead of reading every file, the agent looked for *similar patterns* (how is `query_cmd.py` structured?) and extrapolated. This is faster and more reliable than comprehensive reading.

**Skill implication**: Include "find similar patterns" as a core investigation strategy.

### Insight 8: Assumptions Should Be Stated Up Front

Implicit assumptions ("export probably goes in CLI layer", "there's probably a CSV library") should be explicit. Making them explicit focuses the investigation.

**Skill implication**: Require stating assumptions before investigating, then explicitly confirm/refute each.

### Insight 9: Explicit Contradiction-Seeking Prevents Confirmation Bias

By explicitly asking for evidence that *contradicts* the assumption, the agent was forced to look for counter-examples rather than just confirming what it expected to find.

**Skill implication**: The investigation process MUST include an explicit "seek contradictions" step.

### Insight 10: Confidence Levels Aid Decision-Making

The verdict used a confidence scale (strongly confirmed / weakly confirmed / inconclusive / weakly contradicted / strongly contradicted). This helps consumers know how much to trust the finding.

**Skill implication**: Findings should include confidence levels, not just yes/no answers.

---

## Questions and Resolutions

### Question: What triggers codebase investigation?

**Options considered**: Before planning only / During planning only / After planning only / Any phase

**Resolution**: Investigation can happen at any phase, but the *type* of investigation differs:
- **Before planning**: Broad exploration to understand what exists
- **During planning**: Targeted verification of specific assumptions
- **After planning**: Validation that the plan matches reality

**Skill implication**: Skill should support all three modes with appropriate investigation strategies for each.

### Question: Who consumes the findings?

**Options considered**: Humans only / LLM agents only / Both

**Resolution**: Both equally. Findings must be:
- Human-readable (clear prose, logical structure)
- Agent-consumable (precise file paths, line numbers, structured verdicts)

**Skill implication**: Output format must satisfy both audiences.

### Question: How deep should investigation go?

**Options considered**: Shallow survey / Targeted depth / Exhaustive

**Resolution**: Depth should match the question. Shallow for "what tech stack?" Deep for "does this pattern hold everywhere?"

**Skill implication**: Include guidance on calibrating investigation depth to question type.

---

## Cross-Skill Notes

- **`designing-software`**: Should reference this skill when making architectural assumptions
- **`writing-useful-tests`**: Investigation of existing tests is a valid way to understand expected behavior

---

## Process Summary: Performing Codebase Research

### Purpose

Systematically explore a codebase to:
- Verify design and planning assumptions
- Find existing patterns before proposing new code
- Ground decisions in truth rather than hallucination

### Inputs Required

Before starting, you need:
- **A specific question or assumption to verify** (not "explore the codebase")
- **Access to the codebase** (local path or repository)
- **Context for why you're investigating** (planning, designing, implementing)

### Investigation Types

| Type | When to Use | Depth | Output |
|------|-------------|-------|--------|
| **Survey** | Initial orientation | Broad, shallow | Project profile |
| **Targeted** | Verify specific assumption | Narrow, deep | Confirmation/refutation |
| **Pattern search** | Find how X is done | Medium | Examples with locations |
| **Feature planning** | Where would X live? | Medium | Recommendations with evidence |

### Step-by-Step Process

#### Step 1: State the Investigation Goal

Before touching the codebase, write down:
1. **The question or assumption** you're investigating
2. **Why you need to know** (context for the investigation)
3. **What you expect to find** (pre-registered hypothesis)

This prevents aimless exploration and creates a baseline to compare findings against.

#### Step 2: Fingerprint the Project

Check fingerprint files to identify project type:

| File | Reveals |
|------|---------|
| `pyproject.toml`, `setup.py` | Python project, dependencies |
| `package.json` | Node.js project, dependencies |
| `Cargo.toml` | Rust project, dependencies |
| `go.mod` | Go project, dependencies |
| `pom.xml`, `build.gradle` | Java project, build system |
| `Makefile`, `CMakeLists.txt` | Build commands |
| `.env`, `.env.example` | Environment configuration |

**Questions to answer**:
- What language(s) and framework(s)?
- What package manager and build tools?
- What are the key dependencies?

#### Step 3: Map the Structure

Scan directory layout to understand architecture:

| Directory Name | Likely Purpose |
|----------------|----------------|
| `src/`, `lib/` | Source code |
| `api/` | API layer (routes, handlers) |
| `models/`, `entities/` | Data models |
| `services/` | Business logic |
| `storage/`, `db/`, `repositories/` | Persistence layer |
| `cli/`, `cmd/` | Command-line interface |
| `tests/`, `__tests__/` | Test files |
| `config/` | Configuration |
| `scripts/` | Development scripts |

**Questions to answer**:
- What architectural pattern is used (layered, hexagonal, monolithic)?
- Where does each concern live?
- Are there clear boundaries between layers?

#### Step 4: Find Entry Points

Locate where execution begins:

| Project Type | Entry Point Locations |
|--------------|----------------------|
| Python CLI | `__main__.py`, `cli/main.py`, `pyproject.toml [tool.poetry.scripts]` |
| Node.js | `package.json "main"`, `index.js`, `src/index.ts` |
| Web backend | `app.py`, `server.js`, `main.go`, route definitions |
| Library | Public exports, `__init__.py`, `index.ts` |

**Questions to answer**:
- How does the application start?
- What's the command structure (if CLI)?
- What routes/endpoints exist (if web)?

#### Step 5: Investigate Based on Goal Type

**For assumption verification**:
1. State the assumption explicitly
2. Search for evidence that SUPPORTS it
3. Search for evidence that CONTRADICTS it
4. Weigh evidence and render verdict

**For pattern search**:
1. Find one clear example of the pattern
2. Search for similar patterns across the codebase
3. Note variations and exceptions
4. Document the canonical pattern with file:line references

**For feature planning**:
1. Find where similar features live
2. Identify the conventions used (naming, structure, registration)
3. Check for reusable utilities or base classes
4. Document the "landing zone" with rationale

#### Step 6: Examine Tests (When Relevant)

Tests reveal expected behavior:
- **Test structure**: How are tests organized? (mirrors source? by type?)
- **Fixtures**: What test data patterns exist?
- **Mocking**: How are external dependencies handled?
- **Coverage**: What's tested vs. untested?

#### Step 7: Synthesize Findings

Compile results into a findings report (see Output Format below).

### Output Format

Findings must be both human-readable and agent-consumable.

```markdown
## Investigation: [Question/Assumption]

### Context
[Why this investigation was needed]

### Approach
[What was searched and how]

### Findings

#### Evidence For
- [Finding with file:line reference]
- [Finding with file:line reference]

#### Evidence Against
- [Finding with file:line reference] (or "None found")

### Verdict

**[Confidence level]**: [strongly confirmed | weakly confirmed | inconclusive | weakly contradicted | strongly contradicted]

[One-paragraph explanation of verdict]

### Implications for Design/Planning
[What this means for the work that prompted the investigation]
```

### Validation Checks

Before finalizing findings:
- [ ] Investigation goal was clearly stated before starting
- [ ] Both supporting AND contradicting evidence was sought
- [ ] All file references include paths AND line numbers
- [ ] Confidence level is explicitly stated
- [ ] Findings are actionable (someone could act on them)

---

## Investigation Strategies Reference

### Strategy: Grep for Patterns
Use when you need to find all instances of something:
- Find all SQL statements in Python files
- Find all imports of a specific module
- Find all usages of a function

### Strategy: Trace from Entry Point
Use when you need to understand data flow:
1. Start at CLI command or API endpoint
2. Follow the calls through service layer
3. Note what's touched at each layer
4. Map the complete flow

### Strategy: Compare Similar Files
Use when you need to understand conventions:
1. Find two files that do similar things
2. Note what's identical (the pattern)
3. Note what differs (the variation points)
4. Extract the template

### Strategy: Check Test Fixtures
Use when you need realistic data examples:
1. Find `conftest.py` or test setup files
2. Look for fixture functions
3. These show the expected data shapes

### Strategy: Read the Docs (in code)
Use when you need to understand intent:
1. Check README files at each level
2. Look for docstrings in key modules
3. Check for `docs/` directory
4. Look for ADRs (Architecture Decision Records)

---

## Next Steps

- [ ] Create SKILL.md from these working notes
- [ ] Create subagent configuration
- [ ] Pressure test on different codebase types
