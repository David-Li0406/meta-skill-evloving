# Research & Planning

Exploration, architecture decisions, spikes, and technical investigation.

## Mental Model

Research is about reducing uncertainty. You start with unknowns and end with a plan.

```
Unknown: "How should we implement real-time features?"
         ↓
Requirements: What exactly do we need? Latency? Scale? Complexity?
         ↓
Exploration: What exists? Libraries? Patterns? Similar implementations?
         ↓
Evaluation: Which options meet our requirements? Trade-offs?
         ↓
Recommendation: This is what we should do and why
         ↓
Plan: Here's how to implement it
```

## Key Principles

### Requirements First
Document what you need before exploring solutions.
- What problem are we solving?
- What constraints exist?
- What does success look like?
- Without requirements, you'll chase shiny objects.

### Assume It Exists
Whatever you're trying to build, someone has probably done it.
- Search for existing solutions first
- Find libraries, packages, patterns
- Learn from how others solved it
- Don't reinvent wheels

### Minimum Effort
The best solution uses existing tools and requires minimal code.
- Prefer mature libraries over custom code
- Prefer simple patterns over clever ones
- Prefer proven approaches over novel ones
- Less code = fewer bugs = easier maintenance

### Deep Exploration
Spend most of your time exploring, not deciding.
- Read documentation thoroughly
- Try things out
- Look at multiple options
- Understand trade-offs before choosing

### Document Everything
Your research is valuable beyond this project.
- Document what you found
- Document what you tried
- Document why you chose what you chose
- Document what you ruled out and why

## Agent Browser CLI Usage

Use browser for research exploration.

**Exploring documentation:**
```bash
agent-browser open https://docs.library.com
agent-browser click "[href='/api']"
agent-browser content > api-docs.txt
agent-browser screenshot api-overview.png
```

**Testing approaches:**
```bash
# Test a prototype or proof of concept
agent-browser open http://localhost:3000/prototype
agent-browser snapshot -i
# Interact and verify the approach works
agent-browser screenshot poc-result.png
```

## What to Extract from Users

- Clear statement of what we're trying to learn/decide
- Constraints (budget, time, team skills, existing systems)
- How the results will be used
- Success criteria for the research itself
- Specific questions that need answers
- Known options or starting points
- Timeline for making decisions

## Expected Deliverables

Research tasks should produce:

1. **Requirements Document**
   - What we need and why
   - Constraints and boundaries
   - Success criteria

2. **Research Findings**
   - What options exist
   - What we tried
   - Pros and cons of each option

3. **System Design** (if applicable)
   - Recommended architecture
   - Component breakdown
   - Integration points

4. **Implementation Plan**
   - How to build the recommendation
   - Phases and dependencies
   - Risk areas

## Red Flags

You're doing it wrong if:
- Jumping to solutions without exploring options
- Not documenting what you found
- Ignoring existing tools and libraries
- Over-engineering when simple solutions exist
- Analysis paralysis (researching forever without deciding)
- Recommending without understanding trade-offs

## Story Structure for Research

Typical research PRD structure:
1. Document requirements - what we need and constraints
2. Explore options - find and evaluate alternatives
3. Prototype/validate - test the leading option
4. Document findings - what we learned
5. Create recommendation - what we should do and why
6. Create implementation plan - how to do it
