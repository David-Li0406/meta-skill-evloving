---
name: dqx-agent-selector
description: Choose the right DQX specialized agent for your task
compatibility: opencode
metadata:
  audience: core-agent
---

## What I do

Help you select the appropriate DQX specialized agent for your task. DQX has 10 specialized agents, each optimized for specific types of work.

---

## Agent Directory

### Workflow Agents (Feature Development)

#### **dqx-plan**
**Purpose**: Create modular design documents (spec, implementation guide, context)
**Temperature**: 0.5 (creative planning)

**When to use**:
- Planning new features
- Architecture design decisions
- Creating implementation roadmaps
- Exploring design alternatives

**Output**: 3 design documents (~900 lines total)

**Example**: "I want to add metric caching" → dqx-plan creates design docs

---

#### **dqx-implement**
**Purpose**: Execute TDD-based implementation phases
**Temperature**: 0.2 (precise implementation)

**When to use**:
- Building features from design docs
- Following implementation guide phases
- Test-driven development
- Phase-by-phase execution

**Skills**: dqx-code-standards, dqx-quality-gate, dqx-conventional-commit, dqx-tdd-cycle

**Example**: "Implement Phase 1: Core data structures" → dqx-implement executes TDD cycle

---

#### **dqx-pr**
**Purpose**: Create comprehensive pull requests with quality verification
**Temperature**: 0.3 (balanced)
**Model**: Haiku 4.5 (efficient)

**When to use**:
- After implementation complete
- Ready to create GitHub PR
- Need quality gate verification
- PR description generation

**Skills**: dqx-quality-gate

**Example**: "Create PR for caching feature" → dqx-pr verifies quality and creates PR

---

#### **dqx-feedback**
**Purpose**: Address CodeRabbit review feedback with targeted fixes
**Temperature**: 0.2 (precise fixes)

**When to use**:
- After PR review received
- CodeRabbit provided feedback
- Need to prioritize comments
- Iterative improvement cycle

**Skills**: dqx-code-standards, dqx-quality-gate, dqx-conventional-commit, dqx-review-priority

**Example**: "Address CodeRabbit feedback on PR #123" → dqx-feedback categorizes and fixes

---

### Specialized Agents (Domain-Specific)

#### **dqx-sql**
**Purpose**: SQL dialects, analyzer, and DQL parser
**Temperature**: 0.2 (precise SQL generation)

**When to use**:
- SQL query generation
- Dialect implementations (DuckDB, BigQuery, Snowflake)
- DQL parser changes
- Analyzer modifications

**Skills**: dqx-code-standards

**Example**: "Add support for BigQuery UNNEST" → dqx-sql implements dialect feature

---

#### **dqx-graph**
**Purpose**: Graph processing and dependency analysis
**Temperature**: 0.2 (precise algorithms)

**When to use**:
- Graph traversal algorithms
- Visitor pattern implementation
- Dependency analysis
- Tree visualization

**Skills**: dqx-code-standards

**Example**: "Optimize graph traversal performance" → dqx-graph refactors traversal

---

#### **dqx-api**
**Purpose**: User-facing API design and developer experience
**Temperature**: 0.3 (balanced design)

**When to use**:
- Public API design
- Method naming decisions
- API consistency checks
- Developer experience improvements

**Skills**: dqx-code-standards

**Example**: "Design API for custom validators" → dqx-api creates consistent API

---

#### **dqx-docs**
**Purpose**: Documentation, examples, and inline docstrings
**Temperature**: 0.4 (creative explanations)

**When to use**:
- Writing user documentation
- Creating examples
- Adding/updating docstrings
- MkDocs content

**Skills**: dqx-code-standards

**Example**: "Document the new caching API" → dqx-docs writes user guide

---

### Quality Agents (Enforcement)

#### **dqx-quality**
**Purpose**: Pre-commit hooks, linting, type checking
**Temperature**: 0.1 (strict enforcement)
**Model**: Haiku 4.5 (efficient)

**When to use**:
- Pre-commit failures
- Linting issues
- Type check errors
- Format problems

**Permissions**: Limited to quality tools only (ruff, mypy, pre-commit)

**Example**: "Fix mypy errors in api.py" → dqx-quality runs checks and fixes

---

#### **dqx-test**
**Purpose**: Test generation and coverage analysis
**Temperature**: 0.1 (strict testing)
**Model**: Haiku 4.5 (efficient)

**When to use**:
- Writing test cases
- Coverage gap analysis
- Test fixture creation
- Edge case identification

**Skills**: dqx-code-standards

**Permissions**: Limited to pytest and coverage tools

**Example**: "Add tests for error handling" → dqx-test generates test cases

---

## Decision Tree

### Primary Question: What type of work are you doing?

**Planning a feature?**
→ `dqx-plan`

**Implementing from a plan?**
→ `dqx-implement`

**Ready for PR?**
→ `dqx-pr`

**Addressing review feedback?**
→ `dqx-feedback`

**Working on SQL/queries?**
→ `dqx-sql`

**Working on graphs/traversal?**
→ `dqx-graph`

**Designing public APIs?**
→ `dqx-api`

**Writing documentation?**
→ `dqx-docs`

**Fix quality issues?**
→ `dqx-quality`

**Need more tests/coverage?**
→ `dqx-test`

---

## Workflow Combinations

### Complete Feature Workflow

```
User Request
    ↓
dqx-plan → Design documents
    ↓
dqx-implement → Working code
    ↓
dqx-pr → GitHub PR
    ↓
dqx-feedback → Address reviews
    ↓
Merge!
```

### Bug Fix Workflow

```
Bug Report
    ↓
dqx-test → Write failing test
    ↓
dqx-implement → Fix bug (TDD)
    ↓
dqx-quality → Verify quality
    ↓
Commit & Push
```

### Documentation Update

```
API Changed
    ↓
dqx-docs → Update docs
    ↓
dqx-api → Verify API consistency
    ↓
Commit
```

---

## Agent Characteristics

### By Speed (Fastest to Slowest)

1. **dqx-quality** (Haiku 4.5) - Fast quality checks
2. **dqx-test** (Haiku 4.5) - Fast test generation
3. **dqx-pr** (Haiku 4.5) - Fast PR creation
4. **dqx-feedback** (Sonnet 4.5, temp 0.2) - Focused fixes
5. **dqx-implement** (Sonnet 4.5, temp 0.2) - Methodical TDD
6. **dqx-sql/graph/api** (Sonnet 4.5, temp 0.2-0.3) - Specialized work
7. **dqx-docs** (Sonnet 4.5, temp 0.4) - Creative writing
8. **dqx-plan** (Sonnet 4.5, temp 0.5) - Deep planning

### By Scope (Narrow to Broad)

**Narrow (Single Domain)**:
- dqx-sql (SQL only)
- dqx-graph (Graphs only)
- dqx-quality (Quality only)
- dqx-test (Testing only)

**Medium (Multi-file Work)**:
- dqx-api (API design)
- dqx-docs (Documentation)
- dqx-feedback (Review fixes)

**Broad (Feature-level)**:
- dqx-implement (Full features)
- dqx-plan (Full design)
- dqx-pr (Full verification)

---

## Common Mistakes

### ❌ Wrong: Using dqx-implement without design
**Problem**: No implementation guide to follow
**Solution**: Run dqx-plan first to create design docs

### ❌ Wrong: Using dqx-pr before code is ready
**Problem**: Quality gates will fail
**Solution**: Run dqx-implement to complete implementation first

### ❌ Wrong: Using dqx-feedback for new features
**Problem**: dqx-feedback is for addressing review comments, not building
**Solution**: Use dqx-implement for new code

### ❌ Wrong: Using core agent for specialized work
**Problem**: Less efficient, generic approach
**Solution**: Delegate to specialized agent (dqx-sql, dqx-graph, etc.)

---

## When to Use Multiple Agents

### Sequential (One after another)

**Feature development**:
```
dqx-plan → dqx-implement → dqx-pr → dqx-feedback
```

**Bug fix with docs**:
```
dqx-implement → dqx-docs → dqx-pr
```

### Parallel (Multiple agents on different files)

**Large feature**:
```
dqx-sql (database layer) + dqx-api (public API) + dqx-docs (user guide)
→ dqx-pr
```

---

## When to use me

Use this skill when:
- **Unsure which agent** to use
- **Multiple agents** might be relevant
- **Learning the DQX** agent ecosystem
- **Coordinating complex** multi-agent tasks

---

## Quick Reference Card

| Task | Agent | Why |
|------|-------|-----|
| Design feature | dqx-plan | Creates specs |
| Build feature | dqx-implement | TDD workflow |
| Fix SQL bug | dqx-sql | SQL specialist |
| Create PR | dqx-pr | Quality verification |
| Address feedback | dqx-feedback | Prioritized fixes |
| Add docs | dqx-docs | Documentation specialist |
| Fix quality issues | dqx-quality | Quality enforcement |
| Need more tests | dqx-test | Test generation |
| Design API | dqx-api | API consistency |
| Graph work | dqx-graph | Graph algorithms |

---

## Reference

Complete details: **AGENTS.md §feature-development-workflow**

All agent files: `.opencode/agents/dqx-*.md`
