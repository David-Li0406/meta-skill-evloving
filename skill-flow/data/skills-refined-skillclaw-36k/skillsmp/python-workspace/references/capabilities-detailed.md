**Skill**: [MQL5→Python Translation Workspace Skill](../SKILL.md)

#### 2. GUI-Based Custom Indicator Export (v4.0.0)

**Status**: ✅ PRODUCTION (file-based config system complete)

**What It Does**:

- Exports custom indicator values via file-based configuration
- 13 configurable parameters (symbol, timeframe, bars, indicator flags)
- Flexible parameter changes without code editing
- Execution time: 20-30 seconds (manual drag-and-drop required)

**Workflow**:

```bash
# Step 1: Generate config
python generate_export_config.py \
  --symbol EURUSD --timeframe M1 --bars 5000 \
  --laguerre-rsi --output custom_export.txt

# Step 2: Drag ExportAligned.ex5 to chart in MT5 GUI, click OK
# Step 3: CSV exported to MQL5/Files/
```

**Use When**: User needs custom indicator values (Laguerre RSI, proprietary indicators)

**Limitations**: Requires GUI interaction (not fully headless)

**Reference**: `/docs/guides/V4_FILE_BASED_CONFIG_WORKFLOW.md`

---

#### 3. Rigorous Validation Framework

**Status**: ✅ PRODUCTION (1.000000 correlation achieved for Laguerre RSI)

**What It Does**:

- Validates Python implementations against MQL5 reference exports
- Calculates 4 metrics: Pearson correlation, MAE, RMSE, max difference
- Stores historical validation runs in DuckDB for regression detection
- 32-test comprehensive suite (P0-P3 priorities)

**Quality Gates**:

- **Correlation**: MUST be ≥0.999 (not 0.95 "good enough")
- **MAE**: MUST be \<0.001
- **NaN Count**: MUST be 0 (after warmup period)
- **Historical Warmup**: MUST use 5000+ bars for adaptive indicators

**Command Example**:

```bash
python validate_indicator.py \
  --csv Export_EURUSD_PERIOD_M1.csv \
  --indicator laguerre_rsi \
  --threshold 0.999
```

**Use When**: User needs to verify Python indicator accuracy

**Critical Requirement**: 5000-bar warmup (NOT 100 or 500 bars)

**Reference**: `/docs/guides/INDICATOR_VALIDATION_METHODOLOGY.md`

---

#### 4. Complete MQL5→Python Migration Workflow (7 Phases)

**Status**: ✅ PRODUCTION (2-4 hours first time, 1-2 hours subsequently)

**What It Does**:

- Phase 1: Locate & analyze MQL5 indicator (40% automated)
- Phase 2: Modify MQL5 to expose buffers (30% automated)
- Phase 3: CLI compile (~1 second, 90% automated)
- Phase 4: Fetch historical data (95% automated)
- Phase 5: Implement Python indicator (20% automated)
- Phase 6: Validate with warmup (95% automated)
- Phase 7: Document lessons (40% automated)

**Overall Automation**: 60-70% (strategic automation at integration points)

**Self-Correction Mechanisms**:

1. Validation-driven re-implementation loop (correlation threshold)
1. Multi-level compilation verification (4 checks)
1. Wine Python MT5 API error handling (actionable messages)
1. DuckDB historical tracking (regression detection)
1. Comprehensive test suite (32 automated tests)

**Use When**: User wants to migrate a complete indicator from MQL5 to Python

**Time Investment**: 2-4 hours first indicator, faster for subsequent indicators

**Reference**: `/docs/guides/MQL5_TO_PYTHON_MIGRATION_GUIDE.md`

---

#### 5. Lessons Learned Knowledge Base (185+ Hours Captured)

**Status**: ✅ COMPREHENSIVE (8 critical gotchas, 6 validation pitfalls)

**What It Contains**:

- **8 Critical Gotchas**: /inc parameter trap, path spaces, warmup requirement, pandas mismatches, array indexing, shared state, parameter passing, temporal assumptions
- **6 Validation Pitfalls**: Cold start comparison, pandas rolling windows, off-by-one errors, series vs iloc, NaN handling, correlation thresholds
- **70+ Legacy Items**: Documented as NOT VIABLE to prevent retesting
- **Time Savings**: 30-50 hours per developer by reading first

**Use When**: User encounters a bug or wants to avoid common mistakes

**Critical Reading**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md` (read BEFORE starting work)

**Reference**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md`

---

### ❌ WHAT THIS WORKSPACE **CANNOT DO**

#### 1. Custom Indicator Headless Automation

**Limitation**: Python MetaTrader5 API cannot access custom indicator buffers

**Why**: API design limitation - no `copy_buffer()` function for custom indicators

**Evidence**:

- `/archive/experiments/spike_1_mt5_indicator_access.py` (confirmed via testing)
- Official MetaQuotes statement: "Python API unable to access indicators"

**Alternative**:

- Use v4.0.0 GUI mode for custom indicator exports
- OR reimplement indicator logic in Python directly

**Time Saved by Knowing**: 2+ hours (don't waste time trying API approach)

**Reference**: `/docs/guides/EXTERNAL_RESEARCH_BREAKTHROUGHS.md` (Research B)

---

#### 2. Reliable Startup.ini Parameter Passing

**Limitation**: MT5 does NOT support named sections or ScriptParameters reliably

**Why**: Fundamental MT5 bugs documented in 30+ community sources (2015-2025)

**Failed Approaches** (v2.1.0 - ALL NOT VIABLE):

1. Named sections `[ScriptName]` - ignored by MT5
1. ScriptParameters directive - blocks execution silently
1. .set preset files - strict requirements + silent failures

**Evidence**:

- `/archive/plans/HEADLESS_MQL5_SCRIPT_SOLUTION_A.NOT_VIABLE.md` (22 KB research)
- Full day of testing, comprehensive community research

**Alternative**:

- Use v3.0.0 Python API (no startup.ini needed)
- OR use v4.0.0 file-based config (MQL5/Files/export_config.txt)

**Time Saved by Knowing**: 6-8 hours (approach is research-confirmed broken)

**Reference**: `/docs/guides/SCRIPT_PARAMETER_PASSING_RESEARCH.md`

---

#### 3. Pandas Rolling Windows for MQL5 ATR

**Limitation**: Pandas `rolling().mean()` does NOT match MQL5 expanding window behavior

**Why**: Different denominator logic

- MQL5: `sum(bars 0-5) / 32` (divide by period, even if partial)
- Pandas: `sum(bars 0-5) / 6` (divide by available bars)

**Impact**: 0.95 correlation (FAILED validation) instead of 1.000000

**Required Fix**: Manual loops (10x slower, but correct)

```python
for i in range(len(tr)):
    if i < period:
        atr.iloc[i] = tr.iloc[:i+1].sum() / period  # NOT pandas rolling
    else:
        atr.iloc[i] = tr.iloc[i-period+1:i+1].mean()
```

**Project Philosophy**: "Correctness > Speed for validation"

**Time Saved by Knowing**: 30-45 minutes debugging NaN values

**Reference**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md` (Gotcha #4)

---

#### 4. Cold Start Validation (\<5000 Bars)

**Limitation**: Cannot validate adaptive indicators without sufficient historical warmup

**Why**: ATR requires 32-bar lookback, Adaptive Period requires 64-bar warmup

**Evidence**:

- 100 bars → 0.951 correlation (FAILED)
- 5000 bars → 1.000000 correlation (PASSED)

**Mental Model**:

```
MQL5: [....4900 bars warmup....][100 bars exported]
Python: [100 bars CSV] ← ZERO context (WRONG!)

Correct: Fetch 5000, calculate on ALL, compare last N
```

**Required Workflow**: Two-stage validation (fetch 5000, calculate all, compare subset)

**Time Saved by Knowing**: 2-3 hours debugging correlation failures

**Reference**: `/docs/guides/PYTHON_INDICATOR_VALIDATION_FAILURES.md` (Failure #5)

---

#### 5. Accept 0.95 Correlation as "Good Enough"

**Limitation**: 0.95 correlation indicates systematic bias, NOT "95% accurate"

**Why**: Small errors compound in live trading

**Production Requirement**: ≥0.999 (99.9% minimum)

**Diagnostic Pattern**:

- 0.95-0.97: Missing historical warmup
- 0.85-0.95: NaN handling mismatch
- 0.70-0.85: Algorithm mismatch
- \<0.70: Fundamental implementation error

**Time Saved by Knowing**: Don't waste time on "good enough" - fix the root cause

**Reference**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md` (Bug Pattern #1)

---

#### 6. Wine/CrossOver Compilation with Spaces in Paths

**Limitation**: Paths with spaces break Wine compilation SILENTLY

**Symptom**: Exit code 0 (success!) but NO .ex5 file created

**Required Workflow**: Copy-Compile-Verify-Move (4 steps)

```bash
# Step 1: Copy to simple path
cp "Complex (Name).mq5" "C:/Temp.mq5"

# Step 2: Compile
metaeditor64.exe /compile:"C:/Temp.mq5"

# Step 3: Verify (.ex5 exists AND log shows 0 errors)
ls -lh "C:/Temp.ex5"

# Step 4: Move to destination
cp "C:/Temp.ex5" "C:/Program Files/.../Script.ex5"
```

**Time Saved by Knowing**: 3+ hours debugging silent failures

**Reference**: `/docs/guides/LESSONS_LEARNED_PLAYBOOK.md` (Gotcha #2)

---

#### 7. Use `/inc` Parameter for Standard Compilation

**Limitation**: `/inc` parameter OVERRIDES (not augments) default include paths

**Common Mistake**:

```bash
# WRONG (causes 102 errors):
metaeditor64.exe /compile:"C:/Program Files/MT5/MQL5/Scripts/Script.mq5" \
  /inc:"C:/Program Files/MT5/MQL5"  # Redundant + breaks

# RIGHT (no /inc needed):
metaeditor64.exe /compile:"C:/Program Files/MT5/MQL5/Scripts/Script.mq5"
```

**When to Actually Use `/inc`**: ONLY when compiling from EXTERNAL directory

**Time Saved by Knowing**: 4+ hours debugging compilation errors

**Reference**: `/docs/guides/EXTERNAL_RESEARCH_BREAKTHROUGHS.md` (Research A)
