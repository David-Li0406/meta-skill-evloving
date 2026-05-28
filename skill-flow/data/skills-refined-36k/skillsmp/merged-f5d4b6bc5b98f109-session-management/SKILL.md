---
name: session-management
description: Use this skill to complete verification steps before starting or ending a work session.
---

# Session Management Checklist

## Session Begin Checklist

**⚠️ IMPORTANT - Duplicate Detection:**

Before proceeding with the full checklist, check if this session was already started:

1. **Read the current conversation context** - Have I already completed this checklist in the current conversation?
2. **Check SESSION_CONTEXT.md timestamp** - Was "Last Updated" modified today?
3. **Check session counter** - Did I already increment the session counter earlier in this conversation?

**If ANY of these are true:**

- ✅ Session is already active
- ⚠️ DO NOT re-run the checklist
- ⚠️ DO NOT re-increment the session counter
- ⚠️ DO NOT re-run startup scripts
- 💬 Example response: "Session already active. Checklist completed earlier. What would you like to work on?"

**If ALL are false:**

- ✅ This is a new session
- ✅ Proceed with full checklist below

---

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
2. **Run the decrypt command** using stdin:
   ```bash
   echo "<user_passphrase>" | node scripts/secrets/decrypt-secrets.js --stdin
   ```
3. **Verify success** - Check that `.env.local` now exists with tokens
4. **Never store or log the passphrase** - Only use it for the decrypt command

**If secrets are already decrypted or no encrypted file exists:**

- Skip this step and continue to Context Loading

---

### 1. Context Loading (MANDATORY)

- [ ] Read [SESSION_CONTEXT.md](../../SESSION_CONTEXT.md) - Current status, active blockers, next goals
- [ ] Increment session counter in [SESSION_CONTEXT.md](../../SESSION_CONTEXT.md)
- [ ] Check [ROADMAP.md](../../ROADMAP.md) for priority changes

### 1b. Stale Documentation Check (MANDATORY - NEW)

**Documentation often drifts from reality.** Before trusting any status in docs, verify against actual commits:

```bash
# Check recent commits to see actual work done
git log --oneline -30
```

**Compare commits against documented status:**

1. Look for PR/feature commits (e.g., "PR7:", "refactor:", "fix:")
2. Cross-reference with INTEGRATED_IMPROVEMENT_PLAN.md task checkboxes
3. If commits show work done but docs show incomplete → **UPDATE THE DOCS**

### 2. Consolidation Status Check

Check [AI_REVIEW_LEARNINGS_LOG.md](../../docs/AI_REVIEW_LEARNINGS_LOG.md) for the "Consolidation Trigger" section:

- If "Reviews since last consolidation" >= 10: **⚠️ CONSOLIDATION WAS MISSED**

**If consolidation was missed:**

1. Note this in your session summary
2. The patterns are still available in AI_REVIEW_LEARNINGS_LOG.md (read if needed)
3. Consolidation will happen at THIS session's end

### 3. Documentation & Planning Awareness

- [ ] Check [INTEGRATED_IMPROVEMENT_PLAN.md](../../docs/archive/completed-plans/INTEGRATED_IMPROVEMENT_PLAN.md) for current step

### 4. Skill Selection (BEFORE starting work)

```
DECISION TREE:
├─ Bug/Error? → Use 'systematic-debugging' skill FIRST
├─ Writing code? → Use 'code-reviewer' agent AFTER completion
├─ Security work? → Use 'security-auditor' agent
├─ UI/Frontend? → Use 'frontend-design' skill
├─ Complex task? → Check available skills with /skills
└─ Multi-step task? → Use TodoWrite to track progress
```

### 5. Code Review Handling Procedures

When receiving code review feedback:

1. **Analyze ALL suggestions** - Read through every comment multiple times
2. **Create TodoWrite checklist** - Track each suggestion as a task
3. **Address systematically** - Don't skip items; mark as resolved or note why skipped
4. **Verify CI impact** - Check if changes affect workflows
5. **Test after changes** - Run `npm test` and `npm run lint` before committing

### 6. Anti-Pattern Awareness

**Before writing code**, scan relevant documentation for critical anti-patterns. Key patterns:

- **Read before edit** - Always read files before attempting to edit
- **Regex performance** - Avoid greedy `.*` in patterns; use bounded `[\s\S]{0,N}?`
- **ESLint flat config** - Spread plugin configs, don't use directly
- **Path-based filtering** - Add pathFilter for directory-specific patterns

### 7. Session Start Scripts (AUTO-RUN)

**Execute these scripts automatically** when processing this command:

```bash
npm run patterns:check
npm run review:check
npm run lessons:surface
```

**Important**: These scripts are **required**. If any script fails:

1. Note the error in session summary
2. Investigate if it's a real issue vs missing script

---

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

### 3. Documentation Updates

- [ ] Update SESSION_CONTEXT.md with:
  - Work completed this session
  - Any new blockers discovered
  - Next steps for future sessions
- [ ] If applicable, update INTEGRATED_IMPROVEMENT_PLAN.md with step progress
- [ ] Log any significant learnings in AI_REVIEW_LEARNINGS_LOG.md

### 4. Learning Consolidation (AUTOMATIC)

Consolidation now runs **automatically** during SessionStart when the threshold is reached (10+ reviews). No manual action required.

### 5. Code Review Completeness Audit

If you received code review feedback this session:

```
VERIFICATION CHECKLIST:
├─ Did you address ALL suggestions? (not just some)
├─ Did you test regex patterns for performance?
└─ Did you commit descriptive messages explaining WHY changes were made?
```

### 6. Automated Verification (RUN BEFORE MANUAL AUDIT)

Execute these automated checks to verify session compliance:

```bash
npm run skills:verify-usage
npm run triggers:check
npm run session:summary
```

### 7. Agent/Skill/MCP/Hook/Script Audit (MANDATORY)

**Complete this audit for every session. If gaps found, document why or fix before ending.**

### 8. Key Learnings to Remember

Today's session reinforced these patterns:

### DO:

- Read files before editing
- Use TodoWrite for multi-step tasks
- Check all code review items multiple times

### DON'T:

- Skip code review suggestions without documenting why
- Forget to test changes before committing

---

Session complete. All work has been verified and documented.