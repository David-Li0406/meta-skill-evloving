# Merge and Deduplicate Lessons

Consolidate extracted lessons into a coherent, non-redundant collection.

## Input

A collection of extracted lessons (from extract_lessons), potentially with duplicates or overlapping content.

## Instructions

1. **Identify Duplicates**
   - Exact matches (same lesson, different wording)
   - Near-duplicates (same core insight, different examples)
   - Contradictions (lessons that conflict)

2. **Merge Similar Lessons**
   - Combine lessons with the same core insight
   - Keep the best examples from each
   - Use the highest confidence score
   - Preserve the earliest ID for tracking

3. **Resolve Contradictions**
   - If lessons genuinely conflict, note the contexts where each applies
   - Don't force-merge incompatible advice
   - Create a parent lesson that explains when to use each approach

4. **Organize by Category**
   - Group lessons under their categories
   - Order by confidence within each category
   - Add cross-references between related lessons

5. **Generate Final Output**
   - Human-readable markdown
   - Machine-readable JSONL

## Output Format

### Markdown (lessons.md)

```markdown
# Lessons Learned

Last updated: [DATE]

## Summary

- Total lessons: [N]
- By category: workflow ([N]), debugging ([N]), ...

## Workflow

### [Lesson Title]

**ID:** lesson-001
**Confidence:** 0.9

[Description]

---

### [Lesson Title]

...

## Debugging

...
```

### JSONL (lessons.jsonl)

One JSON object per line:

```jsonl
{"id":"lesson-001","category":"workflow","title":"...","description":"...","confidence":0.9,"examples":["..."],"caveats":["..."],"related":["lesson-005"]}
```

## Merge Rules

1. **Same insight, different wording**: Keep the clearer version
2. **Same insight, different examples**: Combine examples
3. **Conflicting insights**: Create context-specific variants
4. **Confidence scores**: Use max(scores) for merged lessons
5. **IDs**: Preserve the lowest ID, note merged IDs in metadata

## Quality Checks

- [ ] No duplicate lessons
- [ ] All lessons have unique IDs
- [ ] Categories are consistent
- [ ] Cross-references are valid
- [ ] No sensitive data in outputs
