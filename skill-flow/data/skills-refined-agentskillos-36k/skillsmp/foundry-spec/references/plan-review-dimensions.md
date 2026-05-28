# Review Dimensions

Every spec review examines across 6 dimensions to ensure comprehensive coverage.

## 1. Completeness

Ensures the spec has all necessary information for implementation.

**Checks:**
- All sections present (mission, phases, tasks)
- Sufficient detail for implementation
- No gaps in requirements
- Dependencies fully specified
- Metadata complete (estimates, owners, acceptance criteria)

## 2. Clarity

Ensures descriptions are unambiguous and actionable.

**Checks:**
- Unambiguous descriptions
- Specific acceptance criteria
- Clear success metrics
- Well-defined boundaries
- No jargon or unclear terminology

## 3. Feasibility

Validates that the work is achievable as specified.

**Checks:**
- Realistic time estimates
- Achievable dependencies
- Available resources
- Technical viability
- No circular dependencies

## 4. Architecture

Evaluates design decisions and structural quality.

**Checks:**
- Sound design decisions
- Proper abstractions
- Scalability considerations
- Integration patterns
- Separation of concerns

## 5. Risk Management

Identifies and addresses potential issues.

**Checks:**
- Risks identified
- Edge cases covered
- Mitigation strategies
- Fallback plans
- Security considerations

## 6. Verification

Ensures the spec can be properly validated.

**Checks:**
- Comprehensive test plan
- Quality gates defined
- Acceptance criteria testable
- Coverage expectations
- Verification steps for each phase

## Dimension Coverage by Review Type

| Review Type | Primary Dimensions | Secondary Dimensions |
|-------------|-------------------|---------------------|
| `quick` | Completeness, Clarity | - |
| `full` | All 6 dimensions | Equal weight |
| `security` | Risk Management, Architecture | Verification |
| `feasibility` | Feasibility, Completeness | - |
