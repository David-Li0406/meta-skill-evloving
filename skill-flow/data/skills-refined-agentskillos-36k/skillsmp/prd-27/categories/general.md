# General

For tasks that don't fit neatly into other categories.

## Mental Model

When a task doesn't fit standard categories, fall back to fundamentals.

```
Request: Task that doesn't fit other categories
         ↓
Understand: What are we actually trying to accomplish?
         ↓
Break Down: What are the logical pieces?
         ↓
Implement: Work through pieces, verifying as you go
         ↓
Document: Record what was done
```

## Key Principles

### Understand Before Implementing
Don't start work until you understand the goal.
- What is the actual outcome needed?
- Why does this matter?
- What does success look like?
- What constraints exist?

### Break Into Verifiable Chunks
Complex work should be decomposed.
- Each piece should be independently completable
- Each piece should be independently verifiable
- Order pieces logically by dependencies
- Don't create pieces that are too small or too large

### Verify As You Go
Don't batch all verification at the end.
- Check each piece works before moving on
- Catch problems early
- Build confidence incrementally

### Document What You Did
Enable future understanding.
- What was done and why?
- What decisions were made?
- What issues were encountered?
- What follow-up is needed?

## Adapting to the Task

Since general tasks vary widely, adapt your approach:

### More Like Feature Development
- Has clear specification of what to build
- Has visual/interactive components
- Emphasize specification and browser verification

### More Like Research
- Needs exploration before implementation
- Has significant uncertainty
- Emphasize discovery and documentation

### More Like Maintenance
- Involves existing code changes
- Needs to preserve behavior
- Emphasize understanding current state and verification

### More Like Bug Fixing
- Has specific problem to solve
- Has expected vs. actual behavior gap
- Emphasize reproduction and verification

## Agent Browser CLI Usage

Apply browser verification when relevant.

**If there's any UI component:**
```bash
agent-browser open http://localhost:3000/relevant-page
agent-browser snapshot -i
# Test relevant interactions
agent-browser screenshot verification.png
agent-browser close
```

**For documentation of web resources:**
```bash
agent-browser open https://relevant-docs.com
agent-browser content > reference.txt
```

## What to Extract from Users

Since tasks vary, extract what's relevant:
- Clear goal/outcome expected
- Context and background
- Constraints and requirements
- What success looks like
- What should NOT be done
- Relevant files, systems, or resources
- Timeline and priority

## Story Structure for General Tasks

Adapt based on the task, but typical structure:
1. Context gathering - understand current state and requirements
2. Core work - implement the main task
3. Verification - confirm it works as expected
4. Documentation - record what was done

## When to Use Another Category

If during interview you realize the task fits another category better:
- Mention it to the user
- Ask if they want to switch approach
- Apply the more specific category guidance

Categories exist to provide focused guidance. If general isn't giving you enough direction, consider whether another category applies.
