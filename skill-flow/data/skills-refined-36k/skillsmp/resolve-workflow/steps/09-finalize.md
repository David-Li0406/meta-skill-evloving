---
name: finalize
description: Push branch and create pull request
order: 9

skip_if:
  - mode: "INTERACTIVE"
    unless: "--pr"

next:
  default: STOP

tools:
  - Read
  - Bash
  - AskUserQuestion
---

# Step: Finalize

<context>
This step pushes the branch to remote and creates a pull request.
In AUTO mode, this happens automatically. In INTERACTIVE mode,
the user manages push/PR unless --pr flag is specified.
</context>

## Instructions

<instructions>

### 1. Check Mode

- **AUTO mode**: Proceed with push and PR
- **INTERACTIVE mode without --pr**: STOP (user manages)
- **INTERACTIVE mode with --pr**: Proceed with push and PR

### 2. Apply Create-PR Skill

Apply skill: `~/.claude/skills/create-pr/SKILL.md`

### 3. Push Branch

```bash
git push -u origin {branch-name}
```

### 4. Check for Existing PR

```bash
gh pr list --head {branch-name} --json number,url
```

If PR exists, display URL and skip creation.

### 5. Determine Target Branch

Priority order:
1. `--target` flag if provided
2. `status.json` → `options.base_branch`
3. `ticket.md` → Target Branch metadata (from milestone parsing)
4. Branch pattern matching
5. Project config fallback (`branches.default_base`)

### 6. Gather PR Context

Load for PR body:
- Ticket summary from `ticket.md`
- Implementation summary from `plan.md`
- Visual warnings from `status.json` (if any)

### 7. Create PR

```bash
gh pr create \
  --title "{ticket-id}: {title}" \
  --body "{PR body}" \
  --base {target-branch} \
  {--draft if configured}
```

**PR Body Template**:
```markdown
## Summary

{Brief description from ticket}

## Changes

{List of key changes from plan phases}

## Test Plan

- [ ] {validation steps from plan}

## Visual Verification

{If visual_warnings exist, list them here}
{If Figma URLs available, link them}
```

### 8. Handle PR Options (INTERACTIVE with --pr)

```yaml
AskUserQuestion:
  question: "Options pour la PR ?"
  header: "PR"
  options:
    - label: "Draft (recommande)"
      description: "Creer en brouillon pour review"
    - label: "Ready for review"
      description: "Marquer comme prete pour review"
```

### 9. Display Result

```markdown
## Pull Request Created

- **URL**: {pr_url}
- **Target**: {target-branch}
- **Status**: {draft/ready}

Prochaines etapes:
1. Reviewer la PR sur GitHub
2. Demander une review si necessaire
3. Merger apres approbation
```

### 10. Update Status

Update status: `phases.finalize = "completed"`, `state = "finalized"`, `pr_url = "{url}"`

</instructions>

## Output

<output>
- Branch pushed to remote
- PR created (draft by default)
- PR URL displayed
- Status: `phases.finalize = "completed"`, `state = "finalized"`
</output>

## Auto Behavior

<auto_behavior>
- Push branch automatically
- Create draft PR by default (`pr.draft_by_default = true`)
- Use auto-detected target branch
- Include visual warnings in PR body if any
</auto_behavior>

## Interactive Behavior

<interactive_behavior>
Without `--pr` flag:
- STOP after review, user manages push/PR

With `--pr` flag:
- Prompt for PR options (draft/ready)
- Prompt for target branch confirmation
- Create PR and display URL
</interactive_behavior>

## Error Handling

<constraints>
| Error | Message |
|-------|---------|
| Push failed | Verifiez votre authentification git |
| PR creation failed | Verifiez vos droits sur le repository |
| Target branch not found | La branche cible n'existe pas |
</constraints>
