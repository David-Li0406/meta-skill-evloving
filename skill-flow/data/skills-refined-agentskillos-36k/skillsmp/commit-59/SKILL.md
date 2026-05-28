---
name: Commit
description: AI-optimized atomic commit protocol. Uses deterministic rules for autonomous execution.
---
**CORE PRINCIPLE: ONE logical change = ONE commit. Always.**

## 🎯 QUICK START FOR AI
Execute this exact sequence for ANY commit task:

1. **ANALYZE** → Run `git diff --name-status` to list changed files
2. **CATEGORIZE** → Group files by logical units (use table below)
3. **VALIDATE** → Check: "Can I describe ALL these changes in ONE sentence?"
4. **COMMIT** → Apply template from section below
5. **REPEAT** → Loop until `git diff` is empty

## 🔧 LOGICAL GROUPING RULES (Deterministic)
Use FIRST matching rule:

| Change Pattern | Logical Unit | Example |
|----------------|--------------|---------|
| Same file + same function | SINGLE unit | `user.py:get_user()` changes = 1 commit |
| Different files + same feature | SINGLE unit | `auth.py` + `login.html` for login feature = 1 commit |
| Same file + unrelated functions | SEPARATE units | `utils.py` (fix log + add validation) = 2 commits |
| Fix + feature in same area | SEPARATE units | Fix bug in auth + add OAuth = 2 commits |

**Exception**: If total changes <15 lines AND same logical context → allow single commit.

## 📝 COMMIT TEMPLATE (Copy-Paste Ready)
```bash
# STANDARD (90% of cases)
git commit -m "type(scope): description" \
  -m "" \
  -m "What: [1-sentence change summary]" \
  -m "Why: [1-sentence reason]"

# WITH ISSUE (when ticket exists)
git commit -m "type(scope): description" \
  -m "" \
  -m "What: [summary]" \
  -m "Why: [reason]" \
  -m "" \
  -m "Closes #[number]"

# BREAKING CHANGE (API/database changes)
git commit -m "type(scope)!: description" \
  -m "" \
  -m "What: [summary]" \
  -m "Why: [reason]" \
  -m "" \
  -m "BREAKING CHANGE: [specific impact]"
```

## 🎨 TYPE & SCOPE DECISION TREE
**Type Selection** (pick first match):
- Adds new functionality → `feat`
- Fixes incorrect behavior → `fix`
- Changes formatting/styling only → `style`
- Restructures code without behavior change → `refactor`
- Updates documentation → `docs`
- Adds/modifies tests → `test`
- Other maintenance → `chore`

**Scope Inference** (from file path):
- `src/auth/` → `auth`
- `components/ui/` → `ui`
- `api/` or `routes/` → `api`
- `tests/` → `tests`
- `docs/` → `docs`
- Default: use parent directory name

## ⚡ QUICK REFERENCE CARD
Keep this visible during execution:

### ✅ DO
- One logical change per commit
- Use imperative mood (add, fix, update)
- Keep description <72 chars
- Include "What & Why" in body
- Auto-infer scope from path

### ❌ DON'T
- Mix feature + fix
- Use past tense (added, fixed)
- Write vague descriptions ("update", "fix stuff")
- Bundle unrelated changes

### 🚨 RED FLAGS (Stop and split)
- Changes touch >3 unrelated files
- Commit message needs "and" or "also"
- Diff shows mixed concerns (UI + API + tests)

## 🔄 AUTO-CORRECTION PROTOCOL
If commit violates rules → execute immediately:
```bash
git reset HEAD~1
# Return to ANALYZE step with remaining changes
```

## 📊 VALIDATION CHECKLIST (Pre-Commit)
- [ ] Single logical change? (1-sentence test)
- [ ] Description imperative and <72 chars?
- [ ] Scope inferred correctly?
- [ ] Body has "What & Why"?
- [ ] Breaking changes marked with `!`?

## 🎲 DECISION EXAMPLES
**Scenario 1**: Changed `user.py` (add email validation) and `test_user.py` (add tests)
- ✅ CORRECT: 2 commits: `feat(user): add email validation` + `test(user): add validation tests`

**Scenario 2**: Changed `style.css` (colors) and `layout.css` (spacing) for dark mode
- ✅ CORRECT: 1 commit: `style(ui): implement dark mode colors and spacing`

**Scenario 3**: Fixed bug in `auth.js` AND added new login method in same file
- ✅ CORRECT: 2 commits: `fix(auth): resolve session timeout` + `feat(auth): add biometric login`