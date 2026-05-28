---
name: replit-claude-code-prompting
description: Transforms vague coding requests into optimized Claude Code prompts for Replit projects. Use when helping users craft better prompts for Claude Code, improving agentic coding workflows, structuring coding tasks for AI agents, or when users struggle to get good results from Claude Code in Replit environments. Covers prompt specificity, test-driven workflows, visual iteration, and multi-step task decomposition.
---

# Replit Claude Code Prompting Skill

Transform vague coding requests into effective Claude Code prompts optimized for Replit environments.

## Core Principle: Specificity Drives Success

Claude Code's success rate improves dramatically with specific instructions. Vague prompts lead to misaligned implementations and wasted iterations.

**Transform vague → specific:**

| Vague (Poor) | Specific (Good) |
|--------------|-----------------|
| "add user auth" | "Add email/password authentication using Passport.js with bcrypt for password hashing. Create login/register routes, session middleware, and protect the /dashboard route. Store users in the existing PostgreSQL database." |
| "fix the bug" | "The form submission on /contact throws a 500 error when the email field is empty. Add server-side validation for required fields and return a 400 with specific error messages." |
| "make it look better" | "Update the landing page to match this design: [image]. Use the existing Tailwind classes. The hero should be full-viewport height with the gradient background from our design system." |
| "add tests" | "Write integration tests for the user registration flow covering: successful registration, duplicate email rejection, weak password rejection, and missing required fields. Use Jest with Supertest." |

## Prompt Transformation Workflow

When improving a prompt, follow this sequence:

1. **Identify the task type** → Select appropriate workflow pattern
2. **Extract implicit requirements** → Make hidden assumptions explicit
3. **Add verification criteria** → Define what "done" looks like
4. **Include Replit-specific context** → Reference environment constraints

## Workflow Patterns for Different Task Types

### Pattern 1: Explore → Plan → Code → Commit

Use for: Complex features, architectural changes, unfamiliar codebases.

**Prompt template:**
```
Phase 1 - Research (don't write code yet):
- Read [specific files/folders] to understand the current implementation
- Identify how [related feature] is implemented as a pattern to follow
- Note any constraints or dependencies

Phase 2 - Plan (think hard about this):
- Create a detailed implementation plan
- List files that need to be created or modified
- Identify potential issues or edge cases
- Present the plan for review before proceeding

Phase 3 - Implement:
- Follow the approved plan
- [Specific implementation instructions]
- Run tests/linting after each major change

Phase 4 - Verify and commit:
- Verify [specific success criteria]
- Commit with message describing the change
```

**Example transformation:**

*User's vague prompt:* "Add a payment system"

*Improved prompt:*
```
Phase 1 - Research (don't write code yet):
- Read the existing user model and authentication flow
- Check how we're handling sensitive data elsewhere in the codebase
- Review the current database schema

Phase 2 - Plan (think hard about this):
- Design the Stripe integration architecture
- Plan the checkout flow: cart → payment intent → confirmation
- Identify required environment variables
- Present your plan before writing any code

Phase 3 - Implement:
- Install Stripe SDK
- Create payment routes: POST /api/create-payment-intent, POST /api/webhook
- Add checkout UI component with Stripe Elements
- Handle success/failure states with appropriate user feedback

Phase 4 - Verify:
- Test with Stripe test keys
- Verify webhook signature validation works
- Confirm error states display correctly
- Commit with descriptive message
```

### Pattern 2: Test-Driven Development

Use for: Features with clear inputs/outputs, bug fixes, refactoring.

**Prompt template:**
```
Step 1 - Write tests first (don't write implementation yet):
- Create tests for [feature] covering:
  - [Happy path scenario]
  - [Edge case 1]
  - [Edge case 2]
  - [Error handling scenario]
- Use [testing framework] with the existing test patterns
- Confirm tests fail as expected

Step 2 - Implement to pass tests:
- Write the minimum code to pass all tests
- Don't modify the tests
- Keep iterating until all tests pass

Step 3 - Refactor and commit:
- Clean up the implementation
- Ensure tests still pass
- Commit tests and implementation together
```

**Example transformation:**

*User's vague prompt:* "Add email validation"

*Improved prompt:*
```
Step 1 - Write tests first (don't write implementation):
Create tests in tests/validators.test.js for email validation:
- Valid standard emails (user@domain.com) → returns true
- Valid with subdomains (user@sub.domain.com) → returns true
- Missing @ symbol → returns false with "Invalid email format"
- Missing domain → returns false with "Invalid email format"
- Invalid TLD (user@domain) → returns false
- Empty string → returns false with "Email required"
- Whitespace handling (trim before validation)

Run tests to confirm they fail.

Step 2 - Implement:
Create src/utils/validators.js with validateEmail function
Keep iterating until all tests pass
Don't modify the tests

Step 3 - Integrate:
Add validation to the registration form
Display error messages inline
Commit everything together
```

### Pattern 3: Visual Iteration

Use for: UI work, design implementation, styling fixes.

**Prompt template:**
```
Target: [Describe visual goal or attach reference image]

Implementation approach:
- Use [existing component/style system] as foundation
- Match [specific visual elements]: colors, spacing, typography
- Ensure responsive behavior: [breakpoint requirements]

Iteration loop:
1. Implement initial version
2. Take a screenshot and compare to target
3. Identify differences and fix them
4. Repeat until matching

Success criteria:
- [Specific visual requirements]
- [Responsive requirements]
- [Interaction states]
```

**Example transformation:**

*User's vague prompt:* "Make the dashboard look more modern"

*Improved prompt:*
```
Target: Update dashboard to match Linear's design aesthetic
Reference: Clean, minimal, lots of whitespace, subtle borders, Inter font

Implementation approach:
- Use existing Tailwind setup
- Replace card borders with subtle shadows
- Increase padding and whitespace by 50%
- Update font to Inter (already in project)
- Use gray-50 backgrounds instead of white for sections

Iteration loop:
1. Update the main dashboard container and card components
2. Screenshot the result
3. Compare spacing and visual weight to Linear's UI
4. Adjust until it feels clean and uncluttered

Success criteria:
- Cards have subtle shadow instead of borders
- Minimum 24px padding inside cards
- Clear visual hierarchy with typography
- Works on mobile (stack cards vertically)
```

### Pattern 4: Codebase Q&A → Implementation

Use for: Unfamiliar codebases, understanding before changing.

**Prompt template:**
```
First, answer these questions (don't write code yet):
1. How does [existing feature] work?
2. What patterns does this codebase use for [relevant pattern]?
3. Where should [new code] live based on existing structure?
4. What existing utilities can be reused?

Then implement [feature]:
- Follow the patterns you identified
- Reuse existing utilities where possible
- Match the code style of surrounding files
```

## Replit-Specific Prompt Enhancements

Add these elements when the target is a Replit environment:

### Environment Context
```
Environment: Replit with [Node.js/Python/etc]
- Use Replit's environment variables (Secrets tab) for sensitive data
- The app runs on port 3000 with Replit's built-in hosting
- Use Replit's packager for dependencies (no need for npm install commands)
```

### Database Context
```
Database: [Replit DB / PostgreSQL / etc]
- Connection string is in REPLIT_DB_URL or DATABASE_URL secret
- Use connection pooling for PostgreSQL
- Replit DB is key-value, use for simple persistence
```

### File Structure Awareness
```
Check the existing structure before creating files:
- Follow the existing folder organization
- Match naming conventions in use
- Don't duplicate functionality that exists
```

## Prompt Enhancement Checklist

Before finalizing any improved prompt, verify:

- [ ] **Specific files/folders** mentioned (not "the code" or "the files")
- [ ] **Technology choices** explicit (frameworks, libraries, approaches)
- [ ] **Success criteria** defined (how to know it's done)
- [ ] **Verification steps** included (tests, visual checks, manual testing)
- [ ] **Commit instructions** at the end
- [ ] **Research phase** for complex tasks (read before write)
- [ ] **"Think" trigger** for planning steps ("think hard about the architecture")

## Thinking Budget Keywords

Use these words to trigger extended thinking for complex decisions:

- "think" → Standard extended thinking
- "think hard" → More computation time
- "think harder" → Even more thinking budget
- "ultrathink" → Maximum thinking allocation

**Example:** "Think hard about the database schema before implementing. Consider future scalability and query patterns."

## Anti-Patterns to Avoid

Transform these common mistakes:

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "Make it work" | No success criteria | Add specific verification steps |
| "Do it the right way" | Subjective | Specify the pattern or approach |
| "Add all the features" | Scope creep | List specific features with priority |
| "Fix everything" | Unbounded task | List specific issues to address |
| "Make it production-ready" | Vague standard | Define specific requirements (error handling, logging, etc.) |

## Quick Reference: Prompt Starters

**For new features:**
"Implement [feature] following the existing [pattern] in [reference file]. Include [specific requirements]. Verify by [test/check]. Commit when done."

**For bug fixes:**
"The bug: [specific symptom]. Expected: [correct behavior]. Check [likely locations]. Fix without breaking [related functionality]. Add a test to prevent regression."

**For refactoring:**
"Refactor [target] to [improvement]. Keep the same external behavior. Run existing tests after each change. Don't change [protected areas]."

**For exploration:**
"Explain how [feature] works in this codebase. Read the relevant files and trace the flow from [entry point] to [end point]. Don't make any changes yet."
