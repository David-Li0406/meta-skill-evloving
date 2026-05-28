# /improve Workflow

## Scan Order (Priority)

1. `docs/knowledge-base/` - Patterns to apply (Priority 1)
2. `docs/retrospective/` - Future Improvements (Priority 2)
3. `docs/learnings/` - Gotchas to fix (Priority 3, skip "Distilled")

## Scan Commands

```bash
# Find knowledge-base files
find $PROJECT_ROOT/docs/knowledge-base -name "*.md" -type f | sort -r

# Find retrospective files
find $PROJECT_ROOT/docs/retrospective -name "*.md" -type f | sort -r

# Find learning files (check if not yet distilled)
find $PROJECT_ROOT/docs/learnings -name "*.md" -type f | sort -r
```

## Extract Actionable Items

### From Knowledge Base (Priority 1)

- "## When to Apply" conditions ที่ยังไม่ได้ implement
- Patterns ที่ยังไม่ได้ใช้ในโค้ด
- Anti-patterns ที่ยังมีอยู่ในโค้ด

### From Retrospectives (Priority 2)

- "### Future Improvements" section
- Items ที่ยังไม่ได้ทำ (`- [ ]`)

### From Learnings (Priority 3)

- "## Gotchas & Warnings" ที่ควรแก้ไข
- Actionable items จาก "## What We Learned"
- **Skip** items ที่มี `> **Distilled:**`

## Present to User

```markdown
## Pending Improvements

### From Knowledge Base - Priority 1

kafka-consumer-error-handling.md:
1. [ ] Apply retry pattern to all consumers
2. [ ] Add dead letter queue for failed messages

### From Retrospectives - Priority 2

retrospective_2025-12-23_143000.md:
3. [ ] Add consumer mocks to Makefile
4. [ ] Consider round.status = "settled" after all bets processed

### From Learnings - Priority 3

14.30_redis-connection-issue.md:
5. [ ] Document Redis pubsub patterns in CLAUDE.md
```

## User Selection

Ask:
- "เลือก item ที่ต้องการทำ (ระบุหมายเลข หรือ 'all')"
- หรือ "skip" เพื่อข้าม

## Execute

For each selected item:

1. วิเคราะห์ว่าต้องทำอะไร
2. วางแผนและ implement
3. ทดสอบ (run tests)
4. Commit with atomic commits
5. Update source file:
   - Knowledge Base: เพิ่ม changelog entry
   - Retrospective: เปลี่ยน `- [ ]` เป็น `- [x]`
   - Learning: เพิ่ม note ว่า resolved

## Output Summary

```markdown
## Completed Improvements

- [x] Add consumer mocks to Makefile (commit: abc1234)
- [ ] Consider round.status = "settled" (skipped - needs discussion)

Updated files:
- docs/retrospective/2025-12/retrospective_2025-12-23_143000.md
```

## Notes

- Prioritize knowledge-base items เพราะเป็น curated patterns
- ถ้า item ต้องการ discussion หรือ approval ให้ถามก่อน
- Update source file หลังทำเสร็จแต่ละ item
