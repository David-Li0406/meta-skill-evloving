# Determinism Assessment Guide

## Overview

This guide provides a comprehensive framework for assessing the determinism level of Agent Skills, which determines the appropriate resiliency mechanisms to implement.

## What is Skill Determinism?

**Determinism** in Agent Skills refers to how precisely defined and reproducible the skill's outcomes must be:

- **High Determinism:** Exact, reproducible results required (e.g., deployment scripts, data validation)
- **Medium Determinism:** Structured outcomes with some flexibility (e.g., workflow orchestration, document generation)
- **Low Determinism:** Flexible, creative outcomes (e.g., brainstorming, exploration, content ideation)

## The Four Dimensions of Determinism

### Dimension 1: Output Precision

**Question:** How exact must the output be?

**Scale:**
- **0-2 (Creative):** Multiple valid outputs, subjective quality assessment
  - Example: Generate marketing copy, brainstorm features
- **3-4 (Flexible):** General structure required, details vary
  - Example: Create documentation outline, design system architecture
- **5-6 (Structured):** Specific format required, content may vary
  - Example: Generate config files, create test cases
- **7-8 (Precise):** Exact format and most content specified
  - Example: Database migrations, API contracts
- **9-10 (Bit-Perfect):** Must match exact specification
  - Example: Cryptographic operations, binary protocol implementations

**Assessment Questions:**
- Can two different outputs both be considered "correct"?
- Is there a schema or specification the output must match exactly?
- Could a human judge whether output is "good enough" without precise criteria?
- Would output differences break downstream systems?

### Dimension 2: Process Rigidity

**Question:** How flexible is the execution path?

**Scale:**
- **0-2 (Many Paths):** Numerous valid approaches to achieve goal
  - Example: Problem exploration, research, creative design
- **3-4 (Guided Flexibility):** Several valid approaches within constraints
  - Example: Implement feature (multiple design patterns work)
- **5-6 (Structured Choice):** Limited valid approaches, clear checkpoints
  - Example: Database setup (few valid topologies)
- **7-8 (Mostly Fixed):** Specific sequence required with minor variations
  - Example: Build pipeline, installation procedure
- **9-10 (Exact Sequence):** Must follow precise steps in order
  - Example: Cryptographic key generation, database initialization

**Assessment Questions:**
- Can steps be reordered without breaking functionality?
- Are there multiple tools/approaches that could work?
- Must specific commands be executed in exact order?
- Would skipping a step cause failure or just suboptimal results?

### Dimension 3: Failure Consequence

**Question:** What happens if this skill fails or produces incorrect output?

**Scale:**
- **0-2 (Trivial):** Minor inconvenience, easily regenerated
  - Example: Draft email, format document
- **3-4 (Low Impact):** Time wasted, but no lasting damage
  - Example: Failed test run, documentation error
- **5-6 (Moderate Impact):** Requires cleanup, some downstream effects
  - Example: Database query error, incorrect analysis
- **7-8 (High Impact):** Significant cleanup, affects other systems
  - Example: Broken deployment, data corruption
- **9-10 (Critical):** Catastrophic consequences, data loss, security breach
  - Example: Production database wipe, credential exposure

**Assessment Questions:**
- Can failure be recovered from easily?
- Does failure affect other systems or users?
- Is there risk of data loss or corruption?
- Could failure create security vulnerabilities?
- What's the cost (time, money, reputation) of failure?

### Dimension 4: Recovery Difficulty

**Question:** How hard is it to recover from errors or incorrect execution?

**Scale:**
- **0-2 (Trivial Recovery):** Just run again
  - Example: Regenerate content, re-run analysis
- **3-4 (Easy Recovery):** Clear fix, well-understood recovery
  - Example: Correct config error, restart service
- **5-6 (Moderate Recovery):** Requires manual intervention, documented procedures
  - Example: Restore from backup, manual data correction
- **7-8 (Difficult Recovery):** Complex manual recovery, multiple steps
  - Example: Database rollback with referential integrity, distributed system recovery
- **9-10 (Nearly Impossible):** Cannot fully recover, permanent consequences
  - Example: Leaked credentials (must rotate), published incorrect data

**Assessment Questions:**
- Is there an "undo" mechanism?
- Can the system be restored to pre-execution state?
- How much manual work is needed to recover?
- Is data permanently lost or changed?
- Could recovery itself introduce new errors?

## Scoring Framework

### Calculate Total Determinism Score

1. Score each dimension (0-10)
2. Sum scores (Total: 0-40)
3. Calculate weighted score if needed

**Standard Weighting (Equal):**
```
Total Score = Output Precision + Process Rigidity + Failure Consequence + Recovery Difficulty
Range: 0-40
```

**Alternative Weighting (Consequence-Heavy):**
```
Total Score = Output Precision + Process Rigidity + (2 × Failure Consequence) + Recovery Difficulty
Range: 0-50
```

### Interpret Score

**Total Score: 0-10 (Low Determinism)**
- Flexible, creative tasks
- Multiple valid outcomes
- Low consequences
- Easy recovery
- **Resiliency:** Minimal

**Total Score: 11-20 (Medium-Low Determinism)**
- Somewhat structured tasks
- Preferred outcomes but flexibility accepted
- Moderate consequences
- Recoverable errors
- **Resiliency:** Light

**Total Score: 21-30 (Medium-High Determinism)**
- Structured tasks with clear requirements
- Specific outcomes required
- Significant consequences
- Recovery requires effort
- **Resiliency:** Moderate

**Total Score: 31-40 (High Determinism)**
- Precise, critical tasks
- Exact outcomes required
- Critical consequences
- Difficult recovery
- **Resiliency:** Maximum

## Assessment Examples

### Example 1: Content Generation Skill

**Task:** Generate blog post from outline

**Dimension Scores:**
- **Output Precision:** 2 (creative, multiple valid outputs)
- **Process Rigidity:** 1 (many approaches work)
- **Failure Consequence:** 1 (just regenerate)
- **Recovery Difficulty:** 1 (trivial - try again)

**Total Score:** 5 / 40
**Classification:** Low Determinism
**Resiliency Required:** Minimal (basic quality guidelines)

### Example 2: Database Migration Skill

**Task:** Apply schema migrations to production database

**Dimension Scores:**
- **Output Precision:** 9 (exact schema required)
- **Process Rigidity:** 8 (specific sequence of migrations)
- **Failure Consequence:** 9 (data corruption, downtime)
- **Recovery Difficulty:** 8 (complex rollback procedures)

**Total Score:** 34 / 40
**Classification:** High Determinism
**Resiliency Required:** Maximum (comprehensive validation, rollback, monitoring)

### Example 3: Test Generation Skill

**Task:** Generate unit tests for existing code

**Dimension Scores:**
- **Output Precision:** 5 (must be valid code, coverage varies)
- **Process Rigidity:** 3 (multiple testing approaches valid)
- **Failure Consequence:** 3 (poor tests, but no system damage)
- **Recovery Difficulty:** 2 (easy to regenerate or fix)

**Total Score:** 13 / 40
**Classification:** Medium-Low Determinism
**Resiliency Required:** Light (basic validation, syntax checking)

### Example 4: CI/CD Pipeline Orchestration Skill

**Task:** Orchestrate build, test, and deployment pipeline

**Dimension Scores:**
- **Output Precision:** 7 (specific deployment artifacts required)
- **Process Rigidity:** 7 (defined stages, specific order)
- **Failure Consequence:** 7 (broken deployments, potential downtime)
- **Recovery Difficulty:** 6 (rollback mechanisms exist but complex)

**Total Score:** 27 / 40
**Classification:** Medium-High Determinism
**Resiliency Required:** Moderate (validation checkpoints, health checks, rollback procedures)

### Example 5: Research and Analysis Skill

**Task:** Research competitive landscape and produce analysis

**Dimension Scores:**
- **Output Precision:** 3 (structured findings, subjective analysis)
- **Process Rigidity:** 2 (flexible research approaches)
- **Failure Consequence:** 2 (time wasted, but easily redone)
- **Recovery Difficulty:** 1 (just conduct more research)

**Total Score:** 8 / 40
**Classification:** Low Determinism
**Resiliency Required:** Minimal (research guidelines, citation requirements)

## Decision Tree for Quick Assessment

```
START: Assess this skill

↓
Does failure risk data loss, security breach, or system damage?
├─ YES → High Consequence (7-10 points)
│   ↓
│   Must output match exact specification?
│   ├─ YES → HIGH DETERMINISM (Score: 30+)
│   │   → Implement maximum resiliency
│   └─ NO → Check process rigidity
│       ↓
│       Is execution path strictly defined?
│       ├─ YES → MEDIUM-HIGH DETERMINISM (Score: 21-29)
│       │   → Implement moderate resiliency
│       └─ NO → MEDIUM DETERMINISM (Score: 15-20)
│           → Implement light resiliency
│
└─ NO → Low Consequence (0-6 points)
    ↓
    Must output match specific format/schema?
    ├─ YES → MEDIUM-LOW DETERMINISM (Score: 11-20)
    │   → Implement light resiliency
    └─ NO → LOW DETERMINISM (Score: 0-10)
        → Minimal resiliency (guidelines only)
```

## Resiliency Recommendations by Score

### Score 0-10: Minimal Resiliency

**Implement:**
- Basic usage guidelines
- Anti-pattern documentation
- Example outputs

**Skip:**
- Formal validation
- Checkpoints
- Recovery procedures
- Automated testing

**Example Skills:**
- Brainstorming
- Content ideation
- Exploratory research
- Creative writing

### Score 11-20: Light Resiliency

**Implement:**
- Basic output validation (syntax, format)
- Common error detection
- Simple troubleshooting guide
- Progress indicators

**Skip:**
- Comprehensive validation
- Automated recovery
- Rollback procedures
- Pre-flight checks

**Example Skills:**
- Documentation generation
- Code commenting
- Test case creation
- Log analysis

### Score 21-30: Moderate Resiliency

**Implement:**
- Checkpoint validation
- Phase-level error detection
- Recovery procedures documented
- Pre-execution validation
- Progress tracking
- Rollback guidance

**Optional:**
- Automated recovery scripts
- Health checks
- Integration testing

**Example Skills:**
- CI/CD orchestration
- Multi-step workflows
- Configuration management
- Data processing pipelines

### Score 31-40: Maximum Resiliency

**Implement:**
- Comprehensive pre-flight validation
- Step-by-step verification
- Automated recovery scripts
- Rollback procedures (tested)
- Health monitoring
- Audit logging
- Integration and end-to-end tests
- Backup mechanisms
- Timeout handling
- Retry logic with backoff

**Required:**
- All validation automated
- All recovery procedures tested
- Complete audit trail
- User confirmation for critical actions

**Example Skills:**
- Production deployments
- Database migrations
- Security operations
- Financial transactions
- Data deletion operations

## Special Considerations

### Skill Type Modifiers

Some skill types inherently require adjusted determinism scoring:

**Security-Related Skills (+5 to Consequence)**
- Credential management
- Access control
- Encryption operations
- Security policy enforcement

**Data Operations (+3 to Consequence)**
- Database modifications
- Data deletion
- Data transformation
- Data migration

**Production Operations (+5 to Consequence)**
- Deployment
- Configuration changes
- Service restarts
- Traffic routing

**Reversible Operations (-3 to Recovery Difficulty)**
- Version-controlled changes
- Containerized deployments
- Snapshot-backed modifications
- Transaction-based operations

### Context-Dependent Determinism

Some skills have determinism that varies by context:

**Code Refactoring Skill:**
- In development branch: Low determinism (experimentation ok)
- In main branch: High determinism (must not break functionality)

**Data Analysis Skill:**
- Exploratory analysis: Low determinism (insights vary)
- Regulatory reporting: High determinism (exact format required)

**Configuration Update Skill:**
- Development environment: Medium determinism (failures acceptable)
- Production environment: High determinism (failures critical)

**Solution:** Create skill variants or include context-aware branching:

```markdown
## Context Assessment

Before proceeding, assess execution context:

**Development Context:**
- Use exploratory approach
- Minimal validation
- Experimentation encouraged

**Production Context:**
- Use validated approach
- Comprehensive checks
- All changes reviewed
- Rollback procedures prepared
```

## Reassessment Triggers

Reassess skill determinism when:

1. **Skill usage expands to new contexts**
   - Originally dev-only, now used in production
   - New data types with different criticality

2. **Failures occur in practice**
   - Consequences were underestimated
   - Recovery was harder than expected

3. **Downstream dependencies change**
   - Other systems now depend on exact output format
   - Integration points become more critical

4. **Compliance requirements added**
   - Regulatory oversight imposed
   - Audit trails required
   - Exact reproducibility mandated

5. **User expertise changes**
   - Originally expert users, now novices
   - Self-service adoption increases error risk

## Assessment Worksheet

Use this worksheet for formal assessment:

```markdown
# Skill Determinism Assessment

**Skill Name:** _________________
**Date:** _________________
**Assessor:** _________________

## Dimension Scores

### Output Precision (0-10): ____
Notes:


### Process Rigidity (0-10): ____
Notes:


### Failure Consequence (0-10): ____
Notes:


### Recovery Difficulty (0-10): ____
Notes:


## Context Modifiers

Security-related? (Y/N): ____ (+5 to consequence if Y)
Data operations? (Y/N): ____ (+3 to consequence if Y)
Production operations? (Y/N): ____ (+5 to consequence if Y)
Reversible operations? (Y/N): ____ (-3 to recovery if Y)

## Total Score

Base Score: ____
Modified Score: ____

## Classification

- [ ] Low Determinism (0-10) → Minimal Resiliency
- [ ] Medium-Low Determinism (11-20) → Light Resiliency
- [ ] Medium-High Determinism (21-30) → Moderate Resiliency
- [ ] High Determinism (31-40+) → Maximum Resiliency

## Recommended Resiliency Mechanisms

Based on classification:
-
-
-

## Next Steps

1.
2.
3.
```

## Common Assessment Mistakes

### Mistake 1: Underestimating Consequences

**Symptom:** "It's just a script, failures are no big deal"

**Reality Check:**
- What data does it touch?
- What systems depend on its output?
- What happens if it fails at 3am?

**Fix:** Map downstream dependencies, assess actual impact

### Mistake 2: Confusing Complexity with Determinism

**Symptom:** "This is complex code, so it needs high determinism"

**Reality Check:**
- Complex code can have flexible outputs
- Simple code can require exact outputs
- Complexity ≠ Determinism

**Fix:** Assess output requirements, not code complexity

### Mistake 3: Ignoring Recovery Difficulty

**Symptom:** "We have backups, so recovery is easy"

**Reality Check:**
- How long does backup restoration take?
- What data is lost between backup and failure?
- Who knows how to restore?
- Have restore procedures been tested?

**Fix:** Test recovery procedures, measure actual recovery time

### Mistake 4: Static Assessment

**Symptom:** "We assessed determinism once during design"

**Reality Check:**
- Usage contexts expand
- Dependencies evolve
- Team expertise changes
- Requirements shift

**Fix:** Reassess quarterly or after significant changes

## Summary Checklist

Before finalizing determinism assessment:

- [ ] Scored all four dimensions objectively
- [ ] Considered context modifiers (security, production, etc.)
- [ ] Mapped downstream dependencies
- [ ] Assessed actual failure consequences, not theoretical
- [ ] Verified recovery procedures are tested, not assumed
- [ ] Documented assessment rationale
- [ ] Identified reassessment triggers
- [ ] Aligned resiliency mechanisms with score

---

**Remember:** Determinism assessment is not about judging skill quality—it's about matching resiliency investment to actual requirements. Both high and low determinism skills are valuable; they just need different levels of error correction.
