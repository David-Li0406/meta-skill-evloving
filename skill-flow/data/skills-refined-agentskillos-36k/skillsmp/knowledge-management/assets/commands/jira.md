---
description: Jira integration - create, list, fetch, and manage Jira issues
---

# Jira Integration

จัดการ Jira issues ผ่าน CLI รองรับ Atlassian Cloud

## Usage

```
/jira [command] [arguments]
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/jira init` | ตั้งค่า Jira credentials |
| `/jira test` | ทดสอบ connection |
| `/jira list` | แสดง issues ใน project |
| `/jira my` | แสดง issues ที่ assign ให้ฉัน |
| `/jira get <key>` | ดู issue details |
| `/jira create` | สร้าง issue ใหม่ |
| `/jira search <query>` | ค้นหา issues |
| `/jira transitions <key>` | ดู transitions ที่ทำได้ |
| `/jira transition <key> <id>` | เปลี่ยน status ด้วย transition ID |
| `/jira comment <key>` | เพิ่ม comment |

## Instructions

### Command: init

ตั้งค่า Jira credentials

```bash
./scripts/jira-client.sh init
```

**หลังจาก init สำเร็จ:**
```
Jira configured successfully!

ใช้ /jira test เพื่อทดสอบ connection
```

### Command: test

ทดสอบ connection กับ Jira

```bash
./scripts/jira-client.sh test
```

**Output:**
```
Testing connection to [domain]...
Connected as: [name] ([email])
```

### Command: list

แสดง issues ใน project

```bash
# Default project
./scripts/jira-client.sh list

# Specific project
./scripts/jira-client.sh list PROJ

# Filter by status
./scripts/jira-client.sh list PROJ "In Progress"
```

**แสดงผลในรูปแบบ table:**
```
KEY        STATUS       SUMMARY
PROJ-123   To Do        Fix login bug
PROJ-124   In Progress  Add search feature
PROJ-125   Done         Update docs
```

### Command: my

แสดง issues ที่ assign ให้ user

```bash
./scripts/jira-client.sh my-issues

# Filter by status
./scripts/jira-client.sh my-issues "To Do"
```

### Command: get

ดู issue details

```bash
./scripts/jira-client.sh get PROJ-123
```

**แสดงผล:**
```json
{
  "key": "PROJ-123",
  "summary": "Fix login bug",
  "status": "In Progress",
  "type": "Bug",
  "priority": "High",
  "assignee": "John Doe",
  "url": "https://company.atlassian.net/browse/PROJ-123"
}
```

### Command: create

สร้าง Jira issue ใหม่ (interactive)

**Step 1: ถามข้อมูล issue**

ใช้ AskUserQuestion:

```
สร้าง Jira Issue

1. Project Key (e.g., PROJ)
2. Issue Type (Task, Bug, Story, Epic)
3. Summary (หัวข้อ)
4. Description (รายละเอียด)
5. Priority (Highest, High, Medium, Low, Lowest)
```

**Step 2: สร้าง issue**

```bash
./scripts/jira-client.sh create "[PROJECT]" "[SUMMARY]" "[DESCRIPTION]" "[TYPE]"
```

**Step 3: แสดงผล**

```
Issue Created!

Key: PROJ-123
URL: https://company.atlassian.net/browse/PROJ-123
Summary: [summary]
Type: [type]

ใช้ /focus แล้วเลือก "Jira (existing)" เพื่อเริ่มทำงาน
```

### Workflow: Start Working on Issue

> **Note:** ไม่มีคำสั่ง `/jira start` โดยตรง ให้ใช้ `/focus` แล้วเลือก "Jira (existing)" แทน
> หรือทำ workflow ด้านล่างนี้ด้วยตัวเอง

เริ่มทำงาน Jira issue - ดึงมาเป็น current focus

**Step 1: ดึงข้อมูล issue**

```bash
./scripts/jira-client.sh get [ISSUE_KEY]
```

**Step 2: สร้าง feature branch**

```bash
# Format: [type]/[issue-key]-[short-description]
# Type mapping from Jira issue type:
#   Bug -> fix
#   Story/Task -> feat
#   Epic -> feat
#   Improvement -> refactor

git checkout -b [type]/[ISSUE_KEY]-[slug]
```

**Step 3: Update docs/current.md**

```bash
export TZ='Asia/Bangkok'
cat > docs/current.md << EOF
STATE: working
TASK: [ISSUE_KEY] - [summary]
SINCE: $(date '+%Y-%m-%d %H:%M')
ISSUE: [ISSUE_KEY]
BRANCH: [branch-name]
JIRA_URL: [url]
EOF
```

**Step 4: Update activity.log**

```bash
export TZ='Asia/Bangkok'
echo "$(date '+%Y-%m-%d %H:%M') | working | [ISSUE_KEY] - [summary]" >> docs/logs/activity.log
```

**Step 5: Transition issue to "In Progress" (if available)**

```bash
# Get available transitions
./scripts/jira-client.sh transitions [ISSUE_KEY]

# If "In Progress" or similar transition exists, apply it
./scripts/jira-client.sh transition [ISSUE_KEY] [transition_id]
```

**Step 6: Assign to self**

```bash
./scripts/jira-client.sh assign [ISSUE_KEY] me
```

**Output:**
```
Started: [ISSUE_KEY]
Summary: [summary]
Branch: [branch]

Issue transitioned to: In Progress
Assigned to: you

Ready to work!
```

### Command: transition

เปลี่ยน status ของ issue ผ่าน Jira workflow transitions

**Step 1: แสดง available transitions**

```bash
./scripts/jira-client.sh transitions [ISSUE_KEY]
```

**Step 2: ถามว่าจะเปลี่ยนเป็น status ไหน**

ใช้ AskUserQuestion กับ options จาก transitions

**Step 3: Apply transition**

```bash
./scripts/jira-client.sh transition [ISSUE_KEY] [transition_id]
```

> **Note:** Jira ใช้ workflow transitions แทนการเปลี่ยน status โดยตรง ต้องใช้ transition ID (ตัวเลข) ไม่ใช่ชื่อ status

### Command: comment

เพิ่ม comment ใน issue

**Step 1: ถาม comment**

```
ใส่ comment สำหรับ [ISSUE_KEY]:
```

**Step 2: Add comment**

```bash
./scripts/jira-client.sh comment [ISSUE_KEY] "[comment]"
```

## Configuration

### First-time Setup

1. ไปที่ https://id.atlassian.com/manage-profile/security/api-tokens
2. สร้าง API Token
3. รัน `/jira init`

### Config File Locations

| Type | Location | Priority |
|------|----------|----------|
| Project | `.jira-config` | 1 (highest) |
| User | `~/.config/claude-km/jira.conf` | 2 |
| Environment | `JIRA_*` variables | 3 |

### Required Variables

```bash
JIRA_DOMAIN="company.atlassian.net"
JIRA_EMAIL="user@example.com"
JIRA_API_TOKEN="your-api-token"
JIRA_PROJECT="PROJ"  # default project
```

## Issue Type Mapping

| Jira Type | Git Branch Prefix |
|-----------|-------------------|
| Bug | `fix/` |
| Task | `feat/` |
| Story | `feat/` |
| Epic | `feat/` |
| Improvement | `refactor/` |
| Sub-task | `feat/` |

## Examples

```bash
# Setup
/jira init
/jira test

# Browse issues
/jira list PROJ
/jira my
/jira get PROJ-123

# Create issue
/jira create

# Start work (use /focus with Jira path)
/focus  # then select "Jira (existing)" and enter PROJ-123

# Change status (use transition ID from /jira transitions)
/jira transitions PROJ-123  # see available transitions
/jira transition PROJ-123 31  # 31 = Done (example ID)
/jira comment PROJ-123 "Fixed the issue"
```

## Integration with Other Commands

| Command | Jira Integration |
|---------|------------------|
| `/focus` | เลือกได้ว่าจะสร้าง GitHub Issue หรือ Jira |
| `/td` | อัพเดต Jira status เมื่อจบ session |
| `/recap` | แสดง Jira issue ถ้ามี |

## Error Handling

**Connection Error:**
```
Error: Failed to connect to Jira
Check your credentials with: /jira init
```

**Permission Error:**
```
Error: Permission denied for [ISSUE_KEY]
You may not have access to this project
```

**Invalid Issue:**
```
Error: Issue not found: [ISSUE_KEY]
Check the issue key and try again
```
