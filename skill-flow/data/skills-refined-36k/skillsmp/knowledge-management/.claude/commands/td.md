---
description: Post-task review and retrospective with auto-capture and session memory
---

# Post-Task Review & Retrospective

สร้าง retrospective พร้อม Before/After context และบันทึก session

## Usage

```
/td           # ถามว่างานเสร็จหรือยัง
/td done      # งานเสร็จแล้ว
/td pending   # ยังไม่เสร็จ รอทำต่อ
/td blocked   # ติดปัญหา
```

## Output

`$PROJECT_ROOT/docs/retrospective/YYYY-MM/retrospective_YYYY-MM-DD_hhmmss.md`

## Flow

```
/td → Determine Status → Auto-capture → Gather Info → Comment Issue → Create Retrospective → Update Focus → Commit Docs → Confirm
```

**Note:** สำหรับ tests, build, code review และสร้าง PR ให้ใช้ `/pr` ก่อนรัน `/td`

## Instructions

### Step 0: Read Current Focus

```bash
export TZ='Asia/Bangkok'
echo "=== Current Focus ==="
cat docs/current.md
```

เก็บค่า TASK และ ISSUE ไว้ใช้ใน steps ถัดไป

### Step 1: Determine Completion Status

**ถ้าไม่มี argument (`/td`):**

```
งานเสร็จหรือยัง?

1. เสร็จแล้ว (done)      → STATE = completed
2. ยังไม่เสร็จ (pending)  → STATE = pending
3. ติดปัญหา (blocked)    → STATE = blocked
```

**ถ้ามี argument:**
- `/td done` → STATE = completed
- `/td pending` → STATE = pending
- `/td blocked` → STATE = blocked

### Step 2: Auto-capture Git Context

```bash
export TZ='Asia/Bangkok'
echo "Date: $(date '+%Y-%m-%d')"
echo "Time: $(date '+%H:%M:%S')"
echo "Branch: $(git branch --show-current)"

echo "=== Changed Files ==="
git diff --name-only HEAD

echo "=== Staged Files ==="
git diff --cached --name-only

echo "=== Recent Commits (last 4 hours) ==="
git log --oneline -10 --since="4 hours ago"

echo "=== Status ==="
git status --short
```

### Step 3: Gather Session Info from User

ใช้ AskUserQuestion เพื่อรวบรวมข้อมูล:

1. **Tasks Done**: รายละเอียดงานที่ทำไป
2. **Test Status**: ผ่าน/ไม่ผ่าน (หรือใช้ `/pr` แล้วหรือยัง)
3. **Test Details**: รายละเอียดการทดสอบ
4. **Errors**: ข้อผิดพลาด (ถ้ามี)
5. **Additional Notes**: ข้อมูลเพิ่มเติม

### Step 4: Add Comment to Issue

**อ่าน issue number จาก `docs/current.md`:**

```bash
ISSUE=$(grep "^ISSUE:" docs/current.md | cut -d: -f2 | tr -d ' #')
echo "Issue: #$ISSUE"
```

**Auto-assign issue (ensure user is assigned):**

```bash
# Auto-assign to current user if not already assigned (silently skip on error)
gh issue edit "$ISSUE" --add-assignee @me 2>/dev/null || true
```

**เพิ่ม comment ใน issue:**

```bash
export TZ='Asia/Bangkok'

gh issue comment $ISSUE --body "$(cat <<EOF
## Session Summary

### Tasks Done

[user input - รายละเอียดงานที่ทำ]

### Test Results

| Test | Status |
|------|--------|
| Acceptance Criteria | [user input] |

### Test Details

[user input - รายละเอียดการทดสอบ]

### Errors (if any)

[user input - ข้อผิดพลาด หรือ "None"]

### Additional Notes

[user input - ข้อมูลเพิ่มเติม]

---

*Session: $(date '+%Y-%m-%d %H:%M')*
EOF
)"
```

### Step 5: Create Retrospective File

สร้างไฟล์ `docs/retrospective/YYYY-MM/retrospective_YYYY-MM-DD_hhmmss.md`

(ใช้ template ด้านล่าง)

### Step 6: Update Focus & Activity Log

**Update `docs/current.md`:**

```bash
export TZ='Asia/Bangkok'

# For completed
cat > docs/current.md << EOF
STATE: completed
TASK: [task from original focus]
SINCE: $(date '+%Y-%m-%d %H:%M')
ISSUE: #[issue-number]
EOF
```

**Append to `docs/logs/activity.log`:**

```bash
export TZ='Asia/Bangkok'
echo "$(date '+%Y-%m-%d %H:%M') | completed | [task]" >> docs/logs/activity.log
```

### Step 7: Check PR Status & Commit Docs

**IMPORTANT:** ห้าม commit docs ลง main/master โดยตรง ต้องตรวจสอบ PR status ก่อนเสมอ

#### 7.1 ตรวจสอบ Branch และ PR Status

```bash
export TZ='Asia/Bangkok'

CURRENT_BRANCH=$(git branch --show-current)
ISSUE=$(grep "^ISSUE:" docs/current.md | cut -d: -f2 | tr -d ' #')

echo "=== Current State ==="
echo "Branch: $CURRENT_BRANCH"
echo "Issue: #$ISSUE"

# ตรวจสอบว่าอยู่บน main/master หรือไม่
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
  echo "⚠️  On protected branch - need to create docs branch"
  PR_STATUS="NO_BRANCH"
else
  # ตรวจสอบ PR status สำหรับ branch ปัจจุบัน
  PR_INFO=$(gh pr list --head "$CURRENT_BRANCH" --state all --json number,state,url --jq '.[0]')

  if [ -z "$PR_INFO" ] || [ "$PR_INFO" = "null" ]; then
    echo "No PR found for branch $CURRENT_BRANCH"
    PR_STATUS="NO_PR"
  else
    PR_STATE=$(echo "$PR_INFO" | jq -r '.state')
    PR_NUMBER=$(echo "$PR_INFO" | jq -r '.number')
    echo "PR #$PR_NUMBER state: $PR_STATE"

    if [ "$PR_STATE" = "OPEN" ]; then
      PR_STATUS="OPEN"
    else
      PR_STATUS="CLOSED"  # MERGED or CLOSED
    fi
  fi
fi

echo "PR_STATUS: $PR_STATUS"
```

#### 7.2 Handle ตาม PR Status

**Case A: PR ยังเปิดอยู่ (OPEN)**

> **Note:** ต้องรัน section 7.1 ก่อนเพื่อให้ตัวแปร `PR_NUMBER` ถูกกำหนด

```bash
# PR ยังเปิดอยู่ → commit และ push ไปที่ PR เดิม
# ตรวจสอบว่า PR_NUMBER ถูกกำหนดแล้ว
if [ -z "$PR_NUMBER" ]; then
  echo "ERROR: PR_NUMBER variable is not set. Run section 7.1 first."
  exit 1
fi

echo "✓ PR #$PR_NUMBER is open - committing to existing PR"

# Check for docs changes
echo "=== Docs Changes ==="
git status --short docs/

# Stage all docs
git add docs/

# ตรวจสอบว่ามี changes ที่จะ commit หรือไม่
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

# Commit docs
git commit -m "$(cat <<'EOF'
docs: retrospective and session update for [TASK]

- Updated docs/current.md status
- Added activity log entry
- Created retrospective: [retrospective-file-path]

Related: #[issue-number]
EOF
)"

# Push to update PR (ensure upstream is configured)
CURRENT_BRANCH=$(git branch --show-current)
git push -u origin "$CURRENT_BRANCH"

echo "✓ Docs committed and pushed to PR #$PR_NUMBER"
```

**Case B: ไม่มี PR หรือ PR ถูก merged/closed แล้ว (NO_PR, CLOSED, NO_BRANCH)**

> **Note:** ต้องรัน section 7.1 ก่อนเพื่อให้ตัวแปร `ISSUE` ถูกกำหนด

```bash
# ไม่มี PR หรือ PR ปิดแล้ว → สร้าง branch และ PR ใหม่สำหรับ docs
echo "⚠️  No open PR - creating new docs branch and PR"

# ตรวจสอบว่า ISSUE ถูกกำหนดแล้ว
if [ -z "$ISSUE" ]; then
  echo "ERROR: ISSUE variable is not set. Run section 7.1 first."
  exit 1
fi

# 1. Stash uncommitted docs changes (ป้องกัน changes หาย)
git stash push -m "docs-temp-$ISSUE" -- docs/
echo "✓ Stashed docs changes"

# 2. Checkout main และ pull latest
git checkout main
git pull origin main

# 3. สร้าง docs branch ใหม่
DOCS_BRANCH="docs/$ISSUE-retrospective"
git checkout -b "$DOCS_BRANCH"
echo "✓ Created branch: $DOCS_BRANCH"

# 4. Pop stash เพื่อดึง docs changes กลับมา
git stash pop
echo "✓ Restored docs changes"

# 5. Stage docs
git add docs/

# 6. ตรวจสอบว่ามี changes ที่จะ commit หรือไม่
if git diff --cached --quiet; then
  echo "No changes to commit"
  exit 0
fi

# 7. Commit docs
git commit -m "$(cat <<'EOF'
docs: retrospective and session update for [TASK]

- Updated docs/current.md status
- Added activity log entry
- Created retrospective: [retrospective-file-path]

Related: #[issue-number]
EOF
)"

# 8. Push branch ใหม่
git push -u origin "$DOCS_BRANCH"

# 9. Detect base branch (prefer develop, fallback to default)
if git branch -r | grep -q "origin/develop"; then
  BASE_BRANCH="develop"
else
  BASE_BRANCH=$(git remote show origin | grep 'HEAD branch' | cut -d: -f2 | xargs)
fi
echo "Base branch: $BASE_BRANCH"

# 10. สร้าง PR ใหม่สำหรับ docs
gh pr create \
  --base "$BASE_BRANCH" \
  --title "docs: retrospective for #$ISSUE" \
  --body "$(cat <<'EOF'
## Summary

Session documentation update for issue #[issue-number]

## Changes

- Updated `docs/current.md` status
- Added activity log entry
- Created retrospective document

## Related

- Issue: #[issue-number]
- Original PR: #[original-pr-number] (merged)
EOF
)"

echo "✓ Docs PR created"
```

#### 7.3 Verify Commit

```bash
# Verify commit was created
git log -1 --oneline

# Show current branch
echo "Current branch: $(git branch --show-current)"
```

### Step 8: Check Documentation Updates

**ตรวจสอบว่าต้อง update เอกสารหรือไม่:**

| File | Check When |
|------|------------|
| `README.md` | เพิ่ม feature ใหม่, เปลี่ยน API, เปลี่ยน structure |
| `SETUP.md` | เปลี่ยนขั้นตอนการติดตั้ง |
| `SKILL.md` | เปลี่ยน skill definition |
| `CLAUDE.md` | เปลี่ยน rules หรือ conventions |
| `assets/commands/*.md` | เปลี่ยน command behavior |

**ถ้าพบว่าต้อง update:**

```markdown
📝 **Documentation Check**

การเปลี่ยนแปลงนี้อาจต้อง update เอกสาร:

| File | Reason |
|------|--------|
| `README.md` | [reason] |

ต้องการให้ update เอกสารเลยไหม?
```

### Step 9: Confirm & Remind

```markdown
## Session Complete ✓

### Summary
- Issue: #[issue-number] - Comment added
- Retrospective: docs/retrospective/[path]

### Next Steps
1. ใช้ `/pr` เพื่อรัน tests, build, review และสร้าง PR
2. รอ reviewer approve PR
3. แก้ไขตาม feedback (ถ้ามี)
4. ใช้ `/focus` เพื่อเริ่มงานใหม่
```

## Template (Retrospective)

```markdown
---
date: YYYY-MM-DDTHH:MM:SS+07:00
type: feature|bugfix|refactor|decision|discovery|config|docs
status: completed|pending|blocked
tags: [tag1, tag2]
branch: branch-name
issue: "#123"
duration: ~2h
files_changed:
  - path/to/file.go
---

# [Task Title]

## Session Metadata

| Field | Value |
|-------|-------|
| Date | YYYY-MM-DD |
| Time | HH:MM:SS (Asia/Bangkok) |
| Duration | estimated |
| Type | type |
| Status | completed/pending/blocked |
| Branch | branch |
| Issue | #123 |

---

## Context: Before

- **Problem**: ปัญหาที่เจอ
- **Existing Behavior**: พฤติกรรมเดิม
- **Why Change**: ทำไมต้องเปลี่ยน
- **Metrics**: ตัวเลขก่อนแก้

---

## Context: After

- **Solution**: วิธีแก้
- **New Behavior**: พฤติกรรมใหม่
- **Improvements**: สิ่งที่ดีขึ้น
- **Metrics**: ตัวเลขหลังแก้

---

## Test Results

| Test | Status | Details |
|------|--------|---------|
| Acceptance Criteria | ✅/❌ | |

---

## Decisions & Rationale

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| | | | |

---

## Session Summary

### Task Description
อธิบาย task

### Outcome
ผลลัพธ์

---

## Technical Details

### Files Modified

| File | Changes |
|------|---------|
| `file.go` | changes |

### Recent Commits

```
# commits from auto-capture
```

---

## Honest Feedback

### What Went Well
-

### What Could Be Improved
-

---

## Lessons Learned

- Technical insights
- Process improvements

---

## Validation Checklist

- [ ] Acceptance criteria met
- [ ] Documentation updated (if needed)
- [ ] Used `/pr` for tests, build, review and PR creation
```

## Workflow Integration

```
┌─────────────────────────────────────────────────────────┐
│                   Development Flow                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   /focus  ──→  Work  ──→  /commit  ──→  /pr  ──→  /td   │
│      │                        │          │         │     │
│      │                        │          │         │     │
│   Create                   Atomic     Tests/     Session │
│   Issue                    Commits    Build/     Summary │
│                                       Review/            │
│                                       PR                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/focus` | ตั้ง focus และสร้าง issue |
| `/commit` | Atomic commits |
| `/pr` | รัน tests, build, review และสร้าง PR |
| `/td` | สร้าง retrospective (คุณอยู่ที่นี่) |
| `/recap` | ดู context |
| `/mem` | บันทึก knowledge |
