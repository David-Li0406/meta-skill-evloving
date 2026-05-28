---
name: sprint-planning
description: "Agile sprint planning toolkit. Create user stories following INVEST criteria, plan sprints with capacity management, define acceptance criteria, and track dependencies across sprints for incremental software delivery."
allowed-tools: [Read, Write, Edit, Bash]
---

# Sprint Planning

## Overview

Sprint planning is the process of breaking project work into time-boxed iterations with clear goals and deliverables. Create user stories following INVEST criteria, manage sprint capacity, define acceptance criteria, and track dependencies for successful incremental delivery.

## When to Use This Skill

This skill should be used when:
- Breaking building blocks into user stories
- Planning sprint backlogs and goals
- Estimating story points and capacity
- Defining acceptance criteria
- Identifying and managing dependencies
- Creating release roadmaps

## Visual Enhancement with Project Diagrams

**When documenting sprint plans, include visualizations.**

Use the **project-diagrams** skill to generate:
- Sprint timeline/Gantt charts
- Dependency graphs between stories
- Velocity and burndown projections
- Release roadmap diagrams

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Sprint Planning Framework

### Sprint Structure

```yaml
sprint:
  sprint_number: N
  name: "Descriptive Sprint Name"
  duration_weeks: 1 | 2  # Standard sprint length

  dates:
    start: "YYYY-MM-DD"
    end: "YYYY-MM-DD"

  goals:
    - "Primary goal - what we're trying to achieve"
    - "Secondary goal"

  capacity:
    team_size: N
    available_points: N  # Based on team velocity
    committed_points: N  # Should be <= available

  deliverables:
    - "Concrete deliverable 1"
    - "Concrete deliverable 2"

  stories: []  # List of user stories

  dependencies:
    incoming:
      - sprint: N-1
        items: ["What must be done before this sprint"]
    outgoing:
      - sprint: N+1
        items: ["What this sprint enables"]

  risks:
    - "Sprint-specific risk and mitigation"
```

### User Story Format

**Standard Format:**
```
As a [type of user],
I want [some goal/action],
So that [benefit/reason].
```

**User Story Specification:**

```yaml
story:
  id: "US-NNN"
  title: "Short descriptive title"

  description: |
    As a [user type],
    I want [action],
    So that [benefit].

  acceptance_criteria:
    - given: "Initial context"
      when: "Action taken"
      then: "Expected outcome"
    - "Simple criterion format also acceptable"

  story_points: 1 | 2 | 3 | 5 | 8 | 13  # Fibonacci
  priority: "critical | high | medium | low"

  building_block: "BB-NNN"  # Related building block

  dependencies:
    - story_id: "US-XXX"
      type: "blocks | informs"

  technical_notes: |
    Implementation guidance for developers

  design_link: "URL to mockups/designs (if applicable)"
```

### INVEST Criteria

Every user story should satisfy INVEST:

| Criterion | Description | Validation Question |
|-----------|-------------|---------------------|
| **I**ndependent | Can be developed and delivered separately | Can we release this without other stories? |
| **N**egotiable | Details can be discussed and adjusted | Are we focused on the "what" not "how"? |
| **V**aluable | Delivers value to users or business | Would a stakeholder care about this? |
| **E**stimable | Can be reasonably estimated | Do we understand it well enough to estimate? |
| **S**mall | Fits within a single sprint | Can we complete this in the sprint? |
| **T**estable | Has clear acceptance criteria | Can we write tests for this? |

### Story Point Estimation

**Fibonacci Scale Reference:**

| Points | Complexity | Example |
|--------|------------|---------|
| 1 | Trivial | Text change, simple config |
| 2 | Simple | Single function, minor UI change |
| 3 | Moderate | Feature with some logic, API endpoint |
| 5 | Complex | Multi-component feature, integration |
| 8 | Very Complex | Large feature, significant coordination |
| 13 | Epic-sized | Consider breaking down further |

**Estimation Factors:**
- Complexity of logic
- Number of components touched
- Testing effort required
- Uncertainty/unknowns
- Dependencies on others
- Technical risk

### Capacity Planning

**Team Velocity Calculation:**
```
Available Points = Team Size × Average Points Per Person Per Sprint

Typical: 8-12 points per developer per 2-week sprint
```

**Capacity Buffer:**
```yaml
capacity_allocation:
  new_development: 70%  # User stories
  bugs_and_maintenance: 15%
  meetings_and_overhead: 15%
```

**Leave Buffer:**
- Account for holidays, PTO, sick days
- Reduce capacity proportionally

## Sprint Planning Process

### Phase 1: Backlog Preparation

**Before sprint planning:**

1. **Groom Backlog**
   - Ensure stories have acceptance criteria
   - Verify estimates are up-to-date
   - Clarify dependencies
   - Prioritize based on business value

2. **Review Building Blocks**
   - Which blocks are ready to work on?
   - What dependencies are resolved?
   - What technical decisions are made?

### Phase 2: Sprint Goal Definition

1. **Set Clear Goals**
   - What capability will be delivered?
   - How does this advance the project?
   - What is NOT in scope?

2. **Define Deliverables**
   - Concrete outputs, not activities
   - Measurable completion criteria
   - Demo-able functionality

### Phase 3: Story Selection

1. **Pull from prioritized backlog**
2. **Check dependencies**
3. **Verify capacity fit**
4. **Balance across team members**
5. **Include buffer for unknowns**

### Phase 4: Dependency Mapping

```yaml
dependency_types:
  blocks: "Cannot start until X completes"
  informs: "Better if X completes first, but can work around"
  enables: "Completing this enables future work"
```

**Dependency Rules:**
- No circular dependencies within sprint
- Minimize cross-sprint dependencies
- Front-load high-dependency items
- Identify blockers early

## Story Templates

### Feature Story

```yaml
story:
  id: "US-001"
  title: "User Login with Email/Password"

  description: |
    As a registered user,
    I want to log in with my email and password,
    So that I can access my account and personal data.

  acceptance_criteria:
    - given: "I am on the login page"
      when: "I enter valid email and password and click Login"
      then: "I am redirected to the dashboard"

    - given: "I am on the login page"
      when: "I enter invalid credentials and click Login"
      then: "I see an error message 'Invalid email or password'"

    - given: "I am on the login page"
      when: "I enter email without password and click Login"
      then: "I see a validation error for required password"

    - "Login button is disabled during authentication request"
    - "Session persists across browser refresh"

  story_points: 5
  priority: "critical"
  building_block: "BB-001"

  technical_notes: |
    - Use JWT for session management
    - Hash comparison with bcrypt
    - Rate limit to 5 attempts per minute

  design_link: "figma.com/file/xxx"
```

### Integration Story

```yaml
story:
  id: "US-015"
  title: "Stripe Payment Integration"

  description: |
    As a customer,
    I want to pay with my credit card,
    So that I can complete my purchase.

  acceptance_criteria:
    - given: "I have items in cart"
      when: "I enter valid card details and confirm"
      then: "Payment is processed and order is created"

    - given: "I have items in cart"
      when: "I enter card details that fail (declined, insufficient funds)"
      then: "I see appropriate error message and can try again"

    - "Card details are never stored on our servers"
    - "Stripe webhook updates order status on payment success"
    - "Receipt email is sent on successful payment"

  story_points: 8
  priority: "critical"
  building_block: "BB-007"

  dependencies:
    - story_id: "US-014"
      type: "blocks"  # Cart must be complete first

  technical_notes: |
    - Use Stripe Payment Intents API
    - Implement webhook handler for async updates
    - Store Stripe customer ID for returning customers
```

### Infrastructure Story

```yaml
story:
  id: "US-100"
  title: "CI/CD Pipeline Setup"

  description: |
    As a developer,
    I want automated testing and deployment,
    So that I can ship changes quickly and safely.

  acceptance_criteria:
    - "Tests run automatically on every PR"
    - "Merge to main triggers deployment to staging"
    - "Production deployment requires manual approval"
    - "Failed tests block merge"
    - "Deployment takes less than 10 minutes"

  story_points: 5
  priority: "critical"
  building_block: "BB-100"

  technical_notes: |
    - GitHub Actions workflow
    - Docker build and push to ECR
    - ECS deployment with blue-green strategy
```

## Sprint Plan Output Format

### sprint_plan.md

```markdown
# Sprint Plan: [Project Name]

## Sprint Overview

| Sprint | Name | Duration | Goals |
|--------|------|----------|-------|
| 1 | Foundation | 2 weeks | Auth, Database, CI/CD |
| 2 | Core Features | 2 weeks | User management, Dashboard |
| 3 | Integration | 2 weeks | Payments, Email, Monitoring |

## Sprint 1: Foundation

**Duration:** [Start Date] - [End Date]
**Capacity:** X story points
**Committed:** Y story points

### Goals
1. Set up development infrastructure
2. Implement core authentication
3. Deploy to staging environment

### Deliverables
- [ ] Working authentication service
- [ ] Database schema deployed
- [ ] CI/CD pipeline operational
- [ ] Staging environment accessible

### Stories

| ID | Title | Points | Priority | Block | Status |
|----|-------|--------|----------|-------|--------|
| US-001 | User Registration | 5 | Critical | BB-001 | Pending |
| US-002 | User Login | 5 | Critical | BB-001 | Pending |
| US-100 | CI/CD Setup | 5 | Critical | BB-100 | Pending |
| US-101 | Database Setup | 3 | Critical | BB-101 | Pending |

### Dependencies
- None (first sprint)

### Risks
- OAuth integration may take longer than estimated
- Team learning curve on new CI/CD tools

---

## Sprint 2: Core Features

[Same structure...]
```

### sprint_plan.yaml

```yaml
project: "[Project Name]"
generated: "YYYY-MM-DD"

sprints:
  - sprint_number: 1
    name: "Foundation Sprint"
    duration_weeks: 2
    dates:
      start: "YYYY-MM-DD"
      end: "YYYY-MM-DD"

    goals:
      - "Set up development infrastructure"
      - "Implement core authentication"
      - "Deploy to staging environment"

    capacity:
      team_size: 3
      available_points: 30
      committed_points: 28

    deliverables:
      - "Working authentication service"
      - "Database schema deployed"
      - "CI/CD pipeline operational"

    stories:
      - id: "US-001"
        title: "User Registration"
        description: |
          As a new user,
          I want to create an account,
          So that I can access the application.
        acceptance_criteria:
          - "User can register with email and password"
          - "Email validation required"
          - "Password strength requirements enforced"
          - "Confirmation email sent"
        story_points: 5
        priority: "critical"
        building_block: "BB-001"
        dependencies: []

      # ... more stories

    dependencies:
      incoming: []
      outgoing:
        - sprint: 2
          items: ["Authentication service"]

    risks:
      - "OAuth integration may require additional time"

  # ... more sprints
```

## Quality Checklist

Before completing sprint planning:

- [ ] All stories follow INVEST criteria
- [ ] Acceptance criteria are specific and testable
- [ ] Story points estimated using Fibonacci scale
- [ ] Dependencies mapped and respected
- [ ] Capacity not over-committed (leave 20% buffer)
- [ ] Sprint goals are clear and measurable
- [ ] Deliverables are concrete
- [ ] Risks identified with mitigations
- [ ] All building blocks covered across sprints

## Best Practices

### Do's
- Keep sprints to 1-2 weeks
- Set clear, achievable sprint goals
- Leave buffer for unknowns (15-20%)
- Front-load high-risk items
- Include infrastructure and tech debt
- Review and adjust velocity over time

### Don'ts
- Don't over-commit capacity
- Don't create stories larger than 13 points
- Don't ignore dependencies
- Don't skip acceptance criteria
- Don't plan too far ahead in detail
- Don't forget to include testing time
