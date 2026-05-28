---
name: requirements-elaboration
description: Transform vague requirements into concrete decisions by exploring the decision space. Use when high-level asks spawn implicit decisions, when defaults need challenging, or when you need systematic discovery of actual needs vs assumed solutions.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  domain: software-development
  cluster: requirements-analysis
  type: diagnostic
  mode: assistive
---

# Requirements Elaboration: Decision Discovery Skill

You help transform high-level desires into concrete, justified decisions by systematically exploring the decision space, identifying dependencies, and challenging default assumptions that would otherwise create mediocre implementations.

## Core Principle

**Every high-level requirement explodes into a decision tree. Every default hides assumptions that may be wrong for your specific context. The path to exceptional software is systematically questioning assumptions rather than accepting statistical averages.**

Research from requirements engineering shows that 60-80% of project failures trace back to requirements problems, not technical execution.

## The Decision Cascade Problem

### Requirement Explosion Example

**High-level**: "Users should authenticate"

**Immediate questions**:
- Who are the users?
- What are they authenticating to?
- Why do they need authentication?
- When does authentication occur?
- Where does identity come from?
- How long do sessions last?

**Second-order decisions**:
- Identity source (internal database, LDAP, OAuth, SAML, multiple?)
- Authentication factors (password, MFA, biometric, hardware tokens?)
- Session management (duration, refresh, device binding, concurrent?)

**Hidden assumptions defaulted without thought**:
- "Users have email addresses"
- "Sessions should last 24 hours"
- "Passwords are acceptable"
- "Users have modern browsers"
- "Network is always available"

## The Five Whys for Features

### Systematic Questioning Process

**Initial request**: "We need user profiles"

**Why 1**: "Why do we need user profiles?"
- Answer: "To personalize the experience"
- Follow-up: "What personalization is needed?"

**Why 2**: "Why personalize the experience?"
- Answer: "Users want to see their own data"
- Follow-up: "What data is 'theirs'?"

**Why 3**: "Why separate data by user?"
- Answer: "Different departments use it differently"
- Follow-up: "How many departments? How different?"

**Why 4**: "Why not just department-level separation?"
- Answer: "Individual accountability needed"
- Follow-up: "For what specific actions?"

**Why 5**: "Why is individual accountability needed?"
- Answer: "Regulatory compliance for changes"
- **Discovery**: Real need is audit trail, not profiles

**Actual requirement discovered**:
- NOT needed: User profiles, personalization, preferences, avatars
- ACTUALLY needed: Action attribution, audit logging, department separation, read-only vs edit roles

## Context Discovery Framework

### User Context

**Questions to ask**:
- Who exactly will use this?
- How many concurrent users?
- What's their technical sophistication?
- What devices do they use?
- Where are they located?
- When do they use it?

**Anti-patterns to catch**:
- "Users" without qualification
- "Modern browsers" assumption
- "Mobile-friendly" without mobile users
- "Global" when it's single-office

### Business Context

**Questions to ask**:
- What problem does this solve?
- What's it replacing?
- What's the cost of not having it?
- How does success get measured?
- What's the failure impact?
- Who pays for it?

**Revelations these produce**:
- "Replace spreadsheet" → Import/export critical
- "Compliance need" → Audit over features
- "Cost center" → Minimal maintenance crucial
- "Revenue generator" → Performance critical

### Technical Context

**Questions to ask**:
- What systems must it integrate with?
- What are the hard constraints?
- What technical debt exists?
- What skills does the team have?
- What's the maintenance budget?
- What's the deployment environment?

**Discoveries these enable**:
- "On-premise only" → No cloud services
- "Legacy database" → Schema constraints
- "Small team" → Avoid exotic tech
- "No DevOps" → Simple deployment crucial

## Decision Dependency Mapping

### Dependency Types

**Hard constraints**: If A then must B
- If internal_only → must use corporate_identity_provider
- If regulated_industry → must have audit_trail
- If multi_tenant → must have data_isolation

**Mutual exclusions**: If A then cannot B
- If internal_only → cannot have social_login
- If on_premise → cannot use cloud_only_service

**Soft preferences**: If A then prefer B
- If small_team → prefer simple_tooling
- If high_scale → prefer horizontal_scaling
- If cost_sensitive → prefer open_source

### Lynchpin Decision Identification

Find decisions that unlock or constrain many others:

**Example lynchpin**: "Is this application internal only?"

**If internal_only = true**:
- Enables: Use internal SSO, skip GDPR compliance, simplified security
- Prevents: Social login, public registration, multi-tenant architecture

**If internal_only = false**:
- Enables: External user registration, social auth, public API
- Requires: GDPR compliance, rate limiting, DDoS protection

## Assumption Challenge Protocols

### Default Assumptions to Always Question

**User assumptions**:
| Default | Alternatives |
|---------|--------------|
| "Users have email addresses" | Phone, Employee ID, Username only |
| "Users have persistent identity" | Anonymous, Session-only, Ephemeral |
| "Users want to customize" | Defaults fine, Admin-configured |
| "Users access from multiple devices" | Single workstation, Shared terminals |

**Scale assumptions**:
| Default | Reality Check |
|---------|---------------|
| "Need to handle millions of users" | What's realistic year 1, 3, 5? |
| "Must scale horizontally" | Would vertical work for projected load? |
| "Needs real-time updates" | What latency is actually acceptable? |
| "Requires microservices" | What's the team size and skill? |

**Technical assumptions**:
| Default | Alternatives |
|---------|--------------|
| "Need a database" | Files, In-memory, External API, Event log |
| "Need user accounts" | Shared access, Token-based, IP-based |
| "Need REST API" | GraphQL, RPC, Message queue, Direct DB |
| "Need responsive design" | Desktop only, Mobile only, Fixed viewport |

### Statistical Gravity Resistance

**Symptoms of gravity**:
- "Industry standard" without justification
- "Best practice" without context
- "Everyone uses X" without evaluation
- "Modern apps have Y" without need
- "X is popular" without fit analysis

**Resistance techniques**:

**Devil's Advocate**:
1. Assume the opposite
2. List benefits of NOT having it
3. Find successful counterexamples
4. Calculate real cost
5. Question the rhetoric

**Scenario Testing**:
1. Write concrete user stories
2. Walk through actual workflows
3. Count real interactions
4. Time actual tasks
5. Measure real frequency

## Decision Brief Template

```yaml
Decision Brief:
  header:
    decision_id: "DEC-YYYY-NNN"
    title: "[Decision Name]"
    impact: "[Foundational/Major/Minor]"
    reversibility: "[Easy/Moderate/Difficult]"

  context:
    requirement_trace: "[Original requirement]"
    discovered_context:
      - "[Context item 1]"
      - "[Context item 2]"
    existing_constraints:
      - "[Constraint 1]"
      - "[Constraint 2]"

  options:
    option_1:
      name: "[Option name]"
      description: "[What this means]"
      pros: ["[Pro 1]", "[Pro 2]"]
      cons: ["[Con 1]", "[Con 2]"]
      cost: "[Low/Moderate/High]"
      risk: "[Low/Medium/High]"
      effort: "[Estimate]"

    eliminated_options:
      "[Option name]":
        reason: "[Why eliminated]"

  dependencies:
    decisions_this_enables: ["[Decision 1]"]
    decisions_this_requires: ["[Decision 2]"]

  recommendation:
    choice: "[Recommended option]"
    rationale: ["[Reason 1]", "[Reason 2]"]
    conditions: ["[Condition 1]", "[Condition 2]"]
```

## Specification Generation

### From Decisions to Specifications

**Functional requirements**:
- Source: Validated user needs
- Format: User stories with acceptance criteria
- Traceability: Links to decision records

**Non-functional requirements**:
- Source: Context discoveries
- Format: Measurable constraints
- Categories: Performance, Security, Usability, Compatibility, Compliance

**Technical specifications**:
- Source: Decision briefs
- Format: Implementation directives
- Includes: Technology choices, architecture patterns, data models

**Anti-requirements** (crucial for preventing scope creep):
- Source: Eliminated options
- Format: What NOT to build
- Examples: "No user customization", "No mobile version", "No public access"

## Validation Patterns

### Spike Types

**Technical spike** (1-3 days):
- Purpose: Validate technical feasibility
- Deliverables: Working code, performance metrics, risk assessment

**User spike** (2-5 days):
- Purpose: Validate user acceptance
- Deliverables: Clickable mockup, user feedback, workflow validation

**Integration spike** (3-5 days):
- Purpose: Validate system integration
- Deliverables: API communication proof, data flow, error handling

### Reversal Triggers

**Immediate reversal** needed when:
- Fundamental assumption proved false
- Critical dependency unavailable
- Cost exceeds budget by >50%
- Legal/compliance blocker

**Considered reversal** when:
- Significant complexity discovered
- Better alternative found
- Requirements substantially changed
- Team lacks skills

## Anti-Patterns

### 1. Analysis Paralysis
**Pattern:** Spending months gathering requirements through endless stakeholder meetings without building anything.
**Why it fails:** Requirements evolve when users see working software. Perfect understanding is impossible upfront; stakeholders often don't know what they want until they see what they don't want.
**Fix:** Time-box exploration phases. Build prototypes early. Validate assumptions through spikes rather than meetings. Aim for "good enough to start" rather than "complete."

### 2. Assumption Avalanche
**Pattern:** Accepting defaults without documentation—"obvious" choices everywhere, copy-paste architecture from previous projects.
**Why it fails:** Undocumented decisions become invisible constraints. When problems emerge later, no one remembers why choices were made or whether alternatives were considered.
**Fix:** Document every significant decision with rationale. Challenge defaults explicitly. Create decision briefs even for "obvious" choices so the reasoning is captured.

### 3. Feature Creep During Discovery
**Pattern:** "While we're at it" additions during requirements gathering. Nice-to-have becomes must-have through scope bleed.
**Why it fails:** Discovery expands indefinitely. The "complete" feature set grows faster than implementation capacity. Core value gets buried under accumulated wants.
**Fix:** Maintain strict must/should/could separation. Create anti-requirements (what you will NOT build). Revisit scope when additions emerge—something must leave if something enters.

### 4. Solutioning in Requirements
**Pattern:** Requirements specify technology choices: "Use React" instead of "Users need fast page loads." How before what.
**Why it fails:** Technology choices belong to implementation. Premature technology constraints eliminate potentially better solutions and encode assumptions that may be wrong.
**Fix:** Write requirements as user outcomes and constraints. Keep technology decisions separate. Let implementation choose how to achieve the what.

### 5. Single Stakeholder Capture
**Pattern:** Treating one vocal stakeholder as the voice of all users. Requirements reflect their preferences without broader validation.
**Why it fails:** Individual stakeholders have individual biases. The loudest voice rarely represents typical users. Edge cases become core requirements.
**Fix:** Identify all user categories. Get input from multiple representatives. Validate requirements with actual usage data where available. Weight inputs by user volume.

## Success Metrics

- **Decision velocity**: Decisions made per week (clear trending up early, stabilizing later)
- **Reversal rate**: Decisions reversed / total decisions (target: <10%)
- **Assumption validation rate**: Validated / total assumptions (target: >80%)
- **Requirement stability**: Requirements unchanged after sign-off (target: >90%)

## Integration

### Inbound (feeds into this skill)
| Skill | What it provides |
|-------|------------------|
| requirements-analysis | Initial problem framing and stakeholder identification |
| research | Domain knowledge and prior art discovery |

### Outbound (this skill enables)
| Skill | What this provides |
|-------|-------------|
| system-design | Concrete requirements and constraints for architecture |
| github-agile | User stories and acceptance criteria for implementation |

### Complementary
| Skill | Relationship |
|-------|--------------|
| requirements-analysis | Use requirements-analysis for initial scoping, elaboration for deep decision discovery |
| system-design | Use elaboration to define what, system-design to define how |
