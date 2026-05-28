---
name: mutation-testing
description: Use this skill to validate test quality and effectiveness through mutation testing, which assesses whether tests catch intentional code changes (mutants).
---

# Mutation Testing

Mutation testing evaluates the quality of a test suite by introducing small, deliberate bugs (mutations) into the code and checking if the tests can catch them. This provides a behavioral measure of test effectiveness beyond simple coverage metrics.

## Core Concept

**Mutation testing workflow**:
1. Generate mutations (small code changes).
2. Run the test suite against each mutation.
3. Classify results:
   - **Killed**: Test fails (good - test caught the bug).
   - **Survived**: Test passes (bad - test missed the bug).
   - **Timeout**: Test hangs or exceeds time limit.
4. Calculate mutation score: `killed / (total - timeouts)`.
5. For survived mutants, generate targeted tests.

**Why mutation testing matters**: Tests can achieve 100% line coverage while missing critical bugs. Mutation testing reveals if tests actually verify behavior or just execute code.

## When to Use Mutation Testing

Use mutation testing proactively for:
- Validating newly written tests.
- Ensuring mission-critical code has thorough tests.
- Quality gate during PR reviews to prevent merging code with weak tests.
- Verifying tests catch regressions before changing code.
- Validating tests for complex logic, boundary conditions, and error handling.

**Target mutation scores**:
- Mission-critical code: 90%+
- Core business logic: 80-90%
- General code: 70-80%
- Low-risk code: 60-70%

## Mutation Operators

Common mutation operators include:
| Category      | Original         | Mutant          |
|---------------|------------------|------------------|
| Arithmetic    | `a + b`          | `a - b`          |
| Relational    | `x >= 18`        | `x > 18`         |
| Logical       | `a && b`         | `a || b`         |
| Conditional    | `if (x)`        | `if (true)`      |
| Statement     | `return x`       | *(removed)*      |

## Implementation Process

### 1. Detect Project and Install Tool

```python
def setup_mutation_tool(project_type):
    if project_type == "javascript":
        return "npx stryker init"
    elif project_type == "python":
        return "pip install mutmut"
    elif project_type == "java":
        return "Add pitest plugin to pom.xml"
```

### 2. Configure Mutation Testing

**Stryker (JavaScript)**:
```json
{
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "testRunner": "vitest",
  "reporters": ["html", "progress"],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

**mutmut (Python)**:
```ini
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=pytest
```

**PITest (Java)**:
```xml
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <configuration>
        <targetClasses>
            <param>com.example.*</param>
        </targetClasses>
        <mutationThreshold>80</mutationThreshold>
    </configuration>
</plugin>
```

### 3. Run Mutation Analysis

```bash
# JavaScript
npx stryker run

# Python
mutmut run

# Java
mvn org.pitest:pitest-maven:mutationCoverage
```

### 4. Parse and Report Results

```python
def parse_mutation_results(report_path):
    """Parse mutation testing report"""
    return {
        "total_mutants": 150,
        "killed": 120,
        "survived": 25,
        "timeout": 5,
        "mutation_score": 80.0,
        "survivors": [
            {
                "file": "src/auth/validate.ts",
                "line": 45,
                "mutator": "RelationalOperator",
                "original": "age >= 18",
                "mutant": "age > 18",
                "status": "survived"
            }
        ]
    }
```

## Output Format

### Mutation Testing Report

**Module**: src/auth/  
**Test Suite**: test/auth/

| Metric          | Value         |
|-----------------|---------------|
| Total Mutants   | 150           |
| Killed          | 120 (80%)     |
| Survived        | 25 (17%)      |
| Timeout         | 5 (3%)        |
| **Mutation Score** | **80%**   |

### Recommended Test Improvements
1. **Add boundary tests** for `validate.ts`.
2. **Add error path tests** for `login.ts`.
3. **Test null/undefined cases** in `session.ts`.

## Best Practices

- Focus on high-impact code: Run mutation testing on critical paths, not trivial getters/setters.
- Interpret mutation scores in context: A 75% score with good tests covering critical paths may be better than 95% with superficial tests.
- Handle equivalent mutants: Some mutations don't change behavior and can be ignored.
- Use mutation testing to guide test improvement, not as a one-time audit.

## Related Skills
- `tdd-enforce` - Enforce test-first development.
- `flaky-detect` - Identify unreliable tests.
- `test-sync` - Maintain test-code alignment.