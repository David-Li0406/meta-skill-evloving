---
name: synthesizing-requirements
description: Analyzes unstructured documents, conversations, and notes to generate structured markdown documentation containing user stories, system requirements, and feature specifications. Use this skill when you need to: (1) Process conversation transcripts from meetings, chat logs, or Slack threads about system requirements, (2) Extract structured requirements from PDFs, Word docs, or other unstructured requirement documents, (3) Synthesize technical notes and architecture brainstorming into formal specifications, (4) Transform informal user stories and feature requests into properly formatted documentation, (5) Generate comprehensive markdown documentation ready for the interviewing-stakeholders skill to further refine, or (6) Create a baseline requirements document from any combination of unstructured inputs about a system to be built.
---

# Synthesizing Requirements

## Overview

This skill transforms unstructured product intent into structured, actionable documentation. It's the first step in the Pact workflow, designed to extract meaning from messy inputs and create a foundation for test-driven development.

**Primary Goal**: Convert raw conversations, documents, and notes into clear user stories, system requirements, and feature specifications that can be further refined through stakeholder interviews.

---

## When to Use This Skill

Use `synthesizing-requirements` when you have:

- Conversation transcripts (Slack threads, meeting notes, Teams chats) discussing features
- Requirement documents (PDFs, Word docs, Google Docs) that need structuring
- Technical brainstorming notes that need to be formalized
- Informal user stories or feature requests scattered across multiple sources
- A mix of different document types that all relate to the same system

**This skill works best when**: You have raw material to work with but need to extract the core intent and organize it systematically.

---

## Step-by-Step Workflow

### Step 1: Gather Input Documents

First, collect all unstructured documents and artifacts:

1. **Identify the source materials** - Ask the user to provide:
   - File paths to documents
   - Conversation transcripts (as text files or pasted content)
   - Links to Google Docs, Confluence pages, etc.
   - Any other relevant materials

2. **Read all provided materials** - Use the Read tool or WebFetch tool to access:
   - Local files (markdown, text, PDFs, Word docs)
   - Web-based documents (if URLs provided)
   - Pasted content from the user

3. **Organize by topic** - Mentally categorize content into:
   - Functional requirements (what the system should do)
   - Non-functional requirements (performance, security, etc.)
   - User personas and use cases
   - Technical constraints
   - Business rules and domain logic

### Step 2: Extract Key Information

Analyze the documents systematically:

1. **Identify stakeholders and personas**:
   - Who will use this system?
   - What are their roles and goals?
   - What problems are they trying to solve?

2. **Extract feature requests**:
   - What capabilities does the system need?
   - What workflows should it support?
   - What are the core user journeys?

3. **Capture requirements**:
   - Functional: Specific behaviors and features
   - Non-functional: Performance, security, scalability
   - Technical: Technology choices, integrations, constraints
   - Data: What data needs to be stored, processed, validated?

4. **Identify gaps and ambiguities**:
   - What's unclear or missing?
   - Where are there contradictions?
   - What needs further clarification?

### Step 3: Generate Structured Markdown

Create a comprehensive markdown document with the following structure:

```markdown
# [System Name] - Requirements Synthesis

**Generated**: [Date]
**Sources**: [List of input documents]
**Status**: Draft for stakeholder review

---

## Executive Summary

[2-3 paragraph overview of the system, its purpose, and key stakeholders]

---

## Stakeholders & Personas

### [Persona Name 1]
- **Role**: [Job title or role]
- **Goals**: [What they want to accomplish]
- **Pain Points**: [Current problems they face]
- **Needs**: [What they need from this system]

### [Persona Name 2]
[Same structure...]

---

## User Stories

### Epic: [Epic Name]

#### Story 1: [Story Title]
**As a** [persona]
**I want to** [capability]
**So that** [benefit]

**Acceptance Criteria** (Draft):
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

**Priority**: [High/Medium/Low]
**Estimated Complexity**: [Simple/Medium/Complex]

#### Story 2: [Story Title]
[Same structure...]

---

## System Requirements

### Functional Requirements

#### FR-001: [Requirement Name]
**Description**: [Clear description of what the system must do]
**Priority**: [Must Have / Should Have / Could Have / Won't Have]
**Related Stories**: [Story IDs]

#### FR-002: [Requirement Name]
[Same structure...]

### Non-Functional Requirements

#### NFR-001: Performance
**Description**: [Specific performance requirement]
**Measurement**: [How to measure success]
**Target**: [Specific metric, e.g., "Page load under 2 seconds"]

#### NFR-002: Security
[Same structure...]

### Technical Requirements

#### TR-001: [Requirement Name]
**Description**: [Technical constraint or requirement]
**Justification**: [Why this is necessary]
**Impact**: [How it affects implementation]

---

## Feature Specifications

### Feature: [Feature Name]

**Overview**: [Brief description of the feature]

**User Flows**:
1. [Step-by-step description of primary user flow]
2. [Alternative flows]
3. [Error/edge cases]

**Components**:
- **Frontend**: [UI components needed]
- **Backend**: [API endpoints, services needed]
- **Database**: [Data models, tables needed]

**Dependencies**:
- [Other features or systems this depends on]

**Open Questions**:
- [Questions that need clarification]
- [Decisions that need to be made]

### Feature: [Feature Name 2]
[Same structure...]

---

## Data Requirements

### Entity: [Entity Name]

**Attributes**:
- `field_name` (type): Description
- `another_field` (type): Description

**Relationships**:
- [Relationship to other entities]

**Validation Rules**:
- [Business rules for this data]

### Entity: [Entity Name 2]
[Same structure...]

---

## Integration Points

### [External System 1]
**Purpose**: [Why we integrate with this]
**Type**: [REST API / GraphQL / Message Queue / etc.]
**Data Flow**: [What data is exchanged]
**Dependencies**: [What we depend on from them]

---

## Gaps & Ambiguities

### Clarifications Needed
1. **Topic**: [What's unclear]
   - **Question**: [Specific question to ask stakeholders]
   - **Impact**: [Why this matters]

2. **Topic**: [What's unclear]
   [Same structure...]

### Missing Information
- [List of information not found in source documents]
- [Areas that need more detail]

---

## Next Steps

1. **Review this document** with stakeholders
2. **Run the interviewing-stakeholders skill** to:
   - Clarify ambiguities listed above
   - Gather missing information
   - Validate assumptions
   - Generate detailed Gherkin acceptance criteria
3. **Refine and finalize** requirements based on interview results
4. **Begin implementation** using test-driven development

---

## Appendix

### Source Document Summary
- **[Document 1 Name]**: [Brief summary of what was extracted]
- **[Document 2 Name]**: [Brief summary of what was extracted]

### Assumptions Made
- [List assumptions you made while synthesizing]
- [Helps stakeholders validate your interpretation]
```

### Step 4: Validate and Refine

Before finalizing the document:

1. **Cross-reference**: Ensure all mentions in source docs are captured
2. **Consistency check**: Look for contradictions or inconsistencies
3. **Completeness**: Verify all major topics are covered
4. **Clarity**: Use clear, unambiguous language
5. **Traceability**: Link user stories to requirements and features

### Step 5: Present to User

After generating the document:

1. **Save the markdown file** to an appropriate location (e.g., `docs/requirements/requirements-synthesis.md`)
2. **Summarize key findings**:
   - Number of user stories identified
   - Key features discovered
   - Critical gaps or ambiguities
   - Recommended next steps
3. **Highlight areas needing clarification** - Point out what should be addressed in stakeholder interviews
4. **Ask if the user wants to proceed** with the `interviewing-stakeholders` skill

---

## Best Practices

### Analysis Techniques

- **Look for patterns**: Recurring themes often indicate core features
- **Identify "voice of customer"**: Direct quotes reveal true needs
- **Distinguish requirements from solutions**: Focus on the "what" and "why", not just the "how"
- **Prioritize ruthlessly**: Mark what's truly essential vs. nice-to-have
- **Be objective**: Don't inject your own assumptions - stick to what's in the sources

### Writing Quality Requirements

- **Specific**: Avoid vague terms like "fast" or "user-friendly"
- **Measurable**: Include quantifiable criteria where possible
- **Achievable**: Don't commit to impossible requirements
- **Relevant**: Tie back to user needs and business goals
- **Testable**: Every requirement should be verifiable

### Handling Ambiguity

When you encounter unclear or contradictory information:

1. **Document it explicitly** in the "Gaps & Ambiguities" section
2. **Flag for stakeholder review** - don't guess or assume
3. **Note the source** of each conflicting piece of information
4. **Propose questions** that would resolve the ambiguity

### Working with Different Input Types

**Conversation transcripts**:
- Look for decision points and conclusions
- Capture action items and commitments
- Note who said what (different stakeholders have different priorities)

**Formal documents**:
- Respect existing structure and terminology
- Cross-reference sections for consistency
- Look for version history or change logs

**Technical notes**:
- Distinguish between constraints and preferences
- Capture rationale for technical decisions
- Note any prototypes or proof-of-concepts mentioned

**User stories/feature requests**:
- Standardize format (As a... I want... So that...)
- Extract implicit acceptance criteria
- Group related stories into epics

---

## Example Usage

**User**: "I have meeting notes from our product planning session and a requirements doc from our PM. Can you help synthesize these into structured requirements?"

**You**: I'll use the synthesizing-requirements skill to analyze both documents and create a comprehensive requirements document. Please provide:
1. The meeting notes (file path or paste the content)
2. The requirements doc (file path or link)

[After receiving the documents...]

[Read both documents using Read or WebFetch tools]

[Analyze and extract information per Step 2]

[Generate the structured markdown per Step 3]

[Save to docs/requirements/requirements-synthesis-2026-01-12.md]

"I've synthesized your meeting notes and requirements document into a structured requirements file at [docs/requirements/requirements-synthesis-2026-01-12.md](docs/requirements/requirements-synthesis-2026-01-12.md). Here's what I found:

- **12 user stories** across 3 epics
- **8 functional requirements** (5 must-have, 3 should-have)
- **4 non-functional requirements** (performance, security, scalability, accessibility)
- **3 major features** with detailed specifications
- **7 open questions** that need stakeholder clarification

**Key gaps identified**:
- User authentication method not specified
- Database choice not finalized
- Performance targets not quantified

**Recommended next step**: Run the `interviewing-stakeholders` skill to clarify these gaps and generate detailed Gherkin acceptance criteria for each user story. Would you like me to proceed with that?"

---

## Integration with Pact Workflow

This skill is **Step 1** in the Pact workflow:

1. **synthesizing-requirements** (this skill) ← You are here
2. **interviewing-stakeholders** ← Use this next to fill gaps and create acceptance criteria
3. **Test-driven implementation** ← Build the system using generated Gherkin scenarios

The output of this skill becomes the input for stakeholder interviews, which will then produce detailed, testable acceptance criteria in Gherkin format (Given/When/Then).

---

## Tips for Success

- **Start broad, then narrow**: Get the big picture first, then dive into details
- **Use templates consistently**: The structure above helps maintain quality
- **Don't skip gaps section**: Identifying what you don't know is as important as what you do know
- **Think like a tester**: Ask "How would I verify this?" for each requirement
- **Keep the user involved**: Check in if you encounter major ambiguities
- **Save your work**: Use descriptive filenames with dates for version control

---

## Output Checklist

Before marking your synthesis complete, verify:

- [ ] All source documents have been read and analyzed
- [ ] Executive summary captures the system's essence
- [ ] Stakeholders and personas are identified
- [ ] User stories follow "As a... I want... So that..." format
- [ ] Requirements are categorized (functional, non-functional, technical)
- [ ] Feature specifications include user flows and components
- [ ] Data requirements are documented
- [ ] Integration points are identified
- [ ] Gaps and ambiguities are explicitly listed
- [ ] Next steps are clearly stated
- [ ] Document is saved in an appropriate location
- [ ] User is informed of key findings and recommendations

---

**Remember**: The goal isn't perfection - it's to create a solid foundation that can be refined through stakeholder interviews. When in doubt, document the uncertainty and flag it for clarification.
