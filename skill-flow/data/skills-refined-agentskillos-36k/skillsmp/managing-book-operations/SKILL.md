---
name: managing-book-operations
description: Use when generating table of contents, validating metadata, or exploring book content. Triggers on "generate TOC", "table of contents", "validate frontmatter", "book chat".
---

# Managing Book Operations

Guide for book-level operations: table of contents generation, metadata validation, and conversational content exploration.

## Instructions

### Operation: TOC Generation

When regenerating the table of contents:

**Step 1: Scan Chapter Files**
```
Glob: chapters/**/*.md
Glob: appendices/**/*.md
```

**Step 2: Extract Frontmatter**

For each file, parse YAML frontmatter:
- `title` - entry title
- `part` - number
- `part_title` - part name
- `chapter` - number
- `section` - 0 for index, 1+ for sections
- `order` - sort key (part.chapter.section)

**Step 3: Sort and Group**
- Sort by `order` field (ascending)
- Group by `part_title` to create part sections
- Within parts, group by `chapter` number
- Section 0 files become chapter titles
- Section 1+ become bulleted items under chapters

**Step 4: Generate Markdown**

```markdown
# Table of Contents

## Part 1: Foundations

### Chapter 1: Foundations
- [Foundations](chapters/1-foundations/_index.md)
- [Twelve Leverage Points](chapters/1-foundations/1-twelve-leverage-points.md)

### Chapter 2: Prompt
- [Prompt](chapters/2-prompt/_index.md)
...
```

**Step 5: Write Output**

Write to: `TABLE_OF_CONTENTS.md` (overwrites existing)

**Step 6: Report**
```markdown
### TOC Generation Complete

Generated from {file_count} files across {part_count} parts.

**Output:** TABLE_OF_CONTENTS.md
**Chapters:** {count}
**Sections:** {count}
```

---

### Operation: Interactive Chat

When exploring book content conversationally:

**Step 1: Parse Input**
- Topic or question being asked
- Specific chapter/section references
- Conversation mode (clarification, exploration, connection)

**Step 2: Determine Scope**
- **Direct response**: Simple queries with targeted Grep + Read
- **Complex exploration**: Relationship mapping across chapters
- **Hybrid**: Initial answer + offer to go deeper

**Step 3a: Direct Response**

For straightforward questions:

1. Search: `Grep: {key concepts}`
2. Read: Load identified files
3. Synthesize:
   - Ground answer in book content
   - Provide 1-2 file citations
   - Match book's conversational voice
   - Suggest follow-up topics

**Step 3b: Complex Exploration**

For relationship mapping:

1. Find all related content across chapters
2. Map connections between concepts
3. Identify coverage gaps
4. Present findings conversationally

**Step 4: Format Response**

```markdown
The book addresses this through [concept] in Chapter X...

From `chapters/X/Y.md`:
> [relevant quote or paraphrase]

This connects to [related concept] because [explanation].

Want to explore [specific angle]? I can also map how this relates to [other topics].
```

**Grounding Rules:**
- Stay within documented content
- Acknowledge what's not covered
- Reference _questions.md for planned coverage
- Match book's practical, experience-based voice

---

### Operation: Metadata Validation

When validating frontmatter across book:

**Step 1: Define Scope**
- Path provided: Validate that chapter/section only
- No path: Validate all chapters/ and appendices/

**Step 2: Scan Files**
```
Glob: chapters/**/*.md
Glob: appendices/**/*.md
```

**Step 3: Check Each File**

**Required Fields:**
- `title` - present, non-empty
- `part` - numeric
- `part_title` - matches part number consistently
- `chapter` - numeric
- `section` - numeric (0 for index, 1+ for sections)
- `order` - format X.Y.Z, matches part.chapter.section

**Optional Fields (if present):**
- `description` - non-empty
- `created` - YYYY-MM-DD format
- `last_updated` - YYYY-MM-DD, >= created
- `tags` - array, no duplicates
- `status` - seedling | growing | mature | evergreen

**Consistency Checks:**
- All files in part have matching `part_title`
- `order` matches `part.chapter.section` pattern
- Section 0 files named `_index.md`
- No gaps in chapter/section numbering

**Step 4: Categorize Issues**

**Critical:**
- Missing required fields
- Invalid YAML syntax
- Incorrect order format

**Warnings:**
- Inconsistent part_title
- Numbering gaps
- last_updated before created

**Info:**
- Missing optional fields
- No status field

**Step 5: Report**

```markdown
### Metadata Validation Report

**Scope:** {description}
**Files Checked:** {count}

#### Critical Issues ({count})
| File | Issue | Fix Needed |
|------|-------|------------|
| {path} | Missing 'order' | Add order: X.Y.Z |

#### Warnings ({count})
| File | Issue | Recommendation |
|------|-------|----------------|
| {path} | Part title mismatch | Standardize to "{title}" |

#### Summary
- Valid: {count} files
- Warnings: {count} files
- Critical: {count} files
```

## Key Principles

**TOC Generation Algorithm**
- Always sort by `order` field, never filename
- Use relative paths from repo root
- Part -> Chapter -> Section hierarchy
- Overwrite existing (generated, not authored)
- Skip files without valid frontmatter

**Chat Grounding Rules**
- No speculation beyond documented content
- Match book voice: practical, experience-based
- Natural citations woven into response
- Acknowledge gaps explicitly
- Suggest captures for new insights

**Validation Priority**
- Critical = blocks TOC generation
- Warning = inconsistency, may cause confusion
- Info = enhancement opportunity

**File Naming Conventions**
- `_index.md` - Chapter introductions (section: 0)
- `_questions.md` - Question scaffolding (skip in TOC)
- `1-topic.md` - Numbered sections
- Descriptive kebab-case names

## Examples

### Example 1: Generate TOC
```
Request: "Regenerate table of contents"

Execute:
- Glob chapters/ and appendices/
- Extract frontmatter from 45 files
- Sort by order field
- Generate markdown structure

Output:
- TABLE_OF_CONTENTS.md updated
- 4 parts, 9 chapters, 32 sections
- 2 files skipped (missing frontmatter)
```

### Example 2: Chat about concept
```
Request: "How does the book cover prompt caching?"

Execute:
- Grep: "prompt caching", "cache"
- Find mentions in chapters 4 and 7
- Read relevant sections

Response:
"Chapter 4 (Context) discusses prompt caching in the strategies section...
From `chapters/4-context/2-context-strategies.md`:
> Caching system prompts reduces latency significantly...

The Practices chapter also touches on this from a cost perspective.
Want me to map all the performance-related content?"
```

### Example 3: Validate specific chapter
```
Request: "Validate frontmatter for chapter 6"

Execute:
- Glob: chapters/6-patterns/*.md
- Check 4 files

Findings:
- 1 warning: inconsistent part_title
- 1 info: missing status field
- 2 valid

Report with fix recommendations
```

### Example 4: Chat with gap acknowledgment
```
Request: "What does the book say about fine-tuning?"

Execute:
- Grep: "fine-tuning", "fine tuning"
- No direct coverage found
- Check _questions.md files

Response:
"The book doesn't currently cover fine-tuning in depth.
Chapter 3 (Model) has a placeholder question about when fine-tuning beats prompting.

This could be a good topic to capture. Want to explore related model behavior content instead?"
```
