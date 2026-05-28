# Spec-to-PRP Transformation Prompt (Chain of Thought)

You are transforming a software specification into a Product Requirements Prompt (PRP).

## What is a PRP?

A PRP is an agent-executable blueprint that transforms human intent into structured, verifiable implementation plans. It must be:
- **Unambiguous**: No vague terms like "properly", "quickly", "as needed"
- **Measurable**: All success criteria have numbers and thresholds
- **Verifiable**: Each phase has concrete pass/fail gates
- **Executable**: Validation commands can be copy-pasted and run

## Transformation Process (Think Step by Step)

### Step 1: Extract Problem Statement
- Find the "why" from the spec's overview or background section
- Quantify the pain if possible (e.g., "47% abandonment rate", "3.2% failure rate")
- Keep it to 1-2 sentences focused on the problem, not the solution

### Step 2: Define Solution Summary
- One paragraph describing WHAT we're building (not HOW)
- Focus on outcomes and capabilities
- Avoid implementation details

### Step 3: Map Success Criteria
Transform acceptance criteria into measurable metrics:
- "Fast loading" → "Page load time p95 < 2 seconds"
- "Easy to use" → "Task completion rate > 90%"
- "Reliable" → "Error rate < 0.1%"

Each metric needs:
| Metric | Current | Target | Measurement Method |

### Step 4: Structure Phases with Gates
Convert milestones/tasks into phases:
- Each phase has clear deliverables (checkboxes)
- Each phase ends with a validation gate
- Gates have explicit pass/fail conditions
- Include "If gate fails" action

### Step 5: Identify Risks and Mitigations
Look for:
- External dependencies (APIs, services)
- Technical unknowns
- Security/compliance requirements
- Resource constraints

Each risk needs: Probability, Impact, Mitigation, Owner

### Step 6: Generate Validation Commands
Based on the tech stack, create executable commands:
- Test commands (npm test, pytest, etc.)
- Type checking (tsc, mypy)
- Linting (eslint, ruff)
- Build verification
- Health checks

## Example Transformation

### Input Spec:
```markdown
# User Profile Feature

## Overview
Users need to update their profile information. Currently they must contact support.

## Requirements
- Users can edit name, email, avatar
- Changes require email verification
- Profile updates sync to mobile app

## Acceptance Criteria
- Profile page loads quickly
- Users can update all fields
- Changes persist after refresh
```

### Output PRP Sections:

**Problem Statement:**
Users cannot self-service profile updates, requiring support tickets that take 2-3 days to resolve. This creates friction and increases support load by ~50 tickets/week.

**Solution Summary:**
Build a self-service profile management interface allowing users to update their name, email, and avatar with email verification for sensitive changes.

**Success Criteria:**
| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Profile update time | 2-3 days (support) | < 30 seconds | User analytics |
| Support tickets for profile | 50/week | < 5/week | Zendesk metrics |
| Profile page load (p95) | N/A | < 1.5s | Datadog APM |

**Phase 1: Core Profile UI**
Duration: 1 week
Deliverables:
- [ ] Profile page with edit form
- [ ] Avatar upload component
- [ ] Form validation

Gate 1:
| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| Tests pass | 100% green | CI pipeline |
| Coverage | > 80% | Jest report |

```
GATE_1_PASS := tests_passing AND coverage > 0.8
```

**Validation Commands:**
```bash
# Unit tests
npm test -- --coverage --testPathPattern="profile"

# Type check
npx tsc --noEmit

# Lint
npx eslint src/profile/
```

## Your Task

Transform the following specification into a complete PRP.

**Metadata:**
```json
{{METADATA}}
```

**Specification:**
```markdown
{{SPEC_CONTENT}}
```

**PRP Template Structure:**
{{TEMPLATE_STRUCTURE}}

**Output a complete, filled-in PRP with:**
1. All sections from the template
2. No [FILL_THIS_IN] placeholders - use actual content from the spec
3. Measurable success criteria with numbers
4. Concrete validation gates with pass/fail conditions
5. Executable validation commands for the tech stack
6. Realistic phases based on the requirements

If information is missing from the spec, make reasonable assumptions and note them.
