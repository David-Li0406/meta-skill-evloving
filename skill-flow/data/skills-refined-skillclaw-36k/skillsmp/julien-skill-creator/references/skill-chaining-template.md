# Skill Chaining Template

Skills rarely work in isolation. Document how skills interact using this standardized format.

## Template Structure

Add a **"Skill Chaining"** section at the end of SKILL.md with these subsections:

```markdown
## Skill Chaining

### Skills Required Before
- **skill-name** (obligatoire|recommandé|optionnel): Why needed

### Input Expected
- Format: file path, URL, Git state, env var, etc.
- Environment: Node.js version, SSH access, etc.
- Config: Required files, API keys, etc.

### Output Produced
- **Format**: file path, deployed URL, report format
- **Side effects**: git commits, file changes, etc.
- **Duration**: Estimated time

### Compatible Skills After
**Obligatoires**: Must follow (workflow breaks without)
**Recommandés**: Should follow for best results
**Optionnels**: Can follow in some scenarios

### Called By
- Parent skills that invoke this one
- Git hooks (pre-push.sh, post-merge.sh)
- Direct user invocation scenarios

### Tools Used
- `ToolName` (usage: brief description)

### Visual Workflow
```
[Previous action]
    ↓
[THIS SKILL]
    ├─► Action 1
    └─► Action 2
    ↓
[Next skills]
```

### Usage Example
**Scenario**: Real-world situation
**Command**: Exact invocation
**Result**: Expected outcome
```

## Complete Example

```markdown
## Skill Chaining

### Skills Required Before
- **local-testing** (recommandé): Validates code before deployment

### Input Expected
- Git branch: `main` (production) or `staging` (preview)
- Code validated: build succeeded, TypeScript check passed
- SSH access: `automation@69.62.108.82` configured
- File: `ecosystem.config.cjs` exists on VPS

### Output Produced
- **Format**: Application deployed and running on VPS
- **Side effects**:
  - PM2 process restarted
  - New Git commit checked out on VPS
  - npm dependencies installed/updated
- **Duration**: 2-3 minutes

### Compatible Skills After
**Recommandés:**
- **accessibility-audit**: Audit WCAG compliance
- **image-optimization**: Optimize new images

**Optionnels:**
- **performance-monitoring**: Check Lighthouse scores

### Called By
- **git-workflow-manager**: During deployment workflows
- **post-push.sh hook**: After `git push origin staging|main`
- Direct invocation: Manual deployment

### Tools Used
- `Bash` (usage: rsync, ssh, npm, pm2 commands)
- `Read` (usage: verify config exists)
- `AskUserQuestion` (usage: confirm risky deployments)

### Visual Workflow
```
User: git push origin staging
    ↓
pre-push.sh hook
    ├─► npm run build
    └─► npm run check
    ↓
deployment-manager (this skill)
    ├─► rsync local → VPS
    ├─► npm install
    ├─► npm run build
    └─► pm2 restart
    ↓
Site deployed
    ├─► accessibility-audit (recommended)
    └─► performance-monitoring (optional)
```

### Usage Example
**Scenario**: Deploy feature to preview
**Command**: `git push origin staging`
**Result**: Site updated on https://preview.example.com in ~2-3 minutes
```

## Why Skill Chaining Matters

1. **Discoverability**: Know which skill to use next
2. **Workflow clarity**: See how skills connect
3. **Bidirectional docs**: If A calls B, both mention each other
4. **Debugging**: Clear I/O helps diagnose issues
5. **Onboarding**: Understand complete workflow
