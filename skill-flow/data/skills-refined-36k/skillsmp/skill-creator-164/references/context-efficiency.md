# Context Efficiency Patterns

Techniques for optimizing token usage in skills, agents, rules, and commands.

Source: [developertoolkit.ai performance tuning guide](https://developertoolkit.ai/en/claude-code/advanced-techniques/performance-tuning/)

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Response latency | < 2 seconds | For simple tasks |
| Token efficiency | > 80% | Useful content per token |
| Context utilization | > 70% | Relevance in loaded context |
| First-attempt success | > 90% | For routine operations |
| Context clear threshold | > 80% | Clear when reaching this capacity |

## Token Budget Targets

| Component       | Target           | Rationale                |
| --------------- | ---------------- | ------------------------ |
| Root CLAUDE.md  | ~500 tokens      | Always loaded, high cost |
| Subdirectory CLAUDE.md | ~300 tokens | Per-module context |
| Rules           | ~500 tokens each | Always loaded            |
| Agent body      | 400-600 tokens   | Delegate to templates    |
| Skill SKILL.md  | ~500 tokens      | Delegate to references   |
| Reference files | ~300 tokens each | Loaded on-demand         |

## Thinking Token Budgets

| Task Type | Token Range | Examples |
|-----------|-------------|----------|
| Quick fixes | 0-1,000 | Typos, formatting |
| Standard dev | 5,000-10,000 | Features, bug fixes |
| Complex analysis | 20,000-50,000 | Refactoring, debugging |
| Deep architecture | 100,000-128,000 | System design |

## Hierarchical Context Management

**Tier 1 - Always Loaded (minimize):**

- CLAUDE.md root files
- Rules (`rules/*.md`)
- Skill/agent metadata (name + description)

**Tier 2 - On Trigger (moderate):**

- Skill SKILL.md body
- Agent definitions
- Command bodies

**Tier 3 - On Demand (can be larger):**

- `references/` files
- `_templates/` shared patterns
- Scripts (executed, not loaded)

## Compression Techniques

**Extract Shared Patterns:**

```
# Before: 10 agents × 1,500 tokens = 15,000 tokens
# After: 10 agents × 500 tokens + 1 template = 6,000 tokens

# In agent file:
> Follow workflow in `_templates/orchestrator-base.md`

## Domain Prompt
[Agent-specific content only]
```

**Split Verbose Content:**

```
# Before: skill-creator SKILL.md = 3,807 tokens
# After: SKILL.md (~500) + 3 reference files (~300 each) = ~1,400 tokens
#        Only loaded when needed
```

**Tables Over Prose:**

```markdown
# Before (verbose):

The priority levels are: critical which maps to P0, high which maps to P1...

# After (compact):

| Severity | Priority |
| -------- | -------- |
| Critical | P0       |
| High     | P1       |
```

**Merge Related Rules:**

```
# Before: git-rules.md + workflow-rules.md = 2 always-loaded files
# After: workflow.md = 1 file with both topics
```

## What to Extract vs Keep Inline

| Extract to Reference              | Keep Inline                   |
| --------------------------------- | ----------------------------- |
| Multi-step workflows              | Core principles (3-5 bullets) |
| Tool syntax/examples              | Domain-specific prompt        |
| Large catalogs (anti-patterns)    | Severity definitions          |
| Framework-specific details        | Output format overview        |
| Integration docs (ClickUp, Vanta) | Quick start                   |

## Smart Context Loading

**Focused Queries:**

```markdown
# Bad: "Analyze the codebase for issues"

# Good: "Review src/auth/ for security issues"
```

**Progressive Detail:**

```markdown
## Quick Start

[Essential 3-step workflow]

## Advanced

- **Topic A**: See `references/topic-a.md`
- **Topic B**: See `references/topic-b.md`
```

## Model Selection in Multi-Model Patterns

Match model to task:

- **Haiku**: Simple operations, fast validation
- **Sonnet**: Standard analysis, most work
- **Opus**: Complex reasoning, architecture decisions

## Validation Before Committing Optimizations

When compressing existing prompts:

1. Create optimized version
2. Spawn codex + gemini with both versions:
   ```
   Compare old vs new. Rate instruction preservation:
   POOR/PARTIAL/ACCEPTABLE/FULL. List missing instructions.
   ```
3. Take LOWER rating (conservative)
4. ACCEPTABLE/FULL → commit
5. POOR/PARTIAL → revise and re-validate

## Performance Targets

- **Token Efficiency**: >80% useful content per token
- **Context Utilization**: >70% relevance in loaded context
- **First-Attempt Success**: >90% for routine operations

## Essential Commands

| Command | Purpose |
|---------|---------|
| `/clear` | Reset context between unrelated tasks |
| `/compact` | Compress conversation, keep code/errors/decisions |
| `/context` | Check current token usage and loaded files |
| `--add-dir` | Load only specific directories for focused work |

## Workflow Patterns

**Batch Processing:** Group similar operations in sets of 5 for efficiency.

**Progressive Enhancement:** Basic → validation → security → optimization (build incrementally).

**Parallel Instances:** Run separate terminals for independent concerns (frontend/backend/tests).

**Checkpoint Strategy:** Git commit before major changes for easy rollback.

## Large Codebase Handling

For files exceeding **10,000 lines**:

- Target specific line ranges, not entire files
- Use search to locate relevant methods first
- Create coordination docs (e.g., `REFACTOR_PLAN.md`) for multi-module changes
- Work module-by-module systematically

## Troubleshooting

| Problem | Solutions |
|---------|-----------|
| Slow responses | Clear context, specific queries, faster model, reduce concurrent ops |
| Quality degradation | Reset context, refresh CLAUDE.md, break into steps, upgrade model |
| Token limit errors | Aggressive `/compact`, split operations, clear between tasks |

## Performance Baselines

| Operation | Duration | Tokens |
|-----------|----------|--------|
| Simple feature | 2-5 min | 5-10K |
| Bug fix | 1-3 min | 2-5K |
| Module refactor | 10-20 min | 20-50K |

## Anti-Patterns to Avoid

- README, CHANGELOG, INSTALLATION_GUIDE in skills
- Duplicate info in SKILL.md AND references
- Verbose explanations Claude already knows
- Examples where a table suffices
- Always-loaded content that's rarely needed
