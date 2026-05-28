# Lessons from 2,500+ Agent Files

Distilled from GitHub's analysis of agents.md files across public repositories.

## What Works

### 1. Put Commands Early
- Include executable commands, not just tool names
- Add flags and options: `npm test --coverage`, not just "run tests"
- Commands agents can actually run

### 2. Code Examples Over Explanations
- One real snippet beats three paragraphs
- Show what good output looks like
- Include both ✅ good and ❌ bad examples

### 3. Set Clear Boundaries
- Use three tiers: Always / Ask First / Never
- "Never commit secrets" - most common helpful constraint
- Be explicit about what NOT to touch

### 4. Be Specific About Stack
- Include versions: "React 18 with TypeScript"
- List key dependencies
- Name the actual tools, not categories

### 5. Cover Six Core Areas
1. **Commands**: Executable instructions
2. **Testing**: How to run and write tests
3. **Project Structure**: Where files live
4. **Code Style**: Examples of good patterns
5. **Git Workflow**: Branching, commits, PRs
6. **Boundaries**: What to avoid

## Boundary Template

```markdown
## Boundaries

✅ **Always do:**
- Write to designated directories
- Run tests before commits
- Follow naming conventions

⚠️ **Ask first:**
- Database schema changes
- Adding dependencies
- Modifying CI/CD config

🚫 **Never do:**
- Commit secrets or API keys
- Edit node_modules/ or vendor/
- Modify files outside scope
```

## Persona + Operating Manual

The best agents have:
1. A **specific persona** (not "helpful assistant")
2. A **detailed operating manual** with:
   - Executable commands
   - Concrete code examples
   - Explicit boundaries
   - Tech stack specifics

## Iteration Over Planning

> "The best agent files grow through iteration, not upfront planning."

Start simple:
1. Create minimal agent/skill
2. Test it on real tasks
3. Add detail when it makes mistakes
4. Repeat

## Example Agent Structure

```markdown
---
name: test-agent
description: Writes unit tests for TypeScript functions using Jest
---

You are a QA engineer who writes comprehensive tests.

## Commands
- Run tests: `npm test`
- Coverage: `npm test -- --coverage`
- Single file: `npm test -- path/to/file.test.ts`

## Style Example
```typescript
// ✅ Good - descriptive, handles edge cases
describe('calculateTotal', () => {
  it('returns 0 for empty cart', () => {
    expect(calculateTotal([])).toBe(0);
  });
  
  it('sums item prices correctly', () => {
    const items = [{price: 10}, {price: 20}];
    expect(calculateTotal(items)).toBe(30);
  });
});
```

## Boundaries
✅ Write to `tests/` directory
⚠️ Ask before modifying test config
🚫 Never modify source code in `src/`
🚫 Never delete failing tests
```

## Source Attribution

This document distills lessons from:
- [How to Write a Great agents.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/)
