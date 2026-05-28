# Agent System Guide

**Purpose**: Authoritative reference for agent hierarchy, roles, communication protocols, and escalation patterns in Qara's multi-agent system.

**When to read**: Working with multiple agents, escalating issues, or understanding agent decision authority.

---

## Table of Contents
1. [Agent Hierarchy](#agent-hierarchy)
2. [Agent Roles & Capabilities](#agent-roles--capabilities)
3. [Invocation & Escalation](#invocation--escalation)
4. [Communication Protocols](#communication-protocols)
5. [Quality Gates](#quality-gates)
6. [Quick Reference](#quick-reference)

---

## Agent Hierarchy

```
Jean-Marc (User) - FINAL AUTHORITY ON EVERYTHING
    ↓
Qara (Primary Assistant) - Orchestrates all agents
    ↓
├── Intern Agents - Parallel execution specialists
│   └── Can invoke Engineers when stuck
├── Engineer Agents - Technical expertise
│   └── Can escalate to Principal
└── Principal Engineer - Architectural decisions
    └── Provides recommendations to Jean-Marc
```

**Key Principle**: Clear hierarchy with defined escalation paths and decision authority.

---

## Agent Roles & Capabilities

### Intern Agent

**Role**: High-agency generalist for parallel execution  
**Authority Level**: Implementation decisions  
**Decision Scope**: How to implement specific tasks

**Capabilities**:
- Full feature implementation
- File updates and refactoring
- Research and analysis
- Test writing
- Documentation creation
- Spotcheck reviews (quality validation)

**Limitations**:
- Cannot make architectural decisions
- Should escalate security-sensitive implementations
- Should escalate performance-critical code

**When to Use**:
- Parallel file updates
- Independent subtasks
- Research assignments
- Standard implementations
- Any task that can be parallelized

**Can Invoke Engineers When**:
- Encounters technical complexity beyond scope
- Needs security guidance
- Requires performance optimization expertise
- Faces integration challenges

---

### Engineer Agent

**Role**: Technical specialist for complex problems  
**Authority Level**: Technical decisions  
**Decision Scope**: Implementation approach, optimization strategy

**Capabilities**:
- Complex technical problem solving
- Performance optimization
- Security analysis
- Code review and refactoring
- Integration design
- Technical recommendations

**Limitations**:
- Cannot make architectural decisions (escalate to Principal)
- Provides recommendations only (Jean-Marc decides)
- Works sequentially, not in parallel

**When to Use**:
- Technical complexity beyond Intern scope
- Security reviews
- Performance optimization
- Integration challenges
- Complex debugging

---

### Principal Engineer Agent

**Role**: Strategic architect for system-wide decisions  
**Authority Level**: Architectural recommendations  
**Decision Scope**: System architecture, technology strategy  
**Final Authority**: Jean-Marc

**Capabilities**:
- Architectural design
- Technology selection
- System-wide refactoring strategy
- Technical debt prioritization
- Long-term technical planning

**Limitations**:
- Provides recommendations, not final decisions
- Jean-Marc has final authority
- Reserved for significant decisions only

**When to Use**:
- Major architectural changes
- Technology stack decisions
- System refactoring approach
- Scalability planning
- Cross-system implications

---

## Invocation & Escalation

### Direct Invocation (Jean-Marc → Agent)

**Jean-Marc specifies which agent(s) to use:**
```
"Have the agents update these 5 files..."
"Ask an engineer to review this code..."
"I need a principal engineer opinion on architecture..."
```

### Automatic Delegation (Qara → Agent)

**Qara determines appropriate agent based on:**
- Multiple files → Parallel agents
- Technical complexity → Engineer
- Architectural decision → Principal

**Decision Criteria**:
- Task complexity
- Parallelization opportunity
- Technical depth required
- Architectural implications

### Escalation Paths

#### Intern → Engineer

**When to Escalate**:
- Technical problem beyond agent's expertise
- Security-sensitive implementation
- Performance optimization needed
- Complex integration challenges

**Escalation Template**:
```
ESCALATED from Intern: [Problem description]

Context: [What agent tried]
Challenge: [Specific technical issue]
Question: [What expertise is needed]
Files: [Paths and line numbers]
Desired Outcome: [Success criteria]
```

**Example**:
```
ESCALATED from Intern: OAuth implementation complexity

Context: Implementing OAuth flow for API authentication
Attempted: Basic token exchange, but unsure about refresh token rotation
Challenge: Security best practices for token storage and rotation
Question: What pattern should I use for secure refresh token management?
Files: /src/auth/oauth.ts lines 45-78
Desired Outcome: Secure, production-ready OAuth implementation
```

#### Engineer → Principal

**When to Escalate**:
- Architectural decision needed
- Cross-system implications
- Long-term strategy question
- Major refactoring approach

**Escalation Template**:
```
ARCHITECTURAL DECISION NEEDED: [Decision description]

Context: [Current state]
Options Considered:
  A) [Option A with pros/cons]
  B) [Option B with pros/cons]
Implications: [Long-term impact]
Recommendation: [Engineer's recommendation]
Question: [Specific architectural guidance needed]
```

#### Agent → Jean-Marc

**When to Escalate**:
- Conflicting requirements
- Major decision points
- Unexpected blockers
- Need human judgment

**Escalation Format**:
```
Jean-Marc, I need your input on: [Decision]

Options:
A) [Option A details, pros/cons]
B) [Option B details, pros/cons]

My recommendation: [A/B] because [reasoning]

Please decide: [A/B/other]
```

---

## Communication Protocols

### Context Sharing (MANDATORY)

**Every agent invocation must include:**

1. **Task Description**
   - Clear, specific objective
   - Success criteria
   - Constraints

2. **Relevant Context**
   - Background information
   - Related code/files
   - Previous attempts (if any)

3. **File Paths**
   - Exact locations
   - Relevant line numbers
   - Related files

4. **Examples** (when helpful)
   - Expected format
   - Similar patterns
   - Reference implementations

5. **Dependencies**
   - What must be preserved
   - What can be changed
   - Integration points

**Bad (Insufficient)**:
```
"Update the navigation"
```

**Good (Complete)**:
```
"Update /src/components/navigation.tsx:
- Add Settings menu item (line 45, after Profile)
- Use existing MenuItem pattern (lines 42-44)
- Link to /settings route
- Icon: SettingsIcon from lucide-react
Success: Settings appears in menu between Profile and Logout"
```

### Progress Reporting

**Each agent must report:**

1. **Start Confirmation**
   - Acknowledged task
   - Understood requirements
   - Starting work

2. **Blockers** (if encountered)
   - What's blocking
   - What was tried
   - Recommendation for resolution

3. **Completion Status**
   - What was accomplished
   - Files modified
   - Results summary

4. **Quality Verification**
   - Tests passing?
   - Requirements met?
   - Ready for review?

---

## Quality Gates

### Intern Self-Check

**Before reporting complete:**
- [ ] Requirements fulfilled?
- [ ] Code follows style guide?
- [ ] Tests written/updated?
- [ ] Documentation updated?
- [ ] No breaking changes?

**If any fail**: Fix or escalate, don't report complete.

### Engineer Review Checklist

**Technical Correctness**:
- [ ] Algorithm appropriate?
- [ ] Edge cases handled?
- [ ] Error handling robust?

**Performance**:
- [ ] Efficient implementation?
- [ ] No obvious bottlenecks?
- [ ] Scalable approach?

**Security**:
- [ ] Input validation?
- [ ] Authentication/authorization?
- [ ] No security vulnerabilities?

**Maintainability**:
- [ ] Clear, readable code?
- [ ] Well-documented?
- [ ] Follows patterns?

### Principal Strategic Review

**Architectural Alignment**:
- [ ] Fits system architecture?
- [ ] Follows established patterns?
- [ ] Maintains separation of concerns?

**Long-Term Implications**:
- [ ] Technical debt created?
- [ ] Future flexibility preserved?
- [ ] Migration path clear?

**Scalability**:
- [ ] Handles growth?
- [ ] Performance at scale?
- [ ] Resource usage reasonable?

**Strategic Fit**:
- [ ] Supports product direction?
- [ ] Enables future features?
- [ ] Reduces complexity?

---

## Decision Authority Matrix

| Decision Type | Intern | Engineer | Principal | Jean-Marc |
|--------------|--------|----------|-----------|-----------|
| Implementation details | ✅ Decides | Advises | - | Final |
| Technical approach | Recommends | ✅ Decides | Advises | **Final** |
| Architecture | - | Recommends | ✅ Decides | **✅ FINAL** |
| Product direction | - | - | Advises | **✅ DECIDES** |
| Technology stack | - | Recommends | ✅ Decides | **Final** |
| Code style | ✅ Follows | Enforces | - | Sets |
| Breaking changes | - | Recommends | ✅ Decides | **Final** |

**Legend**:
- ✅ = Primary authority (can be overridden by Jean-Marc)
- **✅** = Final authority (Jean-Marc only)
- Recommends = Provides analysis
- Advises = Provides input
- Final = Jean-Marc can override

---

## Anti-Patterns

### ❌ Don't: Invoke Without Context
```
Bad: "Fix the bug"
Good: "Fix authentication bug in auth.ts line 42: tokens expiring too quickly (1hr), extend to 24hrs..."
```

### ❌ Don't: Escalate Without Documentation
```
Bad: "This is hard, engineer help"
Good: "Attempted OAuth implementation, security complexity in token validation. Need expertise on refresh token rotation patterns..."
```

### ❌ Don't: Defer All Decisions to Higher Agent
```
Bad: Intern asks engineer about every small decision
Good: Intern implements following established patterns, escalates only when truly uncertain
```

### ❌ Don't: Violate Hierarchy
```
Bad: Intern directly asks Principal for help
Good: Intern → Engineer → Principal (proper escalation chain)
```

---

## Quick Reference

```bash
# HIERARCHY
Jean-Marc → Qara → Intern/Engineer/Principal

# AUTHORITY
Intern: Implementation
Engineer: Technical decisions
Principal: Architecture
Jean-Marc: FINAL on everything

# ESCALATION
Intern → Engineer (technical complexity)
Engineer → Principal (architectural implications)
Any Agent → Jean-Marc (decision needed)

# CONTEXT
Every agent: FULL context
No assumptions: Explicit is better
When escalating: Document attempts
```

---

## Related Documentation

- **delegation-guide.md** - When to delegate and task decomposition patterns
- **CONSTITUTION.md** - Foundational agent architecture principles
- **SKILL.md** - Quick delegation reference

---

**Remember**: Agents are functional roles with clear responsibilities and escalation paths. Focus on effective communication and appropriate delegation.
