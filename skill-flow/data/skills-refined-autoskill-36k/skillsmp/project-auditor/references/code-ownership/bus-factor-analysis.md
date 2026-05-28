<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Bus Factor Analysis and Risk Mitigation

## Overview

The "bus factor" (also called "truck factor" or "lottery factor") is the minimum number of team members who would need to be unavailable for a project to stall. This document covers bus factor calculation, risk assessment, and mitigation strategies.

## Bus Factor Definition

**Formal Definition**: The minimum number of team members who, if suddenly unavailable (hit by a bus, win the lottery, leave the company, etc.), would put the project at critical risk due to loss of essential knowledge.

**Key Concept**: Measures knowledge concentration and team resilience.

## Bus Factor Calculation

### Basic Algorithm

```
1. For each file, identify contributors with >10% ownership
2. Sort contributors by total files owned (descending)
3. Simulate removing contributors one by one (highest impact first)
4. Bus factor = number removed before >20% of files have no expert owner
```

### Detailed Steps

**Step 1: Identify Major Contributors**
```
For each file:
  major_contributors = contributors with >10% ownership
```

**Step 2: Calculate Impact Scores**
```
For each contributor:
  impact_score = Σ(ownership_percentage * file_criticality)
```

**Step 3: Simulate Departures**
```
removed = []
uncovered_files = 0

while uncovered_files / total_files < 0.20:
    next_person = highest_impact_contributor(not in removed)
    removed.append(next_person)
    uncovered_files = count_files_without_major_contributor(removed)

bus_factor = length(removed)
```

### Component-Level Bus Factor

Calculate bus factor per service, directory, or module:

```
For each component:
  component_bus_factor = minimum removals before component unmaintainable
```

**Critical Components**:
- Authentication/authorization
- Payment processing
- Data encryption
- Core APIs
- Database migrations
- Infrastructure code
- Security controls

## Bus Factor Thresholds

### Overall Project

- **Healthy**: Bus factor >3 (team can lose 3+ people)
- **Acceptable**: Bus factor = 3 (can lose 3 people)
- **Risky**: Bus factor = 2 (vulnerable to 2 departures)
- **Critical**: Bus factor = 1 (single point of failure)

### Per Component

```
Critical components: Minimum bus factor = 3
Important components: Minimum bus factor = 2
Standard components: Minimum bus factor = 2
Low-priority: Bus factor = 1 acceptable
```

### Team Size Adjustments

```
Team Size    |  Minimum Bus Factor
-------------|--------------------
1-3 people   |  1 (acceptable risk)
4-6 people   |  2
7-15 people  |  3
16+ people   |  4+
```

## Single Point of Failure (SPOF) Detection

### SPOF Criteria

A file/component is a SPOF if it meets multiple criteria:

```
SPOF Indicators:
1. File has only one contributor ever
2. File is in critical path (auth, payments, core API)
3. File has >500 LOC (complex)
4. Owner is sole expert (no backup owner with >15% knowledge)
5. File lacks comprehensive tests (<60% coverage)
6. File lacks documentation (no README, no comments)
```

### Risk Levels

**Critical SPOF**: All 6 criteria met
- Immediate action required
- High business impact
- No redundancy

**High SPOF**: 4-5 criteria met
- Action within 2 weeks
- Significant impact
- Very limited redundancy

**Medium SPOF**: 2-3 criteria met
- Action within quarter
- Moderate impact
- Some limited redundancy

**Low SPOF**: 1 criterion met
- Monitor and plan
- Lower impact
- Acceptable short-term

### SPOF Priority Matrix

```
               │ Critical Code │ Important Code │ Standard Code
───────────────┼───────────────┼────────────────┼───────────────
One Owner      │ P1 - Critical │ P2 - High      │ P3 - Medium
No Tests       │ P1 - Critical │ P2 - High      │ P3 - Medium
No Docs        │ P2 - High     │ P3 - Medium    │ P4 - Low
Complex (>500) │ P2 - High     │ P3 - Medium    │ P4 - Low
```

## Risk Assessment Framework

### Concentration Risk

**Definition**: Risk from ownership being too concentrated in few people.

**Formula**:
```
concentration_risk = 1 if bus_factor = 1
                     0.5 if bus_factor = 2
                     1 / bus_factor otherwise
```

**High Concentration Indicators**:
- Top 1 person owns >20% of codebase
- Top 3 people own >50% of codebase
- Critical component has bus factor = 1

### Departure Risk

**Factors Indicating Departure Risk**:
```
High Risk (Score 1.0):
- Known departure (resignation announced)
- Extended absence (sabbatical, parental leave)
- Transfer to different project

Medium Risk (Score 0.5):
- Declining activity (commits down 50%+)
- No recent contributions (>90 days)
- Limited engagement (missing reviews)

Low Risk (Score 0.2):
- Normal activity levels
- Regular contributions
- Active participation
```

### Documentation Gap Risk

**Assessment**:
```
documentation_gap = 1 - (docs_quality_score / 10)

Docs Quality Score (0-10):
- Has README: +2
- Has architecture diagram: +2
- Has API docs: +2
- Has inline comments: +2
- Has runbook/playbook: +2
```

### Business Impact

**Criticality Scoring (1-10)**:
```
10: Critical - Business cannot operate
    - Authentication system
    - Payment processing
    - Core transaction processing

8-9: High - Major features impaired
     - Key features unavailable
     - Revenue-generating functions
     - Customer-facing services

6-7: Important - Degraded experience
     - Non-critical features
     - Internal tools
     - Secondary services

4-5: Moderate - Minor impact
     - Nice-to-have features
     - Analytics/reporting
     - Background jobs

1-3: Low - Minimal impact
     - Experimental features
     - Admin tools
     - Documentation
```

## Succession Planning

### Priority Score Calculation

```
succession_priority = (
    criticality * 0.40 +
    concentration_risk * 0.30 +
    departure_risk * 0.20 +
    documentation_gap * 0.10
)
```

**Output**: Prioritized list of areas needing succession planning.

### Knowledge Transfer Estimation

**Transfer Timeline by Complexity**:
```
Simple Component (1-2 weeks):
- Clear, well-documented code
- Good test coverage (>80%)
- Low complexity (<1000 LOC)
- Few external integrations
- Straightforward business logic

Moderate Component (3-4 weeks):
- Some documentation present
- Moderate test coverage (50-80%)
- Medium complexity (1000-5000 LOC)
- Several external integrations
- Moderately complex business logic

Complex Component (6-8 weeks):
- Limited or poor documentation
- Low test coverage (<50%)
- High complexity (>5000 LOC)
- Many external integrations
- Complex business logic
- Tribal knowledge required
```

### Transfer Activities

**Week 1: Foundation**
- Architecture overview
- Code walkthrough
- Development environment setup
- Access and credentials
- Key contacts introduction

**Week 2-3: Hands-on**
- Pair programming sessions
- Shadow on-call
- Make supervised changes
- Review recent PRs and issues
- Debugging practice

**Week 4+: Independence**
- Solo implementation tasks
- Lead code reviews
- Handle incidents
- Knowledge verification
- Documentation updates

### Verification Checklist

Knowledge transfer complete when successor can:
- [ ] Explain system architecture without notes
- [ ] Make changes independently
- [ ] Debug common issues
- [ ] Perform deployments
- [ ] Handle production incidents
- [ ] Identify who to escalate to
- [ ] Review others' code in area
- [ ] Explain business logic and trade-offs

## Mitigation Strategies

### Immediate Actions (Bus Factor = 1)

**Priority 1: Identify Backup Owner**
- Find team member with highest existing familiarity
- Assign as backup in CODEOWNERS
- Schedule weekly pairing sessions

**Priority 2: Document Critical Knowledge**
- System architecture
- Key design decisions
- Common failure modes
- Deployment procedures
- On-call runbooks

**Priority 3: Increase Test Coverage**
- Add integration tests
- Document test scenarios
- Automate smoke tests
- Create test data

**Priority 4: Code Review Sharing**
- Require backup owner on all reviews
- Rotate review assignments
- Document review findings

### Short-term Actions (2-4 weeks)

**Knowledge Transfer Sprint**:
- 2-3 pairing sessions per week
- Assign backup owner real tasks
- Review and refactor documentation
- Create video walkthroughs
- Document tribal knowledge

**Test and Documentation Improvement**:
- Increase test coverage to >70%
- Add architecture diagrams
- Document APIs and interfaces
- Create troubleshooting guides
- Record deployment procedures

### Long-term Actions (Quarter)

**Ownership Distribution**:
- Gradually reassign ownership
- Cross-train team members
- Rotate component ownership
- Encourage code tourism

**Process Improvements**:
- Mandatory code review by backup owners
- Documentation requirements in DoD
- Test coverage requirements
- Pair programming schedule
- Knowledge sharing sessions

### Preventive Measures

**Team Structure**:
- Never allow single owner for critical code
- Require minimum 2 owners per critical component
- Balance workload across team
- Regular ownership audits

**Development Practices**:
- Pair programming for complex features
- Cross-functional team involvement
- Rotation programs
- Mentorship assignments

**Documentation Standards**:
- Architecture decision records (ADRs)
- API documentation requirements
- Runbook templates
- Code comment standards

**Monitoring and Alerts**:
- Track ownership concentration
- Alert on increasing bus factor risk
- Monitor staleness metrics
- Review quarterly

## Tools and Automation

### Automated Bus Factor Calculation

```bash
# Example using git log
#!/bin/bash
# Calculate contributors per file
git ls-files | while read file; do
  owners=$(git log --format="%an" -- "$file" | sort | uniq -c | sort -rn | head -3)
  echo "$file: $owners"
done
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Bus Factor Check
on: [push, pull_request]
jobs:
  bus-factor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Calculate Bus Factor
        run: |
          ./scripts/bus-factor-analyser.sh
      - name: Fail if Critical
        run: |
          if [ "$BUS_FACTOR" -eq 1 ]; then
            echo "Critical: Bus factor is 1!"
            exit 1
          fi
```

### Dashboard Integration

**Key Metrics to Display**:
- Overall bus factor
- Components with bus factor = 1
- Top SPOFs by criticality
- Staleness of critical owners
- Succession planning progress

## Case Studies

### Example 1: Authentication Service (Bus Factor = 1)

**Situation**:
- Single developer (Alice) wrote entire auth service
- 2500 LOC, complex OAuth integration
- No documentation, 30% test coverage
- Alice announced departure in 3 weeks

**Actions Taken**:
1. Week 1: Emergency documentation sprint
   - Alice created architecture diagram
   - Documented OAuth flow
   - Recorded setup video
   - Added inline comments

2. Week 2: Knowledge transfer
   - Daily 2-hour pairing with Bob
   - Bob deployed auth service
   - Alice reviewed Bob's test PRs

3. Week 3: Transition
   - Bob handled auth issues with Alice available
   - Increased test coverage to 60%
   - Updated CODEOWNERS to @bob @auth-team

**Result**: Smooth transition, no production issues

### Example 2: Payment Processing (Bus Factor = 1)

**Situation**:
- Critical payment code owned by former employee
- No documentation, no backup owner
- Discovered during incident

**Actions Taken**:
1. Immediate: Assigned two senior engineers as owners
2. Week 1-2: Reverse engineering and documentation
3. Week 3-4: Refactoring and test addition
4. Month 2: Split into smaller, well-tested modules

**Lessons Learned**:
- Don't wait for incident to discover SPOFs
- Proactive audits critical
- Investment in refactoring pays off

## References

- "An Analysis of the Effect of Code Ownership on Software Quality" (Microsoft Research)
- "On the usefulness of ownership metrics in open-source software projects" (ScienceDirect, 2015)
- Various bus factor analysis tools and research
