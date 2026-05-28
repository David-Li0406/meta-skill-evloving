---
description: Scan learnings and suggest topics to distill into knowledge base
---

# Knowledge Curator

Agent สำหรับ scan learnings และแนะนำ topics ที่ควร distill เป็น knowledge base entries

## Purpose

- Scan docs/learnings/ หา patterns
- Group related learnings by topic
- แนะนำ topics ที่มี 3+ learnings
- ช่วยเตรียม input สำหรับ `/distill`
- Track knowledge gaps

## When to Use

- Weekly/periodic knowledge review
- เมื่อมี learnings สะสมหลายรายการ
- ก่อนใช้ `/distill`
- เมื่อต้องการหา knowledge gaps

## Instructions

### Step 1: Scan Learnings Directory

```bash
# List all learnings
find docs/learnings -name "*.md" -type f | head -50

# Count learnings per month
find docs/learnings -name "*.md" | wc -l
```

### Step 2: Extract Topics from Each Learning

For each learning file:
1. Read the file content
2. Extract:
   - Title/slug from filename
   - Tags from frontmatter
   - Key concepts mentioned
   - Technology/tools mentioned

### Step 3: Group by Topic

Analyze and group learnings by:
- Common tags
- Similar titles
- Related technologies
- Problem domain

### Step 4: Identify Distill Candidates

A topic is ready for distill when:
- 3+ learnings on same topic
- Clear pattern emerges
- Reusable across projects
- Not already in knowledge-base

### Step 5: Check Existing Knowledge Base

```bash
# List existing knowledge base entries
ls -la docs/knowledge-base/
```

Compare with candidates to avoid duplicates.

### Step 6: Prioritize Topics

| Priority | Criteria |
|----------|----------|
| High | 5+ learnings, frequently referenced |
| Medium | 3-4 learnings, clear pattern |
| Low | 3 learnings, still evolving |

## Output Format

```markdown
## Knowledge Curation Report

**Learnings Scanned:** N files
**Date Range:** YYYY-MM-DD to YYYY-MM-DD
**Distill Candidates:** X topics

---

### Ready to Distill (3+ learnings)

#### 1. [Topic Name] ⭐ High Priority
**Learnings:** 5 files
**Pattern:** Brief description of the pattern

| File | Date | Key Point |
|------|------|-----------|
| `HH.MM_slug.md` | YYYY-MM-DD | Key insight |
| ... | ... | ... |

**Suggested Distill Title:** `topic-name.md`
**Suggested Tags:** tag1, tag2, tag3

---

#### 2. [Topic Name] 🔶 Medium Priority
[Similar format]

---

### Growing Topics (2 learnings)

These topics need 1 more learning before distill:

| Topic | Count | Latest |
|-------|-------|--------|
| [topic] | 2 | YYYY-MM-DD |

---

### Existing Knowledge Base

| Entry | Related Learnings | Last Updated |
|-------|-------------------|--------------|
| `topic.md` | 5 | YYYY-MM-DD |

---

### Knowledge Gaps

Areas with learnings but no knowledge base entry:
- [gap 1]
- [gap 2]

---

### Recommendations

1. **Distill Now:** [topic] - has 5+ learnings
2. **Watch:** [topic] - needs 1 more learning
3. **Review:** [existing entry] - might need update
```

## Topic Extraction Patterns

Look for these in learnings:

### Technology Topics
- Framework/library patterns
- Language-specific idioms
- Tool configurations
- API patterns

### Problem Domains
- Error handling patterns
- Performance optimization
- Security practices
- Testing strategies

### Process Topics
- Development workflows
- Debugging techniques
- Code review practices
- Documentation patterns

## Integration

- Run weekly or bi-weekly
- Feeds into `/distill` command
- Complements `/improve` workflow
- Track in activity log

## Example Workflow

```bash
# 1. Run knowledge curation
User: Scan my learnings and suggest what to distill

# 2. Agent produces report with candidates

# 3. User selects topic
User: Let's distill the "error-handling" topic

# 4. Use /distill command
/distill error-handling
```
