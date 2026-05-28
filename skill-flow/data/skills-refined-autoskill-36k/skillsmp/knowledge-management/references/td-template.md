# /td Template

## File Path

```
docs/retrospective/YYYY-MM/retrospective_YYYY-MM-DD_hhmmss.md
```

## Frontmatter

```yaml
---
date: YYYY-MM-DDTHH:MM:SS+07:00
type: feature|bugfix|refactor|decision|discovery|config|docs
tags: [tag1, tag2]
branch: branch-name
issue: "#123"
pr: "#456"
duration: ~2h
files_changed:
  - path/to/file1.go
  - path/to/file2.yaml
---
```

## Template

```markdown
# [Task Title]

## Session Metadata

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Time | HH:MM:SS (Asia/Bangkok) |
| Duration | estimated |
| Focus | task description |
| Type | Feature/Bugfix/Refactor/Decision/Discovery/Config/Docs |
| Branch | current branch |
| Issue | #number if applicable |
| PR | #number if applicable |

---

## Context: Before

> สถานะก่อนเริ่ม session - ปัญหา/สภาพเดิม

- **Problem**: อธิบายปัญหาที่เจอ
- **Existing Behavior**: พฤติกรรมเดิมเป็นยังไง
- **Why Change**: ทำไมต้องเปลี่ยน/แก้ไข
- **Metrics** (if applicable): ตัวเลขก่อนแก้ (error rate, latency, etc.)

---

## Context: After

> สถานะหลังจบ session - ผลลัพธ์

- **Solution**: อธิบาย solution ที่ implement
- **New Behavior**: พฤติกรรมใหม่เป็นยังไง
- **Improvements**: สิ่งที่ดีขึ้น
- **Metrics** (if applicable): ตัวเลขหลังแก้

---

## Decisions & Rationale

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| การตัดสินใจ | A, B, C | A | เหตุผลที่เลือก A |

---

## Session Summary

### Task Description
อธิบายสิ่งที่ต้องทำ

### Outcome
ผลลัพธ์ที่ได้

---

## Timeline

| Time | Activity |
|------|----------|
| HH:MM | กิจกรรม |

---

## Technical Details

### Files Modified

| File | Changes |
|------|---------|
| `path/to/file.go` | อธิบายการเปลี่ยนแปลง |

### Key Implementation Details

- Implementation detail 1
- Implementation detail 2

---

## Honest Feedback

### What Went Well
- สิ่งที่ทำได้ดี

### What Could Be Improved
- สิ่งที่ควรปรับปรุง

### Blockers Encountered
- อุปสรรคที่เจอ

---

## Lessons Learned

### Technical Insights
- ความรู้ทางเทคนิคที่ได้

### Process Improvements
- การปรับปรุง process

---

## Next Steps

### Immediate
- [ ] Task ที่ต้องทำทันที

### Future Improvements
- [ ] Task ที่ทำในอนาคต

---

## Validation Checklist

- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] Mocks regenerated (if interface changed)
- [ ] Changes committed with atomic commits
- [ ] No hardcoded values
- [ ] Error handling implemented
- [ ] Tracing/spans added
- [ ] Consistent with existing code patterns

---

## Related

- **Learnings**: link to /mem files
- **Knowledge Base**: link to /distill patterns
```

## Gather Context

```bash
# Current branch
git branch --show-current

# Changed files
git diff --name-only HEAD

# Recent commits
git log --oneline -10 --since="4 hours ago"

# Create directory
mkdir -p docs/retrospective/$(TZ='Asia/Bangkok' date '+%Y-%m')
```

## Commit

```bash
git add docs/retrospective/
git commit -m "docs(retro): [type] - [title]"
```

## Example: Bugfix

```markdown
---
date: 2025-12-23T14:30:00+07:00
type: bugfix
tags: [mongodb, timeout, connection-pool]
branch: fix/mongodb-timeout
issue: "#456"
duration: ~2h
files_changed:
  - internal/database/mongo.go
  - config/database.yaml
---

# Fix MongoDB Connection Timeout Under Load

## Context: Before

- **Problem**: MongoDB connections timeout under high load
- **Existing Behavior**: Error "context deadline exceeded" after 30s
- **Why Change**: 5% of requests failing during peak hours
- **Metrics**: p99 latency = 2s, error rate = 5%

## Context: After

- **Solution**: Increased connection pool + retry with exponential backoff
- **New Behavior**: Connections stable under load
- **Improvements**: Zero timeouts in load test
- **Metrics**: p99 latency = 200ms, error rate < 0.1%

## Decisions & Rationale

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| Pool size | 50, 100, 200 | 100 | Matches max concurrent requests |
| Retry strategy | Fixed, Exponential, Circuit Breaker | Exponential | Simpler, sufficient for transient issues |
```
