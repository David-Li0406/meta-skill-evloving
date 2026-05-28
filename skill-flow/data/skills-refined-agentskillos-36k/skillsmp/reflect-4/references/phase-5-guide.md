# Phase 5: Advanced Features Guide

This guide covers the advanced features implemented in Phase 5 of the reflect plugin improvement plan.

## Overview

Phase 5 adds two major capabilities:

1. **Batch Skill Analysis (M2)** - Analyze all skills at once to find cross-skill patterns
2. **Automated Cleanup Integration (L2)** - Scheduled archival to prevent unbounded growth

These features enable systemic improvements and long-term sustainability of the reflect system.

---

## Feature 1: Batch Skill Analysis

### Purpose

Traditional reflect analyzes one skill at a time. Batch analysis looks across ALL skills to identify:

- Patterns affecting multiple skills (accessibility, type safety, testing, etc.)
- Skills with high rejection rates (signal detection issues)
- Skills benefiting most from external feedback
- Cross-skill improvement opportunities

### Usage

#### Basic Analysis

```bash
/reflect analyze-all
```

This generates a report showing:
- Skills with high rejection rates
- External feedback patterns
- Critic score analysis
- Common change themes
- Recommended actions

#### With Options

```bash
# Analyze last 30 days only
/reflect analyze-all --days 30

# Require pattern to affect 3+ skills
/reflect analyze-all --min-skills 3

# Save report to file
/reflect analyze-all --output batch-analysis.md

# Verbose output
/reflect analyze-all --verbose

# Combination
/reflect analyze-all --days 30 --min-skills 3 --output report.md --verbose
```

### Example Report

```markdown
# Batch Skill Analysis Report

**Generated**: 2026-01-17 10:30:00 UTC
**Analysis Period**: Last 90 days
**Minimum Skills for Pattern**: 2

---

## High Rejection Rates

Skills with multiple rejections (may indicate misaligned signal detection):

| Skill | Rejections |
|-------|------------|
| frontend-design | 3 |
| code-reviewer | 2 |

## External Feedback Patterns

Skills with objective signals (tests, lint, build errors):

| Skill | Feedback Events |
|-------|-----------------|
| code-reviewer | 12 |
| python-pro | 8 |
| frontend-design | 5 |

**Recommendation**: High external feedback indicates skills that benefit most from objective signals.

## Critic Score Analysis

### Average Scores by Skill

| Skill | Avg Score | Approved | Rejected |
|-------|-----------|----------|----------|
| frontend-design | 82 | 4 | 2 |
| code-reviewer | 75 | 3 | 2 |
| python-pro | 88 | 2 | 0 |

**Insights**:
- Scores 90-100: Excellent proposals (approve immediately)
- Scores 70-89: Good proposals (minor improvements)
- Scores <70: Need significant revision

## Common Change Themes

Recurring themes across multiple skills:

- **Accessibility** (4 mentions) - aria-labels, semantic HTML, a11y compliance
- **Type Safety** (5 mentions) - TypeScript, type hints, type checking
- **Testing** (3 mentions) - test coverage, missing tests, test quality

## Recommended Actions

### Cross-Skill Improvements

1. **Review ~/.claude/memories/skill-patterns.md**
   - Add "Accessibility" as cross-skill pattern (affects 4 skills)
   - Add "Type Safety" as cross-skill pattern (affects 5 skills)
   - Document shared implementation guidance

2. **Update High-Rejection Skills**
   - frontend-design: 3 rejections - review signal detection
   - code-reviewer: 2 rejections - may need confidence adjustment

3. **Leverage External Feedback**
   - code-reviewer has 12 feedback events - prioritize objective signals
   - Include test/lint errors as HIGH confidence signals in analysis

4. **Improve Low-Scoring Proposals**
   - No skills with avg scores <70 (all good!)
```

### When to Run

- **Monthly**: Regular cross-skill pattern review
- **After major changes**: When updating multiple skills
- **Quarterly**: Systemic improvement planning
- **Ad-hoc**: When noticing recurring issues across skills

### Interpreting Results

#### High Rejection Rates

**What it means**: Signal detection may be misaligned

**Actions**:
- Review recent proposals for that skill
- Check if rejections have common reasons
- Consider adjusting confidence thresholds
- May need to update meta-learnings

#### External Feedback Patterns

**What it means**: Skills with many test/lint errors

**Actions**:
- These skills benefit MOST from external feedback
- Include test/lint errors as HIGH confidence signals
- Prioritize objective signals over conversation interpretation

#### Common Themes

**What it means**: Patterns affecting 2+ skills

**Actions**:
- Create entry in `~/.claude/memories/skill-patterns.md`
- Document shared implementation guidance
- Update all affected skills to reference pattern
- Prevents duplicate learnings across skills

#### Critic Scores

**What it means**: Proposal quality trends

**Actions**:
- Avg <70: Review proposal-validation-guide.md
- High approved/rejected ratio: Good signal detection
- Low scores + rejections: Fundamental alignment issues

### Output Formats

**Markdown** (default):
```bash
/reflect analyze-all --output analysis.md
```

Human-readable report with tables and recommendations.

**JSON** (future):
```bash
/reflect analyze-all --format json --output analysis.json
```

Machine-readable for programmatic processing.

---

## Feature 2: Automated Cleanup

### Purpose

Prevent unbounded growth of memories, metrics, and external feedback by archiving old data.

### What Gets Cleaned

| Item | Default Age | Action | Location |
|------|-------------|--------|----------|
| Memory files | 90 days | Archive | `~/.claude/memories/` → `~/.claude/memories-archive/YYYY-MM/` |
| Metrics | 180 days | Delete | `~/.claude/reflect-metrics.jsonl` |
| External feedback | 30 days | Delete | `~/.claude/reflect-external-feedback/*.jsonl` |

**Note**: `README.md` in memories is never archived.

### Usage

#### Manual Cleanup

```bash
# Basic cleanup (dry-run first)
/reflect cleanup --dry-run

# Actually run cleanup
/reflect cleanup

# With options
/reflect cleanup --age-days 60                    # Custom age threshold
/reflect cleanup --clean-metrics --clean-feedback # Also clean metrics/feedback
/reflect cleanup --force                          # Skip confirmation prompts

# Complete cleanup
/reflect cleanup --clean-metrics --clean-feedback --force
```

#### Automated Cleanup

**Recommended**: Set up monthly automated cleanup.

See `skills/reflect/references/automated-cleanup-guide.md` for detailed setup instructions:

- **Cron** (Linux/macOS)
- **Launchd** (macOS preferred)
- **systemd Timer** (Linux systemd)

**Quick setup (macOS launchd)**:

1. Create launch agent:
   ```bash
   cat > ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist <<EOF
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
       "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>dev.claude.reflect.cleanup</string>
       <key>ProgramArguments</key>
       <array>
           <string>$HOME/.claude/scripts/reflect-cleanup-memories.sh</string>
           <string>--force</string>
           <string>--clean-metrics</string>
           <string>--clean-feedback</string>
       </array>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Day</key>
           <integer>1</integer>
           <key>Hour</key>
           <integer>2</integer>
       </dict>
       <key>StandardOutPath</key>
       <string>$HOME/.claude/cleanup.log</string>
       <key>StandardErrorPath</key>
       <string>$HOME/.claude/cleanup.error.log</string>
   </dict>
   </plist>
   EOF
   ```

2. Load:
   ```bash
   launchctl load ~/Library/LaunchAgents/dev.claude.reflect.cleanup.plist
   ```

### Cleanup Policies

**Conservative** (long history):
- Age: 180 days
- Frequency: Quarterly
- Metrics/feedback: Keep all

**Recommended** (most users):
- Age: 90 days (default)
- Frequency: Monthly
- Metrics: Clean 180+ days
- Feedback: Clean 30+ days

**Aggressive** (high activity):
- Age: 60 days
- Frequency: Weekly/bi-weekly
- Metrics: Clean 90+ days
- Feedback: Clean 14+ days

### Monitoring

Check cleanup logs:
```bash
tail -f ~/.claude/cleanup.log
```

View archives:
```bash
ls -lah ~/.claude/memories-archive/
```

Check metrics size:
```bash
wc -l ~/.claude/reflect-metrics.jsonl
ls -lh ~/.claude/reflect-metrics.jsonl
```

### Restoration

To restore an archived memory:

```bash
# Copy from archive
cp ~/.claude/memories-archive/2026-01/old-skill-prefs.md \
   ~/.claude/memories/skill-prefs.md

# Update timestamp
sed -i '' "s/Last updated: .*/Last updated: $(date +%Y-%m-%d)/" \
   ~/.claude/memories/skill-prefs.md
```

---

## Integration with Other Phases

### Phase 3: Memory Migration

Batch analysis helps identify cross-skill patterns to add to `skill-patterns.md`.

**Workflow**:
1. Run `/reflect analyze-all`
2. Identify themes affecting 2+ skills
3. Create entries in `~/.claude/memories/skill-patterns.md`
4. Update affected skills to reference pattern

### Phase 4: Multi-Agent Reflection

Batch analysis shows which skills have low average critic scores.

**Workflow**:
1. Run `/reflect analyze-all`
2. Find skills with avg scores <70
3. Review critic feedback in metrics
4. Common issues: vague evidence, scope creep, breaking changes
5. Improve proposal quality for those skills

### Continuous Improvement Loop

```
1. Weekly: Use skills → accumulate metrics
2. Monthly: /reflect analyze-all → identify patterns
3. Monthly: /reflect cleanup → archive old data
4. Quarterly: Review cross-skill patterns → systemic improvements
```

---

## Best Practices

### For Batch Analysis

1. **Run monthly**: Regular cross-skill pattern review
2. **Act on findings**: Don't just generate reports, implement recommendations
3. **Track themes**: Document recurring themes in skill-patterns.md
4. **Review high-rejection skills**: Fix signal detection issues
5. **Leverage external feedback**: Prioritize objective signals

### For Automated Cleanup

1. **Start conservative**: Use default 90-day threshold initially
2. **Monitor first**: Check logs after first few automated runs
3. **Adjust as needed**: Tune age threshold based on usage
4. **Review archives**: Periodically check if old memories still needed
5. **Backup important data**: Optional extra safety for critical memories

### Integration

1. **Schedule together**: Run batch analysis before cleanup
2. **Document patterns first**: Add to memories before archiving
3. **Archive less useful**: Keep patterns that affect multiple skills
4. **Track effectiveness**: Monitor if cleanups improve performance

---

## Troubleshooting

### Batch Analysis Shows "No proposals"

**Cause**: Metrics file empty or all proposals older than threshold

**Solution**:
- Check metrics file: `wc -l ~/.claude/reflect-metrics.jsonl`
- Increase days: `/reflect analyze-all --days 365`
- Verify metrics are being logged: check recent proposals

### Cleanup Not Archiving Anything

**Cause**: No files older than threshold (normal)

**Solution**:
- Run with `--dry-run --verbose` to see what's being checked
- Lower threshold: `--age-days 30`
- Check file modification dates: `ls -lt ~/.claude/memories/`

### Automated Cleanup Not Running

**Cause**: Scheduler not configured correctly

**Solution**:
- Check cron/launchd/systemd status
- View logs: `cat ~/.claude/cleanup.log`
- Test manually: `/reflect cleanup --dry-run`
- See `automated-cleanup-guide.md` for detailed troubleshooting

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `/reflect analyze-all` | Batch analysis across all skills |
| `/reflect analyze-all --days N` | Analyze last N days |
| `/reflect analyze-all --min-skills N` | Require N+ skills for pattern |
| `/reflect analyze-all --output FILE` | Save report to file |
| `/reflect cleanup` | Manual cleanup with prompts |
| `/reflect cleanup --dry-run` | Show what would be archived |
| `/reflect cleanup --force` | Skip confirmation prompts |
| `/reflect cleanup --clean-metrics` | Also clean old metrics |
| `/reflect cleanup --clean-feedback` | Also clean old feedback |

---

## Expected Benefits

**Batch Analysis (M2)**:
- Identify systemic improvements affecting multiple skills
- Reduce duplicate learnings across skills
- Find signal detection issues early
- Prioritize skills needing most improvement

**Automated Cleanup (L2)**:
- Prevent unbounded growth (memory leaks)
- Keep system performant long-term
- Preserve only relevant recent data
- Reduce noise in metrics/memories

**Combined**:
- Sustainable long-term operation
- Cross-skill learning amplification
- Data-driven systemic improvements
- Scalable to dozens of skills

---

*Part of Phase 5: Advanced Features*
*See also*:
- `automated-cleanup-guide.md` - Detailed scheduler setup
- `../SKILL.md` - Main reflect skill workflow
- `memory-system.md` - Memory architecture (Phase 3)
- `proposal-validation-guide.md` - Critic validation (Phase 4)

*Last updated: 2026-01-17*
