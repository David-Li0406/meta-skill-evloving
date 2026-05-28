---
name: feature-research
description: Perform in-depth research on a feature using Jira, Confluence, and codebase analysis. Produces a comprehensive research document with feature overview, technology primers, gap analysis, and code impact assessment.
argument-hint: "<feature description or Jira/Confluence URLs>"
---

# Feature Research Skill

You are conducting in-depth feature research. Your goal is to produce a comprehensive research document that will serve as the foundation for implementation planning.

## Input

The user has provided the following feature request or research context:

$ARGUMENTS

## Research Process

### Step 1: Extract and Identify Resources

First, identify all resources provided:
- **Jira Issues**: Look for URLs like `https://*.atlassian.net/browse/*` or issue keys like `PROJ-123`
- **Confluence Pages**: Look for URLs like `https://*.atlassian.net/wiki/*`
- **Feature Description**: Any plain text describing the feature

### Step 2: Gather Information from Atlassian (if links provided)

If Jira or Confluence links are present, use the Atlassian MCP tools to gather comprehensive information:

**For Jira Issues:**
- Use `mcp__plugin_atlassian_atlassian__getJiraIssue` to fetch issue details
- Use `mcp__plugin_atlassian_atlassian__getJiraIssueRemoteIssueLinks` to find linked Confluence pages
- Look at linked issues, subtasks, and epic relationships
- Review comments for additional context and decisions

**For Confluence Pages:**
- Use `mcp__plugin_atlassian_atlassian__getConfluencePage` to fetch page content
- Use `mcp__plugin_atlassian_atlassian__getConfluencePageDescendants` for child pages
- Check for linked requirements, design docs, or technical specifications

**For Discovery:**
- Use `mcp__plugin_atlassian_atlassian__search` to find related documentation
- Search for related issues, decisions, and historical context

### Step 3: Analyze the Codebase

Study the existing codebase to understand:
- Current architecture and patterns in use
- Existing implementations of similar features
- Code areas that will likely need modification
- Dependencies and integrations that may be affected

Use the Explore agent or direct file searches to:
- Find relevant source files
- Understand existing patterns and conventions
- Identify integration points
- Map the code structure related to this feature

### Step 4: Research Technologies

For any technologies critical to the feature:
- Use WebSearch to gather current documentation and best practices
- Use Context7 MCP tools to fetch library documentation if applicable
- Summarize key concepts the team needs to understand

## Output Document Structure

Ask the user where to save the research document if no path was specified in the arguments. Suggest a reasonable default like `docs/research/<feature-name>-research.md` or similar based on the project structure.

Create a comprehensive markdown document with the following structure:

```markdown
# Feature Research: [Feature Name]

**Research Date:** [Date]
**Source Issues:** [List of Jira issues researched]
**Source Documents:** [List of Confluence pages researched]

---

## Executive Summary

[2-3 paragraph summary of the feature, its purpose, and key findings]

---

## 1. Feature Overview

### 1.1 Goals and Objectives
[What the feature aims to accomplish]

### 1.2 User Stories / Requirements
[Key requirements extracted from Jira/Confluence]

### 1.3 Acceptance Criteria
[Specific criteria that define "done"]

### 1.4 Delivery Requirements
[Timeline, milestones, dependencies on other work]

---

## 2. Technical Context

### 2.1 Technologies Involved
[List of technologies, frameworks, protocols this feature requires]

### 2.2 Architecture Considerations
[How this fits into the existing system architecture]

### 2.3 Integration Points
[External systems, APIs, or services this will interact with]

---

## 3. Technology Primers

[For each critical technology, provide a concise primer]

### 3.1 [Technology Name]

**What it is:** [Brief description]

**Key Concepts:**
- [Concept 1]
- [Concept 2]

**Relevant Features for This Implementation:**
- [Feature 1 and why it matters]
- [Feature 2 and why it matters]

**Resources:**
- [Link to official documentation]
- [Link to relevant guides]

[Repeat for each critical technology]

---

## 4. Codebase Impact Analysis

### 4.1 Files Requiring Modification

| File Path | Change Type | Description |
|-----------|-------------|-------------|
| `path/to/file.go` | Modify | [What needs to change] |
| `path/to/new.go` | Create | [New file purpose] |

### 4.2 Functions/Components Affected

- `package.FunctionName()` - [Why/how it needs to change]
- `ComponentName` - [What modifications are needed]

### 4.3 Database/Schema Changes
[If applicable, describe any data model changes]

### 4.4 API Changes
[If applicable, describe any API additions or modifications]

### 4.5 Testing Considerations
[What types of tests will be needed]

---

## 5. Gaps and Open Questions

### 5.1 Missing Information

| # | Gap | Impact | Suggested Resolution |
|---|-----|--------|---------------------|
| 1 | [What's missing] | [Why it matters] | [Who to ask or where to look] |

### 5.2 Open Questions

1. **[Question]**
   - Context: [Why this question matters]
   - Suggested owner: [Who might know]

2. **[Question]**
   - Context: [Why this question matters]
   - Suggested owner: [Who might know]

### 5.3 Assumptions Made

[List any assumptions made during research that should be validated]

---

## 6. Recommendations

### 6.1 Implementation Approach
[High-level recommended approach]

### 6.2 Risk Areas
[Potential challenges or areas of concern]

### 6.3 Suggested Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Appendix

### A. Raw Notes
[Any additional notes or context gathered during research]

### B. Related Links
[All URLs referenced during research]
```

## Important Guidelines

1. **Be thorough but concise** - Include all relevant information without unnecessary verbosity
2. **Cite sources** - Always reference where information came from (Jira issue, Confluence page, code file)
3. **Flag uncertainty** - Clearly mark any assumptions or areas where information was incomplete
4. **Be actionable** - The document should enable someone to start planning implementation
5. **Ask for clarification** - If critical information is missing and can't be found, ask the user

## Handling Missing Output Path

If no output path is specified in the arguments, ask the user:

"I've completed the feature research. Where would you like me to save the research document?

Suggested locations based on this project:
- `docs/research/[feature-name]-research.md`
- `[feature-name]-research.md` (current directory)

Please provide the desired path or select one of the suggestions."
