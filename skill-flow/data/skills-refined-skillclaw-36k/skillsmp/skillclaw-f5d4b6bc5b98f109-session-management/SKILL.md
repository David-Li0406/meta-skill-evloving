---
name: session-management
description: Use this skill to complete verification steps before starting or ending a work session.
---

# Skill body

## Session Begin Checklist

**⚠️ IMPORTANT - Duplicate Detection:**

Before proceeding with the full checklist, check if this session was already started:

1. **Read the current conversation context** - Have I already completed this checklist in the current conversation?
2. **Check SESSION_CONTEXT.md timestamp** - Was "Last Updated" modified today?
   - **Note**: Field stores date only (YYYY-MM-DD), not time.
3. **Check session counter** - Did I already increment the session counter earlier in this conversation?

**If ANY of these are true:**

- ✅ Session is already active
- ⚠️ DO NOT re-run the checklist
- ⚠️ DO NOT re-increment the session counter
- ⚠️ DO NOT re-run startup scripts
- 💬 Example response: "Session #35 already active (started earlier in this conversation). Checklist completed earlier. What would you like to work on?"

**If ALL are false:**

- ✅ This is a new session
- ✅ Proceed with full checklist below

### 0. Secrets Decryption Check (REMOTE SESSIONS)

**Check if MCP tokens need decrypting:**

```bash
# Check secrets status
if [ -f ".env.local.encrypted" ] && [ ! -f ".env.local" ]; then
  echo "⚠️ Encrypted secrets found but not decrypted"
fi
```

**If secrets need decrypting:**

1. **Ask the user for their passphrase** - Example: "Your MCP tokens need decrypting. What's your passphrase?"
2. **Run the decrypt command** using stdin (avoids shell history exposure):
   ```bash
   echo "<user_passphrase>" | node scripts/secrets/decrypt-secrets.js --stdin
   ```
3. **Verify success** - Check that `.env.local` now exists with tokens
4. **Never store or log the passphrase** - Only use it for the decrypt command

**If secrets are already decrypted or no encrypted file exists:**

- Skip this step and continue to Context Loading

## Session End Checklist

Before ending the session, complete these verification steps:

### 1. Work Verification

- [ ] All TodoWrite items marked as completed or documented as blocked
- [ ] All commits pushed to remote branch
- [ ] All code review suggestions addressed or documented as skipped (with reason)
- [ ] Tests pass: `npm test`
- [ ] Lint passes: `npm run lint`
- [ ] Pattern check passes: `npm run patterns:check`

### 2. CI Verification

If you modified any of these, verify they still work:

- [ ] `.github/workflows/ci.yml` - Main CI pipeline
- [ ] `.github/workflows/docs-lint.yml` - Documentation linting
- [ ] `scripts/check-docs-light.js` - Doc linter script
- [ ] `scripts/check-pattern-compliance.js` - Pattern checker
- [ ] `eslint.config.mjs` - ESLint configuration

### 3. Documentation Updates

- [ ] Update SESSION_CONTEXT.md with:
  - Work completed this session
  - Any new blockers discovered
  - Next steps for future sessions
- [ ] If applicable, update INTEGRATED_IMPROVEMENT_PLAN.md with step progress
- [ ] Log any significant learnings in AI_REVIEW_LEARNINGS_LOG.md
- [ ] Archive completed/cancelled plans to `docs/archive/completed-plans/`
- [ ] **Cross-document check**: Review docs modified this session against [DOCUMENT_DEPENDENCIES.md](../../docs/DOCUMENT_DEPENDENCIES.md#cross-document-update-triggers) trigger matrix - update any dependent documents

### 3.1 Roadmap Sync Check (MANDATORY for Feature Work)

If you implemented features, completed tasks, or made significant progress this session:

- [ ] **Verify ROADMAP.md reflects current status**
  - Check Active Sprint tasks - mark completed items with `[x]`
  - Check M1.6/M2 phase tasks - update status indicators
  - Update sprint progress percentage if significant work done
- [ ] **No new features without roadmap entry**
  - If you added a new feature not in ROADMAP.md, add it now
  - If you completed a planned feature, mark it done

**Quick Check:**

```bash
# See what code was changed this session
git diff --name-only HEAD~5

# If you see new components/features, verify they're in ROADMAP.md
```