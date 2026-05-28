---
name: compound-plugin-analyzer
description: Analyze Every Compound Engineering plugin and compare to our plugin for improvement suggestions
argument-hint: "[optional: focus area e.g. 'agents', 'skills', 'patterns', 'commands']"
model: claude-opus-4-5-20251101
context: fork
agent: Explore
allowed-tools:
  - WebFetch
  - WebSearch
  - Read
  - Grep
  - Glob
extended-thinking: true
---

# Compound Plugin Analyzer

Thoroughly analyze the Every Compound Engineering plugin from GitHub and compare it to the PSD Claude Coding System plugin, generating prioritized improvement suggestions.

## Source Information

**Every Compound Engineering Plugin:**
- Repository: https://github.com/EveryInc/compound-engineering-plugin
- Raw content base: https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/

**Our Plugin:**
- Location: /Users/hagelk/non-ic-code/psd-claude-coding-system/plugins/psd-claude-coding-system

## Analysis Workflow

### Phase 1: Fetch Every Plugin Structure

Use WebFetch to retrieve remote plugin content:

1. **README and Version:**
   - Fetch: `https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md`
   - Extract version, feature list, architecture overview

2. **Plugin Metadata:**
   - Fetch: `https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/plugins/compound-engineering/.claude-plugin/plugin.json`
   - Extract version, commands list

3. **CLAUDE.md Patterns:**
   - Fetch: `https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/plugins/compound-engineering/CLAUDE.md`
   - Extract architectural patterns, model selection, workflow patterns

4. **Agents Directory:**
   - Use GitHub API or WebSearch to find agent list
   - Fetch key agents to understand patterns:
     - Agent-native-reviewer
     - Data-migration-expert
     - Deployment-verification-agent
     - Language-specific reviewers (kieran-rails, kieran-python, kieran-typescript)

5. **Skills Directory:**
   - Identify all skill directories
   - Fetch SKILL.md files from key skills:
     - git-worktree
     - gemini-imagegen
     - agent-browser
     - compound (knowledge compounding)

6. **Commands:**
   - Identify command naming patterns (namespace prefix like `/workflows:`)
   - Fetch command files to understand structure

### Phase 2: Analyze Our Plugin Structure

Use Read, Grep, and Glob to analyze local plugin:

1. **Agents Analysis:**
   ```
   Glob: plugins/psd-claude-coding-system/agents/*.md
   ```
   - Count total agents
   - Categorize by function (domain, quality, meta-learning, multi-LLM)
   - Extract unique capabilities (UX heuristics, telemetry, etc.)

2. **Skills Analysis:**
   ```
   Glob: plugins/psd-claude-coding-system/skills/*/SKILL.md
   Glob: plugins/psd-claude-coding-system/skills/*.md
   ```
   - Count total skills
   - Identify skill patterns (directory vs single file)
   - Extract frontmatter patterns

3. **Hooks Analysis:**
   ```
   Read: plugins/psd-claude-coding-system/hooks/hooks.json
   Glob: plugins/psd-claude-coding-system/scripts/*.sh
   ```
   - Document telemetry collection approach
   - Identify hook patterns

4. **CLAUDE.md Patterns:**
   ```
   Read: CLAUDE.md
   ```
   - Extract our architectural patterns
   - Document model selection strategy
   - Note workflow patterns

### Phase 3: Gap Analysis

Compare across these dimensions:

#### 3.1 Agent Coverage
- List agents they have that we don't
- List agents we have that they don't
- Identify complementary capabilities

#### 3.2 Skill Patterns
- Compare directory structure (SKILL.md + /scripts/ vs flat)
- Compare frontmatter fields
- Compare model selection (inherit vs explicit)

#### 3.3 Command Organization
- Compare namespace strategies
- Compare command discovery patterns
- Compare argument handling

#### 3.4 Safety Mechanisms
- Compare confirmation patterns
- Compare checklist approaches
- Compare error handling

#### 3.5 Documentation Patterns
- Compare CLAUDE.md structure
- Compare inline documentation
- Compare example usage

#### 3.6 Unique Strengths
**Theirs:**
- Agent-native architecture validation
- Data migration expertise
- Git worktree management
- Figma design sync
- Multi-language reviewers

**Ours:**
- 68-heuristic UX evaluation
- Multi-LLM council (GPT-5, Gemini 3)
- Meta-learning system (10 commands)
- Automatic telemetry hooks
- Pre-implementation security

### Phase 4: Generate Improvement Report

Output the analysis in this format:

```markdown
# Compound Plugin Analysis Report

## Executive Summary
- Every Plugin Version: [detected]
- Our Plugin Version: [from plugin.json]
- Analysis Date: [current date]
- Focus Area: [if specified, else "Full Analysis"]

## Gap Analysis

### Agents We Should Add
| Priority | Agent Name | Purpose | Implementation Complexity | Notes |
|----------|------------|---------|---------------------------|-------|
| HIGH | ... | ... | Low/Medium/High | ... |
| MEDIUM | ... | ... | ... | ... |
| LOW | ... | ... | ... | ... |

### Skills We Should Add
| Priority | Skill Name | Purpose | Implementation Complexity | Notes |
|----------|------------|---------|---------------------------|-------|
| HIGH | ... | ... | Low/Medium/High | ... |
| MEDIUM | ... | ... | ... | ... |
| LOW | ... | ... | ... | ... |

### Patterns to Adopt
1. **Pattern Name**
   - Description: What it does
   - Their Implementation: How they do it
   - Our Adaptation: How we should implement
   - Files to Modify: Specific files

2. ...

### Our Unique Strengths (Keep/Enhance)
| Strength | Current Implementation | Enhancement Opportunity |
|----------|----------------------|------------------------|
| UX Specialist | 68 heuristics | ... |
| Multi-LLM Council | GPT-5, Gemini | ... |
| Meta-Learning | 10 commands | ... |
| Auto Telemetry | Hook-based | ... |

## Recommended Actions

### Immediate (This Week)
1. [Action item with specific files]
2. ...

### Short-Term (This Month)
1. ...

### Long-Term (This Quarter)
1. ...

## Implementation Roadmap

### Phase 1: Quick Wins (1-2 days each)
- ...

### Phase 2: Medium Effort (3-5 days each)
- ...

### Phase 3: Significant Features (1+ weeks each)
- ...

## Raw Data

### Every Plugin Stats
- Total Agents: X
- Total Skills: X
- Total Commands: X
- Unique Patterns: [list]

### Our Plugin Stats
- Total Agents: X
- Total Skills: X
- Total Commands: X
- Unique Patterns: [list]
```

## Focus Area Handling

If an optional focus area argument is provided, narrow the analysis:

- **`agents`**: Deep dive on agent comparison only
- **`skills`**: Deep dive on skill patterns only
- **`patterns`**: Focus on architectural/workflow patterns
- **`commands`**: Focus on command organization and naming
- **`safety`**: Focus on safety mechanisms and confirmations

When focused, still provide context from other areas but prioritize depth over breadth.

## Key URLs Reference

```
# README
https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/README.md

# Plugin metadata
https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/plugins/compound-engineering/.claude-plugin/plugin.json

# CLAUDE.md
https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/plugins/compound-engineering/CLAUDE.md

# Sample agents (adjust paths based on actual structure)
https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/plugins/compound-engineering/agents/[agent-name].md

# Sample skills
https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main/plugins/compound-engineering/skills/[skill-name]/SKILL.md
```

## Execution Notes

1. **Rate Limiting**: Space WebFetch calls appropriately to avoid rate limiting
2. **Error Handling**: If a URL fails, note it and continue with available data
3. **Caching**: Results can be saved for comparison over time
4. **Completeness**: Prioritize getting accurate counts and patterns over fetching every file

## Example Output Snippet

```markdown
### Agents We Should Add
| Priority | Agent Name | Purpose | Complexity | Notes |
|----------|------------|---------|------------|-------|
| HIGH | deployment-verification-agent | Go/No-Go deployment checklists | Medium | Complements our security-analyst |
| HIGH | data-migration-expert | Validates ID mappings in migrations | Medium | We lack migration-specific tooling |
| MEDIUM | agent-native-reviewer | Validates AI-native architecture | Low | Useful for our meta-learning work |
| MEDIUM | worktree-manager | Parallel git worktree management | High | Nice for complex feature work |
| LOW | figma-design-sync | Sync Figma designs to web | High | Only if we use Figma |
```
