# Category Selection Overview

Different task types require different approaches. Select the category that best matches the work.

## The Categories

| Category | When to Use |
|----------|-------------|
| **Feature Development** | New features, enhancements, integrations |
| **Bug Fixing** | Investigating and fixing bugs, regressions |
| **Research & Planning** | Exploration, architecture decisions, spikes |
| **Quality Assurance** | Testing, code review, security audits |
| **Maintenance** | Documentation, cleanup, refactoring, optimization |
| **DevOps** | Deployment, CI/CD, infrastructure changes |
| **General** | Anything that doesn't fit above |

## How to Select

Use AskUserQuestion with the categories above. Let the user choose.

Sometimes the category is obvious from their request. Sometimes it's ambiguous. When ambiguous, ask.

## Why Categories Matter

Each category has:
- A different mental model for approaching the work
- Different priorities for what matters most
- Different verification approaches
- Different risk profiles

Following category-specific guidance helps ensure you:
- Ask the right questions during interview
- Structure the PRD appropriately
- Include appropriate verification
- Avoid common pitfalls for that type of work

## Category Selection Guidelines

### Clear Cases

- "Add a button that..." → Feature Development
- "Fix the bug where..." → Bug Fixing
- "Figure out how we should..." → Research & Planning
- "Test the..." or "Review the..." → Quality Assurance
- "Clean up..." or "Refactor..." → Maintenance
- "Deploy..." or "Set up CI..." → DevOps

### Ambiguous Cases

Some tasks span categories:

- "Improve performance" → Could be QA (find issues) or Maintenance (refactor)
- "Update the API" → Could be Feature (new endpoint) or Maintenance (refactor)
- "Handle edge cases" → Could be Bug Fixing or Feature Development

When ambiguous:
1. Ask the user which category feels right
2. Or ask about their primary goal to determine the right frame
3. You can combine approaches if needed

## Reading Category Guidance

Each category file contains:
- Mental model (how to think about this work)
- Key principles (what matters most)
- Workflow philosophy (not rigid phases)
- Agent Browser CLI usage
- Red flags (what indicates wrong approach)

These are thinking frameworks, not scripts. Apply them intelligently.
