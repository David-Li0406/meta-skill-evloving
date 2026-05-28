---
name: verify-deploy
description: Full system verification loop for deployment readiness
---

# Verify & Deploy Skill

This skill runs the complete verification suite to confirm the system is ready for deployment or commit.

## Usage
Invoke with: `/verify-deploy` or "run the verify deploy skill"

## Prerequisites
- Python virtual environment activated
- All dependencies installed

## Steps

// turbo-all

### Step 1: Audit Critical Paths
Verify required files exist:
```powershell
$paths = @('.env', 'config/default.json', '.venv')
$results = @()
foreach ($p in $paths) {
    $exists = Test-Path $p
    $results += [PSCustomObject]@{Path=$p; Exists=$exists}
}
$results | Format-Table -AutoSize
```

### Step 2: Run Unit Tests
```powershell
$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -m pytest tests/ -v --tb=short
```
**Pass Condition**: Exit code 0, no failures.

### Step 3: Smoke Backtest
```powershell
$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe -m src.laptop_agents.run --mode backtest --source mock --backtest 100
```
**Pass Condition**: Exit code 0, `runs/latest/summary.html` exists.

### Step 4: Live System Test
```powershell
$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe scripts/test_live_system.py
```
**Pass Condition**: Exit code 0.

### Step 5: Integration Test
```powershell
$env:PYTHONPATH="src"; .\.venv\Scripts\python.exe scripts/test_dual_mode.py
```
**Pass Condition**: Exit code 0.

### Step 6: Output Summary
After all steps complete, output a summary table:

| Step | Command | Status |
|:---|:---|:---|
| Audit Paths | `Test-Path ...` | PASS/FAIL |
| Unit Tests | `pytest tests/` | PASS/FAIL |
| Smoke Backtest | `--mode backtest` | PASS/FAIL |
| Live System Test | `test_live_system.py` | PASS/FAIL |
| Integration | `test_dual_mode.py` | PASS/FAIL |

## Success Criteria
All 5 steps must PASS for the skill to succeed.

## On Failure
- Do NOT commit any changes
- Report which step failed
- Check `runs/latest/` for artifacts
