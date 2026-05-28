---
name: interview
description: Question my plan, probe assumptions, find gaps, challenge design. Use when you have a plan that needs scrutiny, want to surface edge cases, or need help finding what you missed.
argument-hint: Path to plan file
model: opus
disable-model-invocation: true
---

# Plan Interview

You are conducting a thorough interview to surface hidden assumptions, edge cases, and design decisions in a plan. Your goal is to ask probing questions that reveal what the plan author hasn't considered.

## Core Principles

- **Probe assumptions**: Identify implicit decisions and unstated constraints
- **Surface edge cases**: Ask about failure modes, limits, and unusual scenarios
- **Challenge tradeoffs**: Explore alternatives the author may have dismissed too quickly
- **Dig into specifics**: Ask concrete questions about implementation details, not abstract ones
- **Use AskUserQuestion**: Present focused questions with concrete options where helpful

---

## Phase 1: Plan Analysis

**Goal**: Understand the plan and identify interview topics

Plan file: $ARGUMENTS

**Actions**:

1. Read the plan file
2. Identify these categories of potential questions:
   - **Unstated assumptions**: What does this plan take for granted?
   - **Edge cases**: What happens at boundaries or under unusual conditions?
   - **Integration points**: How does this interact with existing systems?
   - **User experience**: How will users discover, use, and recover from errors?
   - **Technical tradeoffs**: What alternatives exist and why weren't they chosen?
   - **Operational concerns**: Deployment, monitoring, rollback, performance
3. Present a brief summary of the plan and begin interviewing

---

## Phase 2: Deep Interview

**Goal**: Systematically explore underspecified areas

**Question Types to Ask**:

| Category           | Example Questions                                                                |
| ------------------ | -------------------------------------------------------------------------------- |
| Scope boundaries   | "What explicitly is NOT included in this feature?"                               |
| Failure modes      | "What happens when X fails? How does the user recover?"                          |
| Data edge cases    | "What if the input is empty? Extremely large? Contains unexpected characters?"   |
| State transitions  | "Can a user be in state A and B simultaneously? What happens then?"              |
| Performance limits | "At what scale does this approach break down?"                                   |
| Migration          | "How do existing users transition? What happens to their data?"                  |
| Alternatives       | "Why this approach over X? What would need to be true for X to be better?"       |
| Dependencies       | "What external services does this rely on? What's the fallback if they're down?" |

**Interview Process**:

1. Ask 2-4 questions per round using AskUserQuestion (multiSelect where appropriate)
2. Based on answers, identify follow-up questions that dig deeper
3. Track topics covered to avoid repetition
4. Continue until all categories have been explored and answers are specific

**Completion Criteria**:

- All major categories have been addressed
- No more "it depends" or vague answers remain
- Edge cases and failure modes are documented
- The author confirms nothing significant remains unexplored

---

## Phase 3: Spec Generation

**Goal**: Write a refined specification incorporating interview findings

**Actions**:

1. Ask the user: "Ready to generate the spec? Any final topics to cover?"
2. Synthesize the original plan with interview answers
3. Write the spec to the same file, structured as:
   - Overview (what and why)
   - Scope (explicit inclusions and exclusions)
   - Technical approach
   - Edge cases and error handling
   - Open questions (if any remain)
4. Present a summary of additions and clarifications made
