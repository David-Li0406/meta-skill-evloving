# Spec Python Tools

Automated validation and critique tools for feature specifications.

## Tools

### 1. validate_spec.py

**Purpose:** Structural validation of generated specifications

**Usage:**
```bash
python validate_spec.py /path/to/job-queue/feature-{name}
```

**Checks Performed:**

#### File Existence
- docs/FRD.md
- docs/FRS.md
- docs/GS.md
- docs/TR.md
- docs/task-list.md

#### File Content
- Files not empty (> 100 bytes)
- Has section headers (markdown `#`)
- Reasonable file sizes

#### Gherkin Syntax (GS.md)
- Has `Feature:` declaration
- Has `Scenario:` declarations
- Has Given/When/Then steps
- Optional: Background section

#### Task List Quality
- Has actionable items (at least 3)
- Tasks have clear descriptions (> 50 chars)
- Not all tasks are vague

#### Gitignore Check
- .gitignore contains `/job-queue` entry

#### Cross-References
- FRS.md references FRD.md
- TR.md references FRS.md
- GS.md covers FRS requirements

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["TR.md missing API endpoint details"],
  "completeness_score": 0.85,
  "checks_passed": 17,
  "total_checks": 20
}
```

**Exit Codes:**
- 0: Validation passed (no errors)
- 1: Validation failed (errors found)

---

### 2. critique_plan.py

**Purpose:** Critical quality analysis of specifications

**Usage:**
```bash
python critique_plan.py /path/to/job-queue/feature-{name}
```

**Optional Focus Areas:**
```bash
python critique_plan.py /path/to/feature {--focus requirements,tasks}
```

**Analysis Categories:**

#### 1. Requirement Quality (FRD.md, FRS.md)

**Specificity Check:**
- Flags vague requirements (generic verbs without specifics)
- Looks for measurable criteria (timings, sizes, counts)
- Checks requirement length and detail

**Acceptance Criteria:**
- Has "Acceptance Criteria" section?
- Criteria are measurable?
- Quantifiable metrics present?

**Edge Cases:**
- Error handling mentioned?
- Validation rules documented?
- Boundary conditions covered?

**Score:** 0.0 - 1.0 per category

#### 2. Task Breakdown (task-list.md)

**Atomicity:**
- Tasks specific and actionable?
- Not too broad ("Implement X")?
- Reasonable task descriptions?

**Sequencing:**
- Tasks numbered or phased?
- Logical order (setup → implementation → testing)?
- Dependencies identified?

**Estimates:**
- Realistic complexity?
- Tasks not too large?

**Score:** 0.0 - 1.0 per category

#### 3. Technical Design (TR.md)

**API Definitions:**
- Endpoints documented?
- HTTP methods specified?
- Request/response schemas defined?

**Data Models:**
- Schema/entity definitions?
- Field types specified?
- Relationships documented?

**Error Handling:**
- Error scenarios covered?
- Retry/fallback logic?
- HTTP error codes?

**Security:**
- Authentication mentioned?
- Authorization rules?
- Input validation?
- Data protection?

**Score:** 0.0 - 1.0 per category

#### 4. Testability (GS.md)

**Scenario Automation:**
- Gherkin steps concrete?
- Specific values used?
- Steps automatable?

**Test Data:**
- Example data provided?
- Test fixtures mentioned?
- Scenario outlines with tables?

**Score:** 0.0 - 1.0 per category

**Output:**
```json
{
  "critique_score": 0.75,
  "critical_issues": [
    {
      "file": "FRS.md",
      "issue": "Requirement FR-003 is vague",
      "suggestion": "Specify exact input validation rules"
    }
  ],
  "warnings": [
    {
      "file": "task-list.md",
      "issue": "Task 'Set up authentication' too broad",
      "suggestion": "Break into: 1) Choose library, 2) Implement login, 3) Add tests"
    }
  ],
  "recommendations": [
    "Add security requirements to TR.md",
    "Specify error handling in FRS.md"
  ],
  "score_breakdown": {
    "requirement_specificity": 0.6,
    "acceptance_criteria": 0.9,
    "edge_cases": 0.6,
    "task_atomicity": 0.7,
    "task_sequencing": 0.9,
    "api_definitions": 0.75,
    "data_models": 0.5,
    "error_handling": 0.6,
    "testability": 0.8
  }
}
```

**Exit Codes:**
- 0: Always returns 0 (critique is informational)

---

## Dependencies

**None!** Both tools use Python standard library only:
- `json` - JSON parsing
- `sys` - CLI arguments
- `re` - Regular expressions
- `pathlib` - File path handling

No `pip install` required.

---

## Integration

### With Skills

**`/spec review`** uses both tools:
1. Runs `validate_spec.py` first
2. If valid, runs `critique_plan.py`
3. Presents combined results

### With Hook

**`feedback-loop.md`** hook automatically runs both:
1. After spec-writer agent completes
2. Validates structure
3. Critiques quality
4. Presents to user

### Standalone

Can be run independently:
```bash
# Validate only
python validate_spec.py /path/to/feature

# Critique only
python critique_plan.py /path/to/feature

# Both
python validate_spec.py /path/to/feature && \
python critique_plan.py /path/to/feature
```

---

## Scoring Interpretation

### Validation Completeness Score

- **0.9 - 1.0:** Excellent (all checks passed)
- **0.7 - 0.9:** Good (minor warnings)
- **0.5 - 0.7:** Fair (several warnings, no errors)
- **< 0.5:** Poor (errors present)

### Critique Quality Score

- **0.8 - 1.0:** High quality (ready for development)
- **0.6 - 0.8:** Good quality (minor improvements recommended)
- **0.4 - 0.6:** Fair quality (several issues to address)
- **< 0.4:** Low quality (major revision needed)

---

## Error Handling

Both tools handle errors gracefully:

**File Not Found:**
```json
{
  "valid": false,
  "errors": ["Feature folder not found: /path"],
  ...
}
```

**Invalid Arguments:**
```json
{
  "valid": false,
  "errors": ["Usage: python validate_spec.py /path/to/feature-folder"],
  ...
}
```

**Script Errors:**
- Print JSON with error message
- Exit with code 1
- Never crash silently

---

## Performance

Both tools are fast:
- **validate_spec.py:** < 2 seconds
- **critique_plan.py:** < 3 seconds
- **Total:** ~5 seconds combined

Suitable for automatic execution in hooks.

---

## Testing

Test both tools with sample specs:

```bash
# Create test specs
mkdir -p /tmp/test-feature/docs
echo "# FRD" > /tmp/test-feature/docs/FRD.md
echo "Feature: Test" > /tmp/test-feature/docs/GS.md
# ... create other files

# Run validation
python validate_spec.py /tmp/test-feature

# Run critique
python critique_plan.py /tmp/test-feature
```

---

## Future Enhancements

Potential improvements (not implemented):

1. **Validation:**
   - Check for duplicate requirement IDs
   - Validate markdown links
   - Check for TODO comments

2. **Critique:**
   - Estimate task complexity (story points)
   - Detect missing API versioning
   - Flag security vulnerabilities

3. **Both:**
   - Configurable thresholds
   - Custom validation rules
   - HTML report output

---

See `../README.md` for complete spec system documentation.
