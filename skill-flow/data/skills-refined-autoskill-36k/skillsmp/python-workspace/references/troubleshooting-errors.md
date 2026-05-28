**Skill**: [MQL5→Python Translation Workspace Skill](../SKILL.md)

## Critical Requirements & Assumptions

### Required Assumptions:

1. ✅ **MT5 Terminal Running**: API approaches require logged-in terminal
1. ✅ **Wine/CrossOver Installed**: No native macOS MT5 support
1. ✅ **Python 3.12+ in Wine**: Required for MetaTrader5 package
1. ✅ **NumPy 1.26.4**: MUST use this version (not 2.x - Wine incompatible)
1. ✅ **5000+ Bar Warmup**: Required for validation (not 100 or 500 bars)
1. ✅ **Manual Loops for ATR**: Cannot use pandas rolling windows
1. ✅ **≥0.999 Correlation**: Strict threshold (not 0.95 "good enough")
1. ✅ **Copy-Compile-Move**: Required for paths with spaces in Wine

### Incorrect Assumptions:

1. ❌ startup.ini parameter passing works reliably
1. ❌ Python API can access custom indicator buffers
1. ❌ Pandas operations match MQL5 behavior automatically
1. ❌ 0.95 correlation is "good enough"
1. ❌ 100 bars is sufficient for validation
1. ❌ `/inc` parameter helps with standard compilation
1. ❌ Paths with spaces work in Wine compilation
1. ❌ NumPy 2.x works with MetaTrader5 package

---

## Common User Workflows

### 1. Quick Market Data Export (Beginner - 10-15 seconds)

**Use Case**: User wants EURUSD M1 data with RSI

**Workflow**:

```bash
# One-liner (v3.0.0 headless)
CX_BOTTLE="MetaTrader 5" \
WINEPREFIX="$HOME/Library/Application Support/CrossOver/Bottles/MetaTrader 5" \
wine "C:\\Program Files\\Python312\\python.exe" \
  "C:\\users\\crossover\\export_aligned.py" \
  --symbol EURUSD --period M1 --bars 5000
```

**Output**: CSV with OHLCV + RSI_14 at `users/crossover/exports/`

**Reference**: `/docs/guides/V4_FILE_BASED_CONFIG_WORKFLOW.md` (Quick Start)

---

### 2. Custom Laguerre RSI Export (Intermediate - 20-30 seconds)

**Use Case**: User wants Laguerre RSI indicator values

**Workflow**:

```bash
# Step 1: Generate config
python generate_export_config.py --symbol XAUUSD --timeframe M1 \
  --bars 5000 --laguerre-rsi --output laguerre_export.txt

# Step 2: Open MT5 GUI, drag ExportAligned.ex5 to XAUUSD M1 chart, click OK

# Step 3: CSV at MQL5/Files/Export_XAUUSD_M1_Laguerre.csv
```

**Output**: CSV with OHLCV + Laguerre_RSI + ATR + Adaptive_Period

**Reference**: `/docs/guides/V4_FILE_BASED_CONFIG_WORKFLOW.md` (Example 3)

---

### 3. Validate Python Indicator (Intermediate - 5-10 minutes)

**Use Case**: User wrote Python Laguerre RSI, needs to verify accuracy

**Workflow**:

```bash
# Step 1: Fetch 5000 bars from MT5 (v3.0.0 OR v4.0.0)

# Step 2: Calculate Python indicator on ALL 5000 bars

# Step 3: Validate
python validate_indicator.py \
  --csv Export_EURUSD_PERIOD_M1.csv \
  --indicator laguerre_rsi \
  --threshold 0.999

# Output:
# [PASS] Laguerre_RSI: correlation=1.000000
# [PASS] ATR: correlation=0.999987
# Status: PASS - All buffers meet threshold
```

**Success Criteria**: All buffers ≥0.999 correlation

**Reference**: `/docs/guides/INDICATOR_VALIDATION_METHODOLOGY.md`

---

### 4. Complete Indicator Migration (Advanced - 2-4 hours)

**Use Case**: User wants to translate new MQL5 indicator to Python

**Workflow**: 7-phase checklist-driven process

**Checklist**: `/docs/templates/INDICATOR_MIGRATION_CHECKLIST.md` (copy-paste ready)

**Key Phases**:

1. Locate & analyze (bash commands + manual review)
1. Modify MQL5 (expose hidden buffers)
1. CLI compile (~1 second)
1. Fetch 5000 bars (automated)
1. Implement Python (manual + pandas patterns)
1. Validate ≥0.999 (automated)
1. Document lessons (manual + git)

**Time Investment**: 2-4 hours first time, 1-2 hours subsequently

**Reference**: `/docs/guides/MQL5_TO_PYTHON_MIGRATION_GUIDE.md`

---

## Documentation Hub (Single Source of Truth)

### Quick Start (35-45 minutes)

- **New Users**: `/docs/guides/MQL5_TO_PYTHON_MIGRATION_GUIDE.md` (7-phase workflow)
- **Critical Gotchas**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md` (read FIRST)
- **Copy-Paste Checklist**: `/docs/templates/INDICATOR_MIGRATION_CHECKLIST.md`

### Execution Workflows

- **Headless Export**: `/docs/guides/WINE_PYTHON_EXECUTION.md` (v3.0.0)
- **GUI Export**: `/docs/guides/V4_FILE_BASED_CONFIG_WORKFLOW.md` (v4.0.0)
- **Validation**: `/docs/guides/INDICATOR_VALIDATION_METHODOLOGY.md`

### Critical References

- **Lessons Learned**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md` (8 gotchas)
- **Validation Failures**: `/docs/guides/PYTHON_INDICATOR_VALIDATION_FAILURES.md` (3-hour journey)
- **External Research**: `/docs/guides/EXTERNAL_RESEARCH_BREAKTHROUGHS.md` (game-changers)
- **Legacy Assessment**: `/docs/reports/LEGACY_CODE_ASSESSMENT.md` (what NOT to retry)

### Architecture & Tools

- **Environment Setup**: `/docs/guides/CROSSOVER_MQ5.md` (Wine/CrossOver)
- **File Locations**: `/docs/guides/MT5_FILE_LOCATIONS.md` (paths reference)
- **CLI Compilation**: `/docs/guides/MQL5_CLI_COMPILATION_SUCCESS.md` (~1s compile)

### Navigation

- **Task Navigator**: `/docs/MT5_REFERENCE_HUB.md` (decision trees, canonical map)
- **Project Memory**: `/CLAUDE.md` (hub-and-spoke architecture)
- **Documentation Index**: `/docs/README.md` (complete guide catalog)

---

## Skill Activation Guidelines

### When to Activate This Skill

Activate when user mentions:

- "MQL5" or "MetaTrader 5" or "MT5"
- "indicator translation" or "export data"
- "Python validation" or "correlation check"
- "CrossOver bottle" or "Wine Python"
- "Laguerre RSI", "ATR", "technical indicators"
- File paths containing `MetaTrader 5/drive_c`

### How to Guide Users

**1. Understand Intent First**

- What do they want to export? (market data vs custom indicator)
- What's their experience level? (beginner vs advanced)
- What's their time constraint? (quick export vs full migration)

**2. Recommend Appropriate Workflow**

- Headless automation → v3.0.0 (built-in indicators only)
- Custom indicators → v4.0.0 (GUI mode)
- Validation → Universal framework (≥0.999 threshold)
- Full migration → 7-phase workflow (2-4 hours)

**3. Set Clear Expectations**

- What CAN be done (with confidence)
- What CANNOT be done (with alternatives)
- Time investment (realistic estimates)
- Quality gates (≥0.999 correlation non-negotiable)

**4. Prevent Common Mistakes**

- Read Lessons Learned Playbook FIRST (saves 8-12 hours)
- Use 5000 bars for validation (not 100 or 500)
- Don't retry NOT VIABLE approaches (30-50 hours saved)
- Respect "Correctness > Speed" philosophy

**5. Reference Documentation Frequently**

- This workspace has 95/100 documentation readiness score
- Every failure documented with solutions
- Hub-and-spoke architecture (single source of truth per topic)

---

## Error Handling Patterns

### Common Errors & Solutions

**Error**: `correlation=0.951 (threshold 0.999) - FAILED`
**Diagnosis**: Missing historical warmup
**Solution**: Fetch 5000 bars, calculate on ALL, compare last N
**Time**: 2-3 hours if not known upfront

**Error**: `No module named 'MetaTrader5'`
**Diagnosis**: Running in macOS Python (not Wine Python)
**Solution**: Use Wine Python: `wine "C:\\...\\python.exe"`
**Time**: 5-10 minutes

**Error**: `Exit code 0 but no .ex5 file created`
**Diagnosis**: Path has spaces, Wine compilation silent failure
**Solution**: Copy-Compile-Verify-Move (4-step pattern)
**Time**: 3+ hours if not known upfront

**Error**: `102 compilation errors`
**Diagnosis**: `/inc` parameter overrides defaults
**Solution**: Remove `/inc` parameter entirely
**Time**: 4+ hours if not known upfront

**Error**: `99 NaN values in indicator output`
**Diagnosis**: Using pandas rolling windows (returns NaN until full window)
**Solution**: Use manual loops for expanding window logic
**Time**: 30-45 minutes
