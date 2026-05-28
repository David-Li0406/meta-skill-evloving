---
name: adversarial-reasoning
description: Red-team thinking for robustness testing and edge case discovery. Use when you need to stress-test solutions, find vulnerabilities, anticipate failures, or challenge assumptions. Ideal for security review, system design validation, decision stress-testing, and pre-mortem analysis. Example: "We've designed an auth system" → Attack it from 10 angles before shipping.
license: MIT
---

# Adversarial Reasoning (AR)

**Purpose**: Systematically attack your own solutions to find weaknesses before reality does. AR assumes the role of an intelligent adversary trying to break, exploit, or invalidate your design.

## When to Use Adversarial Reasoning

**✅ Use AR when:**
- Validating a proposed solution before implementation
- Security review of systems or processes
- Pre-mortem analysis ("how could this project fail?")
- Stress-testing business decisions
- Finding edge cases in algorithms
- Challenging group consensus (devil's advocate)

**❌ Don't use AR when:**
- Still exploring solution space (use BoT first)
- Optimizing between options (use ToT first)
- Debugging existing issues (use HE)
- Need constructive ideation, not critique

**Examples:**
- "Attack our authentication design" ✅
- "How could this product launch fail?" ✅
- "What are the edge cases in this algorithm?" ✅
- "What features should we build?" ❌ (use BoT)

---

## Core Methodology: STRIKE Framework

### S - Specify the Target

**Goal**: Clearly define what you're attacking and success criteria

**Template:**
```markdown
## Attack Target Specification

**Subject**: [System/Decision/Design being attacked]
**Defender's Goal**: [What the subject is supposed to achieve]
**Attack Success Criteria**: [What counts as "breaking" it]
**Scope Boundaries**: [What's out of scope for this analysis]
**Assumed Adversary**: [Skill level: Script kiddie / Skilled / Nation-state]
```

**Example:**
```markdown
## Attack Target Specification

**Subject**: JWT-based authentication system
**Defender's Goal**: Only authenticated users access protected resources
**Attack Success Criteria**: Unauthorized access, token forgery, session hijacking
**Scope Boundaries**: Physical access attacks out of scope
**Assumed Adversary**: Skilled attacker with standard tools
```

---

### T - Threat Modeling (STRIDE+)

**Goal**: Systematically enumerate attack categories

**Use STRIDE+ Framework:**

| Category | Question | Examples |
|----------|----------|----------|
| **S**poofing | Can identity be faked? | Forged tokens, impersonation, credential theft |
| **T**ampering | Can data be modified? | MITM attacks, input manipulation, DB injection |
| **R**epudiation | Can actions be denied? | Missing audit logs, unsigned transactions |
| **I**nformation Disclosure | Can secrets leak? | Error messages, timing attacks, logs |
| **D**enial of Service | Can availability be attacked? | Resource exhaustion, algorithmic complexity |
| **E**levation of Privilege | Can access be escalated? | IDOR, role confusion, JWT claim manipulation |
| **+Supply Chain** | Can dependencies be compromised? | Malicious packages, compromised CI/CD |
| **+Social Engineering** | Can humans be exploited? | Phishing, pretexting, insider threats |

**Process:**
1. For each STRIDE+ category, brainstorm 3-5 specific attacks
2. Don't filter for feasibility yet - enumerate first
3. Include "obvious" attacks (they're often overlooked)

---

### R - Risk-Ranked Attack Generation

**Goal**: Prioritize attacks by impact and feasibility

**For each attack, assess:**

```markdown
## Attack: [Name]

**Category**: [STRIDE+ category]
**Description**: [How the attack works]
**Prerequisites**: [What attacker needs]
**Impact**: [1-5] - What damage if successful?
  - 5: Complete system compromise / data breach
  - 4: Significant unauthorized access
  - 3: Moderate data exposure or disruption
  - 2: Limited impact, contained damage
  - 1: Minimal impact, theoretical only

**Feasibility**: [1-5] - How easy to execute?
  - 5: Trivial (automated tools, no special access)
  - 4: Easy (basic skills, public exploits)
  - 3: Moderate (requires expertise or access)
  - 2: Difficult (advanced skills, insider access)
  - 1: Very difficult (nation-state resources)

**Risk Score**: Impact × Feasibility = [1-25]
```

**Priority Ranking:**
- **Critical (20-25)**: Must address before shipping
- **High (15-19)**: Address in current cycle
- **Medium (8-14)**: Plan mitigation
- **Low (1-7)**: Accept or defer

---

### I - Investigate Attack Paths

**Goal**: Develop detailed attack scenarios for top risks

**For each Critical/High risk attack, create attack narrative:**

```markdown
## Attack Path: [Name]

### Attacker Profile
- **Motivation**: [Financial / Ideological / Competitive / Chaos]
- **Resources**: [Time, tools, insider access, budget]
- **Risk Tolerance**: [Will they risk detection?]

### Attack Sequence
1. **Reconnaissance**: [How attacker discovers the vulnerability]
2. **Weaponization**: [Tools/techniques prepared]
3. **Delivery**: [How attack reaches the target]
4. **Exploitation**: [Exact steps to exploit]
5. **Installation**: [Persistence mechanisms if applicable]
6. **Command & Control**: [Ongoing access methods]
7. **Actions on Objectives**: [What attacker does with access]

### Detection Opportunities
- [Where could we detect this attack?]
- [What logs/alerts would trigger?]

### Current Mitigations
- [Existing defenses that apply]
- [Gaps in current defenses]
```

---

### K - Kill Chain Disruption

**Goal**: Design countermeasures that break attack paths

**For each attack path, identify disruption points:**

```markdown
## Countermeasures: [Attack Name]

### Prevention (Stop attack from succeeding)
| Kill Chain Stage | Countermeasure | Effort | Effectiveness |
|------------------|----------------|--------|---------------|
| Reconnaissance | [Control] | [L/M/H] | [%] |
| Delivery | [Control] | [L/M/H] | [%] |
| Exploitation | [Control] | [L/M/H] | [%] |

### Detection (Identify attack in progress)
- [Alert/monitor that would trigger]
- [Expected detection latency]

### Response (Limit damage if attack succeeds)
- [Containment procedures]
- [Recovery procedures]

### Recommended Prioritization
1. [Highest ROI countermeasure]
2. [Second priority]
3. [Third priority]
```

**Defense-in-Depth Principle**: Implement controls at multiple kill chain stages. No single control is sufficient.

---

### E - Edge Case Enumeration

**Goal**: Find non-malicious but problematic edge cases

**Categories:**

| Category | Questions |
|----------|-----------|
| **Boundary Conditions** | What happens at min/max values? Zero? Negative? |
| **Timing** | Race conditions? Timeout handling? Clock skew? |
| **Scale** | 10x users? 100x data? Empty inputs? |
| **State** | Invalid state transitions? Partial failures? |
| **Environment** | Different regions? Timezones? Languages? |
| **Integration** | Dependency failures? Version mismatches? |
| **Data** | Null? Unicode? Emoji? SQL injection characters? |
| **Concurrency** | Parallel requests? Duplicate submissions? |

**Template:**
```markdown
## Edge Case: [Name]

**Category**: [From table above]
**Scenario**: [Specific situation]
**Expected Behavior**: [What should happen]
**Potential Failure**: [What might go wrong]
**Test Case**: [How to verify handling]
```

---

## Pre-Mortem Variant

For project/decision risk analysis (not security):

**Prompt**: "It's 6 months from now. This project has failed spectacularly. What happened?"

**Categories:**
1. **Technical Failures**: Architecture, scalability, integration
2. **Resource Failures**: Budget, timeline, staffing
3. **Stakeholder Failures**: Changing requirements, politics, sponsorship
4. **Market Failures**: Competition, timing, demand
5. **Operational Failures**: Deployment, monitoring, support
6. **Team Failures**: Burnout, turnover, skill gaps

**For each failure mode:**
- Probability (1-5)
- Impact (1-5)
- Early warning signs
- Preventive actions

---

## Red Team / Blue Team Exercise

**For comprehensive validation, run adversarial simulation:**

**Red Team (Attackers):**
1. Review target specification
2. Generate attacks using STRIDE+
3. Develop top 5 attack paths in detail
4. Attempt exploitation (in test environment)
5. Document successful attacks

**Blue Team (Defenders):**
1. Review same target specification
2. Implement defenses based on threat model
3. Monitor for red team activity
4. Respond to detected attacks
5. Document defensive gaps

**Purple Team (Collaboration):**
1. Red team shares successful attacks
2. Blue team explains what was missed
3. Jointly develop improved defenses
4. Update threat model with learnings

---

## Common Mistakes

1. **Being Too Nice**: Pulling punches, not exploring dark scenarios
   - Fix: Adopt genuine adversarial mindset

2. **Scope Creep**: Attacking things outside defined scope
   - Fix: Clear scope boundaries in target specification

3. **Ignoring Low-Tech Attacks**: Focusing only on sophisticated attacks
   - Fix: Include social engineering, misconfiguration, human error

4. **Attack Without Defense**: Finding problems without solutions
   - Fix: Every attack must have countermeasure recommendations

5. **One-Time Exercise**: Treating AR as checkbox activity
   - Fix: Regular red team exercises, continuous threat modeling

---

## Integration with Other Patterns

**ToT → AR**: After ToT selects best solution, use AR to validate before implementation

**AR → ToT**: If AR finds critical flaws, use ToT to evaluate fix options

**BoT → AR**: After BoT generates options, use AR on top candidates

**AR → HE**: If AR reveals actual vulnerability was exploited, use HE to investigate

---

## Output Template

```markdown
# Adversarial Analysis: [Subject]

## Executive Summary
- **Target**: [What was analyzed]
- **Critical Findings**: [Top 3 risks]
- **Recommendation**: [Ship / Fix / Redesign]

## Threat Model
[STRIDE+ analysis summary]

## Top 5 Attack Paths
[Detailed attack scenarios]

## Countermeasure Recommendations
[Prioritized defense improvements]

## Edge Cases Identified
[Non-malicious failure modes]

## Residual Risk
[What risks remain after mitigations]

## Confidence: [X]%
- [Justification - coverage, depth, expertise]
```
