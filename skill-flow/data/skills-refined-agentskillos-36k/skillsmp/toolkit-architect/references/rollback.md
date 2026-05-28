# Rollback Procedures

## Table of Contents

- [When to Rollback](#when-to-rollback)
- [Rollback Methods](#rollback-methods)
- [Rollback Safety](#rollback-safety)
- [Emergency Rollback](#emergency-rollback)
- [Rollback Verification](#rollback-verification)
- [Post-Rollback Actions](#post-rollback-actions)
- [Rollback Documentation](#rollback-documentation)
- [Incident](#incident)
- [Scope](#scope)
- [Actions Taken](#actions-taken)
- [Outcome](#outcome)
- [Lessons Learned](#lessons-learned)
- [Prevention Strategies](#prevention-strategies)

## When to Rollback

### Critical Issues
- Plugin no longer functions
- Major regressions introduced
- Data corruption occurred
- Security vulnerabilities created
- Quality score decreased

### Decision Criteria
- Impact: High severity
- Reversibility: Changes can be undone
- Risk: Continued use unsafe
- Effort: Rollback easier than fix

---

## Rollback Methods

### Method 1: Full Plugin Rollback

**Use when**: Multiple components affected, unknown scope

**Steps**:
```bash
# 1. Stop current plugin
pkill -f plugin-name

# 2. Remove current version
rm -rf plugin-name

# 3. Restore from backup
cp -r backups/plugin-name.[timestamp] ./plugin-name

# 4. Verify restoration
diff -r plugin-name backups/plugin-name.[timestamp]

# 5. Restart plugin
./plugin-name/start.sh
```

**Verification**:
```bash
# Check restoration
ls -la plugin-name/
diff -r plugin-name/ backups/plugin-name.[timestamp]/

# Test functionality
./plugin-name/test.sh
```

---

### Method 2: Partial Rollback

**Use when**: Specific files affected, limited scope

**Steps**:
```bash
# 1. Identify affected files
grep -r "ERROR\|FAIL" refinement.log

# 2. Restore specific files
cp backups/plugin-name.[timestamp]/path/to/file plugin-name/path/to/file

# 3. Verify file
diff backups/plugin-name.[timestamp]/path/to/file plugin-name/path/to/file

# 4. Test affected component
./scripts/test-component.sh
```

**Examples**:
```bash
# Rollback single skill
cp backups/plugin.20260121_2055/skills/api-review/SKILL.md plugin-name/skills/api-review/SKILL.md

# Rollback manifest
cp backups/plugin.20260121_2055/.claude-plugin/plugin.json plugin-name/.claude-plugin/plugin.json

# Rollback hooks
cp backups/plugin.20260121_2055/hooks/hooks.json plugin-name/hooks/hooks.json
```

---

### Method 3: Configuration Rollback

**Use when**: Configuration issues, settings problems

**Steps**:
```bash
# 1. Backup current config
cp plugin-name/config.yaml plugin-name/config.yaml.broken

# 2. Restore config
cp backups/plugin-name.[timestamp]/config.yaml plugin-name/config.yaml

# 3. Verify config
./plugin-name/validate-config.sh
```

---

## Rollback Safety

### Before Rollback
- [ ] Document current state
- [ ] Identify rollback scope
- [ ] Verify backup exists
- [ ] Stop plugin services
- [ ] Create emergency backup

### During Rollback
- [ ] Follow procedures exactly
- [ ] Verify each step
- [ ] Check file permissions
- [ ] Maintain logs
- [ ] Document actions

### After Rollback
- [ ] Verify functionality
- [ ] Run tests
- [ ] Check quality score
- [ ] Monitor for issues
- [ ] Document outcome

---

## Emergency Rollback

### Quick Rollback (< 5 minutes)

**For critical failures**:

```bash
# Immediate rollback
./scripts/emergency-rollback.sh

# Verify
./scripts/verify-rollback.sh
```

**emergency-rollback.sh**:
```bash
#!/bin/bash
set -e

echo "=== Emergency Rollback ==="

# Find latest backup
BACKUP=$(ls -t backups/*.tar.gz 2>/dev/null | head -1)

if [ -z "$BACKUP" ]; then
    echo "❌ No backup found!"
    exit 1
fi

echo "Using backup: $BACKUP"

# Stop services
pkill -f plugin-name

# Restore
rm -rf plugin-name
tar -xzf "$BACKUP"

echo "✅ Rollback complete"
```

---

## Rollback Verification

### Functionality Tests
```bash
# Test 1: Plugin loads
./plugin-name/health-check.sh

# Test 2: Skills work
./plugin-name/test-skills.sh

# Test 3: Commands execute
./plugin-name/test-commands.sh

# Test 4: Agents function
./plugin-name/test-agents.sh

# Test 5: Hooks trigger
./plugin-name/test-hooks.sh
```

### Quality Check
```bash
# Re-run audit
/plugin-review-orchestrator plugin-name

# Check quality score
grep "Quality Score:" audit-report.txt

# Compare with pre-refinement
echo "Before: $BEFORE_SCORE"
echo "After: $AFTER_SCORE"
```

---

## Post-Rollback Actions

### Immediate (0-1 hours)
1. Verify plugin functionality
2. Check system logs
3. Monitor performance
4. Test critical workflows
5. Document rollback reason

### Short-term (1-24 hours)
1. Review what went wrong
2. Analyze rollback logs
3. Identify root cause
4. Plan corrective action
5. Update procedures

### Long-term (1+ weeks)
1. Implement fixes
2. Improve testing
3. Enhance rollback procedures
4. Update documentation
5. Prevent recurrence

---

## Rollback Documentation

### Template
```markdown
# Rollback Report

## Incident
- **Date**: YYYY-MM-DD HH:MM
- **Plugin**: plugin-name
- **Version**: vX.Y.Z
- **Trigger**: [reason]

## Scope
- **Components Affected**: skills, commands, agents, hooks
- **Files Changed**: N files
- **Severity**: Critical/High/Medium

## Actions Taken
1. Rollback method: Full/Partial/Config
2. Backup used: backups/plugin.[timestamp]
3. Verification: Passed/Failed
4. Downtime: X minutes

## Outcome
- **Result**: Successful/Failed
- **Issues Remaining**: [list]
- **Quality Score**: Before X.Y → After X.Y

## Lessons Learned
1. What went wrong
2. What worked well
3. Improvements needed
4. Prevention measures
```

---

## Prevention Strategies

### Before Refinement
1. Create comprehensive backup
2. Document baseline state
3. Define success criteria
4. Plan rollback strategy
5. Test rollback procedure

### During Refinement
1. Validate each change
2. Test incrementally
3. Monitor quality score
4. Document all actions
5. Stop if issues arise

### After Refinement
1. Comprehensive testing
2. Quality validation
3. Performance monitoring
4. User feedback
5. Continuous improvement
