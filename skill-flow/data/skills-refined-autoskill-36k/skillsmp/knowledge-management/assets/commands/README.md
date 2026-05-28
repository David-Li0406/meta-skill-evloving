# Claude Commands

ระบบ commands สำหรับจัดการ session และ knowledge ใน Claude Code

## Quick Start

```bash
/recap                          # เริ่ม session - โหลด context
/focus Implement feature X      # ตั้ง focus + สร้าง issue (ถามรายละเอียด)
# ... ทำงาน ...
/commit                         # commit แบบ atomic
/pr                             # test + build + review + สร้าง PR
/td done                        # สร้าง retrospective + comment issue
```

---

## Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                        SESSION START                            │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      /recap         │
                    │  โหลด context เดิม   │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      /focus         │
                    │  ตั้งงาน + สร้าง issue │
                    └─────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │         ทำงาน                   │
              │  /mem - บันทึก insight         │
              │  /commit - atomic commits      │
              │  /review - manual code review  │
              └────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        /pr          │
                    │  1. make test       │
                    │  2. make build      │
                    │  3. code review     │
                    │     (subagent)      │
                    │  4. create PR       │
                    │  (update issue ทุกstep)│
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        /td          │
                    │  1. ถาม status      │
                    │  2. gather info     │
                    │  3. comment issue   │
                    │  4. retrospective   │
                    └─────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                        SESSION END                               │
│  ⚠️ ห้าม merge PR เอง - รอ reviewer approve                      │
│  ⚠️ ห้ามปิด issue เอง - จะปิดอัตโนมัติเมื่อ PR merge             │
└─────────────────────────────────────────────────────────────────┘
                               │
                               │ (เมื่อได้รับ review)
                               ▼
                    ┌─────────────────────┐
                    │     /pr-review      │
                    │  1. ดู PR + reviews │
                    │  2. วิเคราะห์ feedback │
                    │  3. แก้ไข + reply   │
                    │  4. update issue    │
                    │  5. สร้าง learning  │
                    │  6. push changes    │
                    └─────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WAIT FOR RE-REVIEW                            │
│  รอ reviewer approve แล้ว merge PR                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Commands Reference

### Session Management

| Command | Description | Usage |
|---------|-------------|-------|
| `/recap` | โหลด context เริ่ม session | `/recap` |
| `/focus` | ตั้ง focus + สร้าง issue (GitHub/Jira) | `/focus [task description]` |
| `/td` | สร้าง retrospective + comment issue | `/td [done\|pending\|blocked]` |

### Git & Code

| Command | Description | Usage |
|---------|-------------|-------|
| `/commit` | Atomic commit (via tdg:atomic) | `/commit` |
| `/pr` | Test + Build + Review + Create PR | `/pr` |
| `/review` | Manual code review | `/review` |
| `/pr-review` | Handle PR review feedback | `/pr-review [pr-number]` |
| `/permission` | จัดการ permissions | `/permission suggest` |

### Knowledge Capture

| Command | Description | Usage |
|---------|-------------|-------|
| `/mem` | Quick knowledge capture | `/mem [title]` |
| `/distill` | Extract patterns จาก learnings | `/distill [topic]` |
| `/improve` | Work on pending improvements | `/improve` |

### Jira Integration

| Command | Description | Usage |
|---------|-------------|-------|
| `/jira init` | ตั้งค่า Jira credentials | `/jira init` |
| `/jira test` | ทดสอบ connection | `/jira test` |
| `/jira list` | แสดง issues ใน project | `/jira list [project] [status]` |
| `/jira my` | แสดง issues ที่ assign ให้ฉัน | `/jira my [status]` |
| `/jira get <key>` | ดู issue details | `/jira get PROJ-123` |
| `/jira create` | สร้าง issue ใหม่ | `/jira create` |
| `/jira search <query>` | ค้นหา issues | `/jira search "query"` |
| `/jira transitions <key>` | ดู transitions ที่ทำได้ | `/jira transitions PROJ-123` |
| `/jira transition <key> <id>` | เปลี่ยน status | `/jira transition PROJ-123 21` |
| `/jira comment <key> <text>` | เพิ่ม comment | `/jira comment PROJ-123 "text"` |

> See [references/jira-integration.md](../../references/jira-integration.md) for full documentation.

---

## /pr Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                            /pr                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐                                                   │
│  │make test │──fail──→ Comment Issue → Stop                     │
│  └────┬─────┘          (user fixes & reruns /pr)                │
│       │pass                                                      │
│       ▼                                                          │
│  ┌──────────┐                                                   │
│  │make build│──fail──→ Comment Issue → Stop                     │
│  └────┬─────┘          (user fixes & reruns /pr)                │
│       │pass                                                      │
│       ▼                                                          │
│  ┌───────────────┐                                              │
│  │ Code Review   │──fail──→ Comment Issue                       │
│  │  (subagent)   │              │                               │
│  └───────┬───────┘              ▼                               │
│          │              ┌───────────────┐                       │
│          │              │ Agent Auto-fix│                       │
│          │              └───────┬───────┘                       │
│          │                      │                               │
│          │              Comment Issue                           │
│          │                      │                               │
│          │              ◄───────┘ (re-review)                   │
│          │pass                                                  │
│          ▼                                                      │
│  ┌──────────┐                                                   │
│  │ git push │                                                   │
│  └────┬─────┘                                                   │
│       ▼                                                          │
│  ┌──────────┐                                                   │
│  │Create PR │──→ Comment Issue                                  │
│  └──────────┘                                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Issue Comments Timeline

| Step | Comment |
|------|---------|
| Test Start | 🧪 Running Tests |
| Test Pass | 🧪 Tests Passed ✅ |
| Test Fail | 🧪 Tests Failed ❌ |
| Build Pass | 🏗️ Build Passed ✅ |
| Build Fail | 🏗️ Build Failed ❌ |
| Review Start | 🔍 Code Review Started |
| Review Pass | 🔍 Code Review Passed ✅ |
| Review Fail | 🔍 Code Review Failed ❌ |
| Auto-fix | 🔧 Auto-fix Applied |
| PR Created | 🎉 Pull Request Created |

---

## Issue Tracker Integration

`/focus` รองรับทั้ง GitHub Issues และ Jira:

| Tracker | Setup | Usage |
|---------|-------|-------|
| GitHub Issues | ไม่ต้องตั้งค่า (default) | เลือก "GitHub Issues" |
| Jira | `/jira init` ครั้งแรก | เลือก "Jira" หรือ "Jira (existing)" |

```
/focus [task]
     │
     ├── ถ้ามี Jira config ──→ เลือก: GitHub / Jira (new) / Jira (existing)
     │
     └── ถ้าไม่มี Jira ──→ ใช้ GitHub Issues (default)
```

---

## Issue Format (GitHub)

เมื่อใช้ `/focus` จะถามข้อมูลและสร้าง issue ด้วย format:

```markdown
## Overview
Brief description of the feature/bug.

## Current State
What exists now.

## Proposed Solution
What should be implemented.

## Technical Details
- Components affected
- Implementation approach

## Acceptance Criteria
- [ ] Specific testable criteria
- [ ] Performance requirements
- [ ] UI/UX requirements
```

---

## Comment Format

เมื่อใช้ `/td` จะเพิ่ม comment ใน issue:

```markdown
## Session Summary

### Tasks Done
รายละเอียดงานที่ทำไป

### Test Results
| Test | Status |
|------|--------|
| Acceptance Criteria | ✅/❌ |

### Errors (if any)
ข้อผิดพลาด

### Additional Notes
ข้อมูลเพิ่มเติม
```

---

## PR Format

เมื่อใช้ `/pr` จะสร้าง PR ด้วย format:

```markdown
## Summary
Brief summary of the changes made.

## Changes Made
- List of key changes.

## Testing
| Test | Status |
|------|--------|
| Unit Tests | ✅ Passed |
| Build | ✅ Passed |
| Code Review | ✅ Passed |

## Related Issues
Fixes #issue_number
```

---

## Pre-Push Checklist (via /pr)

| Check | Command | Required |
|-------|---------|----------|
| Tests | `make test` | ✅ Must pass |
| Build | `make build` | ✅ Must pass |
| Code Review | Subagent | ✅ No critical issues |

**Note:** `/pr` จะรันทุกขั้นตอนนี้ให้อัตโนมัติพร้อม update issue ทุก step

---

## Forbidden Actions

| Action | Reason |
|--------|--------|
| ❌ Merge PR | ต้องรอ reviewer approve |
| ❌ Close Issue | จะปิดอัตโนมัติเมื่อ PR merge |
| ❌ Force Push | อันตราย ห้ามใช้ |
| ❌ Skip Tests | ต้อง pass ก่อน push |

---

## Knowledge Layer System

```
                    ระหว่างทำงาน
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: /mem                                                  │
│  Quick capture → docs/learnings/YYYY-MM/DD/HH.MM_slug.md       │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ (เมื่อมี 3+ learnings เรื่องเดียวกัน)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2: /distill                                              │
│  Extract patterns → docs/knowledge-base/topic.md               │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ (periodic review)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: /improve                                              │
│  Work on pending items from knowledge-base + retrospectives    │
└─────────────────────────────────────────────────────────────────┘
```

---

## State Machine

```
          /focus
ready ─────────────▶ working ──/td done──▶ completed
  ▲                     │                      │
  │                     │ /td pending          │
  │ /focus new          ▼                      │
  └───────────────── pending ◀────────────────┘
                        │        /focus new task
                        │
                        │ /td blocked
                        ▼
                     blocked
```

| State | Meaning | Next Action |
|-------|---------|-------------|
| `ready` | ว่าง รอ task | `/focus` เพื่อตั้งงาน |
| `working` | กำลังทำ | `/pr` แล้ว `/td` เมื่อจบ |
| `pending` | รอทำต่อ | `/recap` แล้ว `/focus` |
| `blocked` | ติดปัญหา | แก้ปัญหาก่อน |
| `completed` | เสร็จแล้ว | `/focus` งานใหม่ |

---

## Files Structure

```
docs/
├── current.md                    # STATE, TASK, SINCE, ISSUE
├── logs/
│   └── activity.log              # timestamp | state | task
├── retrospective/
│   └── YYYY-MM/
│       └── retrospective_*.md    # session summaries
├── learnings/
│   └── YYYY-MM/
│       └── DD/
│           └── HH.MM_slug.md     # quick captures (/mem)
├── knowledge-base/
│   └── topic.md                  # distilled patterns (/distill)
└── auto-captured/
    └── YYYY-MM/
        └── DD/
            └── HH.MM_session-*.md # auto-captured drafts
```

---

## Daily Workflow Example

```bash
# 1. เริ่ม session ใหม่
/recap                              # ดู context + state เดิม

# 2. ตั้ง focus + สร้าง issue
/focus Implement user login API     # จะถามรายละเอียดเพิ่มเติม

# 3. ทำงาน...
# - เขียน code
# - test
# - /mem "JWT token refresh pattern"  # บันทึก insight ระหว่างทาง
# - /commit                            # commit เมื่อเสร็จ chunk

# 4. สร้าง PR
/pr                                 # จะทำ:
                                    # - make test
                                    # - make build
                                    # - code review (subagent)
                                    # - create PR
                                    # (update issue ทุก step)

# 5. จบ session
/td done                            # จะทำ:
                                    # - ถาม session info
                                    # - comment issue
                                    # - สร้าง retrospective

# 6. (Weekly) Review และ distill
/distill error-handling             # รวม learnings เป็น knowledge
/improve                            # ทำ pending improvements
```

---

## Permission Management

ใช้ `/permission` เพื่อ pre-allow safe commands

### Usage

```bash
/permission              # แสดง permissions ปัจจุบัน + แนะนำ
/permission show         # แสดง permissions ทั้งหมด
/permission suggest      # แนะนำ permissions ตาม project type
/permission add [type]   # เพิ่ม permissions ตาม preset
```

### Available Presets

| Preset | Commands |
|--------|----------|
| `node` | npm, bun, pnpm, yarn |
| `go` | go build, test, mod, fmt |
| `python` | pip, pytest, poetry, uv, ruff |
| `rust` | cargo commands |
| `make` | make targets |
| `docker` | docker, docker-compose |
| `git` | safe git operations |
| `gh` | GitHub CLI |
| `common` | ls, cat, grep, find, jq |

---

## Tips

1. **เริ่ม session ด้วย `/recap` เสมอ** - เพื่อโหลด context และรู้ว่ามีงานค้างไหม

2. **ใช้ `/focus` ก่อนเริ่มงาน** - จะถามรายละเอียดและสร้าง issue อัตโนมัติ

3. **`/mem` เมื่อพบ insight** - อย่ารอ จด immediately ก่อนลืม

4. **`/commit` แทน `git commit`** - ได้ atomic commits ที่ clean

5. **`/pr` ก่อนจบ session** - จะ test, build, review และสร้าง PR พร้อม update issue

6. **`/td` ทุกครั้งที่จบ session** - สร้าง retrospective และ comment issue

7. **`/distill` เมื่อมี 3+ learnings** - รวมเป็น reusable knowledge

8. **ห้าม merge PR หรือปิด issue เอง** - รอ reviewer approve

9. **`/pr-review` เมื่อได้รับ review** - จัดการ feedback และเรียนรู้จากมัน

---

## PR Review Workflow

เมื่อ PR ได้รับ review จาก reviewer:

```bash
# 1. ตรวจสอบ PR ที่ได้รับ review
/pr-review                      # ดู PR ของ current branch
/pr-review 42                   # ดู PR #42 เฉพาะเจาะจง
```

### What /pr-review Does

1. **ดู PR ที่ open** - หา PR ที่ได้รับ review แล้ว
2. **วิเคราะห์ feedback** - แยกประเภท comment (ต้องแก้/พิจารณา/รับทราบ)
3. **แก้ไขตาม feedback** - อ่าน code และแก้ไขตามที่ reviewer แนะนำ
4. **Reply comments** - ตอบกลับแต่ละ comment ว่าทำอะไรไปบ้าง
5. **Update issue** - เพิ่ม progress comment ใน related issues
6. **สร้าง learning doc** - บันทึกสิ่งที่เรียนรู้จาก review
7. **Commit และ push** - push changes เพื่อ update PR

### Example Flow

```
PR Created → Reviewer comments → /pr-review → Fix + Reply → Re-review → Approved → Merge
```

---

## Related Files

- [CLAUDE.md](../../CLAUDE.md) - Project-level Claude instructions
- [docs/knowledge-base/](../../docs/knowledge-base/) - Distilled knowledge patterns
