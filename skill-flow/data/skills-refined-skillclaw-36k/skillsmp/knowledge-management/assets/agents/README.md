# Subagents

Automated workflow agents ตามแนวทาง [Boris Cherny](https://twitter.com/bcherny) - ผู้สร้าง Claude Code

## Quick Reference

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `code-reviewer` | Review code หา bugs, security, performance | ก่อน commit/push |
| `code-simplifier` | Simplify code ลด complexity | หลังเขียน code |
| `security-auditor` | ตรวจสอบ OWASP Top 10 vulnerabilities | ก่อน push |
| `knowledge-curator` | Scan learnings → แนะนำ distill topics | Weekly review |
| `session-analyzer` | วิเคราะห์ session → สร้าง retrospective | จบ session |
| `build-validator` | ตรวจสอบ build + tests + lint | ก่อน push |

---

## Usage

### วิธีเรียกใช้ Subagent

```
Use the [agent-name] agent to [task]
```

### ตัวอย่าง

```bash
# Review code ก่อน commit
Use the code-reviewer agent to review my changes

# Simplify code ที่เพิ่งเขียน
Use the code-simplifier agent to simplify the code I just wrote

# Security audit
Use the security-auditor agent to audit this project for vulnerabilities

# หา topics ที่ควร distill
Use the knowledge-curator agent to scan my learnings and suggest topics

# สร้าง retrospective draft
Use the session-analyzer agent to analyze this session

# Validate build ก่อน push
Use the build-validator agent to validate the build
```

---

## Agent Details

### 1. Code Reviewer

**Purpose:** ตรวจสอบ code quality ก่อน commit

**Checks:**
- Logic errors และ bugs
- Security vulnerabilities
- Performance issues
- Code style และ best practices
- Missing error handling

**Output:** Report พร้อม severity levels (Critical/Warning/Info)

**ใช้เมื่อ:**
- ก่อน `git commit`
- ก่อน `git push`
- กับ `/review` command

---

### 2. Code Simplifier

**Purpose:** ลด complexity และทำให้ code อ่านง่าย

**Checks:**
- Over-engineering
- Deep nesting
- Long functions
- Duplicate code
- Unnecessary abstractions

**Output:** Before/After suggestions พร้อมเหตุผล

**ใช้เมื่อ:**
- หลังเขียน code เสร็จ
- เมื่อ code ดู complex เกินไป
- ก่อน commit สำหรับ clean up

---

### 3. Security Auditor

**Purpose:** ตรวจสอบ security vulnerabilities ตาม OWASP Top 10

**Checks:**
- Injection (SQL, NoSQL, Command)
- Authentication/Authorization issues
- Sensitive data exposure
- Hardcoded secrets
- Security misconfiguration

**Output:** Security report พร้อม risk levels และ remediation

**ใช้เมื่อ:**
- ก่อน push ไป production
- Periodic security audit
- หลังเพิ่ม auth/sensitive features

---

### 4. Knowledge Curator

**Purpose:** Scan learnings และแนะนำ topics ที่ควร distill

**Checks:**
- Group learnings by topic
- หา topics ที่มี 3+ learnings
- ตรวจสอบกับ knowledge-base ที่มีอยู่
- Identify knowledge gaps

**Output:** Distill candidates พร้อม priority และ related learnings

**ใช้เมื่อ:**
- Weekly/bi-weekly review
- ก่อนใช้ `/distill`
- เมื่อมี learnings สะสมหลายรายการ

---

### 5. Session Analyzer

**Purpose:** วิเคราะห์ session และสร้าง retrospective draft

**Checks:**
- Git changes (files, commits)
- Session duration
- Type classification
- Before/After context extraction

**Output:** Retrospective draft พร้อม metadata

**ใช้เมื่อ:**
- ก่อนใช้ `/td` command
- จบ coding session
- Auto-capture trigger

---

### 6. Build Validator

**Purpose:** ตรวจสอบ build, tests, lint ก่อน push

**Checks:**
- Test results (pass/fail)
- Build success
- Lint errors/warnings
- Type check (if applicable)

**Output:** Validation report พร้อม recommendation

**ใช้เมื่อ:**
- ก่อน `git push`
- ใน `/td` workflow
- CI/CD validation

---

## Workflow Integration

### Pre-Commit Workflow

```
1. เขียน code เสร็จ
2. Use code-simplifier → simplify code
3. Use code-reviewer → review changes
4. /commit → atomic commit
```

### Pre-Push Workflow

```
1. Use build-validator → validate build/tests
2. Use security-auditor → security check
3. git push
```

### Session End Workflow

```
1. Use session-analyzer → create retrospective draft
2. /td → complete session with PR
```

### Weekly Review Workflow

```
1. Use knowledge-curator → scan learnings
2. /distill [topic] → create knowledge base entry
3. /improve → work on pending items
```

---

## Best Practices

1. **ใช้ code-reviewer ก่อน commit ทุกครั้ง** - จับ bugs ก่อน merge

2. **ใช้ code-simplifier หลังเขียน feature ใหญ่** - ลด technical debt

3. **ใช้ security-auditor ก่อน production** - ป้องกัน vulnerabilities

4. **ใช้ knowledge-curator weekly** - ไม่ให้ learnings สูญหาย

5. **ใช้ session-analyzer ก่อน /td** - ได้ retrospective ที่ดีขึ้น

6. **ใช้ build-validator ก่อน push** - ไม่ push code ที่ broken

---

## Customization

แก้ไข agent files ใน `.claude/agents/` เพื่อ:

- เพิ่ม project-specific checks
- ปรับ output format
- เพิ่ม integration กับ tools อื่น

---

## Related

- [Boris Cherny's workflow](https://twitter.com/bcherny) - ต้นแบบ subagents
- [Claude Code docs](https://docs.anthropic.com/claude-code) - Official documentation
- `/review` command - ใช้ code-reviewer
- `/td` command - ใช้ session-analyzer + build-validator
