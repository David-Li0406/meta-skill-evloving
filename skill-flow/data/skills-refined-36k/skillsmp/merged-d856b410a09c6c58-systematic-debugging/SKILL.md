---
name: systematic-debugging
description: Use this skill when debugging complex issues, intermittent bugs, or performing root cause analysis.
---

# Systematic Debugging

A systematic approach to debugging aimed at identifying the root causes of complex bugs.

## 🎯 Scope of Use

**Use this skill when**:
- ✅ Error messages are vague or unclear
- ✅ Issues are intermittent or hard to reproduce
- ✅ Multiple attempts have failed to resolve the issue
- ✅ Deep analysis of the root cause is required

**Do not use this skill for**:
- ❌ Clear error messages (e.g., curl errors, encoding errors)
- ❌ Quick diagnostics for straightforward technical issues

**Collaborative Process**:
```
Encounter an error
  ↓
Is the error message clear?
  ├─ Yes → Use quick diagnostics first
  │         ↓
  │      Was it resolved?
  │         ├─ Yes → Done
  │         └─ No ↓
  └──────────────→ Use systematic debugging for deep analysis
```

---

## Debugging Steps

```
1. Define the problem      2. Isolate the scope      3. List hypotheses
   ↓                          ↓                          ↓
   └────────────────────────────────────────────────────┘
                 ↓
           4. Validate hypotheses
                 ↓
           5. Confirm root cause → Fix → Validate
```

### Step 1: Define the Problem

**Goal**: Clearly describe the problem, removing vague statements.

```bash
# ❌ Vague: "Code doesn't work"
# ✅ Precise: "API call to api/users/123 returns 500, expected 200"
```

**Problem Definition Template**:
```
- Action taken: ___________
- Expected result: ___________
- Actual result: ___________
- Frequency: Always / Intermittent (___%) / Hard to reproduce
- Environment: OS/version/dependencies
```

---

### Step 2: Isolate the Scope

**Goal**: Narrow down the problem area to reduce variables.

#### Binary Search Method

```python
# Suspect an error in a long process?
# Insert logs to determine if the issue is in the first or second half.

def long_process(data):
    logger.info("Checkpoint 1: input=%s", data)  # Checkpoint 1
    result1 = step1(data)

    logger.info("Checkpoint 2: result1=%s", result1)  # Checkpoint 2
    result2 = step2(result1)

    logger.info("Checkpoint 3: result2=%s", result2)  # Checkpoint 3
    return step3(result2)
```

#### Control Variables

```bash
# Test different input combinations
test_normal.py    # Normal input → Pass?
test_edge1.py     # Edge case 1 → Fail?
test_edge2.py     # Edge case 2 → Fail?
test_empty.py     # Empty input → Fail?
```

#### Environment Isolation

```bash
# Can it be reproduced locally?
docker-compose up  # Clean environment
```

---

### Step 3: List Hypotheses

**Goal**: List all possible causes, ordered by probability.

```
Hypothesis List Example:

| Hypothesis | Probability | Validation Method | Status |
|------------|-------------|-------------------|--------|
| Network timeout | High | Check network logs | Unverified |
| Memory leak | Medium | Check memory usage | Unverified |
| Race condition | Low | Test with locks | Unverified |
```

---

### Step 4: Validate Hypotheses

**Goal**: Design experiments to validate or eliminate hypotheses.

```bash
# Experiment 1: Validate network hypothesis
curl -v https://api.example.com 2>&1 | grep -i timeout
```

**Validation Principles**:
- Validate one hypothesis at a time.
- Each experiment should clearly confirm or eliminate a hypothesis.
- Keep records of experiments (including negative results).

---

### Step 5: Confirm Root Cause → Fix → Validate

#### Root Cause Confirmation Criteria

When the issue disappears after modification, ensure:
- ✅ Understanding of why the modification resolved the issue.
- ✅ Minimal changes (no unrelated code modified).
- ✅ Relevant tests pass.

---

## Common Debugging Strategies

### Strategy 1: Rubber Ducking

Explain the problem to someone (or a rubber duck):

```
"Okay, I'm calling this function, passing in parameter X,
and then it throws an error at line Y saying Z..."
```

### Strategy 2: Minimal Reproducible Example

```python
# ❌ Complex project hard to debug
# my_project/app/service/controller.py (500+ lines)

# ✅ Extract to a standalone script
# debug_repro.py
def reproduce():
    data = {"key": "problematic_value"}  # Minimal input
    result = function_under_test(data)
    return result

reproduce()  # Reproduce bug
```

### Strategy 3: Binary Logging Injection

```bash
# Add logs around suspicious code
logger.debug("BEFORE: x=%s", x)
# ... suspicious code ...
logger.debug("AFTER: x=%s", x)
```

### Strategy 4: Version Rollback

```bash
# When was the issue introduced?
git bisect start
git bisect bad HEAD      # Current version has a bug
git bisect good tags/v1.0  # Old version is fine

# Automatically test each intermediate version
git bisect run npm test
```

---

## Handling Intermittent Bugs

### Characteristics

- Hard to reproduce
- Occasional failures
- Possible causes: race conditions, resource leaks, timing dependencies

### Handling Methods

```bash
# 1. Increase logging to capture full context
logger.info("Full context: state=%s, thread=%s, timestamp=%s",
            state, thread_id, time.time())

# 2. Stress test to amplify the issue
for i in {1..1000}; do npm test; done
```

---

## Common Trigger Scenarios

You might hear:
- "Can't find the bug's cause"
- "Intermittent failure"
- "Occasional bug"
- "Root cause analysis"
- "Hard to reproduce"
- "Complex bug"
- "Root cause analysis"
- "Intermittent failure"

---

## Debugging Tools Reference

```bash
# General
strace -p <pid>              # System call tracing
ltrace -p <pid>              # Library call tracing
gdb -p <pid>                 # Attach debugger

# Node.js
node --inspect               # Enable debugging protocol
node --heap-prof             # Memory analysis

# Python
python -m pdb script.py      # Debugger
python -m trace --trace script.py  # Execution tracing

# Network debugging
curl -v https://api.example.com 2>&1 | tee curl.log
tcpdump -i any port 443      # Packet capture
```