# Specificity Adjustment Factor (SAF) Methodology

## Overview

The Specificity Adjustment Factor (SAF) measures work item specification quality on a 0-1 scale. Well-specified work items receive full credit, while poorly-specified items receive reduced credit.

**Formula:**
```
SAF = (Clarity + Acceptance + Technical + Scope + Dependencies) / 5

Adjusted UUCW = Base UUCW × Category Multiplier × (0.7 + 0.3 × SAF)
```

**Key principle:** SAF ensures that vague requirements don't inflate UCP estimates.

---

## Five Dimensions of SAF

### 1. Clarity (Weight: 1/5)

**Question:** Is the work item description clear and unambiguous?

| Rating | Criteria | Example |
|--------|----------|---------|
| 0.0-0.2 | Vague, confusing | "Fix the system" |
| 0.3-0.4 | Somewhat clear, missing context | "Update authentication" |
| 0.5-0.6 | Clear purpose, some ambiguity | "Implement JWT authentication for API" |
| 0.7-0.8 | Very clear with context | "Implement JWT authentication for REST API endpoints with token refresh capability" |
| 0.9-1.0 | Crystal clear, no ambiguity | "Implement JWT authentication for REST API endpoints including access tokens (15min expiry), refresh tokens (7 day expiry), and token rotation on refresh" |

### 2. Acceptance Criteria (Weight: 1/5)

**Question:** Are there testable acceptance criteria defined?

| Rating | Criteria | Example |
|--------|----------|---------|
| 0.0-0.2 | No acceptance criteria | Just a title |
| 0.3-0.4 | Vague criteria | "Should work properly" |
| 0.5-0.6 | Some criteria, not testable | "Users can log in" |
| 0.7-0.8 | Testable criteria, some gaps | "1. User enters credentials 2. System validates 3. User is redirected" |
| 0.9-1.0 | Complete testable criteria | "1. User enters email/password 2. System validates against DB 3. System generates JWT access token (15min) and refresh token (7d) 4. System returns tokens in JSON response 5. System redirects to /dashboard 6. System logs login event with timestamp" |

### 3. Technical Detail (Weight: 1/5)

**Question:** Is sufficient technical detail provided for implementation?

| Rating | Criteria | Example |
|--------|----------|---------|
| 0.0-0.2 | No technical detail | "Build the feature" |
| 0.3-0.4 | Mentions technology | "Use JWT" |
| 0.5-0.6 | Some technical guidance | "Use JWT with RS256 algorithm" |
| 0.7-0.8 | Clear technical approach | "Use JWT with RS256, store tokens in httpOnly cookies, implement token refresh endpoint" |
| 0.9-1.0 | Implementation guide | "Use JWT (jsonwebtoken npm package) with RS256 algorithm, 2048-bit RSA keys stored in Azure Key Vault, access tokens 15min expiry, refresh tokens 7 day expiry with sliding window, store in httpOnly/secure cookies, implement /auth/refresh endpoint with token rotation" |

### 4. Scope Definition (Weight: 1/5)

**Question:** Is the scope well-bounded and clear?

| Rating | Criteria | Example |
|--------|----------|---------|
| 0.0-0.2 | Scope unclear | "Improve the system" |
| 0.3-0.4 | Broad scope, unbounded | "Implement authentication" |
| 0.5-0.6 | Scope identified, not bounded | "Implement JWT authentication for APIs" |
| 0.7-0.8 | Well-bounded scope | "Implement JWT authentication for 10 REST API endpoints listed in #123" |
| 0.9-1.0 | Precisely bounded | "Implement JWT authentication for exactly these endpoints: GET /api/users, POST /api/projects, PUT /api/projects/:id, DELETE /api/projects/:id. Out of scope: OAuth, SSO, MFA, password reset" |

### 5. Dependencies (Weight: 1/5)

**Question:** Are dependencies and prerequisites identified?

| Rating | Criteria | Example |
|--------|----------|---------|
| 0.0-0.2 | No dependencies mentioned | No context |
| 0.3-0.4 | Some awareness | "Requires database" |
| 0.5-0.6 | Key dependencies listed | "Depends on User model, database migration" |
| 0.7-0.8 | Dependencies and order clear | "Depends on: 1) User Story #234 (User model) completed 2) Azure Key Vault provisioned 3) Database migration #56 applied" |
| 0.9-1.0 | All dependencies mapped | "Prerequisites: US-234 (User model), US-235 (Redis session store). Blocking: US-240 (API rate limiting depends on this). External: Azure Key Vault access, HTTPS certificate. Technical: jsonwebtoken@9.0, express middleware compatibility" |

---

## SAF Impact on UUCW

### Formula Breakdown

```
Adjusted UUCW = Base UUCW × Category Multiplier × (0.7 + 0.3 × SAF)
```

**Components:**
- **Base UUCW:** Classification weight (Simple=5, Average=10, Complex=15)
- **Category Multiplier:** Work type (Stories=1.0x, Tasks=0.6x, Bugs=0.4x, Tests=0.3x)
- **SAF Adjustment:** 0.7 + (0.3 × SAF)

**Why 0.7 minimum?** Even poorly-specified work has some value; we give 70% credit minimum.

### Impact Table

| SAF Score | SAF Multiplier | Credit Given | Interpretation |
|-----------|----------------|--------------|----------------|
| 1.0 | 0.7 + (0.3 × 1.0) = 1.00x | 100% | Full credit - excellent specification |
| 0.9 | 0.7 + (0.3 × 0.9) = 0.97x | 97% | Near-perfect specification |
| 0.8 | 0.7 + (0.3 × 0.8) = 0.94x | 94% | Very good specification |
| 0.7 | 0.7 + (0.3 × 0.7) = 0.91x | 91% | Good specification (typical well-run project) |
| 0.6 | 0.7 + (0.3 × 0.6) = 0.88x | 88% | Adequate specification |
| 0.5 | 0.7 + (0.3 × 0.5) = 0.85x | 85% | Marginal specification |
| 0.4 | 0.7 + (0.3 × 0.4) = 0.82x | 82% | Poor specification |
| 0.3 | 0.7 + (0.3 × 0.3) = 0.79x | 79% | Very poor specification |
| 0.2 | 0.7 + (0.3 × 0.2) = 0.76x | 76% | Minimal specification |
| 0.1 | 0.7 + (0.3 × 0.1) = 0.73x | 73% | Nearly no specification |
| 0.0 | 0.7 + (0.3 × 0.0) = 0.70x | 70% | No specification (minimum credit) |

---

## Example SAF Assessments

### Example 1: High-Quality User Story (SAF = 0.90)

**Title:** User Story 575 - EventStreamer & FileWatcher Workspace-Scoping

**Description:**
> As a developer using the extension across multiple workspaces, I need workspace-scoped EventStreamer and FileWatcher services so that events and file changes are isolated per workspace and don't leak across workspace boundaries.

**Acceptance Criteria:**
1. Remove EventStreamer singleton pattern
2. Implement workspace-scoped EventStreamer with independent event queues
3. Remove FileWatcherService singleton pattern
4. Implement workspace-scoped FileWatcher with per-workspace file monitoring
5. Update event subscription model to include workspace context
6. Implement per-workspace file watching with isolated watchers
7. Update all event handlers to handle workspace-specific events
8. Handle workspace-specific events without cross-workspace contamination
9. Integration tests pass for multi-workspace scenarios

**Technical Detail:**
- Replace singleton with factory pattern using workspace ID as key
- Store instances in WeakMap keyed by workspace
- Update GlobalServices to provide workspace-aware instances
- VSCode FileSystemWatcher per workspace
- Event emitter with workspace prefix

**Dependencies:**
- Depends on User Story 566 (GlobalServices foundation)
- Blocks User Story 576 (ConfigManager workspace-scoping)

**SAF Breakdown:**
- **Clarity:** 0.9 (Crystal clear what needs to change)
- **Acceptance Criteria:** 1.0 (9 testable, specific criteria)
- **Technical Detail:** 0.9 (Clear approach with specific patterns)
- **Scope Definition:** 0.9 (Precisely what's in scope)
- **Dependencies:** 0.8 (Prerequisites and blocking items identified)

**SAF = (0.9 + 1.0 + 0.9 + 0.9 + 0.8) / 5 = 0.90**

**Impact:**
```
Base UUCW: 15 (Complex, 9 transactions)
Category Multiplier: 1.0 (User Story)
SAF Adjustment: 0.7 + (0.3 × 0.90) = 0.97

Final UUCW = 15 × 1.0 × 0.97 = 14.6 UUCW
```

---

### Example 2: Medium-Quality Feature (SAF = 0.68)

**Title:** Feature 5.4 - Supporting Services Workspace-Scoping

**Description:**
> Update supporting services (EventStreamer, FileWatcher, ConfigManager, ActivityMonitor) to be workspace-scoped rather than singletons, enabling proper multi-workspace support.

**Key Deliverables:**
- EventStreamer workspace-scoped buffering
- FileWatcher per-workspace monitoring
- ConfigManager workspace configuration
- ActivityMonitor per-workspace tracking

**Dependencies:**
- Depends on Feature 5.1 (GlobalServices foundation)

**SAF Breakdown:**
- **Clarity:** 0.7 (Clear what services, but how they interact unclear)
- **Acceptance Criteria:** 0.5 (Key deliverables listed, not testable criteria)
- **Technical Detail:** 0.6 (Mentions workspace-scoping, lacks implementation detail)
- **Scope Definition:** 0.8 (4 services clearly identified)
- **Dependencies:** 0.8 (Prerequisite identified)

**SAF = (0.7 + 0.5 + 0.6 + 0.8 + 0.8) / 5 = 0.68**

**Impact:**
```
Base UUCW: 15 (Complex, estimated 8 transactions)
Category Multiplier: 1.0 (Feature treated as story)
SAF Adjustment: 0.7 + (0.3 × 0.68) = 0.90

Final UUCW = 15 × 1.0 × 0.90 = 13.5 UUCW
```

**Note:** Feature-level specification is less detailed than User Story, so SAF is lower.

---

### Example 3: Poor-Quality Epic (SAF = 0.30)

**Title:** Epic 455 - Enterprise Policy Enforcement System

**Description:**
> Implement a comprehensive enterprise policy enforcement system that fetches policies from AI-SOC service, evaluates user activities against policy rules, enforces policy violations, and maintains complete audit trails for compliance requirements.

**SAF Breakdown:**
- **Clarity:** 0.4 (High-level, what "comprehensive" means unclear)
- **Acceptance Criteria:** 0.0 (None provided)
- **Technical Detail:** 0.2 (Mentions AI-SOC service, no implementation detail)
- **Scope Definition:** 0.3 (Broad, unbounded - "comprehensive")
- **Dependencies:** 0.6 (Mentions AI-SOC service dependency)

**SAF = (0.4 + 0.0 + 0.2 + 0.3 + 0.6) / 5 = 0.30**

**Impact:**
```
Base UUCW: 15 (Assumed Complex)
Category Multiplier: 1.0 (If counted as use case)
SAF Adjustment: 0.7 + (0.3 × 0.30) = 0.79

Final UUCW = 15 × 1.0 × 0.79 = 11.9 UUCW
```

**Problem:** Epic should not be counted as use case at all! SAF doesn't fix wrong granularity.

---

## SAF Quality Distribution Analysis

### Typical Project SAF Distribution

| SAF Range | Quality Level | Percentage (Typical Project) |
|-----------|---------------|------------------------------|
| 0.9-1.0 | Excellent | 10-20% |
| 0.8-0.9 | Very Good | 20-30% |
| 0.7-0.8 | Good | 30-40% |
| 0.6-0.7 | Adequate | 20-30% |
| 0.5-0.6 | Marginal | 5-10% |
| <0.5 | Poor | 0-5% |

**Average SAF for well-run project:** 0.70-0.75

### Agent Studio Pro Example (142 work items)

| SAF Range | Count | Percentage |
|-----------|-------|------------|
| High Quality (≥0.8) | 42 | 29.6% |
| Good Quality (0.6-0.8) | 63 | 44.4% |
| Moderate Quality (<0.6) | 37 | 26.0% |
| **Average SAF** | **0.68** | *Good quality overall* |

---

## Best Practices for Improving SAF

### For User Stories

1. **Use "As a [actor], I want [action], so that [benefit]" format**
   - Forces clarity about who, what, why

2. **Write 4-7 numbered acceptance criteria**
   - Each should be testable
   - Include positive and negative cases
   - Specify expected outcomes

3. **Include technical implementation notes**
   - Key technologies/libraries
   - Integration points
   - Performance considerations

4. **Define explicit scope boundaries**
   - What's in scope
   - What's explicitly out of scope
   - Edge cases to handle

5. **Map dependencies in both directions**
   - Prerequisites (this needs)
   - Blocking (this blocks)
   - External systems

### For Features

Features typically have lower SAF than User Stories. To improve:

1. **Break down into "Key Deliverables"**
   - Bulleted list of 3-5 concrete deliverables
   - Each deliverable should be specific

2. **Link to User Stories**
   - Feature should reference 2-4 child User Stories
   - User Stories provide the detailed acceptance criteria

3. **Provide architectural context**
   - How does this fit in the system?
   - What components are affected?

### Red Flags (Low SAF Indicators)

❌ **Vague verbs:** "improve," "enhance," "optimize," "update"
❌ **No acceptance criteria**
❌ **No technical detail**
❌ **Unbounded scope:** "comprehensive," "robust," "flexible"
❌ **No dependencies listed**

✅ **Good indicators:** Numbered criteria, specific verbs, clear boundaries, dependencies mapped

---

## SAF in Context of v4.0 Complete Work Coverage

### SAF Applies to All 4 Categories

| Category | Base Multiplier | SAF Application | Result |
|----------|----------------|-----------------|--------|
| Stories (1.0x) | High quality work items | Full SAF impact | 0.70-1.00 adjustment |
| Tasks (0.6x) | Often lower SAF | SAF reduces credit | 0.42-0.60 effective multiplier |
| Bugs (0.4x) | Variable SAF | SAF adjusts credit | 0.28-0.40 effective multiplier |
| Tests (0.3x) | Moderate SAF | SAF adjusts credit | 0.21-0.30 effective multiplier |

**Example: Bug with high urgency but poor specification**
```
Base UUCW: 10 (Average)
Category Multiplier: 0.4 (Bug)
Urgency Multiplier: 1.5 (Critical)
SAF: 0.5 (Poor bug report)

SAF Adjustment: 0.7 + (0.3 × 0.5) = 0.85

Final UUCW = 10 × 0.4 × 1.5 × 0.85 = 5.1 UUCW
```

Without SAF, this would have been 6.0 UUCW. SAF reduces credit by 15% for poor specification.

---

## Summary

**SAF Purpose:** Reward high-quality specifications, reduce credit for vague requirements

**SAF Formula:** Average of 5 dimensions (Clarity, Acceptance, Technical, Scope, Dependencies)

**SAF Impact:** Adjusts final UUCW by 0.70x to 1.00x multiplier

**Typical SAF:** 0.65-0.75 for well-run projects

**Best Practice:** Write detailed User Stories with numbered acceptance criteria for SAF ≥ 0.85
