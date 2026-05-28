---
name: skill-resiliency
description: This skill should be used when the user asks to "add resiliency to a skill", "make this skill more robust", "improve error handling", "add validation mechanisms", "create self-correcting behavior", or discusses determinism, robustness, error correction, or homeostatic patterns in Agent Skills. Applies biological resiliency principles from Michael Levin's work to Agent Skill design.
---

# Skill Resiliency

## Overview

This skill applies Michael Levin's biological resiliency principles to Agent Skills design. It provides a framework for building robust, self-correcting skills that maintain goal-directed behavior despite perturbations, with resiliency mechanisms scaled proportionally to the skill's determinism requirements.

**Core Principle:** The degree of resiliency in a skill should be positively correlated with its determinism. More deterministic skills (those requiring precise, repeatable outcomes) need stronger resiliency mechanisms to maintain their target behavior.

**Inspired by:** Michael Levin's research on anatomical homeostasis, error correction in biological systems, and collective intelligence in cellular networks.

## When to Use This Skill

Apply resiliency patterns when:
- Creating skills that require deterministic outcomes
- Building skills with complex multi-step workflows
- Designing skills that interact with external systems or tools
- Improving existing skills that fail under edge cases
- Developing skills for critical operations (deployment, data processing, security)

**Resiliency Level Guide:**
- **High Determinism** (scripts, automation, data validation) → **High Resiliency** (extensive validation, recovery, monitoring)
- **Medium Determinism** (structured workflows, domain guidance) → **Medium Resiliency** (checkpoint validation, error detection)
- **Low Determinism** (creative tasks, exploration, ideation) → **Low Resiliency** (minimal constraints, flexible adaptation)

## Biological Resiliency Principles

Michael Levin's research reveals how biological systems achieve remarkable robustness through:

### 1. Anatomical Homeostasis
Biological systems actively maintain target morphology by continuously reducing error. Example: salamander limb regeneration stops when (and only when) a "correct salamander limb" is complete.

**Applied to Skills:** Skills should define clear success criteria and include mechanisms to validate progress toward those goals.

### 2. Error Correction
Systems activate effectors at multiple scales to reduce error relative to target states. Cells coordinate to repair damage and restore function.

**Applied to Skills:** Skills should include validation checkpoints that detect deviations from expected states and trigger corrective actions.

### 3. Robustness Through Collective Intelligence
Cell swarms exhibit both robustness (reliable outcomes) and plasticity (multiple valid paths). The system is resilient to perturbations while exploring solution space.

**Applied to Skills:** Skills should define required outcomes while allowing flexibility in implementation paths. Multiple approaches can achieve the same validated result.

### 4. Goal-Directed Behavior
Biological systems work toward specific outcomes across timescales, using feedback loops to navigate toward target states despite noise and variation.

**Applied to Skills:** Skills should specify goals explicitly and provide feedback mechanisms to assess progress and adjust course.

## Resiliency Design Framework

### Step 1: Assess Determinism Requirements

Classify your skill's determinism level:

**High Determinism Indicators:**
- Executes scripts or automated processes
- Modifies production systems or data
- Requires specific file formats or structures
- Depends on external tool outputs
- Has compliance or security requirements
- Must produce bit-perfect reproducible results

**Medium Determinism Indicators:**
- Follows structured workflows with clear phases
- Creates artifacts with defined schemas
- Interacts with version control or APIs
- Requires validation of intermediate states
- Has quality gates or checkpoints

**Low Determinism Indicators:**
- Explores problem space creatively
- Generates ideas or content
- Provides guidance without strict structure
- Adapts to user preferences dynamically
- Has subjective success criteria

### Step 2: Design Resiliency Mechanisms

Based on determinism level, implement appropriate resiliency patterns:

#### High Determinism Skills: Comprehensive Resiliency

**Pre-Execution Validation:**
- Validate all inputs against schemas
- Check preconditions (file existence, permissions, dependencies)
- Verify tool availability and versions
- Create backup/snapshot points
- Document expected state

**Execution Monitoring:**
- Validate each step's output before proceeding
- Log state transitions and decisions
- Implement retry mechanisms with exponential backoff
- Set timeouts for external operations
- Capture error context for debugging

**Post-Execution Verification:**
- Verify final output against success criteria
- Run test suites or validation scripts
- Check system state consistency
- Generate execution report
- Provide rollback instructions if validation fails

**Recovery Procedures:**
- Include explicit rollback steps
- Document manual recovery procedures
- Provide diagnostic scripts
- Log all state changes for audit trail

**Example Structure:**
```
high-determinism-skill/
├── SKILL.md                    # Core workflow with validation checkpoints
├── scripts/
│   ├── validate-input.py      # Pre-execution validation
│   ├── verify-output.py       # Post-execution verification
│   └── rollback.sh            # Recovery procedure
├── references/
│   ├── schemas.md             # Input/output schemas
│   └── recovery-guide.md      # Detailed recovery procedures
└── examples/
    └── validated-workflow.md  # Example with all checkpoints
```

#### Medium Determinism Skills: Balanced Resiliency

**Checkpoint Validation:**
- Define phase boundaries with clear exit criteria
- Validate artifacts at checkpoints
- Provide status summaries
- Enable phase restart without full restart

**Error Detection:**
- Identify common failure modes
- Provide clear error messages with context
- Suggest corrective actions
- Document troubleshooting steps

**State Management:**
- Create summary files tracking progress
- Enable resumption from checkpoints
- Document current state clearly
- Track key decisions

**Example Structure:**
```
medium-determinism-skill/
├── SKILL.md                        # Workflow with checkpoints
├── scripts/
│   └── validate-checkpoint.sh     # Phase validation
├── references/
│   └── troubleshooting.md         # Common issues and fixes
└── examples/
    └── checkpoint-workflow.md     # Example with phase validation
```

#### Low Determinism Skills: Minimal Resiliency

**Guidance and Constraints:**
- Provide principles, not procedures
- Suggest rather than prescribe
- Enable exploration within bounds
- Document anti-patterns to avoid

**Adaptive Feedback:**
- Ask for user feedback on direction
- Offer multiple valid approaches
- Adjust based on user preferences
- Validate satisfaction, not output

**Example Structure:**
```
low-determinism-skill/
├── SKILL.md                    # Principles and guidance
└── references/
    └── examples.md            # Diverse example approaches
```

### Step 3: Implement Feedback Loops

Design homeostatic feedback mechanisms appropriate to determinism level:

**For High Determinism:**
- Automated validation at each step
- Fail-fast on validation errors
- Required checkpoints before proceeding
- Automated rollback on critical failures

**For Medium Determinism:**
- Explicit user confirmation at phase boundaries
- Validation with override capability
- Warning system for potential issues
- Manual recovery guidance

**For Low Determinism:**
- Periodic progress checks
- User satisfaction validation
- Flexible adaptation to feedback
- Optional validation only

### Step 4: Document Target States

Clearly define success criteria and target states:

**For Scripts and Automation:**
- Exact file structures, formats, schemas
- Required tool versions and configurations
- Expected output patterns
- Performance criteria (timeouts, resource limits)

**For Workflows:**
- Deliverables for each phase
- Quality criteria for artifacts
- Integration points and dependencies
- Completion criteria

**For Guidance Skills:**
- Principles to follow
- Anti-patterns to avoid
- Subjective quality indicators
- User satisfaction metrics

## Implementation Patterns

### Pattern 1: The Validation Checkpoint

Insert validation checkpoints at critical boundaries:

```markdown
## Phase 1: Initialize

[Instructions for phase 1]

**Validation Checkpoint:**
Before proceeding to Phase 2, verify:
- [ ] Input file exists and is readable
- [ ] Required tools are available (version >= X.Y)
- [ ] Output directory has write permissions
- [ ] No conflicting processes running

Run `scripts/validate-phase1.sh` to check all conditions.

If validation fails, see `references/troubleshooting.md` Section 1.
```

### Pattern 2: The Self-Correcting Loop

Implement error detection and correction:

```markdown
## Step 3: Process Data

Process the input file using the following approach:

1. Load and validate input schema
2. Transform data according to rules
3. **Validation:** Check output against schema
4. **If validation fails:**
   - Log specific validation errors
   - Attempt automatic correction (see `scripts/auto-correct.py`)
   - If auto-correction fails, provide manual fix guidance
   - Retry validation after fixes
5. Proceed only after validation passes
```

### Pattern 3: The Resilient Script

For skills that bundle scripts, add resiliency directly:

```python
#!/usr/bin/env python3
"""
Resilient data processor with built-in validation and error handling.
"""

def validate_input(data):
    """Pre-execution validation."""
    # Check schema, types, ranges, etc.
    if not meets_criteria(data):
        raise ValueError("Input validation failed: [specific error]")

def process_with_retry(data, max_retries=3):
    """Process with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            result = process(data)
            if validate_output(result):
                return result
            else:
                log_warning(f"Output validation failed on attempt {attempt + 1}")
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt
            log_info(f"Retry in {wait_time}s after error: {e}")
            time.sleep(wait_time)

def validate_output(result):
    """Post-execution validation."""
    # Verify result meets success criteria
    return meets_success_criteria(result)
```

### Pattern 4: The Homeostatic Summary

Maintain state awareness through summary files:

```markdown
## summary.md Template

---
status: in-progress  # or: completed, blocked, failed
phase: execution
determinism: high    # high, medium, low
last-validated: 2026-01-07T15:30:00Z
---

# Execution Summary

## Current State
Currently executing Phase 2 of 4. Last checkpoint passed at 15:25.

## Validations Passed
- ✅ Input validation (15:20)
- ✅ Phase 1 completion (15:25)
- ⏳ Phase 2 in progress

## Known Issues
None

## Next Checkpoint
Phase 2 validation at step 5

## Rollback Point
Can rollback to Phase 1 completion using `scripts/rollback.sh phase1`
```

## Resiliency Checklist by Determinism Level

### High Determinism Checklist

- [ ] Input validation with schema checking
- [ ] Precondition verification (files, tools, permissions)
- [ ] Step-by-step output validation
- [ ] Retry mechanisms for transient failures
- [ ] Timeout handling for external operations
- [ ] Post-execution verification
- [ ] Rollback procedures documented
- [ ] Error logging with full context
- [ ] Recovery scripts provided
- [ ] Test suite for validation logic

### Medium Determinism Checklist

- [ ] Phase boundaries with clear exit criteria
- [ ] Checkpoint validation
- [ ] Progress tracking in summary file
- [ ] Common error detection
- [ ] Troubleshooting guide
- [ ] Restart-from-checkpoint capability
- [ ] User confirmation at key transitions
- [ ] Warning system for potential issues

### Low Determinism Checklist

- [ ] Clear principles documented
- [ ] Anti-patterns identified
- [ ] Multiple example approaches
- [ ] Periodic progress checks
- [ ] User satisfaction validation
- [ ] Flexible adaptation to feedback

## Anti-Patterns to Avoid

### Over-Engineering Low Determinism Skills
**Wrong:** Adding extensive validation to creative or exploratory skills.
**Right:** Provide principles and guidance, allow flexibility.

### Under-Engineering High Determinism Skills
**Wrong:** Assuming scripts will work without validation.
**Right:** Validate inputs, outputs, and intermediate states comprehensively.

### Silent Failures
**Wrong:** Continuing execution after validation failures without alerting.
**Right:** Fail fast and provide clear error context.

### Validation Without Recovery
**Wrong:** Detecting errors but providing no path forward.
**Right:** Include recovery procedures or rollback instructions for all validation failures.

### False Homeostasis
**Wrong:** Checking that "something happened" without verifying it's correct.
**Right:** Validate against explicit success criteria, not just completion.

## Testing Resiliency

Validate your skill's resiliency by testing:

**Failure Modes:**
- Missing files or dependencies
- Invalid inputs
- Interrupted execution
- Tool failures or timeouts
- Partial completion scenarios

**Recovery Paths:**
- Rollback procedures work correctly
- Checkpoints enable restart
- Error messages are actionable
- Recovery scripts function as documented

**Validation Effectiveness:**
- False positives (flagging valid states as errors)
- False negatives (missing actual errors)
- Validation coverage (all critical states checked)

## Additional Resources

### Reference Files

For deeper understanding of resiliency concepts:
- **`references/levin-principles.md`** - Michael Levin's biological resiliency principles in detail
- **`references/determinism-assessment.md`** - Comprehensive guide to assessing skill determinism
- **`references/validation-patterns.md`** - Extensive validation pattern library

### Example Files

Working examples demonstrating resiliency levels:
- **`examples/high-determinism-deployment.md`** - Deployment skill with full resiliency
- **`examples/medium-determinism-workflow.md`** - Workflow skill with checkpoints
- **`examples/low-determinism-creative.md`** - Creative skill with minimal constraints

### Scripts

Utility scripts for implementing resiliency:
- **`scripts/generate-validation.py`** - Generate validation scripts from schemas
- **`scripts/test-resiliency.sh`** - Test skill under failure conditions

---

**Remember:** Resiliency is not about preventing all failures—it's about detecting deviations from target states and providing pathways to correction. Match resiliency mechanisms to determinism requirements: over-engineering adds friction, under-engineering invites failure.
