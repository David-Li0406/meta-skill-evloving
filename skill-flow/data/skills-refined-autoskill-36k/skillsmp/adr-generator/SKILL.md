---
name: adr-generator
description: Guide users through creating Architecture Decision Records (ADRs) by systematically gathering all required information and formatting it into a complete, high-quality ADR document. Use when users want to (1) Document an architectural decision, (2) Create an ADR, (3) Record design choices, (4) Formalize architecture discussions, or (5) Need help structuring architectural documentation.
---

# ADR Generator

## Overview

Guide users through creating complete Architecture Decision Records (ADRs) by systematically collecting all necessary information and formatting it according to the standard ADR template.

## Workflow

Creating an ADR involves these steps:

1. Understand the architectural decision being documented
2. Gather context and problem statement
3. Identify decision drivers
4. List all considered options
5. Determine the chosen option and justification
6. Document consequences
7. Collect pros and cons for each option
8. Add optional metadata and additional information
9. Format the complete ADR

Follow each step sequentially, using questions to gather complete information from the user.

## Step 1: Understand the Decision

Start by understanding what architectural decision needs to be documented. Ask:

- What architectural decision are you documenting?
- What problem does this decision address?
- What is the scope of this decision?

Ensure clarity on the decision before proceeding.

## Step 2: Gather Context and Problem Statement

Collect detailed context about the decision. Ask targeted questions:

- What is the current situation or context?
- What problem are you trying to solve?
- Why is this decision necessary now?
- Are there any relevant background details?
- Can you describe this in 2-3 sentences or as a story?

The context should clearly explain why this decision is needed.

## Step 3: Identify Decision Drivers

Decision drivers are forces or concerns that influence the decision. Ask:

- What factors are driving this decision?
- What requirements or constraints must be considered?
- What quality attributes matter (performance, security, maintainability, etc.)?
- What are the key concerns or forces at play?

Common decision drivers include:
- Performance requirements
- Security constraints
- Cost considerations
- Team expertise
- Time constraints
- Scalability needs
- Maintainability
- Regulatory compliance

## Step 4: List Considered Options

Gather all alternatives that were evaluated. For each option, ask:

- What options did you consider?
- What is the title/name of this option?
- Can you briefly describe each option?

Ensure at least 2-3 options are documented. If the user only mentions one option, ask what alternatives were considered.

## Step 5: Determine Decision Outcome

Identify the chosen option and its justification. Ask:

- Which option did you choose?
- Why did you choose this option?
- What made this option better than the alternatives?
- Does this option meet specific criteria that others don't?

The justification should clearly connect the chosen option to the decision drivers.

## Step 6: Document Consequences

Every decision has trade-offs. For the chosen option, ask:

- What are the positive consequences of this decision?
- What are the negative consequences or trade-offs?
- What improvements do you expect?
- What challenges or compromises does this introduce?

Document both good and bad consequences honestly.

## Step 7: Collect Pros and Cons for Each Option

For thorough documentation, gather pros and cons for each considered option. For each option, ask:

- What are the advantages of this option?
- What are the disadvantages?
- Are there any neutral aspects worth noting?

Use "Good, because...", "Bad, because...", and "Neutral, because..." format.

This step can be marked as optional if the user prefers a lighter ADR.

## Step 8: Add Optional Metadata

Collect optional but valuable metadata. Ask if they want to include:

- **Status**: Is this proposed, accepted, rejected, or deprecated?
- **Date**: When was this decision made or last updated? (Use today's date: 2026-01-14 if current)
- **Decision-makers**: Who made this decision?
- **Consulted**: Who was consulted for expert input?
- **Informed**: Who should be kept informed?
- **Confirmation**: How will implementation compliance be validated?
- **More Information**: Any additional context, links, or future considerations?

Not all metadata is required. Use what makes sense for the decision.

## Step 9: Format the ADR

Once all information is gathered, format it using the standard ADR template from `references/adr-template.md`.

Create a complete, well-formatted ADR document with:
- YAML frontmatter (if metadata provided)
- Descriptive title
- All required sections filled
- Optional sections included as appropriate
- Proper markdown formatting

Review the completed ADR with the user to ensure accuracy and completeness.

## Tips for Quality ADRs

- **Be specific**: Vague statements reduce value. Use concrete details.
- **Be honest**: Document real trade-offs, not idealized outcomes.
- **Be concise**: Clear and brief is better than verbose.
- **Focus on "why"**: Explain reasoning, not just what was chosen.
- **Link to context**: Reference relevant documents, issues, or discussions.
- **Consider the future**: Future readers should understand the decision without additional context.

## Resources

### references/
- **adr-template.md**: Complete ADR template format with field explanations
