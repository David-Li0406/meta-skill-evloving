---
description: Extract patterns from learnings into knowledge base
---

# Distill - Extract Patterns & Lessons

สังเคราะห์ความรู้จาก /mem learnings เป็น patterns (Layer 2)

## Usage

```
/distill [topic-name]
```

**Input:** `docs/learnings/`
**Output:** `docs/knowledge-base/[topic-name].md`

## Instructions

1. **Scan learnings** for related content (3+ files on same topic)
2. **Analyze** for patterns, anti-patterns, insights
3. **Create** knowledge entry with template below
4. **Mark sources** as "Distilled"
5. **Commit**: `git commit -m "knowledge: [topic] - [summary]"`

## Template

```markdown
# [Topic Name]

| Field | Value |
|-------|-------|
| **Created** | YYYY-MM-DD |
| **Sources** | learnings ที่ใช้ |
| **Tags** | `tag1` `tag2` |

---

## Key Insight

> One-sentence summary

---

## The Problem

| Attempt | Result |
|---------|--------|
| ทำแบบ X | เกิดปัญหา Y |

---

## The Solution

### Pattern: [Name]

```go
// Code example
```

**Why this works:**
- Reason 1

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| Bad | Good |

---

## When to Apply

- ใช้เมื่อ...
- ไม่ใช้เมื่อ...

---

## Decision Rationale (Optional)

> ใช้เมื่อ knowledge นี้เกี่ยวข้องกับการตัดสินใจสำคัญ

### Decision

[สรุปการตัดสินใจ]

### Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Option A | ... | ... |
| **Chosen** ✓ | ... | ... |

### Why This Choice?

- เหตุผล 1
- เหตุผล 2

### Trade-offs Accepted

- ยอมรับ X เพื่อได้ Y

---

## Related

- Learnings: source files
- Code: relevant code paths
```

## After Distilling

Mark source learnings:
```markdown
> **Distilled:** → `docs/knowledge-base/[topic].md`
```

## When to Distill

| Trigger | Action |
|---------|--------|
| 3+ learnings เรื่องเดียวกัน | รวมเป็น knowledge |
| พบ pattern ใช้ซ้ำได้ | สร้าง knowledge |
| Weekly review | Scan pending learnings |
