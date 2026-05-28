# Waste Analysis Framework for Conversation Logs

## Core Principle

**User conversation time is waste.** Every message the user sends, every character they type, every clarification they provide - that's time they can't spend doing something else.

Agent execution time is irrelevant to the user. An agent that runs for 5 minutes and one that runs for 15 minutes cost the user the same amount of conversation time (approximately zero).

**Goal**: Identify patterns where users repeatedly spend conversation time on things that could be eliminated by creating a skill.

## The Six Waste Patterns

### 1. Repetition Waste

**Definition**: User provides the same instructions, context, or preferences across multiple conversations.

**What to look for**:

- Instructions that appear verbatim or near-verbatim in multiple conversations
- Preferences stated repeatedly ("always", "every time", "remember to")
- Context re-provided ("as I mentioned before", "like last time")
- Standards or conventions re-stated ("use our format", "follow the pattern")

**Examples**:

- "Remember to exclude test accounts where email contains '@test.com'"
- "Use the staging environment for all deployments"
- "Follow our commit message format: type(scope): description"
- "Always run tests before committing"
- "Don't use emojis in commit messages"

**Skill opportunity**: Encode the repeated instruction as a persistent standard or preference.

**Detection strategy**: Look for instructions that appear across multiple conversation timestamps. High-value targets have exact or near-exact repetition.

### 2. Clarification Waste

**Definition**: User spends multiple messages refining, rephrasing, or explaining what should have been clear from their first message.

**What to look for**:

- Progressive refinement over multiple messages
- Explicit rephrasing ("let me rephrase", "what I meant was")
- Corrections of misunderstanding ("no, not X, I need Y")
- Additional constraints added after initial request
- Follow-up questions the user has to answer

**Examples**:

- Message 1: "Update the config"
- Message 2: "No, the production config, not staging"
- Message 3: "The database config specifically"

Or:

- "Let me rephrase that..."
- "What I'm trying to say is..."
- "To be more specific..."
- "Actually, I need X instead"

**Skill opportunity**: Create clearer patterns, templates, or decision trees that reduce ambiguity.

**Detection strategy**: Look for clusters of messages from the user in short time spans. Count how many messages the user sends before the agent proceeds with work.

### 3. Correction Waste

**Definition**: User spends time identifying and correcting agent errors, bugs, or misunderstandings.

**What to look for**:

- Error reports or bug descriptions
- Explicit corrections ("that's not right", "wrong", "incorrect")
- Requests to fix or try again
- Identification of missed requirements
- Pointing out mistakes

**Examples**:

- "That code doesn't work"
- "You forgot to handle the error case"
- "The test is still failing"
- "That's not what I asked for"
- "You skipped step 3"
- "Try again"
- Pasted error messages followed by "fix this"

**Skill opportunity**: Add validation requirements, testing protocols, or quality checks that prevent the error class.

**Detection strategy**: Look for negative feedback, error reports, or requests to retry/fix. Also look for patterns where the same type of error appears across multiple conversations (systemic issues).

### 4. Procedural Waste

**Definition**: User provides detailed step-by-step instructions for tasks that should be routine or automated.

**What to look for**:

- Multi-step workflows written out explicitly
- Ordered lists of steps ("first X, then Y, then Z")
- Conditional logic specified manually ("if A then B, else C")
- Validation steps enumerated
- Detailed process descriptions

**Examples**:

- "First analyze the form, then create the mapping, then validate it, then fill the form"
- "Run the tests, if they pass then commit, if they fail then fix them"
- "Check the staging deployment, verify the endpoints work, then promote to production"
- "Create a branch, make the changes, run the linter, run tests, commit, push, create PR"

**Skill opportunity**: Encode the procedure as a workflow or automated sequence.

**Detection strategy**: Look for numbered lists, sequential instructions ("first", "then", "next", "finally"), and conditional logic. High-value targets appear across multiple conversations.

### 5. Context Teaching Waste

**Definition**: User explains domain-specific knowledge, terminology, or system architecture that the agent should already know.

**What to look for**:

- Definitions of domain terms
- Explanations of system architecture
- Project-specific conventions
- Business logic descriptions
- Acronym explanations

**Examples**:

- "In our system, 'verified' means the user has confirmed their email AND completed onboarding"
- "MRR is Monthly Recurring Revenue - sum of all active subscriptions"
- "The staging environment is at staging.example.com, production is at app.example.com"
- "We use 'customer' for paid users and 'user' for trial accounts"
- "A 'deployment' means pushing to staging first, then production after validation"

**Skill opportunity**: Create domain-specific reference material that pre-loads this knowledge.

**Detection strategy**: Look for definitions ("X means Y", "X is defined as"), explanations of project-specific terms, and architectural descriptions. Especially valuable when the same concepts are explained repeatedly.

### 6. Scope Constraint Waste

**Definition**: User spends time reining in agent over-engineering or unnecessary work.

**What to look for**:

- Requests to simplify
- Explicit scope reduction
- Stopping unnecessary work
- Removing features or steps
- Constraining complexity

**Examples**:

- "You don't need to add error handling for that"
- "Keep it simple, don't over-engineer"
- "Just do X, skip Y and Z"
- "That's too complex"
- "No need for abstraction here"
- "Don't add features I didn't ask for"
- "This is too much"

**Skill opportunity**: Establish clear defaults about appropriate scope, when to add abstractions, and when simplicity is preferred.

**Detection strategy**: Look for negative instructions (what NOT to do), simplification requests, and pushback on agent suggestions. Patterns here reveal where agents systematically over-deliver.

## What This Framework Doesn't Capture

- Agent execution time (irrelevant to user)
- Agent efficiency or elegance (user doesn't care)
- Waiting time (when not spent conversing)
- Internal agent processes (invisible to user)

Focus exclusively on user conversation time spent.
