---
name: interview
description: Conduct an in-depth interview about a feature, spec, or idea to surface non-obvious concerns, edge cases, and tradeoffs. Use when user wants to think through a feature, refine requirements, or explore implementation details.
version: 1.0.0
author: Your Team
tags: [development, workflow, requirements, specification, design]
---

# Interview Skill

## Purpose

This skill conducts a thorough interview to surface non-obvious concerns, edge cases, and tradeoffs for any feature, spec, or idea. It helps refine requirements before implementation by systematically exploring technical, operational, and design considerations.

## When to Use

- Before creating a new issue spec for a milestone
- When refining an existing issue spec that needs clarification
- When exploring a new feature idea or concept
- When requirements are ambiguous or incomplete
- When you need to think through implementation details and tradeoffs

## Core Workflow

The skill follows this execution pattern:

1. **Determine Input** - Identify what to interview about (file, topic, or prompt)
2. **Interview Systematically** - Probe all relevant areas using structured questions
3. **Deep Dive** - Explore areas where complexity is revealed
4. **Synthesize** - Summarize findings and decisions
5. **Output** - Write refined spec or provide summary

## Input

The skill accepts various input formats:

- **File path:** `docs/03-build-notes/milestones/m{n}/01-{short-name}.md` - Interview about an existing issue spec
- **Topic string:** `"user authentication flow"` - Interview about a concept or feature
- **No argument:** Prompt user for what they want to discuss

### Path Conventions

If working with issue specs:
- **Issue spec files:** `docs/03-build-notes/milestones/<milestone>/*.md`
- **Implementation plans:** `docs/03-build-notes/milestones/<milestone>/IMPLEMENTATION_PLAN.md`
- **Epic files:** `docs/03-build-notes/milestones/<milestone>/00-epic.md`

## Required Context Files

When interviewing about issue specs, always load:
- `docs/guides/implementation-workflow.md` - For understanding workflow conventions
- `docs/guides/dev-cadence.md` - For understanding milestone structure
- Related issue spec files if interviewing about a specific milestone

## Interview Areas

Use AskUserQuestion to systematically probe these areas:

### 1. Technical Implementation
- Architecture and design patterns
- Data models and schemas
- API design and contracts
- State management
- Integration points and dependencies
- Technology choices and tradeoffs

### 2. UI/UX Considerations
- User flows and interactions
- Error states and handling
- Loading states and feedback
- Accessibility requirements
- Edge cases in user experience
- Mobile/responsive considerations

### 3. Operational Concerns
- Monitoring and observability
- Debugging and troubleshooting
- Rollback and recovery procedures
- Logging and audit trails
- Alerting and incident response
- Deployment and release strategy

### 4. Security and Privacy
- Authentication and authorization
- Data protection and encryption
- Input validation and sanitization
- Rate limiting and abuse prevention
- Privacy implications and compliance
- Threat modeling

### 5. Performance and Scalability
- Performance targets and SLAs
- Scalability requirements
- Caching strategies
- Database query optimization
- Resource constraints
- Load testing considerations

### 6. Maintainability and Extensibility
- Code organization and structure
- Testing strategy and coverage
- Documentation requirements
- Future extensibility needs
- Backward compatibility
- Deprecation strategy

## Question Guidelines

Follow these principles when asking questions:

- **Avoid obvious questions** - Don't ask surface-level questions that are already clear
- **Focus on tradeoffs** - Ask "why this over alternatives" not just "what"
- **Probe failure modes** - Ask "what happens when X fails/is missing/is invalid"
- **Challenge assumptions** - Question decisions that seem arbitrary or unstated
- **Use open-ended questions** - Prefer questions that require explanation over yes/no
- **Go deeper** - Follow up on answers that reveal complexity or uncertainty
- **Be systematic** - Cover all relevant areas, not just the obvious ones

## Execution Steps

### 1. Determine Input

1. **If file path provided:**
   - Read the spec file first
   - Understand current state, acceptance criteria, and implementation notes
   - Use as starting context for interview

2. **If topic/prompt provided:**
   - Use the topic as starting context
   - Begin with clarifying questions about scope and goals

3. **If no argument:**
   - Ask user: "What feature, spec, or idea would you like to discuss?"

### 2. Interview Systematically

1. **Start with high-level context:**
   - What problem are we solving?
   - Who are the users/stakeholders?
   - What are the success criteria?

2. **Probe each area systematically:**
   - Technical Implementation
   - UI/UX Considerations
   - Operational Concerns
   - Security and Privacy
   - Performance and Scalability
   - Maintainability and Extensibility

3. **Use AskUserQuestion for each probe:**
   - One question at a time
   - Wait for response before moving to next area
   - Follow up on interesting or unclear answers

### 3. Deep Dive

- When answers reveal complexity, go deeper in that area
- Ask follow-up questions to clarify edge cases
- Explore alternative approaches and their tradeoffs
- Identify dependencies and integration points

### 4. Synthesize Findings

After all areas are explored:
- Summarize key decisions and clarifications
- List identified edge cases and failure modes
- Document tradeoffs and chosen approaches
- Note any remaining open questions or risks

### 5. Output

1. **If original file was provided:**
   - Offer to write refined spec back to that file
   - Update with clarifications, decisions, and new acceptance criteria
   - Preserve existing structure and format

2. **If no file provided:**
   - Offer to create a new issue spec file
   - Suggest location: `docs/03-build-notes/milestones/<milestone>/<nn>-<short-name>.md`
   - Or provide summary of findings

3. **Format output:**
   - Follow issue spec format
   - Include YAML frontmatter with title and labels
   - Structure with: Done Definition, Implementation Notes, Test Expectations, Acceptance Criteria

## Examples

### Example 1: Interviewing About Existing Issue Spec

**Input:**
```
/interview docs/03-build-notes/milestones/m1/01-user-auth.md
```

**Process:**
1. Read the issue spec file
2. Understand current requirements
3. Interview about technical implementation (database schema, relationships)
4. Interview about operational concerns (migrations, rollback)
5. Interview about security (data isolation, access patterns)
6. Synthesize findings
7. Offer to update the spec file with clarifications

### Example 2: Interviewing About New Feature

**Input:**
```
/interview "user session management"
```

**Process:**
1. Start with clarifying scope and goals
2. Interview about technical implementation (data model, computation strategy)
3. Interview about operational concerns (monitoring, alerting)
4. Interview about performance (computation cost, caching)
5. Synthesize findings
6. Offer to create new issue spec file

## Limitations

- Requires user to be available for questions (not fully automated)
- Cannot make implementation decisions - only surfaces concerns and tradeoffs
- Depends on user's knowledge and availability to answer questions
- May take significant time for complex features

## Error Handling

- **Missing file:** Report error and ask if user wants to create new spec
- **Invalid path:** Suggest correct path format based on milestone structure
- **Ambiguous topic:** Ask clarifying questions to narrow scope
- **User unavailable:** Summarize findings so far and save for later

## Notes

- This skill is interactive and requires user participation
- Questions should be thoughtful and avoid obvious or surface-level topics
- Focus on surfacing non-obvious concerns, edge cases, and tradeoffs
- The goal is to refine requirements before implementation begins
- Output should be actionable and ready for use in issue specs

## See Also

- [Implementation Workflow](../../../docs/guides/implementation-workflow.md) - Daily workflow guide
- [Development Cadence](../../../docs/guides/dev-cadence.md) - High-level milestone process
