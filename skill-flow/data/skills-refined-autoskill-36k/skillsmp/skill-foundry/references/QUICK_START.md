# Quick Start: Creating Your First Skill

## 5-Minute Skill

1. **Decide what your skill does** (one sentence)
2. **Write the description** (what + when)
3. **Create the file**
   ```bash
   mkdir -p .claude/skills/my-skill
   cd .claude/skills/my-skill
   touch SKILL.md
   ```
4. **Write SKILL.md**
   ```yaml
   ---
   name: my-skill
   description: Does X when Y. Use when the user mentions Z.
   ---
   
   # My Skill
   
   ## When to Use
   - Trigger condition 1
   - Trigger condition 2
   
   ## Commands
   - `command --flag`
   - `another-command arg`
   
   ## Process
   1. Step 1
   2. Step 2
   3. Step 3
   ```
5. **Test it**
   ```
   @claude I need help with [task that triggers your skill]
   ```

## Example: API Testing Skill

```yaml
---
name: api-testing
description: Run API tests using pytest against staging environment. Use when testing endpoints, validating API responses, or checking against OpenAPI specs. Never tests against production.
---

# API Testing Skill

## When to Use
- Testing API endpoints
- Validating API responses
- Checking against OpenAPI specs
- Writing new API tests

## Commands
- Run all API tests: `pytest tests/api/ -v`
- Run specific test: `pytest tests/api/test_users.py -v`
- List tests: `pytest --collect-only tests/api/`

## Process
1. Identify the endpoint to test
2. Check OpenAPI spec in `/docs/api/openapi.yaml`
3. Write test in `tests/api/test_<resource>.py`
4. Run test against staging
5. Verify response matches spec

## Boundaries
✅ Test against staging environment
⚠️ Ask before modifying test fixtures
🚫 Never test against production
🚫 Never modify API source code
```

## Next Steps

- Read [BEST_PRACTICES.md](BEST_PRACTICES.md) for depth
- Read [SKILL_ANATOMY.md](SKILL_ANATOMY.md) to understand progressive disclosure
- Use the scaffold script for more complex skills:
  ```bash
  python scripts/scaffold.py my-skill "Description here"
  ```
- Iterate based on real usage (test and refine)

## Common Patterns

### Pattern: Command Reference Skill
Good for: Documenting project-specific CLI tools

```yaml
---
name: cli-reference
description: Reference for custom CLI commands and flags
---

## Commands
- Build: `npm run build -- --prod`
- Test: `npm test -- --watch`
- Deploy: `./scripts/deploy.sh staging`
```

### Pattern: Code Style Skill
Good for: Enforcing team conventions

```yaml
---
name: code-style
description: Team code style conventions and examples
---

## Examples

✅ Good:
```typescript
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

❌ Bad:
```typescript
function calc(i) {
  let s = 0;
  for (let x of i) s += x.price;
  return s;
}
```
```

### Pattern: Workflow Skill
Good for: Multi-step processes

```yaml
---
name: release-process
description: Step-by-step release workflow
---

## Process
1. Update CHANGELOG.md
2. Bump version in package.json
3. Run tests: `npm test`
4. Create tag: `git tag v1.2.3`
5. Push: `git push --tags`
6. Create GitHub release
```

## Validation

Before using your skill in production:

```bash
# Validate structure
python .claude/skills/skill-foundry/scripts/validate.py .claude/skills/my-skill/SKILL.md

# Test with Claude
# - Create a test conversation
# - Try tasks that should trigger the skill
# - Verify Claude uses it correctly

# Refine
# - Add examples if Claude misunderstands
# - Clarify boundaries if it does wrong things
# - Add commands if it asks how to do things
```

## Tips

- **Start small**: Don't try to document everything at once
- **Test early**: Create the skill, test it immediately, then expand
- **Use examples**: One good example beats paragraphs of explanation
- **Set boundaries**: Tell Claude what NOT to do (prevents mistakes)
- **Iterate**: Skills improve through real usage, not upfront planning
