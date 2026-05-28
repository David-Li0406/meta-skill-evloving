---
name: spec-plan
description: Pre-planning and research for feature specifications
args:
  feature_description:
    type: string
    description: Brief description of the feature to plan (e.g., "build a auth feature")
    required: false
---

# Spec Plan: Pre-Planning & Research

Research, gather context, and launch spec-writer agent with comprehensive documentation.

## Usage

```bash
# With feature description
/spec plan build a user authentication feature

# Without (interactive mode)
/spec plan
```

## Purpose

This skill handles the **pre-planning stage** of feature specification:
1. Clarify requirements with the user
2. Fetch latest documentation (MCP tools)
3. Check Memory Bank for existing work
4. Launch spec-writer agent with full context

## Workflow

### Phase 0: Feature Description

**If user provided feature description as argument:**
- Use it as the starting point
- Skip to clarifying questions with context

**If no argument provided:**
- Ask: "What feature would you like to plan specifications for?"

### Phase 1: Clarify Requirements

Ask the user clarifying questions (using feature description as context if provided):

**Technology Stack:**
- What frameworks/technologies will this feature use?
- Are there specific patterns or APIs to leverage?
- What version of the framework are you using?

**Feature Context:**
- What larger epic/initiative does this belong to?
- What problem does this solve for users?
- What are the key acceptance criteria?

**Constraints:**
- Any performance requirements?
- Security considerations?
- Integration requirements with existing systems?

### Phase 2: Fetch Latest Documentation

Based on the tech stack, gather current best practices:

#### For Next.js Projects

```bash
# Initialize Next.js docs
mcp__next-devtools__init

# Search for relevant patterns
mcp__next-devtools__nextjs_docs
  path: [from llms-index]
  anchor: [specific section]

# Focus areas:
- Server Actions (if server-side logic)
- Route Handlers (if API endpoints)
- Data Fetching patterns (if data-heavy)
- Caching strategies (if performance-critical)
```

#### For Other Frameworks

```bash
# Web search for latest docs
WebSearch query: "[framework] [version] [feature] documentation 2026"

# Fetch specific pages
WebFetch url: [official docs URL]
  prompt: "Extract best practices for [feature]"
```

#### General Research

- Search for similar implementations
- Find case studies or examples
- Identify potential pitfalls
- Check for recent framework changes

### Phase 3: Check Memory Bank

Avoid duplication by checking existing work:

```bash
# Read system architecture
Read memory-bank/systemPatterns.md

# Search for similar features
mcp__memory__search_nodes
  query: "[feature keywords]"

# Check active work
Read memory-bank/activeContext.md
```

**Document:**
- Existing patterns to follow
- Reusable components identified
- Similar features for reference
- Architecture constraints

### Phase 4: Launch Spec-Writer Agent

Now launch the spec-writer agent with comprehensive context:

```bash
Task tool with subagent_type="spec-writer"
```

**Agent Prompt Template:**

```
I need comprehensive feature specifications for: [FEATURE NAME from arg or clarification]

**Initial Request:**
[Include the feature_description argument if provided, e.g., "build a user authentication feature"]

**Context from Documentation Research:**
[Summarize MCP/WebSearch findings]
- Latest patterns: [list]
- Recommended APIs: [list]
- Framework version considerations: [notes]
- Best practices discovered: [list]

**Current System Architecture:**
[Summarize Memory Bank findings]
- Existing components to reuse: [list]
- Architecture patterns to follow: [list]
- Integration points: [list]
- Current tech stack: [list]

**Feature Requirements:**
- Larger Feature Context: [epic/initiative]
- Feature Description: [from arg or detailed from conversation]
- Acceptance Criteria:
  - [criterion 1]
  - [criterion 2]
  - [criterion 3]
- Technology Stack: [frameworks, libraries, tools]
- Performance Requirements: [if any]
- Security Requirements: [if any]

**Documentation Requirements:**
Generate in folder: /job-queue/feature-[name]/docs/

Required files:
1. FRD.md - Feature Requirement Document
   - Business objectives
   - User problems solved
   - Success metrics

2. FRS.md - Functional Requirement Specification
   - Detailed functional requirements
   - User workflows
   - Acceptance criteria per requirement

3. GS.md - Gherkin Specification
   - Feature declaration
   - Background (if applicable)
   - Scenarios with Given/When/Then
   - Example tables

4. TR.md - Technical Requirements
   - API contracts (endpoints, methods, schemas)
   - Data models (entities, fields, types)
   - Dependencies (libraries, services)
   - Error handling strategy
   - Security considerations

5. task-list.md - Actionable Task Breakdown
   - Numbered phases
   - Specific tasks (not "implement X")
   - Task dependencies noted
   - Logical sequencing

**Special Instructions:**
- Reference latest documentation patterns: [list key findings]
- Highlight reusable components: [from Memory Bank]
- Follow framework version: [X.Y.Z]
- Note security requirements: [if applicable]
- Include performance considerations: [if applicable]
- Ensure .gitignore contains /job-queue
```

## Expected Outcomes

After this skill completes:

1. ✅ User requirements clarified
2. ✅ Latest documentation researched
3. ✅ Existing codebase analyzed
4. ✅ Spec-writer agent launched with full context
5. ✅ Agent generating comprehensive specs

## Next Step

Once spec-writer agent completes, use `/spec review` to:
- Validate generated specs
- Critique quality
- Collect user feedback
- Iterate if needed

## Tools Used

- **MCP Tools** - Documentation fetching
- **WebSearch/WebFetch** - General research
- **Memory Bank** - Existing codebase analysis
- **Task Tool** - Spec-writer agent launch

## Notes

- **Documentation-first:** Always research before generating
- **No duplication:** Always check Memory Bank first
- **Latest practices:** Use MCP tools for current best practices
- **Context is key:** The better the context, the better the specs

---

**Estimated time:** 5-10 minutes for research and agent launch
**Token usage:** ~800 tokens (focused on research workflow)
