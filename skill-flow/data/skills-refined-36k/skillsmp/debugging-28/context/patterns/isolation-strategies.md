# Isolation Strategies for Debugging

## The Core Principle

Debugging is about reducing a complex system to the simplest case that still reproduces the bug. The faster you can isolate, the faster you can fix.

## Binary Search Debugging

The most powerful isolation technique. Cut the problem space in half repeatedly.

### Application to Code:
```
1. Bug exists somewhere in 1000 lines
2. Add breakpoint/log at line 500
3. Is data correct at line 500?
   - Yes → Bug is in lines 501-1000
   - No → Bug is in lines 1-500
4. Repeat until found (10 iterations max for 1000 lines)
```

### Application to Commits:
```bash
# Find which commit introduced the bug
git bisect start
git bisect bad                  # Current commit is bad
git bisect good abc123          # Known good commit
# Git checks out middle commit
# Test and mark:
git bisect good  # or
git bisect bad
# Repeat until found
git bisect reset  # When done
```

### Application to Changes:
```
Recent changes: A, B, C, D, E
1. Revert C, D, E - Bug still exists?
   - Yes → Bug is in A or B
   - No → Bug is in C, D, or E
2. Continue halving
```

## Comment-Out Strategy

Systematically disable code to find the problem.

### Process:
```python
def problematic_function():
    step_a()
    # step_b()  # Commented out
    step_c()
    # step_d()  # Commented out
    step_e()

# Does bug still occur?
# Yes → Bug is in step_a, step_c, or step_e
# No → Bug is in step_b or step_d
```

### Best practices:
- Comment out in logical chunks
- Keep track of what you've tried
- Restore code after finding bug
- Don't ship commented code

## Minimal Reproduction

Create the smallest possible case that demonstrates the bug.

### Steps:
1. Start with the full broken scenario
2. Remove components one at a time
3. After each removal, test if bug persists
4. Stop when removing anything makes bug disappear
5. What remains is the minimal reproduction

### Example:
```
Full scenario:
- User logs in
- Navigates to settings
- Changes profile picture
- Clicks save
- Error occurs

Minimal reproduction:
- POST /api/profile with image > 5MB
- Error occurs

Root cause: Missing file size validation
```

## Environment Isolation

Determine if the bug is code or environment.

### Compare environments:
```
Does it work in:
□ Development?
□ Staging?
□ Production?
□ Different machine?
□ Different browser?
□ Docker vs native?
```

### Isolate differences:
```bash
# Compare environment variables
diff <(ssh prod printenv | sort) <(ssh staging printenv | sort)

# Compare versions
python --version
node --version
docker-compose config
```

## Dependency Isolation

Is the bug in your code or a dependency?

### Test without dependency:
```python
# Replace with stub
class MockDatabase:
    def query(self, q):
        return [{"id": 1, "name": "test"}]

db = MockDatabase()  # Instead of real DB
```

### Version comparison:
```bash
# Test with different versions
pip install package==1.0.0  # Known good
pip install package==2.0.0  # Suspected bad
```

## Input Isolation

What input triggers the bug?

### Boundary testing:
```
Test inputs:
- Empty: ""
- Single: "a"
- Normal: "hello"
- Unicode: "日本語"
- Special chars: "<script>"
- Long: "a" * 10000
- Null: None
- Negative: -1
- Zero: 0
- Max int: 2^31-1
```

### Diff the inputs:
```
Working input: {"name": "Alice", "age": 30}
Broken input:  {"name": "Bob", "age": null}

Difference: null age value
```

## Timing Isolation

Is it a race condition?

### Add delays:
```python
# Slow things down
import time
time.sleep(0.1)  # Add between operations
```

### Add synchronization:
```python
# Force sequential execution
with lock:
    operation_a()
with lock:
    operation_b()
```

### Check timing:
```python
import time
start = time.time()
operation()
print(f"Operation took: {time.time() - start}s")
```

## State Isolation

Is there corrupted or unexpected state?

### Snapshot state:
```python
import json
print(json.dumps(state, indent=2, default=str))
```

### Compare states:
```python
before = capture_state()
operation()
after = capture_state()
diff = find_differences(before, after)
print(f"State changes: {diff}")
```

### Fresh start:
```bash
# Clear all state
rm -rf .cache/
docker-compose down -v
npm cache clean --force
```

## Network Isolation

Is it a network issue?

### Test locally:
```bash
# Bypass network entirely
curl http://localhost:8080/api/test
```

### Mock external services:
```python
# Use local mock instead of real API
responses.add(
    responses.GET,
    "https://api.external.com/data",
    json={"mock": "data"}
)
```

## The Isolation Checklist

When debugging, ask:

```
□ Can I reproduce it consistently?
□ Can I reproduce it in isolation?
□ What's the minimal case?
□ When did it start working/breaking?
□ What changed between working and broken?
□ Does it happen everywhere or specific conditions?
□ Can I rule out environment factors?
□ Can I rule out timing factors?
□ Can I rule out state factors?
□ Can I rule out dependencies?
```

## Anti-Patterns

### Don't:
- Change multiple things at once
- Assume without verifying
- Skip creating minimal reproduction
- Ignore "it works on my machine"
- Trust without testing

### Do:
- Change one thing at a time
- Verify every assumption
- Create minimal reproduction first
- Investigate environment differences
- Test your hypotheses
