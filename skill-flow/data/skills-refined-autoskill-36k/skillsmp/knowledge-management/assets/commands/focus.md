---
description: Set current focus - update docs/current.md and log to activity.log
---

# Set Focus

ตั้ง focus สำหรับงานใหม่ พร้อมสร้าง issue (GitHub หรือ Jira) ด้วย format มาตรฐาน

## Usage

```
/focus [task description]
```

## Instructions

### Step 1: Check Current State

```bash
export TZ='Asia/Bangkok'
echo "=== Current Focus ==="
cat docs/current.md

echo ""
echo "=== Git Status ==="
echo "Branch: $(git branch --show-current)"
git status --short
```

### Step 2: Handle Existing Focus

ถ้า `STATE` ไม่ใช่ `ready` หรือ `completed`:

```
มี focus อยู่แล้ว:
TASK: [current task]
STATE: [current state]

ต้องการ:
1. ทำต่องานเดิม (keep)
2. เปลี่ยนไปทำงานใหม่ (switch) - งานเดิมจะถูก mark เป็น pending
```

ถ้า user เลือก switch → เพิ่ม pending entry ใน `docs/logs/activity.log`

### Step 3: Get Task from User

ถ้าไม่มี argument:
```
งานที่จะทำคืออะไร?
```

ถ้ามี argument → ใช้เป็น task description

### Step 3.5: Choose Issue Tracker

ใช้ AskUserQuestion เพื่อเลือก issue tracker:

**ตรวจสอบ Jira config ก่อน:**
```bash
if [[ -f ".jira-config" ]] || [[ -f "$HOME/.config/claude-km/jira.conf" ]]; then
    echo "Jira: configured"
else
    echo "Jira: not configured"
fi
```

**ถ้ามี Jira config:**
```
เลือก Issue Tracker:
1. GitHub Issues - สร้าง GitHub issue ใหม่
2. Jira - สร้าง Jira issue ใหม่
3. Jira (existing) - ดึง Jira issue ที่มีอยู่มาทำ
```

**ถ้าไม่มี Jira config:**
ข้ามไป Step 4 (ใช้ GitHub เป็น default)

---

## Path A: GitHub Issues (Default)

### Step 4: Gather Issue Details

ใช้ AskUserQuestion เพื่อรวบรวมข้อมูลสำหรับ issue:

**ถามข้อมูลต่อไปนี้:**

1. **Type**: ประเภทของงาน
   - feat (new feature)
   - fix (bug fix)
   - refactor (code restructure)
   - docs (documentation)
   - test (testing)
   - chore (maintenance)

2. **Overview**: อธิบายสั้นๆ ว่างานนี้คืออะไร

3. **Current State**: สถานะปัจจุบันเป็นอย่างไร (ปัญหาที่เจอ, behavior เดิม)

4. **Proposed Solution**: วิธีแก้ไขที่เสนอ

5. **Technical Details**:
   - Components ที่เกี่ยวข้อง
   - Implementation approach

6. **Acceptance Criteria**: เกณฑ์การทดสอบ (อย่างน้อย 3 ข้อ)
   - Specific testable criteria
   - Performance requirements (ถ้ามี)
   - UI/UX requirements (ถ้ามี)

### Step 5: Create GitHub Issue

สร้าง GitHub issue ด้วย format มาตรฐาน:

```bash
export TZ='Asia/Bangkok'

gh issue create \
  --title "[type]: [descriptive title]" \
  --body "$(cat <<EOF
## Overview

[user input - brief description]

## Current State

[user input - what exists now]

## Proposed Solution

[user input - what should be implemented]

## Technical Details

- **Components affected:** [user input]
- **Implementation approach:** [user input]

## Acceptance Criteria

- [ ] [user input criteria 1]
- [ ] [user input criteria 2]
- [ ] [user input criteria 3]

---

## Session Info

- **Started:** $(date '+%Y-%m-%d %H:%M')
- **Branch:** [type]/[issue-number]-[short-slug]
- **Status:** In Progress
EOF
)"
```

เก็บ issue number ที่ได้ (เช่น `#123`) ไว้ใช้ใน Step 6

### Step 5.5: Auto-assign Issue (GitHub)

**อัตโนมัติ assign user ให้กับ issue:**

```bash
# Get issue number from creation output
ISSUE_NUMBER=[issue-number-from-step-5]

# Auto-assign to current user (silently skip on error)
if gh issue edit "$ISSUE_NUMBER" --add-assignee @me 2>/dev/null; then
    echo "✓ Assigned issue #$ISSUE_NUMBER to you"
else
    echo "→ Auto-assign skipped (already assigned or no permission)"
fi
```

**Edge Cases Handled:**
- Issue already has assignee → adds as additional assignee
- User not authenticated → skips silently
- Permission denied → skips silently

**ไปที่ Step 6: Create Feature Branch**

---

## Path B: Jira (New Issue)

### Step 4B: Gather Jira Issue Details

ใช้ AskUserQuestion:

1. **Project Key**: รหัส project ใน Jira (e.g., PROJ)
2. **Issue Type**: Task, Bug, Story, Epic
3. **Summary**: หัวข้อ issue
4. **Description**: รายละเอียด

### Step 5B: Create Jira Issue

```bash
# Get Jira type to git type mapping
# Bug -> fix, Task/Story/Epic -> feat, Improvement -> refactor
JIRA_TYPE="[selected type]"
case "$JIRA_TYPE" in
    Bug) GIT_TYPE="fix" ;;
    Improvement) GIT_TYPE="refactor" ;;
    *) GIT_TYPE="feat" ;;
esac

# Create issue
RESULT=$(./scripts/jira-client.sh create "[PROJECT]" "[SUMMARY]" "[DESCRIPTION]" "[JIRA_TYPE]")
ISSUE_KEY=$(echo "$RESULT" | grep -E '^[A-Z]+-[0-9]+$' | head -1)

echo "Created: $ISSUE_KEY"
```

เก็บ `ISSUE_KEY` (เช่น `PROJ-123`) ไว้ใช้ใน Step 6

**ไปที่ Step 6: Create Feature Branch**

---

## Path C: Jira (Existing Issue)

### Step 4C: Select Existing Jira Issue

**แสดง issues ที่ assign ให้ user:**
```bash
./scripts/jira-client.sh my-issues
```

**หรือ list issues ใน project:**
```bash
./scripts/jira-client.sh list [PROJECT] "To Do"
```

**ถาม user:**
```
ใส่ Issue Key ที่ต้องการทำ (e.g., PROJ-123):
```

### Step 5C: Fetch Issue Details

```bash
./scripts/jira-client.sh get [ISSUE_KEY]
```

**Map Jira type to git type:**
```bash
JIRA_TYPE=$(./scripts/jira-client.sh get [ISSUE_KEY] | jq -r '.type')
case "$JIRA_TYPE" in
    Bug) GIT_TYPE="fix" ;;
    Improvement) GIT_TYPE="refactor" ;;
    *) GIT_TYPE="feat" ;;
esac
```

**ไปที่ Step 6: Create Feature Branch**

---

## Step 6: Create Feature Branch (Required)

**ข้อบังคับ:** ถ้าอยู่บน `main`, `master`, หรือ default branch ต้องสร้าง branch ใหม่เสมอ

```bash
export TZ='Asia/Bangkok'

CURRENT_BRANCH=$(git branch --show-current)
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')

# ถ้าไม่มี default branch ให้ใช้ main หรือ master
if [ -z "$DEFAULT_BRANCH" ]; then
  if git show-ref --verify --quiet refs/heads/main; then
    DEFAULT_BRANCH="main"
  else
    DEFAULT_BRANCH="master"
  fi
fi

# ตรวจสอบว่าอยู่บน main/master/default branch หรือไม่
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ] || [ "$CURRENT_BRANCH" = "$DEFAULT_BRANCH" ]; then
  echo "Currently on $CURRENT_BRANCH - creating feature branch..."

  # สร้าง branch name
  # GitHub: [type]/[issue-number]-[short-slug]
  # Jira: [type]/[ISSUE-KEY]-[short-slug]

  git checkout -b "[type]/[issue-id]-[short-slug]"
  echo "Created and switched to branch: [type]/[issue-id]-[short-slug]"
else
  echo "Already on feature branch: $CURRENT_BRANCH"
fi
```

**Branch Naming Convention:**

| Type | Branch Prefix | GitHub Example | Jira Example |
|------|---------------|----------------|--------------|
| feat | `feat/` | `feat/123-add-auth` | `feat/PROJ-123-add-auth` |
| fix | `fix/` | `fix/45-login-bug` | `fix/PROJ-45-login-bug` |
| refactor | `refactor/` | `refactor/67-simplify` | `refactor/PROJ-67-simplify` |
| docs | `docs/` | `docs/89-readme` | `docs/PROJ-89-readme` |

**Short slug rules:**
- ใช้ lowercase
- แทนที่ space ด้วย `-`
- ตัดคำที่ไม่จำเป็นออก (a, an, the)
- จำกัดความยาวไม่เกิน 30 ตัวอักษร

## Step 7: Update Files

**Update `docs/current.md`:**

For GitHub:
```bash
export TZ='Asia/Bangkok'
cat > docs/current.md << EOF
STATE: working
TASK: [task description from user]
SINCE: $(date '+%Y-%m-%d %H:%M')
ISSUE: #[issue-number]
BRANCH: [type]/[issue-number]-[short-slug]
EOF
```

For Jira:
```bash
export TZ='Asia/Bangkok'
cat > docs/current.md << EOF
STATE: working
TASK: [ISSUE_KEY] - [summary]
SINCE: $(date '+%Y-%m-%d %H:%M')
ISSUE: [ISSUE_KEY]
BRANCH: [type]/[ISSUE_KEY]-[short-slug]
JIRA_URL: https://[domain]/browse/[ISSUE_KEY]
EOF
```

**Append to `docs/logs/activity.log`:**

```bash
export TZ='Asia/Bangkok'
echo "$(date '+%Y-%m-%d %H:%M') | working | [task description] ([issue-id])" >> docs/logs/activity.log
```

## Step 8: Jira Post-Setup (Jira only)

**Transition to In Progress (if available):**
```bash
# Get available transitions
./scripts/jira-client.sh transitions [ISSUE_KEY]

# Apply "In Progress" or similar transition
./scripts/jira-client.sh transition [ISSUE_KEY] [transition_id]
```

**Assign to self:**
```bash
./scripts/jira-client.sh assign [ISSUE_KEY] me
```

## Step 9: Confirm

**For GitHub:**
```markdown
## Focus Set

**Issue Created:** #[issue-number]
**Title:** [type]: [title]
**Branch:** [type]/[issue-number]-[short-slug]

STATE: working
TASK: [task]
SINCE: [timestamp]

### Acceptance Criteria
- [ ] [criteria 1]
- [ ] [criteria 2]
- [ ] [criteria 3]

พร้อมเริ่มงาน! ใช้ `/td` เมื่อจบ session
```

**For Jira:**
```markdown
## Focus Set

**Jira Issue:** [ISSUE_KEY]
**Summary:** [summary]
**URL:** https://[domain]/browse/[ISSUE_KEY]
**Branch:** [type]/[ISSUE_KEY]-[short-slug]

STATE: working
TASK: [ISSUE_KEY] - [summary]
SINCE: [timestamp]

Status: In Progress
Assigned to: you

พร้อมเริ่มงาน! ใช้ `/td` เมื่อจบ session
```

## Issue Title Format

| Type | Prefix | Example |
|------|--------|---------|
| feature | `feat:` | `feat: Add user authentication` |
| bug fix | `fix:` | `fix: Resolve login timeout` |
| refactor | `refactor:` | `refactor: Simplify auth middleware` |
| docs | `docs:` | `docs: Update API documentation` |
| test | `test:` | `test: Add unit tests for auth` |
| chore | `chore:` | `chore: Update dependencies` |

## Examples

```bash
# With argument
/focus Implement user authentication

# Without argument (will ask)
/focus
```

## States Reference

| State | Meaning | Next Action |
|-------|---------|-------------|
| `ready` | ว่าง รอ task | `/focus` เพื่อตั้งงาน |
| `working` | กำลังทำ | `/td` เมื่อจบ |
| `pending` | รอทำต่อ | `/recap` แล้ว `/focus` |
| `blocked` | ติดปัญหา | แก้ปัญหาก่อน |
| `completed` | เสร็จแล้ว | `/focus` งานใหม่ |

## Related Commands

| Command | Description |
|---------|-------------|
| `/jira init` | ตั้งค่า Jira credentials |
| `/jira list` | ดู Jira issues |
| `/jira transitions` | ดู transitions ที่ทำได้ |
| `/td` | จบ session + retrospective |
