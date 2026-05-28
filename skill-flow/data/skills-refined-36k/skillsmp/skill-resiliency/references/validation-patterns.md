# Validation Patterns Library

## Overview

This library provides reusable validation patterns for implementing resiliency in Agent Skills. Patterns are organized by validation type and determinism level.

## Pattern Categories

1. **Input Validation** - Verify preconditions before execution
2. **Step Validation** - Check intermediate states during execution
3. **Output Validation** - Verify final results meet criteria
4. **State Validation** - Continuous monitoring of system state
5. **Recovery Validation** - Verify recovery procedures work

## Input Validation Patterns

### Pattern: Schema Validation

**Use When:** Input must match specific structure/format
**Determinism Level:** Medium to High
**Complexity:** Low

**Implementation:**

```markdown
## Input Validation

Before proceeding, validate input against schema:

1. Check file exists: `test -f input.json`
2. Validate schema: `python scripts/validate-schema.py input.json schemas/input-schema.json`
3. If validation fails:
   - Review error report at `validation-errors.log`
   - Common issues:
     - Missing required fields
     - Incorrect data types
     - Values out of range
   - Fix issues and re-validate

**Proceed only after validation passes.**
```

**Supporting Script (scripts/validate-schema.py):**

```python
#!/usr/bin/env python3
import json
import sys
from jsonschema import validate, ValidationError

def validate_input(input_file, schema_file):
    with open(input_file) as f:
        data = json.load(f)

    with open(schema_file) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        print(f"✅ Validation passed: {input_file}")
        return True
    except ValidationError as e:
        print(f"❌ Validation failed: {e.message}")
        print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        return False

if __name__ == "__main__":
    result = validate_input(sys.argv[1], sys.argv[2])
    sys.exit(0 if result else 1)
```

### Pattern: Precondition Check

**Use When:** Execution requires specific system state
**Determinism Level:** Medium to High
**Complexity:** Low

**Implementation:**

```markdown
## Pre-Execution Checklist

Verify all preconditions are met:

```bash
# Check required tools
command -v docker >/dev/null 2>&1 || { echo "Docker required"; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "kubectl required"; exit 1; }

# Check permissions
if [ ! -w /var/run/docker.sock ]; then
    echo "Docker socket not writable"
    exit 1
fi

# Check resources
FREE_DISK=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$FREE_DISK" -lt 10 ]; then
    echo "Insufficient disk space (need 10GB, have ${FREE_DISK}GB)"
    exit 1
fi

echo "✅ All preconditions met"
```

**If any check fails, do not proceed.**
```

### Pattern: Dependency Version Check

**Use When:** Skill requires specific tool versions
**Determinism Level:** High
**Complexity:** Low

**Implementation:**

```markdown
## Dependency Validation

Verify tool versions meet requirements:

Run: `scripts/check-versions.sh`

Required versions:
- Python >= 3.9
- Node >= 18.0
- Docker >= 20.10

If versions don't match, see `references/installation-guide.md`
```

**Supporting Script (scripts/check-versions.sh):**

```bash
#!/bin/bash
set -e

check_version() {
    local tool=$1
    local required=$2
    local actual=$3

    if ! command -v $tool &> /dev/null; then
        echo "❌ $tool not found"
        return 1
    fi

    if [ "$(printf '%s\n' "$required" "$actual" | sort -V | head -n1)" != "$required" ]; then
        echo "❌ $tool version $actual is below required $required"
        return 1
    fi

    echo "✅ $tool version $actual meets requirement >=$required"
    return 0
}

PYTHON_VER=$(python3 --version | cut -d' ' -f2)
NODE_VER=$(node --version | cut -d'v' -f2)
DOCKER_VER=$(docker --version | cut -d' ' -f3 | tr -d ',')

check_version "python3" "3.9.0" "$PYTHON_VER"
check_version "node" "18.0.0" "$NODE_VER"
check_version "docker" "20.10.0" "$DOCKER_VER"

echo ""
echo "✅ All version requirements met"
```

## Step Validation Patterns

### Pattern: Checkpoint Validation

**Use When:** Multi-phase workflow needs validation between phases
**Determinism Level:** Medium to High
**Complexity:** Medium

**Implementation:**

```markdown
## Phase 1: Data Extraction

[Phase 1 instructions...]

### Checkpoint: Phase 1 Complete

Validate Phase 1 completion before proceeding:

```bash
scripts/validate-phase1.sh
```

**Validation checks:**
- [ ] Extracted data file exists (`data/extracted.json`)
- [ ] Record count >= 1
- [ ] No extraction errors in logs
- [ ] Data format matches expected structure

**If validation fails:**
1. Review logs: `tail -f logs/extraction.log`
2. Check common issues in `references/troubleshooting.md` Section 1
3. Re-run Phase 1 after fixing issues
4. Re-validate

**Proceed to Phase 2 only after validation passes.**
```

### Pattern: Idempotency Check

**Use When:** Steps might be executed multiple times
**Determinism Level:** Medium to High
**Complexity:** Medium

**Implementation:**

```markdown
## Step 3: Create Resources

Before creating resources, check if they already exist:

```bash
# Check if resource exists
if kubectl get deployment myapp -n production >/dev/null 2>&1; then
    echo "⚠️  Deployment 'myapp' already exists"
    echo "Options:"
    echo "  1. Skip creation (recommended if configuration matches)"
    echo "  2. Update existing deployment"
    echo "  3. Delete and recreate (data loss warning)"
    read -p "Choose option (1-3): " choice

    case $choice in
        1) echo "Skipping creation"; exit 0 ;;
        2) kubectl apply -f deployment.yaml ;;
        3) kubectl delete deployment myapp -n production && kubectl create -f deployment.yaml ;;
    esac
else
    kubectl create -f deployment.yaml
fi
```

Verify creation:
```bash
kubectl get deployment myapp -n production
```
```

### Pattern: Progressive Validation

**Use When:** Long-running operations need incremental verification
**Determinism Level:** Medium
**Complexity:** Medium

**Implementation:**

```markdown
## Data Processing Loop

Process data in batches with incremental validation:

```python
#!/usr/bin/env python3
import json

def process_batch(batch, batch_num):
    """Process single batch with validation."""
    results = []
    errors = []

    for item in batch:
        try:
            result = transform(item)
            if validate_output(result):
                results.append(result)
            else:
                errors.append({"item": item, "error": "Validation failed"})
        except Exception as e:
            errors.append({"item": item, "error": str(e)})

    # Checkpoint: Log batch results
    with open(f"checkpoint-{batch_num}.json", "w") as f:
        json.dump({
            "batch": batch_num,
            "processed": len(results),
            "errors": len(errors),
            "results": results,
            "errors_detail": errors
        }, f)

    # Validation: Check error rate
    error_rate = len(errors) / len(batch)
    if error_rate > 0.1:  # More than 10% errors
        print(f"⚠️  Batch {batch_num}: High error rate ({error_rate:.1%})")
        print(f"   Review checkpoint-{batch_num}.json")
        response = input("Continue? (y/n): ")
        if response.lower() != 'y':
            raise Exception("Processing halted due to high error rate")

    return results, errors

# Process all batches
all_results = []
all_errors = []

for i, batch in enumerate(batches):
    print(f"Processing batch {i+1}/{len(batches)}...")
    results, errors = process_batch(batch, i+1)
    all_results.extend(results)
    all_errors.extend(errors)

# Final validation
total_error_rate = len(all_errors) / (len(all_results) + len(all_errors))
print(f"\n✅ Processing complete:")
print(f"   Success: {len(all_results)}")
print(f"   Errors: {len(all_errors)} ({total_error_rate:.1%})")

if total_error_rate > 0.05:
    print("⚠️  Error rate above threshold (5%)")
    print("   Review error details before using results")
```
```

## Output Validation Patterns

### Pattern: Comprehensive Output Verification

**Use When:** Output must meet multiple criteria
**Determinism Level:** High
**Complexity:** Medium

**Implementation:**

```markdown
## Output Validation

After execution completes, verify output meets all criteria:

Run: `scripts/validate-output.sh`

**Validation Suite:**

1. **Structure Check**
   - Output file exists
   - File format is valid JSON/YAML/etc.
   - Required fields present

2. **Content Check**
   - Values within expected ranges
   - References are valid
   - Calculations are correct

3. **Integration Check**
   - Output compatible with downstream systems
   - APIs return expected responses
   - Database constraints satisfied

4. **Quality Check**
   - No warnings or errors in logs
   - Performance within acceptable range
   - Resource usage within limits

**If any validation fails:**
- Review detailed report: `validation-report.txt`
- See recovery procedures in `references/recovery-guide.md`
- Do NOT use output until all validations pass
```

**Supporting Script (scripts/validate-output.sh):**

```bash
#!/bin/bash
set -e

OUTPUT_FILE="$1"
REPORT="validation-report.txt"

echo "Output Validation Report" > $REPORT
echo "========================" >> $REPORT
echo "File: $OUTPUT_FILE" >> $REPORT
echo "Time: $(date)" >> $REPORT
echo "" >> $REPORT

FAILURES=0

# Structure validation
echo "Structure Validation:" >> $REPORT
if [ -f "$OUTPUT_FILE" ]; then
    echo "  ✅ File exists" >> $REPORT
else
    echo "  ❌ File missing" >> $REPORT
    ((FAILURES++))
fi

if jq empty "$OUTPUT_FILE" 2>/dev/null; then
    echo "  ✅ Valid JSON" >> $REPORT
else
    echo "  ❌ Invalid JSON" >> $REPORT
    ((FAILURES++))
fi

# Content validation
echo "" >> $REPORT
echo "Content Validation:" >> $REPORT
REQUIRED_FIELDS=("id" "timestamp" "data")
for field in "${REQUIRED_FIELDS[@]}"; do
    if jq -e ".$field" "$OUTPUT_FILE" >/dev/null 2>&1; then
        echo "  ✅ Field '$field' present" >> $REPORT
    else
        echo "  ❌ Field '$field' missing" >> $REPORT
        ((FAILURES++))
    fi
done

# Summary
echo "" >> $REPORT
if [ $FAILURES -eq 0 ]; then
    echo "✅ All validations passed" >> $REPORT
    cat $REPORT
    exit 0
else
    echo "❌ $FAILURES validation(s) failed" >> $REPORT
    cat $REPORT
    exit 1
fi
```

### Pattern: Diff-Based Validation

**Use When:** Output should match known-good reference
**Determinism Level:** High
**Complexity:** Low

**Implementation:**

```markdown
## Output Verification

Compare generated output against reference:

```bash
# Generate output
./generate-config.sh > output/config.yaml

# Compare against reference
if diff -u references/expected-config.yaml output/config.yaml > config-diff.txt; then
    echo "✅ Output matches reference"
else
    echo "❌ Output differs from reference"
    echo "See diff: config-diff.txt"
    echo ""
    cat config-diff.txt
    echo ""
    echo "If differences are expected, update reference:"
    echo "  cp output/config.yaml references/expected-config.yaml"
    exit 1
fi
```
```

### Pattern: Property-Based Validation

**Use When:** Output must satisfy properties, not exact values
**Determinism Level:** Medium to High
**Complexity:** Medium

**Implementation:**

```markdown
## Output Properties Validation

Verify output satisfies required properties:

```python
#!/usr/bin/env python3
import json

def validate_properties(output_file):
    """Validate output satisfies all required properties."""
    with open(output_file) as f:
        data = json.load(f)

    errors = []

    # Property 1: All IDs are unique
    ids = [item['id'] for item in data['items']]
    if len(ids) != len(set(ids)):
        errors.append("Property violated: IDs must be unique")

    # Property 2: Timestamps are monotonically increasing
    timestamps = [item['timestamp'] for item in data['items']]
    if timestamps != sorted(timestamps):
        errors.append("Property violated: Timestamps must be increasing")

    # Property 3: All references are valid
    all_ids = set(ids)
    for item in data['items']:
        if 'parent_id' in item and item['parent_id'] not in all_ids:
            errors.append(f"Property violated: Invalid reference {item['parent_id']}")

    # Property 4: Sum of parts equals total
    total = data['summary']['total']
    computed_total = sum(item['value'] for item in data['items'])
    if abs(total - computed_total) > 0.01:  # Floating point tolerance
        errors.append(f"Property violated: Total mismatch ({total} vs {computed_total})")

    if errors:
        print("❌ Property validation failed:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print("✅ All properties satisfied")
        return True

if __name__ == "__main__":
    import sys
    result = validate_properties(sys.argv[1])
    sys.exit(0 if result else 1)
```
```

## State Validation Patterns

### Pattern: Continuous State Monitoring

**Use When:** Long-running operations need state tracking
**Determinism Level:** Medium to High
**Complexity:** High

**Implementation:**

```markdown
## State Monitoring

Track system state throughout execution:

```python
#!/usr/bin/env python3
import time
import json
from datetime import datetime

class StateMonitor:
    def __init__(self):
        self.state = {
            "status": "initializing",
            "phase": None,
            "progress": 0.0,
            "started_at": datetime.utcnow().isoformat(),
            "checkpoints": [],
            "errors": []
        }
        self.save_state()

    def update(self, **kwargs):
        """Update state and persist."""
        self.state.update(kwargs)
        self.state["updated_at"] = datetime.utcnow().isoformat()
        self.save_state()

    def checkpoint(self, name, validation_passed=True):
        """Record checkpoint with validation result."""
        self.state["checkpoints"].append({
            "name": name,
            "timestamp": datetime.utcnow().isoformat(),
            "validation_passed": validation_passed
        })
        self.save_state()

    def error(self, message):
        """Record error."""
        self.state["errors"].append({
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save_state()

    def save_state(self):
        """Persist state to file."""
        with open("state.json", "w") as f:
            json.dump(self.state, f, indent=2)

    def validate_state(self):
        """Validate current state is consistent."""
        errors = []

        # Check phase progression
        valid_phases = ["init", "process", "validate", "complete"]
        if self.state["phase"] not in valid_phases:
            errors.append(f"Invalid phase: {self.state['phase']}")

        # Check progress bounds
        if not (0 <= self.state["progress"] <= 1.0):
            errors.append(f"Invalid progress: {self.state['progress']}")

        # Check checkpoint sequence
        for i, cp in enumerate(self.state["checkpoints"]):
            if not cp["validation_passed"]:
                errors.append(f"Checkpoint {i} failed: {cp['name']}")

        return len(errors) == 0, errors

# Usage
monitor = StateMonitor()

try:
    monitor.update(status="running", phase="init", progress=0.1)
    # ... do work ...
    monitor.checkpoint("initialization")

    monitor.update(phase="process", progress=0.5)
    # ... do work ...
    valid, errors = monitor.validate_state()
    if not valid:
        raise Exception(f"State validation failed: {errors}")
    monitor.checkpoint("processing")

    monitor.update(status="complete", progress=1.0)
except Exception as e:
    monitor.error(str(e))
    monitor.update(status="failed")
    raise
```

Check state at any time:
```bash
cat state.json | jq .
```
```

## Recovery Validation Patterns

### Pattern: Rollback Verification

**Use When:** Rollback procedures must be reliable
**Determinism Level:** High
**Complexity:** High

**Implementation:**

```markdown
## Rollback Procedure

If execution fails, rollback to pre-execution state:

### Step 1: Capture Pre-Execution Snapshot

Before making changes:
```bash
scripts/create-snapshot.sh pre-execution
```

This creates:
- `snapshots/pre-execution/database-dump.sql`
- `snapshots/pre-execution/config-backup.tar.gz`
- `snapshots/pre-execution/state.json`

### Step 2: Execute with Failure Detection

[Normal execution steps...]

### Step 3: Rollback on Failure

If execution fails:
```bash
scripts/rollback.sh pre-execution
```

### Step 4: Verify Rollback

After rollback, verify state was restored:
```bash
scripts/verify-rollback.sh pre-execution
```

**Verification checks:**
- [ ] Database matches pre-execution snapshot
- [ ] Configuration files restored
- [ ] No residual changes remain
- [ ] System is operational

**If rollback verification fails:**
This is a critical failure. See `references/emergency-recovery.md`
```

**Supporting Script (scripts/verify-rollback.sh):**

```bash
#!/bin/bash
set -e

SNAPSHOT=$1
SNAPSHOT_DIR="snapshots/$SNAPSHOT"

echo "Verifying rollback to: $SNAPSHOT"
echo ""

FAILURES=0

# Verify database
echo "Checking database..."
CURRENT_HASH=$(pg_dump mydb | sha256sum | cut -d' ' -f1)
SNAPSHOT_HASH=$(sha256sum "$SNAPSHOT_DIR/database-dump.sql" | cut -d' ' -f1)

if [ "$CURRENT_HASH" == "$SNAPSHOT_HASH" ]; then
    echo "  ✅ Database matches snapshot"
else
    echo "  ❌ Database differs from snapshot"
    ((FAILURES++))
fi

# Verify config files
echo "Checking configuration..."
if diff -r config/ "$SNAPSHOT_DIR/config-backup/" >/dev/null 2>&1; then
    echo "  ✅ Configuration matches snapshot"
else
    echo "  ❌ Configuration differs from snapshot"
    ((FAILURES++))
fi

# Verify system state
echo "Checking system state..."
if systemctl is-active --quiet myapp; then
    echo "  ✅ System is running"
else
    echo "  ❌ System is not running"
    ((FAILURES++))
fi

echo ""
if [ $FAILURES -eq 0 ]; then
    echo "✅ Rollback verified successfully"
    exit 0
else
    echo "❌ Rollback verification failed ($FAILURES issues)"
    echo "See references/emergency-recovery.md"
    exit 1
fi
```

### Pattern: Recovery Test Suite

**Use When:** Recovery procedures must be pre-validated
**Determinism Level:** High
**Complexity:** High

**Implementation:**

```markdown
## Recovery Testing

Periodically test recovery procedures to ensure they work:

Run: `scripts/test-recovery.sh`

**Test Suite:**

1. **Test Snapshot Creation**
   - Create snapshot in test environment
   - Verify all components captured
   - Check snapshot integrity

2. **Test Rollback Procedure**
   - Make controlled changes
   - Execute rollback
   - Verify state restored

3. **Test Failure Scenarios**
   - Simulate partial failures
   - Verify detection mechanisms work
   - Confirm recovery paths function

4. **Test Recovery Documentation**
   - Follow documented procedures step-by-step
   - Identify missing steps or unclear instructions
   - Update documentation as needed

**Run recovery tests:**
- Monthly in production-like environment
- After any recovery procedure changes
- Before critical operations
```

## Pattern Selection Guide

### By Determinism Level

**Low Determinism (Score 0-10):**
- Skip most validation patterns
- Use lightweight guidance only

**Medium Determinism (Score 11-25):**
- Input: Schema Validation, Precondition Check
- Step: Checkpoint Validation
- Output: Property-Based Validation
- State: Basic progress tracking
- Recovery: Documentation only

**High Determinism (Score 26-40):**
- Input: All input patterns
- Step: All step patterns
- Output: All output patterns
- State: Continuous State Monitoring
- Recovery: All recovery patterns with testing

### By Skill Type

**Data Processing:**
- Schema Validation (input/output)
- Progressive Validation (batches)
- Property-Based Validation (integrity)

**Deployment/Operations:**
- Precondition Check
- Idempotency Check
- Rollback Verification
- Recovery Test Suite

**Workflow Orchestration:**
- Checkpoint Validation
- State Monitoring
- Phase-level validation

**Content Generation:**
- Minimal validation
- Optional quality checks only

---

**Remember:** Validation patterns are tools, not requirements. Select patterns that match your skill's actual determinism and risk level. Over-validation creates friction; under-validation invites failure.
