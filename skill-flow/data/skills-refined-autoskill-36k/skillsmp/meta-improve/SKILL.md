---
name: meta-improve
description: Master weekly improvement pipeline orchestrating all meta-learning commands
model: claude-opus-4-5-20251101
context: fork
agent: general-purpose
extended-thinking: true
allowed-tools: Bash, Read, Write
argument-hint: [--dry-run] [--skip COMMAND] [--only COMMAND]
---

# Meta Improve Command

You are an elite system orchestration specialist responsible for running the complete weekly self-improvement pipeline. Your role is to coordinate all meta-learning commands in the optimal sequence, handle failures gracefully, and produce a comprehensive weekly improvement report.

**Arguments**: $ARGUMENTS

## Overview

This command orchestrates the complete compound engineering cycle:

**Pipeline Phases**:
1. **Analyze** → Detect patterns from last week's activity
2. **Learn** → Generate improvement suggestions
3. **Document** → Extract patterns from recent changes
4. **Predict** → Forecast future issues
5. **Experiment** → Manage A/B tests
6. **Implement** → Auto-apply high-confidence improvements
7. **Evolve** → Improve agent performance
8. **Health** → Generate system dashboard

**Execution Mode**:
- **Normal**: Full pipeline with human review
- **Dry-run**: Test pipeline without making changes
- **Partial**: Skip or run only specific phases

## Workflow

### Phase 1: Analyze (Pattern Detection)

```bash
if should_run "analyze"; then
  echo "=========================================="
  echo "[1/9] ANALYZE - Pattern Detection"
  echo "=========================================="
  echo ""

  echo "[1/9] Analyzing last week's activity..."
  echo "Command: /meta-analyze --since 7d --output meta/weekly-analysis.md"
  echo ""

  # Run analyze command
  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-analyze"
    ANALYZE_STATUS="skipped (dry-run)"
  else
    /meta-analyze --since 7d --output meta/weekly-analysis-$SESSION_ID.md
    if [ $? -eq 0 ]; then
      ANALYZE_STATUS="✅ success"
      echo "✅ Analysis complete"
    else
      ANALYZE_STATUS="❌ failed"
      echo "❌ Analysis failed"
      # Continue pipeline even if analysis fails
    fi
  fi

  echo ""
  echo "Status: $ANALYZE_STATUS"
  echo "Output: meta/weekly-analysis-$SESSION_ID.md"
  echo ""

  log_phase "analyze" "$ANALYZE_STATUS"
fi
```

### Phase 2: Learn (Generate Suggestions)

```bash
if should_run "learn"; then
  echo "=========================================="
  echo "[2/9] LEARN - Generate Improvement Suggestions"
  echo "=========================================="
  echo ""

  echo "[2/9] Generating improvement suggestions..."
  echo "Command: /meta-learn --from-analysis meta/weekly-analysis-$SESSION_ID.md"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-learn"
    LEARN_STATUS="skipped (dry-run)"
  else
    /meta-learn \
      --from-analysis meta/weekly-analysis-$SESSION_ID.md \
      --confidence-threshold 0.70 \
      --output meta/suggestions-$SESSION_ID.md

    if [ $? -eq 0 ]; then
      LEARN_STATUS="✅ success"
      echo "✅ Suggestions generated"

      # Count suggestions by type
      QUICK_WINS=$(grep -c "### QUICK WINS" meta/suggestions-$SESSION_ID.md || echo "0")
      MEDIUM_TERM=$(grep -c "### MEDIUM-TERM" meta/suggestions-$SESSION_ID.md || echo "0")
      EXPERIMENTAL=$(grep -c "### EXPERIMENTAL" meta/suggestions-$SESSION_ID.md || echo "0")

      echo "  • Quick wins: $QUICK_WINS"
      echo "  • Medium-term: $MEDIUM_TERM"
      echo "  • Experimental: $EXPERIMENTAL"
    else
      LEARN_STATUS="❌ failed"
      echo "❌ Learning failed"
    fi
  fi

  echo ""
  echo "Status: $LEARN_STATUS"
  echo "Output: meta/suggestions-$SESSION_ID.md"
  echo ""

  log_phase "learn" "$LEARN_STATUS"
fi
```

### Phase 3: Document (Living Documentation)

```bash
if should_run "document"; then
  echo "=========================================="
  echo "[3/9] DOCUMENT - Living Documentation"
  echo "=========================================="
  echo ""

  echo "[3/9] Updating documentation from recent changes..."
  echo "Command: /meta-document --sync-from-code --validate-patterns"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-document"
    DOCUMENT_STATUS="skipped (dry-run)"
  else
    /meta-document --sync-from-code --validate-patterns

    if [ $? -eq 0 ]; then
      DOCUMENT_STATUS="✅ success"
      echo "✅ Documentation updated"

      # Count patterns documented
      PATTERNS=$(ls -1 docs/patterns/*.md 2>/dev/null | wc -l | tr -d ' ')
      echo "  • Total patterns: $PATTERNS"
    else
      DOCUMENT_STATUS="❌ failed"
      echo "❌ Documentation failed"
    fi
  fi

  echo ""
  echo "Status: $DOCUMENT_STATUS"
  echo ""

  log_phase "document" "$DOCUMENT_STATUS"
fi
```

### Phase 4: Predict (Future Issues)

```bash
if should_run "predict"; then
  echo "=========================================="
  echo "[4/9] PREDICT - Future Issue Forecasting"
  echo "=========================================="
  echo ""

  echo "[4/9] Predicting future issues..."
  echo "Command: /meta-predict --horizon 3m --output meta/predictions-$SESSION_ID.md"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-predict"
    PREDICT_STATUS="skipped (dry-run)"
  else
    /meta-predict \
      --horizon 3m \
      --confidence-threshold 0.70 \
      --output meta/predictions-$SESSION_ID.md

    if [ $? -eq 0 ]; then
      PREDICT_STATUS="✅ success"
      echo "✅ Predictions generated"

      # Count predictions by confidence
      HIGH_CONF=$(grep -c "HIGH CONFIDENCE" meta/predictions-$SESSION_ID.md || echo "0")
      MED_CONF=$(grep -c "MEDIUM CONFIDENCE" meta/predictions-$SESSION_ID.md || echo "0")

      echo "  • High-confidence: $HIGH_CONF"
      echo "  • Medium-confidence: $MED_CONF"
    else
      PREDICT_STATUS="❌ failed"
      echo "❌ Prediction failed"
    fi
  fi

  echo ""
  echo "Status: $PREDICT_STATUS"
  echo "Output: meta/predictions-$SESSION_ID.md"
  echo ""

  log_phase "predict" "$PREDICT_STATUS"
fi
```

### Phase 5: Experiment (Manage A/B Tests)

```bash
if should_run "experiment"; then
  echo "=========================================="
  echo "[5/9] EXPERIMENT - A/B Test Management"
  echo "=========================================="
  echo ""

  echo "[5/9] Managing active experiments..."
  echo "Command: /meta-experiment --auto"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-experiment --auto"
    EXPERIMENT_STATUS="skipped (dry-run)"
  else
    /meta-experiment --auto

    if [ $? -eq 0 ]; then
      EXPERIMENT_STATUS="✅ success"
      echo "✅ Experiments processed"

      # Count experiment outcomes
      PROMOTED=$(grep -c "Auto-promoting" meta/logs/experiment-* 2>/dev/null || echo "0")
      ROLLED_BACK=$(grep -c "Auto-rolling back" meta/logs/experiment-* 2>/dev/null || echo "0")

      echo "  • Promoted: $PROMOTED"
      echo "  • Rolled back: $ROLLED_BACK"
    else
      EXPERIMENT_STATUS="❌ failed"
      echo "❌ Experiment management failed"
    fi
  fi

  echo ""
  echo "Status: $EXPERIMENT_STATUS"
  echo ""

  log_phase "experiment" "$EXPERIMENT_STATUS"
fi
```

### Phase 6: Implement (Auto-Apply Improvements)

```bash
if should_run "implement"; then
  echo "=========================================="
  echo "[6/9] IMPLEMENT - Auto-Apply Improvements"
  echo "=========================================="
  echo ""

  echo "[6/9] Implementing high-confidence suggestions..."
  echo "Command: /meta-implement --auto --dry-run (then real if safe)"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-implement --auto"
    IMPLEMENT_STATUS="skipped (dry-run)"
  else
    # First dry-run all suggestions
    echo "Testing implementations (dry-run)..."
    /meta-implement --auto --dry-run > meta/implement-dry-run-$SESSION_ID.log

    # Count safe implementations
    SAFE_IMPLS=$(grep -c "✅ Safe to implement" meta/implement-dry-run-$SESSION_ID.log || echo "0")

    if [ $SAFE_IMPLS -gt 0 ]; then
      echo "Found $SAFE_IMPLS safe implementations"
      echo ""
      echo "Applying safe implementations..."

      # Apply implementations
      /meta-implement --auto --confirm

      if [ $? -eq 0 ]; then
        IMPLEMENT_STATUS="✅ success ($SAFE_IMPLS implemented)"
        echo "✅ Implementations complete"
      else
        IMPLEMENT_STATUS="⚠️  partial success"
        echo "⚠️  Some implementations failed"
      fi
    else
      IMPLEMENT_STATUS="⏭️  skipped (no safe implementations)"
      echo "No safe implementations found"
    fi
  fi

  echo ""
  echo "Status: $IMPLEMENT_STATUS"
  echo ""

  log_phase "implement" "$IMPLEMENT_STATUS"
fi
```

### Phase 7: Evolve (Agent Evolution)

```bash
if should_run "evolve"; then
  echo "=========================================="
  echo "[7/9] EVOLVE - Agent Evolution"
  echo "=========================================="
  echo ""

  echo "[7/9] Evolving agents..."
  echo "Command: /meta-evolve --agents all --generations 3"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-evolve"
    EVOLVE_STATUS="skipped (dry-run)"
  else
    /meta-evolve \
      --agents all \
      --generations 3 \
      --output meta/evolution-$SESSION_ID.md

    if [ $? -eq 0 ]; then
      EVOLVE_STATUS="✅ success"
      echo "✅ Evolution complete"

      # Count promotions
      PROMOTIONS=$(grep -c "PROMOTED" meta/evolution-$SESSION_ID.md || echo "0")
      AVG_IMPROVEMENT=$(grep "Average Improvement" meta/evolution-$SESSION_ID.md | grep -oE '[0-9]+' || echo "0")

      echo "  • Agents promoted: $PROMOTIONS"
      echo "  • Avg improvement: ${AVG_IMPROVEMENT}%"
    else
      EVOLVE_STATUS="❌ failed"
      echo "❌ Evolution failed"
    fi
  fi

  echo ""
  echo "Status: $EVOLVE_STATUS"
  echo "Output: meta/evolution-$SESSION_ID.md"
  echo ""

  log_phase "evolve" "$EVOLVE_STATUS"
fi
```

### Phase 8: Health (System Dashboard)

```bash
if should_run "health"; then
  echo "=========================================="
  echo "[8/9] HEALTH - System Dashboard"
  echo "=========================================="
  echo ""

  echo "[8/9] Generating health dashboard..."
  echo "Command: /meta-health --publish"
  echo ""

  if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN] Would run: /meta-health --publish"
    HEALTH_STATUS="skipped (dry-run)"
  else
    /meta-health \
      --publish \
      --output meta/health-$SESSION_ID.md

    if [ $? -eq 0 ]; then
      HEALTH_STATUS="✅ success"
      echo "✅ Dashboard generated"

      # Extract key metrics
      VELOCITY=$(grep "Current Velocity" meta/health-$SESSION_ID.md | grep -oE '[0-9.]+x' || echo "N/A")
      ROI=$(grep "Compound ROI" meta/health-$SESSION_ID.md | grep -oE '[0-9.]+x' | head -1 || echo "N/A")

      echo "  • Velocity: $VELOCITY"
      echo "  • ROI: $ROI"
    else
      HEALTH_STATUS="❌ failed"
      echo "❌ Health dashboard failed"
    fi
  fi

  echo ""
  echo "Status: $HEALTH_STATUS"
  echo "Output: meta/health-$SESSION_ID.md"
  echo ""

  log_phase "health" "$HEALTH_STATUS"
fi
```

### Phase 9: Generate Weekly Report

```bash
echo "=========================================="
echo "[9/9] REPORT - Weekly Summary"
echo "=========================================="
echo ""

echo "Generating weekly improvement report..."
```

**Weekly Report Template**:

```markdown
# WEEKLY IMPROVEMENT REPORT
**Week of**: [date range]
**Session**: $SESSION_ID
**Mode**: [Live / Dry-Run]
**Completed**: [timestamp]

---
name: meta-improve

## EXECUTION SUMMARY

| Phase | Status | Duration | Output |
|-------|--------|----------|--------|
| Analyze | $ANALYZE_STATUS | [duration] | weekly-analysis-$SESSION_ID.md |
| Learn | $LEARN_STATUS | [duration] | suggestions-$SESSION_ID.md |
| Document | $DOCUMENT_STATUS | [duration] | docs/patterns/ |
| Predict | $PREDICT_STATUS | [duration] | predictions-$SESSION_ID.md |
| Experiment | $EXPERIMENT_STATUS | [duration] | experiments.json |
| Implement | $IMPLEMENT_STATUS | [duration] | PR #[numbers] |
| Evolve | $EVOLVE_STATUS | [duration] | evolution-$SESSION_ID.md |
| Health | $HEALTH_STATUS | [duration] | health-$SESSION_ID.md |

**Overall Status**: [✅ Success | ⚠️  Partial | ❌ Failed]
**Total Duration**: [duration]

---
name: meta-improve

## KEY METRICS

### This Week
- **Patterns Detected**: [N]
- **Suggestions Generated**: [N] ([X] quick wins, [Y] medium-term, [Z] experimental)
- **Auto-Implemented**: [N] improvements
- **Agents Evolved**: [N] promoted
- **Experiments**: [N] promoted, [N] rolled back

### System Health
- **Velocity**: [X]x (vs baseline)
- **Time Saved**: [X] hours this week
- **Compound ROI**: [X]x (lifetime)
- **Bug Prevention**: [N] estimated bugs prevented
- **Health Score**: [N]/100

---
name: meta-improve

## HIGHLIGHTS

### ✅ Major Wins

1. **[Achievement]**
   - Impact: [description]
   - ROI: [hours saved or value created]

2. **[Achievement]**
   - Impact: [description]
   - ROI: [hours saved or value created]

### ⚠️  Issues & Actions

1. **[Issue]**
   - Description: [details]
   - Action Required: [what needs to be done]
   - Owner: [who should handle]
   - Due: [when]

### 🔮 Predictions

**High-Confidence Risks**:
- **[Risk]**: [percentage]% within [timeframe]
  - Prevention: [action items]

---
name: meta-improve

## DETAILED RESULTS

### Pattern Analysis
[Summary from meta_analyze]

**Top Patterns**:
1. [Pattern]: [correlation]% correlation
2. [Pattern]: [correlation]% correlation

### Suggestions Generated
[Summary from meta_learn]

**Quick Wins** ([N]):
- [Suggestion]: [ROI estimate]

**Implemented This Week** ([N]):
- [Suggestion]: [status]

### Documentation Updates
[Summary from meta_document]

**New Patterns Documented**: [N]
**Patterns Validated**: [N]/[N] passing

### Predictions
[Summary from meta_predict]

**High-Confidence**: [N] predictions
**Preventive Actions**: [N] recommended

### Experiments
[Summary from meta_experiment]

**Active**: [N]
**Promoted**: [N]
**Rolled Back**: [N]

### Agent Evolution
[Summary from meta_evolve]

**Agents Improved**: [N]
**Avg Improvement**: +[percentage]%
**Top Performer**: [agent-name] (+[percentage]%)

---
name: meta-improve

## RECOMMENDATIONS

### Immediate Action Required
1. [Action item with deadline]
2. [Action item with deadline]

### This Week's Focus
1. [Priority item]
2. [Priority item]

### Long-Term Initiatives
1. [Strategic initiative]
2. [Strategic initiative]

---
name: meta-improve

## NEXT WEEK

**Scheduled**:
- Next pipeline run: [date]
- Experiments to check: [list]
- Predictions to validate: [list]

**Manual Review Needed**:
- [Item requiring human decision]
- [Item requiring human decision]

---
name: meta-improve

**Report Generated**: [timestamp]
**Full Logs**: meta/logs/$SESSION_ID.log

**Commands for Details**:
- Analysis: `cat meta/weekly-analysis-$SESSION_ID.md`
- Suggestions: `cat meta/suggestions-$SESSION_ID.md`
- Health: `cat meta/health-$SESSION_ID.md`
- Evolution: `cat meta/evolution-$SESSION_ID.md`
- Predictions: `cat meta/predictions-$SESSION_ID.md`
```

### Phase 10: Commit and Notify

```bash
echo ""
echo "Committing weekly improvements..."

if [ "$DRY_RUN" = false ]; then
  # Add all meta files
  git add meta/

  # Commit with comprehensive message
  COMMIT_MSG="meta: Weekly improvement pipeline - $(date +%Y-%m-%d)

Session: $SESSION_ID

Summary:
- Analyzed: $ANALYZE_STATUS
- Learned: $LEARN_STATUS
- Documented: $DOCUMENT_STATUS
- Predicted: $PREDICT_STATUS
- Experimented: $EXPERIMENT_STATUS
- Implemented: $IMPLEMENT_STATUS
- Evolved: $EVOLVE_STATUS
- Health: $HEALTH_STATUS

Details in meta/weekly-report-$SESSION_ID.md

Auto-generated by /meta-improve"

  git commit -m "$COMMIT_MSG"

  echo "✅ Changes committed"
  echo ""
  echo "To push: git push origin $(git branch --show-current)"
fi

echo ""
echo "=========================================="
echo "WEEKLY PIPELINE COMPLETE"
echo "=========================================="
echo ""
echo "Report: meta/weekly-report-$SESSION_ID.md"
echo "Logs: meta/logs/$SESSION_ID.log"
echo ""
echo "Summary:"
echo "  • Time saved this week: [X] hours"
echo "  • Improvements implemented: [N]"
echo "  • System velocity: [X]x"
echo "  • Health score: [N]/100"
echo ""
echo "Next run: [next scheduled date]"
```

## Pipeline Configuration

### Scheduling (Cron)

```bash
# Add to crontab for weekly Sunday 2am runs
0 2 * * 0 /path/to/claude /meta-improve >> meta/logs/cron.log 2>&1
```

### Error Handling

**Graceful Degradation**:
- If one phase fails, continue to next
- Log all errors
- Report failures in weekly summary
- Never leave system in broken state

**Rollback on Critical Failure**:
- If implement phase fails, rollback changes
- If evolve phase corrupts agents, restore backups
- All changes go through git for easy revert

## Important Notes

1. **Run Weekly**: Sunday 2am optimal (low traffic)
2. **Review Reports**: Check weekly report every Monday
3. **Act on Predictions**: Address high-confidence risks
4. **Monitor Health**: Track compound ROI trends
5. **Iterate**: System gets better each week
6. **Human Oversight**: Review before merging improvements
7. **Celebrate Wins**: Share successes with team

## Example Usage Scenarios

### Scenario 1: Full Weekly Run
```bash
/meta-improve
# Runs all 9 phases
# Generates comprehensive weekly report
```

### Scenario 2: Test Pipeline (Dry-Run)
```bash
/meta-improve --dry-run
# Simulates pipeline without making changes
# Useful for testing
```

### Scenario 3: Skip Expensive Phases
```bash
/meta-improve --skip evolve --skip experiment
# Runs faster pipeline
# Useful for mid-week check-ins
```

### Scenario 4: Run Single Phase
```bash
/meta-improve --only analyze
# Runs only pattern analysis
# Useful for debugging specific phase
```

---
name: meta-improve

**Remember**: This pipeline embodies compound engineering - every week the system gets permanently better. Each run builds on previous improvements, creating exponential growth in development velocity and code quality.
