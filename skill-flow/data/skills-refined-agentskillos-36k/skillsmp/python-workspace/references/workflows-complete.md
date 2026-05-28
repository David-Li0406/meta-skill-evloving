**Skill**: [MQL5→Python Translation Workspace Skill](../SKILL.md)

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
