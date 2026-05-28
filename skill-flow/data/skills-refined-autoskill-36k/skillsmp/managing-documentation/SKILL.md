---
name: managing-documentation
description: Creates, updates, and maintains documentation for projects following best practices for clarity, accessibility, and inclusivity. Use when creating new docs, improving existing documentation, checking documentation standards, ensuring global audience compatibility, validating for inclusive language, or applying agile documentation principles. Handles guides, API documentation, README files, and internal documentation with emphasis on lean/agile practices, clarity for global audiences, and inclusive content.
allowed-tools: Read, Write, Edit, Glob, Grep, Task
---

# Managing Documentation

Comprehensive agent skill for creating, updating, and maintaining high-quality project documentation. Follows established best practices from agile, Google, and Write the Docs methodologies.

## When to Use This Skill

Activate when:
- Creating new documentation for projects, features, or products
- Updating or improving existing documentation quality
- Validating documentation against style and inclusivity standards
- Writing guides, API documentation, or README files
- Ensuring documentation works for global, diverse audiences
- Checking for inclusive language and accessibility
- Applying lean/agile documentation principles
- Planning documentation structure and organization
- Reviewing documentation for clarity and completeness

## Core Workflows

### Workflow 1: Creating New Documentation

#### Step 1: Define Purpose and Audience
Before writing:
- **Clarify purpose**: What is this documentation meant to achieve? Who will use it?
  - **If unclear, ask user**: "What problem should this documentation solve? Who will read it?"
- **Identify customers**: Actual end-users, developers, operators, support staff?
  - **If uncertain, ask user**: "Who is the primary audience? What's their experience level?"
- **Determine scope**: What should be covered? What's out of scope?
  - **If uncertain, ask user**: "What specific topics must be covered? What can be linked or omitted?"
- **Choose doc type**: Guide, API reference, README, tutorial, troubleshooting, architecture overview

#### Step 2: Plan Structure
Follow these principles:
- **Skimmable**: Use clear headings, start paragraphs with key concepts, use lists
- **Cumulative**: Order content so prerequisites come first (especially for guides/tutorials)
- **Exemplary**: Include examples for most concepts, especially in guides and API docs
- **Concise**: Keep just barely good enough - avoid over-documentation

Structure recommendations:
- **Getting Started Guides**: Introductory context → prerequisites → step-by-step → examples
- **API Documentation**: Purpose of API group → parameter descriptions → examples → error cases
- **README**: Brief intro → installation/quick start → usage → contributing → license
- **Troubleshooting**: Common problems → diagnostics → solutions with examples

#### Step 3: Write with Global Audience in Mind
- Use **simple, concise language**: Avoid idioms, colloquialisms, jargon (unless industry-standard and explained)
- Use **active voice and present tense** for clarity
- Use **shorter sentences** - easier to understand and translate
- **Define abbreviations** on first use
- **Avoid phrasal verbs** when simpler verbs work (use "start" not "commence")
- **Use concrete examples** - show don't just tell
- Avoid **dated language** like "new", "currently", "soon" - focus on what is, not what changed

Example: ❌ "Our product now supports the latest feature" ✅ "Our product supports feature X for use case Y"

**Never document future features:**
- Don't pre-announce anything unless approved by legal counsel
- Focus on current capabilities, not roadmaps or planned features
- Document what exists now, not what will exist later
- Example: ❌ "Feature X will be available soon" ✅ [omit until released]

**Avoid excessive or unverifiable claims:**
- Don't use superlatives: "best", "fastest", "simplest", "never", "always"
- Be careful with "ensure" and "guarantee" - use only when truly guaranteed
- Reference data sources for performance claims
- Example: ❌ "Our product is the fastest" ✅ "Our product processes X requests/sec"
- Example: ❌ "Prevents all security attacks" ✅ "Helps prevent attacks by..."
- Example: ❌ "The best solution for your needs" ✅ "A solution that handles X, Y, and Z"

**Avoid overusing politeness:**
- Don't overuse "please" in instructions - it's implied and adds unnecessary words
- Example: ❌ "Please click the button" ✅ "Click the button"
- Example: ❌ "For more information, please see the guide" ✅ "For more information, see the guide"
- Exception: Use "please" when making significant requests or in sensitive contexts

#### Step 4: Ensure Inclusivity
**Avoid problematic language:**
- No ableist terms: ❌ "sanity check" ✅ "final check", ❌ "blind to" ✅ "overlook", ❌ "cripples" ✅ "slows down"
- No gendered terms: ❌ "man-hours" ✅ "person-hours", ❌ "he/she" ✅ "they", avoid gendered pronouns in examples
- No violent language: Avoid "kill", "hit", avoid animal slaughter metaphors
- No culturally specific references, slang, or humor
- Use diverse names in examples

**Be specific about people:**
- "person with disabilities" not "the disabled"
- "older adults" not "seniors" or "the elderly"
- "quadriplegic person" not "a quadriplegic"
- Research community preferences before writing about disabilities

**For code/commands with non-inclusive terms in them**, use code formatting and minimize:
- ✅ "Configure the `master` node (shown in the file)"
- ✅ "Execute the `START SLAVE` statement"
- Use preferred term in surrounding text

#### Step 5: Review and Validate
**Consider automated documentation generation where appropriate:**
- API docs: JSDoc, TSDoc, rustdoc, Sphinx, Doxygen, JavaDoc
- Architecture diagrams: PlantUML, Mermaid diagrams from code
- Dependency graphs: Generated from package managers
- Test reports: Generated from test suites
- Remember: Generated docs still need human review and enhancement

**Alternatives when no technical writer available:**
- Pair documenting: Write documentation with a partner (like pair programming)
- Shared ownership: Multiple people maintain and improve documentation
- Text-to-speech software: Listen to your writing to find awkward passages
- Peer review: Have colleagues review for clarity before publishing

Before publishing, check:
- [ ] Clear purpose defined
- [ ] Audience needs addressed
- [ ] Examples provided for key concepts
- [ ] No jargon without explanation
- [ ] Simple language, active voice
- [ ] No outdated time-based words (new, currently, soon, latest, now)
- [ ] No excessive claims (best, fastest, simplest, never, always)
- [ ] No future features mentioned
- [ ] No overuse of "please" in instructions
- [ ] No ableist, gendered, or violent language
- [ ] No culturally specific references
- [ ] Consistent terminology throughout
- [ ] Concise but sufficient detail
- [ ] Headings clear and descriptive
- [ ] Links to related info (if applicable)

### Workflow 2: Updating Existing Documentation

#### Step 1: Assess Current State
- Read existing documentation completely
- Identify outdated information
- Check for consistency issues
- Look for jargon without explanation
- Check for problematic language (ableist, gendered, violent, cultural specificity)
- Verify examples still work
- Check clarity for non-expert readers

#### Step 2: Prioritize Changes
Categorize improvements:
- **Critical**: Incorrect information, broken examples, high-impact clarity issues
- **Major**: Consistency problems, missing key examples, jargon not explained, outdated phrasing
- **Minor**: Grammar, tone refinement, better formatting

#### Step 3: Update Content
When updating:
- Use "Old approaches" sections for deprecated items (never use dates)
- Preserve working examples while updating references
- Improve clarity by breaking up long paragraphs
- Replace problematic language consistently
- Update jargon explanations
- Ensure consistency with updated terminology

#### Step 4: Verify Changes
- All examples updated and correct
- No broken links or references
- Terminology consistent throughout
- Language inclusive and accessible
- Clarity improved without removing necessary detail
- Matches current product/feature state

### Workflow 3: Validating Documentation Quality

Apply these validation checks:

#### Content Quality (ARID Principles)
- **Accept Repetition**: Some business logic will be described multiple ways - this is acceptable
- **Skimmable**: Readers can quickly find what they need without reading everything
- **Exemplary**: Common use cases have examples, not everything needs examples
- **Consistent**: Same term used consistently, same formatting applied systematically
- **Current**: Reflects actual state of product, not historical or future states

#### Clarity & Accessibility
- No industry jargon without explanation, or uses "click here" link text
- Sentences under 20 words when possible
- Active voice used primarily
- Present tense used for current capabilities
- Examples provided for important concepts
- Headings clearly describe content below

#### Inclusive Language
- No ableist language (sanity check, blind to, cripples, dumb, etc.)
- No gendered terms (man-hours, he/she pronouns, actress/actor distinctions)
- No violent figurative language (kill, hit, slaughter metaphors)
- No unnecessary cultural specificity
- Diverse names in examples when people shown
- Neutral language about disabilities

#### Global Audience
- No colloquialisms, idioms, or slang
- No humor (difficult to translate)
- No geographic specificity (seasons, holidays, sports)
- Dates and times unambiguous and clear
- Simple words chosen over complex synonyms
- No assumed prior knowledge

#### Completeness
- Key information comprehensive (covers all main topics OR clearly states what's excluded)
- Edge cases addressed or acknowledged
- Error scenarios documented
- Prerequisites clearly stated
- Related topics referenced

#### Currency
- No "new", "currently", "now", "soon", "latest" references to product features
- Reflects actual capabilities not future plans
- Deprecated features clearly marked if included
- Version-specific info generalized when possible

### Workflow 4: Applying Agile/Lean Principles

Documentation should be "just barely good enough" - sufficient for current needs without unnecessary detail.

#### Document Late, Update Constantly
- Don't document speculative features before they stabilize
- Write documentation towards end of development when you know what you've built
- Document just-in-time when most needed
- Update only when pain of using outdated docs exceeds effort to update

#### Document with Purpose
- Create documents only when they fulfill clear, important goals
- Focus on what customers actually need, not what you think they should need
- Justify documentation requests: why needed? who benefits? what's the cost?

#### Prefer Executable Specifications
- Use tests as specifications where possible
- Link to code examples rather than duplicate specifications
- Generate system documentation from code when possible

#### Choose Best Communication Medium
Documentation is often NOT the best choice:
- Direct conversation > documentation for immediate understanding
- Involved stakeholders > documentation for knowledge transfer
- Well-structured code > documentation for technical details

Documentation becomes increasingly valuable as distance (physical or temporal) makes direct communication more difficult or less practical.

#### Minimize Document Overlap
- Define scope clearly for each document
- Avoid same information in multiple places
- Use references/links instead of duplication
- Link to single source of truth

#### Display Information Publicly
- Share models, diagrams, documentation during development
- Use documentation as "information radiator" for team communication
- Status indicators help readers understand context (draft vs. finalized)

## Quality Checklist by Document Type

### Guides & Tutorials
- [ ] Introduces topic gently before technical details
- [ ] Prerequisites clearly stated upfront
- [ ] Step-by-step instructions are concrete (not abstract)
- [ ] Examples build on previous examples (not new problems each time)
- [ ] Code examples short (~3-5 lines), not full implementations
- [ ] Assumptions about reader knowledge clearly stated
- [ ] Next steps or related topics referenced at end

### API Documentation
- [ ] Purpose of API group explained before diving into individual methods
- [ ] Each method shows purpose, parameters, return values
- [ ] Examples provided for common use cases
- [ ] Error cases documented
- [ ] Request/response examples clear and realistic but simplified
- [ ] No complex real-world implementations in examples
- [ ] Shared terminology used throughout

### README Files
- [ ] Brief description in opening paragraph
- [ ] Installation/quick start section early
- [ ] Common use cases covered
- [ ] Troubleshooting or FAQ included
- [ ] Links to full documentation
- [ ] Contributing guidelines if accepting contributions
- [ ] License clearly stated

### Architecture/System Documentation
- [ ] High-level overview comes first
- [ ] Diagrams supplement (not replace) text description
- [ ] Key concepts explained at high level before details
- [ ] Links to code for implementation details
- [ ] Major components described (not every detail)
- [ ] Clear what's documented vs. what's in code
- [ ] Design decisions explained (the "why" not just the "what")

## Writing Style Principles

### Tone and Voice
- Conversational, friendly, and respectful (not stuffy or overly formal)
- Sound like knowledgeable friend, not textbook or marketing material
- Be human and memorable, but focus on information delivery
- Avoid super-entertaining or super-dry extremes

### Things to Avoid
- Buzzwords and unnecessary jargon
- Overly cute, wacky, or zany tone
- Ableist language or problematic figures of speech
- Placeholder phrases ("please note", "at this time")
- Choppy or overly long sentences
- Current pop-culture references (won't age well)
- Excessive exclamation marks
- Mixing or overextending metaphors
- Internet slang or abbreviations (tl;dr, ymmv)

### Techniques That Work
- Read aloud - does it sound natural? (not every sentence, but check awkward ones)
- Use transitions between sentences for flow
- Step back and ask "what am I really trying to say?"
- Get colleague feedback on tone and clarity
- Focus on communicating useful info clearly - that's most important

## Tool Usage Patterns for This Skill

### Finding Documentation Files
- **Glob for documentation**: `**/*.md`, `**/README.md`, `**/docs/**`, `**/documentation/**`
- **Glob for API docs**: `**/api/**`, `**/reference/**`, `**/swagger/**`
- **Glob for specific doc types**: `**/CONTRIBUTING.md`, `**/CHANGELOG.md`, `**/LICENSE.md`

### Validating Content for Problematic Terms
Use Grep to search for terms that violate guidelines:
- **Ableist language**: `"sanity|crazy|insane|blind to|cripple|dumb|stupid"`
- **Gendered language**: `"he |she |his |her |man-hours|mankind|actress|waitress"`
- **Violent language**: `" kill | hit |STONITH|hang |hung "`
- **Time-based words**: `"currently|soon|new |latest|now |presently"`
- **Excessive claims**: `"best |fastest|simplest|never |always |ensure |guarantee"`
- **Politeness overuse**: `"[Pp]lease click|[Pp]lease see|[Pp]lease enter"`
- **Future features**: `"will be |coming soon|planned|roadmap"`

### Understanding Context Before Writing
- **Read source code**: Use Read tool to understand features before documenting them
- **Find existing patterns**: Use Grep to find how similar features are documented
- **Check project conventions**: Read existing docs to match style and terminology

### Large-Scale Operations
- **Use Task tool with Haiku** for validating 50+ documentation files simultaneously
- **Use Task tool for codebase exploration** when searching for undocumented features or APIs
- **Use Bash tool** for running documentation generators or build commands

### Example Validation Commands
```bash
# Search for ableist terms across all markdown files
grep -r "sanity\|crazy\|insane\|blind to\|cripple\|dumb" docs/

# Find time-based language
grep -r "currently\|soon\|new \|latest" **/*.md

# Check for gendered pronouns
grep -r " he \| she \| his \| her " docs/
```

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Outdated information | Documented too early | Don't document until feature stabilizes |
| Too much detail | No prioritization | Focus on common cases, link to code for details |
| Unclear jargon | Assumed audience knowledge | Define all industry-specific terms |
| Hard to find info | No clear structure | Use descriptive headings, start paragraphs with key concepts |
| Inconsistent terminology | Multiple authors/rewrites | Maintain consistent term list, audit before publishing |
| Culturally insensitive | No consideration for diversity | Review for idioms, holidays, sports, slang references |
| Violates inclusivity | Ableist/gendered/violent language | Search for: sanity, blind, cripple, he/she, kill, hit, etc. |
| Incomplete examples | Show only happy path | Include error cases, edge cases, realistic scenarios |

## Implementation Approach

When helping with documentation:

1. **Understand context**: What's the purpose? Who reads it? What do they need?
2. **Assess quality**: What's working? What needs improvement?
3. **Plan improvements**: Prioritize critical → major → minor issues
4. **Apply standards**: Use clear structure, simple language, inclusive voice
5. **Validate**: Check against this skill's checklists and principles
6. **Iterate**: Get feedback, refine, publish

The goal is documentation that is clear, accessible, sufficient for actual needs, and welcoming to readers from all backgrounds.