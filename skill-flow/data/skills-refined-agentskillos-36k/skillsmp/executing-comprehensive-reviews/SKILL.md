---
name: executing-comprehensive-reviews
description: Use when reviewing content for clarity, generating questions, or checking alignment. Triggers on "review for clarity", "suggest questions", "check alignment", "comprehensive review".
---

# Executing Comprehensive Reviews

Guide for content review workflows including clarity improvements, question generation, and book-implementation alignment validation.

## Instructions

### Step 1: Parse Review Requirement

Extract from request:
- **Target**: Specific file, chapter, or pattern
- **Review Type**: clarity | questions | alignment | comprehensive
- **Scope**: Single file, chapter, full codebase

**Type Detection:**
- Contains "clarity" or "clear" -> Clarity review
- Contains "question" or "deeper" -> Questions review
- Contains "align" or "implementation" -> Alignment check
- Contains "comprehensive" or "full" -> All types
- Ambiguous -> Ask user which type(s)

### Step 2: Optional Exploration

If requirement is broad or exploratory:

1. Search for relevant content
   ```
   Glob: chapters/**/*.md
   Grep: {topic keywords}
   ```

2. Read identified files to assess coverage

3. Create exploration summary:
   - Relevant entries discovered
   - Content gaps identified
   - Relationship mappings

**Skip exploration if:**
- Specific file path provided
- Review type is alignment (has own discovery)
- User requests direct review only

### Step 3: Execute Review Type(s)

#### Clarity Review

For improving readability without changing voice:

1. **Read target content** completely
2. **Identify clarity issues:**
   - Ambiguous sentences
   - Missing transitions
   - Jargon without context
   - Overly complex structure
3. **Propose improvements** preserving authorial voice
4. **Present suggestions** to user for approval
5. **Apply approved changes**
6. **Update `last_updated`** in frontmatter

**Voice preservation checklist:**
- Maintains first-person where used
- Keeps practical, experience-based tone
- Preserves original examples
- Doesn't over-formalize

#### Questions Review

For generating follow-up questions to deepen content:

1. **Read target content** completely
2. **Identify deepening opportunities:**
   - Claims that could use evidence
   - Patterns that could use examples
   - Concepts that connect to other chapters
   - Edge cases not addressed
3. **Generate 3-5 follow-up questions**
4. **Present questions** to user for selection
5. **Add selected questions** under "### Follow-up" heading
6. **Update `last_updated`** in frontmatter

**Question quality criteria:**
- Answerable from experience/research
- Leads to actionable content
- Not already covered in file
- Connects to reader needs

#### Alignment Check

For validating book-implementation consistency:

1. **Inventory phase:**
   - Scan CLAUDE.md for documented commands/agents
   - List all `.claude/` files and structures

2. **Cross-reference phase:**
   - Check each documented item exists
   - Check each implemented item is documented

3. **Pattern validation:**
   - Verify documented patterns match implementation
   - Check file paths are accurate

4. **Link validation:**
   - Test internal links in documentation
   - Verify file references resolve

5. **Report findings:**
   - Orphans: Exist but undocumented
   - Phantoms: Documented but missing
   - Broken links: Invalid references
   - Pattern compliance: Match/mismatch

**Alignment is read-only** - no modifications, just diagnostics.

### Step 4: Synthesize Findings

Collect outputs from all executed reviews:

**From Exploration (if run):**
- Entries discovered
- Gaps identified
- Relationships mapped

**From Clarity:**
- Issues found
- Suggestions approved
- Files modified

**From Questions:**
- Questions generated
- Questions added
- Themes identified

**From Alignment:**
- Orphan count
- Phantom count
- Broken links
- Compliance status

### Step 5: Prioritize Recommendations

**High Priority** (Breaking issues)
- Alignment: Missing implementations, broken links
- Clarity: Confusing core concepts

**Medium Priority** (Content gaps)
- Questions: Unanswered follow-ups
- Exploration: Missing relationships

**Low Priority** (Polish)
- Clarity: Minor improvements
- Style: Consistency tweaks

### Step 6: Report Results

```markdown
## Review Complete

**Requirement:** {original requirement}

### Reviews Executed

| Type | Status | Key Findings |
|------|--------|--------------|
| Exploration | Complete/Skipped | {entries} found |
| Clarity | Complete/Skipped | {issues} found, {applied} fixed |
| Questions | Complete/Skipped | {count} generated |
| Alignment | Complete/Skipped | {gaps} identified |

### Priority Recommendations

**High:** {numbered list}
**Medium:** {numbered list}
**Low:** {numbered list}

### Files Modified

{list with brief descriptions}

### Next Steps

- {context-specific actions}
```

## Key Principles

**Type Routing Matrix**

| Pattern | Route To |
|---------|----------|
| "review {file} for clarity" | Clarity only |
| "suggest questions for {file}" | Questions only |
| "check alignment" | Alignment only |
| "comprehensive review of {file}" | Clarity + Questions |
| "review chapter {N}" | Explore -> Clarity + Questions |

**Sequential Execution**
- Exploration -> Review -> Synthesis
- Each stage informs the next
- Don't parallelize within a review

**User Choice Points**
- Which review types to run
- Whether to apply clarity suggestions
- Which questions to add
- Alignment runs automatically (read-only, safe)

**Synthesis Over Pass-Through**
- Don't concatenate reports
- Extract key findings across reviews
- Prioritize by impact
- Provide actionable next steps

## Examples

### Example 1: Clarity review on specific file
```
Request: "Review chapters/6-patterns/2-self-improving-experts.md for clarity"

Execute:
- Skip exploration (file specified)
- Read file completely
- Identify 3 clarity issues
- Present suggestions
- User approves 2
- Apply changes
- Update frontmatter

Report: "2 clarity improvements applied"
```

### Example 2: Generate questions for content
```
Request: "Suggest follow-up questions for chapter 8"

Execute:
- Explore chapter 8 structure
- Find 4 relevant entries
- Generate questions for each
- Present: 12 questions total
- User selects 5
- Add to respective files

Report: "5 questions added across 4 files"
```

### Example 3: Alignment check
```
Request: "Check alignment between book and implementation"

Execute:
- Inventory CLAUDE.md references
- Scan .claude/ structure
- Cross-reference

Findings:
- 2 orphan commands (exist, undocumented)
- 1 phantom reference (documented, missing)
- 3 broken internal links

Report: "6 alignment issues found, 1 high priority"
```

### Example 4: Comprehensive chapter review
```
Request: "Comprehensive review of chapter 7"

Execute:
- Explore: Find 6 entries
- Alignment: Check chapter references
- Clarity: Review each entry
- Questions: Generate follow-ups

Synthesize:
- High: 1 broken link
- Medium: 3 clarity issues
- Low: 8 potential questions

Report with prioritized action list
```
