# Auto-Capture Feature

ระบบ auto-capture สำหรับบันทึก session โดยอัตโนมัติเมื่อจบการทำงาน

## 3 Options

### Option 1: Claude Code Hooks (Recommended)

ใช้ hooks ของ Claude Code trigger auto-capture เมื่อ session จบ

**Setup:**

```bash
# Copy hooks to your project
cp ~/.claude/skills/knowledge-management/hooks.json .claude/hooks.json
```

**หรือเพิ่มใน `~/.claude/settings.json`:**

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/skills/knowledge-management/scripts/auto-capture.sh . 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**Pros:**
- Automatic ไม่ต้องจำ
- ทำงานกับทุก project
- ไม่กระทบ workflow

**Cons:**
- ต้อง setup hooks
- อาจ capture session เล็กๆ ที่ไม่ต้องการ

---

### Option 2: Wrapper Script

Wrapper ครอบ `claude` command แสดง summary และถาม capture

**Setup:**

```bash
# Add to ~/.bashrc or ~/.zshrc
alias claude='~/.claude/skills/knowledge-management/scripts/claude-wrap.sh'

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

**Environment Variables:**

```bash
# Always auto-capture (skip prompt)
export CLAUDE_AUTO_CAPTURE=always

# Never auto-capture
export CLAUDE_AUTO_CAPTURE=never

# Use AI-powered capture
export CLAUDE_AUTO_CAPTURE=ai

# Minimum files for capture (default: 3)
export CLAUDE_MIN_FILES=5
```

**Usage:**

```bash
claude  # ใช้งานปกติ แต่จบ session จะแสดง summary
```

**Output Example:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Session Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Started: 2024-01-15 14:30:00
   Duration: 25m 30s
   Files changed: 8
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Auto-capture this session? (8 files changed)

   [1] Basic capture (quick)
   [2] AI-powered capture (detailed, requires API key)
   [n] Skip

Choice [1/2/n]:
```

**Pros:**
- Interactive - เลือกได้ว่าจะ capture หรือไม่
- แสดง session summary
- ไม่ต้อง setup hooks

**Cons:**
- ต้อง setup alias
- ต้องใช้ผ่าน alias เท่านั้น

---

### Option 3: AI-Powered Capture

ใช้ Claude API วิเคราะห์ git diff และ generate intelligent summary

**Requirements:**

```bash
export ANTHROPIC_API_KEY='your-api-key'
```

**Usage:**

```bash
# Direct usage
./scripts/ai-capture.sh .

# Force capture (skip min files check)
./scripts/ai-capture.sh . --force
```

**What AI Generates:**

- **Type classification**: feature, bugfix, refactor, etc.
- **Title**: Brief summary of session
- **Tags**: Relevant keywords
- **Key changes**: Important modifications
- **Insights**: Learnings from the session
- **Before/After context**: Problem and solution

**Pros:**
- Intelligent analysis
- Auto-generates type, tags, summary
- Saves time writing documentation

**Cons:**
- Requires API key
- API costs
- May need review/editing

---

## Output Location

ทุก auto-capture จะเก็บที่:

```
docs/auto-captured/
└── YYYY-MM/           # Year-Month (Bangkok timezone)
    └── DD/            # Day
        └── HH.MM_session-XXXXX.md
```

**Example:**
```
docs/auto-captured/
└── 2024-01/
    ├── 15/
    │   ├── 09.30_session-12345.md
    │   └── 14.45_session-67890.md
    └── 16/
        └── 10.00_session-11111.md
```

---

## Workflow Integration

### After Auto-Capture

1. **Review** draft ที่ `docs/auto-captured/`
2. **Edit** เพิ่ม context, insights
3. **Move** ไปที่ `docs/retrospective/` เมื่อพร้อม

```bash
# Move reviewed capture to retrospective
mv docs/auto-captured/2024-01/15/09.30_session-12345.md \
   docs/retrospective/2024-01/
```

### Skip Capture Conditions

Auto-capture จะ skip ถ้า:
- Files changed < 3 (configurable)
- Not in git repository
- No changes detected

Use `--force` to override:

```bash
./scripts/auto-capture.sh . --force
```

---

## Comparison

| Feature | Hooks | Wrapper | AI-Powered |
|---------|-------|---------|------------|
| Automatic | ✅ | ❌ (asks) | ❌ |
| Interactive | ❌ | ✅ | ❌ |
| Session summary | ❌ | ✅ | ❌ |
| Intelligent analysis | ❌ | ❌ | ✅ |
| Requires API key | ❌ | Optional | ✅ |
| Setup complexity | Medium | Easy | Easy |

---

## Configuration

### Minimum Files Threshold

ทุก script ใช้ minimum 3 files เป็น default:

```bash
# Override via environment
export CLAUDE_MIN_FILES=5

# Or edit in scripts
MIN_CHANGED_FILES=5
```

### Timezone

ทุก script ใช้ Bangkok timezone:

```bash
TZ='Asia/Bangkok'
```

Edit ใน scripts ถ้าต้องการเปลี่ยน

---

## Retention Policy & Cleanup

Auto-capture สร้างไฟล์จำนวนมากตามเวลา ใช้ `/cleanup` เพื่อจัดการ

### Quick Start

```bash
/cleanup                    # Preview what would be deleted (30 days)
/cleanup 14 --archive       # Archive & delete files older than 14 days
/cleanup --all --execute    # Execute cleanup on all targets
```

### What Gets Cleaned

| Target | Policy |
|--------|--------|
| `docs/auto-captured/` | Delete all files older than retention period |
| `docs/learnings/` | Delete only `status: draft` files |
| `docs/retrospective/` | Never auto-deleted |
| `docs/knowledge-base/` | Never auto-deleted |

### Archiving

Enable `--archive` to save files before deletion:

```bash
/cleanup 30 --archive --execute
```

Archives stored in `docs/archives/` as `.tar.gz` files.

### Scheduling (Recommended)

Add cron job for automatic weekly cleanup:

```bash
# Edit crontab
crontab -e

# Add (runs every Sunday at midnight)
0 0 * * 0 cd /path/to/project && ./scripts/cleanup.sh --days 30 --archive --all
```

### Storage Estimates

| Multi-agent Sessions | Daily Files | Monthly | Yearly |
|---------------------|-------------|---------|--------|
| Light (1-2 agents) | ~5-10 | ~150-300 | ~1,800-3,600 |
| Heavy (4+ agents) | ~50-100 | ~1,500-3,000 | ~18,000-36,000 |

**Recommendation**: Use 14-30 days retention with archiving for heavy usage.

---

## Troubleshooting

### Hook not triggering

1. Check hooks.json syntax
2. Verify path to script is correct
3. Make scripts executable: `chmod +x scripts/*.sh`

### AI capture failing

1. Check `ANTHROPIC_API_KEY` is set
2. Verify API key is valid
3. Check network connection
4. Falls back to basic capture on error

### No files detected

1. Check if in git repository
2. Verify files are not in `.gitignore`
3. Use `--force` to skip check
