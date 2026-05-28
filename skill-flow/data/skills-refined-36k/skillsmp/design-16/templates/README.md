# PRP Template System

> Transform validated specs into agent-executable blueprints.

---

## What is a PRP?

**PRP** = Product Requirements Prompt

A PRP is the "compiled output" of a validated spec. Just as a compiler transforms source code into executable machine code, the PRP system transforms human intent (specs) into agent-executable blueprints (PRPs).

```
┌─────────────────────────────────────────────────────────────────────┐
│                        THE COMPILATION PIPELINE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐     ┌───────────┐     ┌──────────────┐     ┌───────┐ │
│  │  Human   │────▶│   Spec    │────▶│  Validator   │────▶│  PRP  │ │
│  │  Intent  │     │ (Source)  │     │ (Type Check) │     │(Binary)│ │
│  └──────────┘     └───────────┘     └──────────────┘     └───────┘ │
│                                                                      │
│       "I want X"    Structured      Invariant         Executable    │
│                     Requirements    Enforcement       Blueprint     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
templates/
├── README.md              # This file
├── prp-base.md            # Master template with all sections
├── execution-probe.md     # Post-execution validation template
├── section-library.md     # Reusable sections for common scenarios
└── prp-examples/
    ├── example-api-integration.md   # Technical integration project
    ├── example-user-feature.md      # Consumer-facing feature
    └── example-data-migration.md    # Data infrastructure project
```

---

## How Specs Map to PRPs

### The Transformation Process

| Spec Element | Invariant Check | PRP Section |
|--------------|-----------------|-------------|
| Problem statement | #1: No ambiguity | 1.1 Problem Statement |
| User journeys | #2: State explicit | 8. State Transitions |
| Emotional goals | #3: Must compile to action | 3. Emotion Mapping |
| Data operations | #4: Recovery required | 4.2 Fallback Strategies |
| Error handling | #5: Fail loudly | 4.3 Circuit Breakers |
| Scope definition | #6: Must be bounded | 1.3 Scope Boundaries |
| Acceptance criteria | #7: Must be executable | 2. Success Criteria |
| External calls | #8: Cost bounded | 5.4 Budget |
| System changes | #9: Blast radius declared | 5.3 External Dependencies |
| Dependencies | #10: Degradation path | 4.2 Fallback Strategies |

### Compilation Examples

**Spec Input:**
```markdown
Users should feel confident when completing checkout
```

**Validator Check:**
```
❌ VIOLATION: Invariant #3 (Emotional Intent Must Compile)
   "feel confident" has no := mapping
```

**Fixed Spec:**
```markdown
Users should feel confident when completing checkout :=
  - Progress indicator shows steps completed
  - Order summary visible throughout
  - Security badges displayed at payment
  - Confirmation page loads <2s
```

**PRP Output:**
```markdown
| Intended Emotion | Triggering Affordance | Verification |
|-----------------|----------------------|--------------|
| Confident (checkout) | Progress indicator, summary, security badges | User testing: 80% report "I knew what was happening" |
```

---

## Using Templates

### Step 1: Validate Your Spec

```bash
# Run validator on your spec
./validator.sh path/to/your-spec.md --domain domains/relevant-domain.md

# Must pass with no blocking violations
# Warnings acceptable if reviewed
```

### Step 2: Choose Your Template Approach

**Option A: Start from prp-base.md**
- Best for: Standard projects
- Copy the template, fill in variables
- Remove sections that don't apply

**Option B: Start from an example**
- Best for: Similar project types
- Copy the closest example
- Modify to match your spec

**Option C: Build from section-library.md**
- Best for: Unique or hybrid projects
- Pick relevant sections
- Combine into custom PRP

### Step 3: Fill in Variables

All variables use the format `{{VARIABLE_NAME}}`. Replace every variable before execution.

```markdown
<!-- Before -->
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| {{METRIC_1}} | {{CURRENT_1}} | {{TARGET_1}} | {{METHOD_1}} |

<!-- After -->
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| Checkout completion rate | 78% | >88% | Analytics funnel |
```

### Step 4: Add Domain-Specific Sections

Based on your domain, add relevant sections from section-library.md:

| Domain | Recommended Sections |
|--------|---------------------|
| consumer | User Testing Protocol, A/B Test Configuration |
| integration | Circuit Breakers, Rate Limiting |
| data-architecture | Data Validation Gates, Replication Monitoring |
| construction | (use physical world checklists, not in library) |
| remote-management | Runbook Template |
| skill-gap | Learning checkpoints (not in library, add inline) |

### Step 5: Verify PRP Completeness

Before execution, verify:

- [ ] All `{{VARIABLE}}` placeholders replaced
- [ ] Meta section has valid prp_id and source_spec
- [ ] Success criteria are measurable
- [ ] All validation gates have pass/fail conditions
- [ ] Rollback/fallback procedures documented
- [ ] Pre-execution checklist completed

---

## Variable Reference

### Required Variables (All PRPs)

| Variable | Format | Description |
|----------|--------|-------------|
| `PRP_ID` | `PRP-YYYY-MM-DD-XXX` | Unique identifier |
| `SOURCE_SPEC_PATH` | File path | Path to validated spec |
| `VALIDATION_STATUS` | `PASSED` or `PASSED_WITH_WARNINGS` | Validator result |
| `VALIDATION_DATE` | `YYYY-MM-DD` | When spec was validated |
| `DOMAIN` | Domain name | Which invariant domain applies |

### Common Variables

| Variable | Type | Example |
|----------|------|---------|
| `METRIC_*` | String with numbers | `Error rate: 3.2%` |
| `GATE_*_CRITERION_*` | Condition description | `All tests passing` |
| `GATE_*_PASS_*` | Measurable threshold | `Coverage > 90%` |
| `RISK_*` | Risk description | `API rate limiting` |
| `PHASE_*_NAME` | Phase title | `Integration Development` |
| `PHASE_*_DURATION` | Time period | `2 weeks` |

### Variable Naming Convention

```
{{CATEGORY_SPECIFICS}}

Examples:
  {{METRIC_PRIMARY}}
  {{METRIC_SECONDARY}}
  {{GATE_1_CRITERION_1}}
  {{GATE_1_CRITERION_2}}
  {{RISK_HIGH_1}}
  {{PHASE_1_DELIVERABLE_1}}
```

---

## Workflow Integration

### Full Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DESIGN OPS PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. RESEARCH          2. JOURNEYS         3. SPEC              4. VALIDATE │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐        ┌──────────┐  │
│  │ Problem  │───────▶│  User    │───────▶│ Detailed │───────▶│ Validator│  │
│  │ Discovery│        │ Journeys │        │ Spec     │        │ Check    │  │
│  └──────────┘        └──────────┘        └──────────┘        └──────────┘  │
│                                                                    │        │
│                                                                    ▼        │
│  8. FEEDBACK          7. EXECUTE         6. READY             5. COMPILE   │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐        ┌──────────┐  │
│  │ Spec     │◀───────│ Agent    │◀───────│ Pre-Exec │◀───────│ Generate │  │
│  │ Delta    │        │ Execution│        │ Checklist│        │ PRP      │  │
│  └──────────┘        └──────────┘        └──────────┘        └──────────┘  │
│       │                                                                     │
│       │  Learnings feed back to improve specs + invariants                 │
│       └─────────────────────────────────────────────────────────────────────│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Integration Points

| Stage | Input | Output | Tool |
|-------|-------|--------|------|
| Validate | Spec | Pass/Fail | `validator.sh` |
| Compile | Validated Spec | PRP | Templates (manual) |
| Execute | PRP | Results | Agent/Team |
| Feedback | Results vs PRP | Spec Delta | `spec-delta/template.md` |

---

## Examples Overview

### example-api-integration.md

**Project Type**: Technical integration (Stripe payment gateway)

**Key Patterns Demonstrated**:
- Circuit breaker configuration
- Staged percentage rollout
- Parallel fallback system
- Cost boundary tracking

**Best For**: Payment integrations, third-party APIs, service migrations

---

### example-user-feature.md

**Project Type**: Consumer feature (Dark mode)

**Key Patterns Demonstrated**:
- User emotion → affordance mapping
- Friction quantification
- Design validation gates
- A/B test decision framework

**Best For**: UI features, UX improvements, consumer-facing changes

---

### example-data-migration.md

**Project Type**: Infrastructure (PostgreSQL → Aurora)

**Key Patterns Demonstrated**:
- Data validation queries
- Replication state machine
- Multi-phase cutover
- 90-day parallel run with rollback

**Best For**: Database migrations, data platform changes, infrastructure moves

---

## Section Library Usage

### When to Use Section Library

| Situation | Approach |
|-----------|----------|
| Standard project type | Start with matching example |
| Unique project | Build from prp-base.md + sections |
| Missing functionality | Add sections from library |
| Repeated patterns | Extract to library |

### Adding New Sections

When you create a pattern that could be reused:

1. Extract the section to section-library.md
2. Generalize with variables
3. Add "When to use", "Customization", "Gotchas"
4. Reference in this README

---

## Best Practices

### Do

- ✅ Validate spec BEFORE creating PRP
- ✅ Use measurable success criteria
- ✅ Define explicit state transitions
- ✅ Include rollback for every change
- ✅ Set circuit breakers for external dependencies
- ✅ Fill out pre-execution checklist

### Don't

- ❌ Skip validation and go straight to PRP
- ❌ Use ambiguous metrics ("improve performance")
- ❌ Leave gates without pass/fail criteria
- ❌ Assume happy path only
- ❌ Forget to document fallbacks
- ❌ Start execution without checklist complete

---

## Troubleshooting

### "Too many variables to fill"

Start with an example that matches your project. Fewer variables to customize.

### "Validation gate criteria unclear"

Ask: "How would I KNOW if this passed?" If you can't answer, the criterion isn't specific enough.

### "State transitions seem overkill"

For simple projects, collapse into fewer states. But keep at least:
- NOT_STARTED → IN_PROGRESS → COMPLETE
- Any state → BLOCKED (for issues)
- BLOCKED → previous state (for recovery)

### "Which domain should I use?"

| Project involves... | Domain |
|--------------------|--------|
| End users directly | consumer |
| Physical materials/construction | construction |
| Database/data pipeline | data-architecture |
| API/service connections | integration |
| Remote team/contractor | remote-management |
| Learning new technology | skill-gap |
| None of the above | universal only |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-20 | Initial release |

---

*PRPs are the executable form of validated human intent.*
