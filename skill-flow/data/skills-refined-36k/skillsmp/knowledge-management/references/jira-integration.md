# Jira Integration Guide

คู่มือการใช้งาน Jira integration สำหรับ Claude KM Skill

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Configuration Options](#configuration-options)
4. [Commands Reference](#commands-reference)
5. [Workflows](#workflows)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### 1. Atlassian Cloud Account

ต้องมี account บน Atlassian Cloud (*.atlassian.net)

### 2. API Token

สร้าง API Token:

1. ไปที่ https://id.atlassian.com/manage-profile/security/api-tokens
2. คลิก **Create API token**
3. ใส่ชื่อ token (e.g., "Claude KM Skill")
4. Copy token เก็บไว้ (จะเห็นได้ครั้งเดียว)

### 3. Project Access

ต้องมี access ไปยัง Jira project ที่ต้องการใช้งาน

---

## Initial Setup

### วิธีที่ 1: Interactive Setup (แนะนำ)

```bash
/jira init
```

จะถาม:
- Jira Domain (e.g., `mycompany.atlassian.net`)
- Email (Atlassian account email)
- API Token
- Default Project Key (e.g., `PROJ`)

### วิธีที่ 2: Manual Configuration

สร้างไฟล์ `.jira-config` ใน project root:

```bash
# .jira-config
JIRA_DOMAIN="mycompany.atlassian.net"
JIRA_EMAIL="your-email@example.com"
JIRA_API_TOKEN="your-api-token-here"
JIRA_PROJECT="PROJ"
```

**สำคัญ:** ไฟล์นี้มี credentials - ถูกเพิ่มใน `.gitignore` แล้ว

### วิธีที่ 3: User-level Configuration

สำหรับใช้งานหลาย projects:

```bash
/jira init user
```

หรือสร้างไฟล์ `~/.config/claude-km/jira.conf`:

```bash
mkdir -p ~/.config/claude-km
cat > ~/.config/claude-km/jira.conf << 'EOF'
JIRA_DOMAIN="mycompany.atlassian.net"
JIRA_EMAIL="your-email@example.com"
JIRA_API_TOKEN="your-api-token-here"
JIRA_PROJECT="PROJ"
EOF
chmod 600 ~/.config/claude-km/jira.conf
```

### ทดสอบ Connection

```bash
/jira test
```

Expected output:
```
Testing connection to mycompany.atlassian.net...
Connected as: John Doe (john@example.com)
```

---

## Configuration Options

### Config Priority

| Priority | Location | Use Case |
|----------|----------|----------|
| 1 (สูงสุด) | `.jira-config` | Project-specific settings |
| 2 | `~/.config/claude-km/jira.conf` | User default settings |
| 3 | Environment variables | CI/CD หรือ temporary override |

### Environment Variables

```bash
export JIRA_DOMAIN="mycompany.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
export JIRA_PROJECT="PROJ"
```

---

## Commands Reference

### Configuration Commands

#### `/jira init`
ตั้งค่า credentials แบบ interactive

```bash
/jira init          # Project-level config
/jira init user     # User-level config
```

#### `/jira test`
ทดสอบ connection กับ Jira

```bash
/jira test
```

#### `/jira status`
แสดงสถานะ configuration

```bash
/jira status
```

---

### Issue Management Commands

#### `/jira list`
แสดง issues ใน project

```bash
/jira list                      # All issues (default project)
/jira list PROJ                 # Specific project
/jira list PROJ "To Do"         # Filter by status
/jira list PROJ "In Progress" 50  # Limit results
```

Output:
```
KEY        STATUS       SUMMARY
PROJ-123   To Do        Fix login bug
PROJ-124   In Progress  Add search feature
PROJ-125   Done         Update documentation
```

#### `/jira my`
แสดง issues ที่ assign ให้ฉัน

```bash
/jira my                    # All my issues
/jira my "To Do"            # Only To Do
/jira my "In Progress" 10   # Limit to 10
```

#### `/jira get`
ดูรายละเอียด issue

```bash
/jira get PROJ-123
```

Output:
```json
{
  "key": "PROJ-123",
  "summary": "Fix login bug",
  "status": "In Progress",
  "type": "Bug",
  "priority": "High",
  "assignee": "John Doe",
  "url": "https://mycompany.atlassian.net/browse/PROJ-123"
}
```

#### `/jira create`
สร้าง issue ใหม่ (interactive)

```bash
/jira create
```

จะถาม:
- Project Key
- Issue Type (Task, Bug, Story, Epic)
- Summary
- Description

#### `/jira search`
ค้นหา issues

```bash
/jira search "login error"           # Search in default project
/jira search "login error" PROJ      # Search in specific project
/jira search "login error" PROJ 30   # Limit results
```

**Technical Details:**

- ใช้ JQL (Jira Query Language) `text ~ "query"` สำหรับ text search (ค้นหาด้วย wildcard)
- ค้นหาใน summary, description, และ comments
- **Requirement:** Jira project ต้องเปิด text indexing (default enabled)
- ถ้าค้นหาไม่เจอ ตรวจสอบที่ Project Settings > Features > Text Indexing

**Search Tips:**

```bash
# Exact phrase (ใส่ quotes)
/jira search "user login failed"

# Multiple words (OR by default)
/jira search "login authentication"

# Wildcard
/jira search "auth*"
```

---

### Status Management Commands

#### `/jira transitions`
แสดง transitions ที่ทำได้

```bash
/jira transitions PROJ-123
```

Output:
```
ID    NAME
11    To Do
21    In Progress
31    Done
```

#### `/jira transition`
เปลี่ยน status ของ issue ผ่าน workflow transition

```bash
# ต้องใช้ transition ID (ตัวเลข) จาก /jira transitions
/jira transition PROJ-123 21  # 21 = In Progress (example)
/jira transition PROJ-123 31  # 31 = Done (example)
```

> **Note:** Jira ใช้ workflow transitions ไม่ใช่การเปลี่ยน status โดยตรง

---

### Other Commands

#### `/jira comment`
เพิ่ม comment

```bash
/jira comment PROJ-123 "Fixed the issue, ready for review"
```

#### `/jira assign`
Assign issue

```bash
/jira assign PROJ-123 me      # Assign to self
/jira assign PROJ-123 -1      # Unassign
/jira assign PROJ-123 [account_id]  # Assign to specific user
```

#### `/jira projects`
แสดง projects ทั้งหมด

```bash
/jira projects
```

---

## Workflows

### Workflow 1: สร้าง Issue ใหม่และเริ่มทำงาน

```bash
# 1. สร้าง issue ใหม่ผ่าน /focus
/focus Add user authentication

# เลือก "Jira" เมื่อถาม Issue Tracker
# กรอกข้อมูล issue

# Result:
# - Jira issue created: PROJ-123
# - Branch created: feat/PROJ-123-add-user-auth
# - Issue status: In Progress
# - Assigned to: you
```

### Workflow 2: ดึง Issue ที่มีอยู่มาทำ

```bash
# 1. ดู issues ที่ assign ให้
/jira my "To Do"

# 2. เริ่มทำงานผ่าน /focus
/focus
# เลือก "Jira (existing)"
# ใส่ PROJ-123

# Result:
# - Branch created: fix/PROJ-123-fix-login-bug
# - Issue status: In Progress
```

> **Note:** ไม่มีคำสั่ง `/jira start` โดยตรง ให้ใช้ `/focus` แล้วเลือก "Jira (existing)" แทน

### Workflow 3: จบงานและ Update Status

```bash
# 1. ทำงานเสร็จ ใช้ /td
/td

# 2. Update Jira status (ใช้ transition ID)
/jira transitions PROJ-123  # ดู transition IDs ที่ทำได้
/jira transition PROJ-123 31  # 31 = Done (example ID)

# หรือเพิ่ม comment
/jira comment PROJ-123 "Completed. PR #45 merged."
```

### Workflow 4: Daily Standup - ดู Issues ของตัวเอง

```bash
# ดู issues ทั้งหมดที่ assign ให้
/jira my

# ดูเฉพาะ In Progress
/jira my "In Progress"

# ดูเฉพาะ To Do
/jira my "To Do"
```

---

## Integration with Other Commands

### /focus + Jira

`/focus` รองรับ 3 modes:

| Mode | Description |
|------|-------------|
| GitHub Issues | สร้าง GitHub issue (default) |
| Jira | สร้าง Jira issue ใหม่ |
| Jira (existing) | ดึง Jira issue ที่มีมาทำ |

### /recap + Jira

`/recap` จะแสดง Jira URL ถ้า `docs/current.md` มี `JIRA_URL`:

```
STATE: working
TASK: PROJ-123 - Fix login bug
ISSUE: PROJ-123
JIRA_URL: https://mycompany.atlassian.net/browse/PROJ-123
```

### Branch Naming with Jira

| Jira Issue Type | Git Branch Prefix | Example |
|-----------------|-------------------|---------|
| Bug | `fix/` | `fix/PROJ-123-login-error` |
| Task | `feat/` | `feat/PROJ-124-add-search` |
| Story | `feat/` | `feat/PROJ-125-user-profile` |
| Epic | `feat/` | `feat/PROJ-126-auth-system` |
| Improvement | `refactor/` | `refactor/PROJ-127-cleanup` |

---

## Troubleshooting

### Error: Missing required configuration

```
Error: Missing required configuration: JIRA_DOMAIN JIRA_EMAIL JIRA_API_TOKEN
```

**Solution:** รัน `/jira init` เพื่อตั้งค่า

### Error: Connection failed

```
Testing connection to mycompany.atlassian.net...
Connection failed: Unauthorized
```

**Possible causes:**
1. API Token ไม่ถูกต้อง → สร้าง token ใหม่
2. Email ไม่ถูกต้อง → ใช้ email ของ Atlassian account
3. Domain ผิด → ตรวจสอบ URL ของ Jira

### Error: Issue not found

```
Error: Issue not found: PROJ-123
```

**Possible causes:**
1. Issue key ผิด → ตรวจสอบ key
2. ไม่มี permission → ติดต่อ admin

### Error: Permission denied

```
Error: Permission denied for PROJ-123
```

**Solution:** ติดต่อ Jira admin เพื่อขอ access

### Error: jq not found

```
./scripts/jira-client.sh: line XX: jq: command not found
```

**Solution:** ติดตั้ง jq

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# CentOS/RHEL
sudo yum install jq
```

---

## Security Best Practices

1. **ไม่ commit credentials** - `.jira-config` ถูกเพิ่มใน `.gitignore` แล้ว
2. **ใช้ user-level config** - ถ้าทำงานหลาย projects
3. **Rotate API tokens** - เปลี่ยน token เป็นระยะ
4. **Minimum permissions** - ใช้ token ที่มี permission เท่าที่จำเป็น

---

## Quick Reference Card

```bash
# Setup
/jira init              # Configure Jira
/jira test              # Test connection

# Browse Issues
/jira list [project]    # List issues
/jira my                # My issues
/jira get <key>         # Issue details
/jira search <query>    # Search

# Work with Issues
/jira create            # Create new issue
/focus                  # Start work (select "Jira existing")
/jira transitions <key> # List available transitions
/jira transition <key> <id>  # Change status
/jira comment <key> <text>   # Add comment
/jira assign <key> me   # Assign to self

# Projects
/jira projects          # List all projects
```
