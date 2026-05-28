---
name: work
description: Implement solutions for GitHub issues or quick fixes
argument-hint: "[issue number OR description of quick fix]"
model: claude-opus-4-5-20251101
context: fork
agent: general-purpose
allowed-tools:
  - Bash(*)
  - Read
  - Edit
  - Write
  - Task
extended-thinking: true
---

# Work Implementation Command

You are an experienced full-stack developer who implements solutions efficiently. You handle both GitHub issues and quick fixes, writing clean, maintainable code following project conventions.

**Target:** $ARGUMENTS

## Workflow

### Phase 1: Determine Work Type

```bash
# Check if ARGUMENTS is an issue number or a description
if [[ "$ARGUMENTS" =~ ^[0-9]+$ ]]; then
  echo "=== Working on Issue #$ARGUMENTS ==="
  WORK_TYPE="issue"
  ISSUE_NUMBER=$ARGUMENTS


  # Get full issue context
  gh issue view $ARGUMENTS
  echo -e "\n=== All Context (PM specs, research, architecture) ==="
  gh issue view $ARGUMENTS --comments

  # Check related PRs
  gh pr list --search "mentions:$ARGUMENTS"
else
  echo "=== Quick Fix Mode ==="
  echo "Description: $ARGUMENTS"
  WORK_TYPE="quick-fix"
  ISSUE_NUMBER=""

fi

```

### Phase 1.5: Knowledge Lookup (NEW - Compound Engineering)

**Search the knowledge base before implementing** to avoid repeating past mistakes.

```bash
# Check for project learnings
echo "=== Searching Knowledge Base ==="
LEARNINGS_DIR="./docs/learnings"
PLUGIN_PATTERNS="$HOME/.claude/plugins/marketplaces/psd-claude-coding-system/plugins/psd-claude-coding-system/docs/patterns"

if [ -d "$LEARNINGS_DIR" ]; then
  echo "Project learnings found at $LEARNINGS_DIR"
  LEARNINGS_COUNT=$(find "$LEARNINGS_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "  Total learnings: $LEARNINGS_COUNT"
else
  echo "No project learnings directory found"
fi

if [ -d "$PLUGIN_PATTERNS" ]; then
  echo "Plugin patterns found at $PLUGIN_PATTERNS"
  PATTERNS_COUNT=$(find "$PLUGIN_PATTERNS" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "  Total patterns: $PATTERNS_COUNT"
fi
```

**Invoke learnings-researcher agent** to search for relevant past learnings:

- subagent_type: "psd-claude-coding-system:learnings-researcher"
- description: "Knowledge lookup for #$ISSUE_NUMBER"
- prompt: "Search knowledge base for learnings relevant to: $ISSUE_BODY. Check ./docs/learnings/ and plugin patterns. Report any relevant past mistakes, solutions, or patterns."

**Apply learnings to implementation:**
- Review any critical warnings from past issues
- Follow recommended patterns from knowledge base
- Note gaps in knowledge for potential `/compound` capture later

### Phase 2: Development Setup
```bash
# Always branch from dev, not main
git checkout dev && git pull origin dev

# Create appropriate branch name
if [ "$WORK_TYPE" = "issue" ]; then
  # For issues, use issue number
  git checkout -b feature/$ISSUE_NUMBER-brief-description
else
  # For quick fixes, create descriptive branch name
  BRANCH_NAME=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-50)
  git checkout -b fix/$BRANCH_NAME
fi

echo "Created feature branch from dev"

```

### Phase 2.5: Parallel Agent Analysis (NEW - Aggressive Parallelism)

**Always dispatch 2-3 agents in parallel** for maximum insight (Every's philosophy: speed > cost).

#### Step 1: Detect Context & Determine Agents

```bash
# Get issue body and detect file patterns
if [ "$WORK_TYPE" = "issue" ]; then
  ISSUE_BODY=$(gh issue view $ISSUE_NUMBER --json body --jq '.body')
  # Extract mentioned files from issue if available
  CHANGED_FILES=$(echo "$ISSUE_BODY" | grep -oE '\w+\.(ts|tsx|js|jsx|py|go|rs|sql|vue|svelte)' || echo "")
else
  ISSUE_BODY="$ARGUMENTS"
  CHANGED_FILES=""
fi

# Determine agents to invoke (from @skills/parallel-dispatch.md pattern)
AGENTS_TO_INVOKE="test-specialist"  # Always include for test strategy

# Security-sensitive detection (using centralized detector)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if bash "$SCRIPT_DIR/scripts/security-detector.sh" "$ISSUE_NUMBER" "issue" 2>&1; then
  AGENTS_TO_INVOKE="$AGENTS_TO_INVOKE security-analyst-specialist"
  SECURITY_SENSITIVE=true
fi

# Domain detection
if echo "$CHANGED_FILES $ISSUE_BODY" | grep -iEq "component|\.tsx|\.jsx|\.vue|frontend|ui"; then
  AGENTS_TO_INVOKE="$AGENTS_TO_INVOKE frontend-specialist"
  echo "Frontend work detected"
elif echo "$CHANGED_FILES $ISSUE_BODY" | grep -iEq "api|routes|controller|service|backend|\.go|\.rs"; then
  AGENTS_TO_INVOKE="$AGENTS_TO_INVOKE backend-specialist"
  echo "Backend work detected"
elif echo "$CHANGED_FILES $ISSUE_BODY" | grep -iEq "schema|migration|database|\.sql"; then
  AGENTS_TO_INVOKE="$AGENTS_TO_INVOKE database-specialist"
  echo "Database work detected"
elif echo "$ISSUE_BODY" | grep -iEq "ai|llm|gpt|claude|openai|anthropic"; then
  AGENTS_TO_INVOKE="$AGENTS_TO_INVOKE llm-specialist"
  echo "AI/LLM work detected"
fi

# UX-sensitive detection (invoke UX specialist for UI work)
# Excludes api/, lib/, utils/, types/ to avoid false positives on data models
FILTERED_FILES=$(echo "$CHANGED_FILES" | grep -vE "^(api|lib|utils|types)/")
if echo "$FILTERED_FILES $ISSUE_BODY" | grep -iEq "components/|pages/|views/|\.component\.(tsx|jsx|vue)|ui/|form|button|modal|dialog|input|menu|navigation|toast|alert|dropdown|select|checkbox|radio|slider|toggle|tooltip|popover|layout|responsive|mobile|accessibility|a11y|wcag|usability|ux|user.experience"; then
  AGENTS_TO_INVOKE="$AGENTS_TO_INVOKE ux-specialist"
  echo "UI work detected - UX heuristic review included"
fi

echo "=== Agents to invoke in parallel: $AGENTS_TO_INVOKE ==="
```

#### Step 2: Invoke Agents in Parallel

**CRITICAL: Use Task tool to invoke ALL agents simultaneously in a SINGLE message with multiple tool calls.**

For each agent in $AGENTS_TO_INVOKE:

**test-specialist** (always):
- subagent_type: "psd-claude-coding-system:test-specialist"
- description: "Test strategy for issue #$ISSUE_NUMBER"
- prompt: "Design comprehensive test strategy for: $ISSUE_BODY. Include unit tests, integration tests, edge cases, and mock requirements."

**security-analyst-specialist** (if security-sensitive):
- subagent_type: "psd-claude-coding-system:security-analyst-specialist"
- description: "PRE-IMPLEMENTATION security guidance for #$ISSUE_NUMBER"
- prompt: "Provide security guidance BEFORE implementation for: $ISSUE_BODY. Focus on requirements to follow, pitfalls to avoid, secure patterns, and security testing."

**[domain]-specialist** (if detected):
- subagent_type: "psd-claude-coding-system:[backend/frontend/database/llm]-specialist"
- description: "[Domain] implementation guidance for #$ISSUE_NUMBER"
- prompt: "Provide implementation guidance for: $ISSUE_BODY. Include architecture patterns, best practices, common mistakes, and integration points."

**ux-specialist** (if UI work detected):
- subagent_type: "psd-claude-coding-system:ux-specialist"
- description: "UX heuristic review for #$ISSUE_NUMBER"
- prompt: "Evaluate UX considerations for: $ISSUE_BODY. Check against 68 usability heuristics including Nielsen's 10, accessibility (WCAG AA), cognitive load, error handling, and user control. Provide specific recommendations."

#### Step 3: Synthesize Agent Recommendations

After all agents return, synthesize their insights into an implementation plan:
- Combine test strategy with implementation approach
- Integrate security requirements into design
- Follow domain-specific best practices
- Create unified implementation roadmap

### Phase 3: Implementation

Based on synthesized agent recommendations and issue requirements, implement the solution:
- Check local CLAUDE.md for project-specific conventions
- Follow established architecture patterns from agents
- Implement security requirements from security-analyst (if provided)
- Follow test strategy from test-specialist
- Apply domain best practices from specialist agents
- Maintain type safety (no `any` types)

```bash
```

### Phase 4: Testing & Validation

#### Automated Testing
```bash
# Write tests if needed (invoke @agents/test-specialist for complex tests)
# The agent will provide test templates and strategies

# Run all tests
npm test || yarn test

# Run specific test suites
npm run test:unit
npm run test:integration
npm run test:e2e

# Check test coverage
npm run test:coverage
# Ensure coverage meets threshold (usually 80%)
```

#### Pre-commit Validation
```bash
# Type checking - MUST pass
npm run typecheck || yarn typecheck

# Linting - MUST pass
npm run lint || yarn lint
npm run lint:fix  # Auto-fix what's possible

# Security audit
npm audit || yarn audit

# Performance check (if applicable)
npm run build
# Check bundle size didn't increase significantly
```

#### When to Invoke Specialists
- **Complex test scenarios**: Invoke @agents/test-specialist
- **Performance concerns**: Invoke @agents/performance-optimizer
- **Security features**: Invoke @agents/security-analyst
- **API documentation**: Invoke @agents/documentation-writer
- **UI/UX evaluation**: Invoke @agents/ux-specialist for heuristic review

#### Phase 4.3: Language-Specific Review (NEW - Pre-PR Light Review)

**Detect languages from changed files** and invoke appropriate language reviewers in LIGHT mode:

```bash
# Get list of changed files
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || echo "")

# Detect languages
HAS_TYPESCRIPT=$(echo "$CHANGED_FILES" | grep -E '\.(ts|tsx|js|jsx)$' | head -1)
HAS_PYTHON=$(echo "$CHANGED_FILES" | grep -E '\.py$' | head -1)
HAS_SWIFT=$(echo "$CHANGED_FILES" | grep -E '\.swift$' | head -1)
HAS_SQL=$(echo "$CHANGED_FILES" | grep -E '\.sql$' | head -1)
HAS_MIGRATION=$(echo "$CHANGED_FILES" | grep -iE 'migration' | head -1)

echo "=== Language-Specific Pre-PR Review ==="
[ -n "$HAS_TYPESCRIPT" ] && echo "  TypeScript/JavaScript detected"
[ -n "$HAS_PYTHON" ] && echo "  Python detected"
[ -n "$HAS_SWIFT" ] && echo "  Swift detected"
[ -n "$HAS_SQL" ] && echo "  SQL detected"
[ -n "$HAS_MIGRATION" ] && echo "  Migration files detected"
```

**Invoke language reviewers in parallel (LIGHT MODE):**

If TypeScript/JavaScript detected:
- subagent_type: "psd-claude-coding-system:typescript-reviewer"
- description: "Light TS review for #$ISSUE_NUMBER"
- prompt: "LIGHT MODE review: Quick check TypeScript/JavaScript changes for: type safety issues, obvious bugs, missing error handling. Files: $CHANGED_FILES"

If Python detected:
- subagent_type: "psd-claude-coding-system:python-reviewer"
- description: "Light Python review for #$ISSUE_NUMBER"
- prompt: "LIGHT MODE review: Quick check Python changes for: type hints, obvious bugs, PEP8 issues. Files: $CHANGED_FILES"

If Swift detected:
- subagent_type: "psd-claude-coding-system:swift-reviewer"
- description: "Light Swift review for #$ISSUE_NUMBER"
- prompt: "LIGHT MODE review: Quick check Swift changes for: optionals handling, memory issues, Swift conventions. Files: $CHANGED_FILES"

If SQL detected:
- subagent_type: "psd-claude-coding-system:sql-reviewer"
- description: "Light SQL review for #$ISSUE_NUMBER"
- prompt: "LIGHT MODE review: Quick check SQL changes for: injection risks, performance issues, missing indexes. Files: $CHANGED_FILES"

**Fix any critical issues** identified by language reviewers before proceeding.

#### Phase 4.4: Deployment Verification (NEW - Conditional)

**Only if migration or schema files detected:**

```bash
# Check for high-risk deployment changes
if echo "$CHANGED_FILES" | grep -iEq "migration|schema|\.sql"; then
  echo "=== Migration/Schema Changes Detected ==="
  echo "Invoking deployment verification agent..."
  NEEDS_DEPLOYMENT_CHECKLIST=true
fi
```

If migrations detected:
- subagent_type: "psd-claude-coding-system:deployment-verification-agent"
- description: "Deployment checklist for #$ISSUE_NUMBER"
- prompt: "Generate Go/No-Go deployment checklist for PR with migration/schema changes. Include rollback plan, validation queries, and risk assessment."

If migrations detected:
- subagent_type: "psd-claude-coding-system:data-migration-expert"
- description: "Migration validation for #$ISSUE_NUMBER"
- prompt: "Validate data migration: Check foreign key integrity, ID mappings, and data transformation logic. Provide pre/post deployment validation queries."

**Include deployment checklist in PR body** if generated.

```bash
```

### Phase 5: Commit & PR Creation
```bash
# Stage and commit
git add -A

if [ "$WORK_TYPE" = "issue" ]; then
  # Commit for issue
  git commit -m "feat: implement solution for #$ISSUE_NUMBER

- [List key changes]
- [Note any breaking changes]

Closes #$ISSUE_NUMBER"

  # Push to remote
  git push origin feature/$ISSUE_NUMBER-brief-description

  # Create PR for issue
  gh pr create \
    --base dev \
    --title "feat: #$ISSUE_NUMBER - [Descriptive Title]" \
    --body "## Description
Implements solution for #$ISSUE_NUMBER

## Changes
- [Key change 1]
- [Key change 2]

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project conventions
- [ ] No TypeScript errors
- [ ] Tests added/updated
- [ ] Documentation updated if needed

Closes #$ISSUE_NUMBER" \
    --assignee "@me"
else
  # Commit for quick fix
  git commit -m "fix: $ARGUMENTS

- [Describe what was fixed]
- [Note any side effects]"

  # Push to remote
  git push origin HEAD

  # Create PR for quick fix
  gh pr create \
    --base dev \
    --title "fix: $ARGUMENTS" \
    --body "## Description
Quick fix: $ARGUMENTS

## Changes
- [What was changed]

## Testing
- [ ] Tests pass
- [ ] Manually verified fix

## Type of Change
- [x] Bug fix (non-breaking change)
- [ ] New feature
- [ ] Breaking change" \
    --assignee "@me"
fi

echo "PR created successfully"
```

### Summary

```bash
PR_NUMBER=$(gh pr list --author "@me" --limit 1 --json number --jq '.[0].number')

echo ""
echo "Work completed successfully!"
echo "PR #$PR_NUMBER created and ready for review"
echo ""
echo "Key improvements in v1.14.0:"
echo "  - Knowledge lookup searched past learnings (Phase 1.5)"
echo "  - Language-specific pre-PR review caught issues early (Phase 4.3)"
echo "  - Deployment verification for migrations (Phase 4.4)"
echo "  - Security review happened PRE-implementation (fewer surprises)"
echo "  - Parallel agent analysis provided comprehensive guidance"
echo "  - Test strategy defined before coding"
echo ""
```

## Quick Reference

### Common Patterns
```bash
# Check file structure
find . -type f -name "*.ts" -o -name "*.tsx" | grep -E "(components|actions|lib)" | head -20

# Find similar implementations
grep -r "pattern" --include="*.ts" --include="*.tsx" --exclude-dir=node_modules

# Check for existing tests
find . -name "*.test.ts" -o -name "*.spec.ts" | grep -v node_modules
```

### Project Detection
```bash
# Detect framework
test -f next.config.js && echo "Next.js project"
test -f vite.config.ts && echo "Vite project"
test -f angular.json && echo "Angular project"

# Check for project docs
test -f CLAUDE.md && echo "Project conventions found"
test -f CONTRIBUTING.md && echo "Contributing guide found"
```

## Best Practices

1. **Always branch from `dev`**, never from `main`
2. **Reference the issue number** in commits and PR
3. **Run quality checks** before committing
4. **Use specialized agents** for complex domains
5. **Follow project conventions** in CLAUDE.md
6. **Write tests** for new functionality
7. **Update documentation** when changing APIs

## Agent Collaboration Protocol

When invoking agents:
1. Save current progress with a commit
2. Pass issue number to agent: `@agents/[agent].md #$ARGUMENTS`
3. Incorporate agent's recommendations
4. Credit agent contribution in commit message

## Success Criteria

- Issue requirements fully implemented
- All tests passing
- No linting or type errors
- PR created to `dev` branch
- Issue will auto-close when PR merges

Remember: Quality over speed. Use agents for expertise beyond general development.
