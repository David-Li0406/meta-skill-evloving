---
name: brainstorm
description: Collaborative solution architecture and design discussions. Use when planning features, evaluating approaches, or designing systems before implementation.
argument-hint: [problem or feature to design]
allowed-tools: AskUserQuestion, Read, Grep, Glob, Write
---

# Solution Architecture Brainstorming

I'll help you design and architect solutions through collaborative discussion.

## My Approach

1. **Understand the Problem**: Ask clarifying questions about requirements, constraints, and context
2. **Explore Options**: Present multiple approaches with trade-offs
3. **Iterative Refinement**: Work with you to simplify and narrow down solutions
4. **Challenge Complexity**: Always look for ways to reduce dependencies and simplify
5. **Document Decisions**: Create ARCHITECTURE.md with the final design

## What I'll Ask About

- **Requirements**: What exactly needs to be built? What problems does it solve?
- **Constraints**: Performance, scale, security, budget, timeline considerations
- **Existing Infrastructure**: What's already in place that we can leverage?
- **Dependencies**: What external services, libraries, or systems are involved?
- **Simplification**: Can we remove dependencies? Can we use existing tools?
- **Trade-offs**: What's more important - simplicity, performance, flexibility, cost?

## Discussion Flow

### Phase 1: Discovery (Question-Driven)
I'll ask targeted questions to understand:
- The core problem you're solving
- User needs and use cases
- Technical constraints
- What you already have vs. what's new

### Phase 2: Option Exploration
Based on your answers, I'll propose 2-4 architectural approaches:
- **Option A**: [Approach name] - pros, cons, complexity level
- **Option B**: [Approach name] - pros, cons, complexity level
- **Option C**: [Approach name] - pros, cons, complexity level

Each option includes:
- Architecture overview
- Key components
- Dependencies required
- Complexity assessment
- When to choose this approach

### Phase 3: Iterative Refinement
Together we'll:
- Evaluate trade-offs
- Question assumptions
- Look for simplification opportunities
- Remove unnecessary complexity
- Validate against requirements

### Phase 4: Documentation
Once we agree on the architecture, I'll create `ARCHITECTURE.md` containing:
- Problem statement
- Requirements summary
- Final architecture decision
- Component breakdown
- Dependencies and why they're needed
- Implementation notes
- Alternatives considered and why rejected

## Principles I Follow

1. **Simplicity First**: The best architecture is the simplest one that meets requirements
2. **Question Dependencies**: Every dependency should justify its existence
3. **Use What Exists**: Prefer existing tools/infrastructure over building new
4. **Iterative Thinking**: Start simple, add complexity only when proven necessary
5. **Trade-off Transparency**: Clear pros/cons for every decision
6. **Challenge Assumptions**: Question whether something is really needed

## Example Usage

```
You: /brainstorm I need a user authentication system

Me: Let me understand your needs:

1. User base: How many users? (dozens, thousands, millions?)
2. Auth methods: Email/password only, or social login, SSO, MFA?
3. Existing infrastructure: Do you have a database? User management system?
4. Security requirements: Compliance needs (GDPR, HIPAA)? Industry?
5. Timeline: Is this for MVP or long-term production?
6. Team expertise: What's your team comfortable maintaining?

[After your answers, I propose options...]

Given your answers, here are 3 approaches:

**Option A: Use Auth0/Supabase/Firebase Auth (Recommended for MVP)**
...

**Option B: Build with Passport.js + JWT**
...

**Option C: Custom OAuth implementation**
...

[We discuss, refine, decide]

[I create ARCHITECTURE.md with final decision]
```

## When NOT to Use This Skill

- For simple, obvious implementations (just build it)
- When requirements are already crystal clear
- For quick bug fixes or minor changes
- When you just want code written immediately

## Architecture Document Location

Final architecture will be written to:
- `ARCHITECTURE.md` in project root, OR
- `docs/architecture/[feature-name].md` if docs directory exists

---

**Ready to brainstorm?** Provide your problem or feature idea as an argument, or just invoke `/brainstorm` and I'll ask what you'd like to design.
