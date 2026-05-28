# Mandatory Skills Reference

These skills are always installed during setup, regardless of project type.

## 1. PRD Skill

**Purpose:** Create product requirements documents for planning features and implementations.

**Invocation:** `/prd`

**What it does:**
- Interviews user to gather requirements
- Generates structured PRD with user stories
- Creates acceptance criteria
- Defines testing strategy
- Outputs prd.json for automation

**Source:** `cc-guide/skills/prd/`

**Installation:**
```bash
cp -r /path/to/cc-guide/skills/prd .claude/skills/
```

**Why mandatory:**
Planning is essential before implementation. The PRD skill helps Claude understand what to build before writing code, reducing rework and ensuring alignment with user expectations.

---

## 2. Agent Browser Skill

**Purpose:** Browser automation and E2E testing guidance.

**Invocation:** `/agent-browser`

**What it does:**
- Guides headless browser automation
- Helps write E2E tests
- Provides patterns for web scraping
- Integrates with Agent Browser CLI

**Source:** `cc-guide/skills/agent-browser/`

**Installation:**
```bash
cp -r /path/to/cc-guide/skills/agent-browser .claude/skills/
```

**Why mandatory:**
Browser automation is a common need across all web projects. Having this skill available ensures Claude can help with E2E testing and browser tasks from day one.

---

## 3. Ralph Pre-Flight Skill

**Purpose:** Validate Ralph TUI configuration before starting a loop.

**Invocation:** `/ralph-preflight`

**What it does:**
- Checks for global CLAUDE.md conflicts
- Validates config.toml and prompt_template paths
- Verifies prd.json structure and template variable mapping
- Detects common configuration issues
- Provides ready-to-use launch commands

**Source:** `cc-guide/skills/ralph-preflight/`

**Installation:**
```bash
cp -r /path/to/cc-guide/skills/ralph-preflight .claude/skills/
```

**Why mandatory:**
Running a Ralph loop with incorrect configuration wastes iterations and can produce confusing results. This pre-flight check catches issues before they cause problems.

---

## Installation Flow

### Step 1: Locate cc-guide

Check common locations:
```bash
# Check common paths
for path in ~/Documents/cc-guide ~/cc-guide ~/.claude/cc-guide; do
  if [ -d "$path/skills" ]; then
    echo "Found: $path"
    break
  fi
done
```

If not found, ask user:
```
Question: "Where is the cc-guide repository located?"
Options:
- ~/Documents/cc-guide
- ~/cc-guide
- Let me specify the path
```

### Step 2: Verify Skills Exist

```bash
ls -la /path/to/cc-guide/skills/prd/SKILL.md
ls -la /path/to/cc-guide/skills/agent-browser/SKILL.md
```

### Step 3: Copy to Project

```bash
mkdir -p .claude/skills
cp -r /path/to/cc-guide/skills/prd .claude/skills/
cp -r /path/to/cc-guide/skills/agent-browser .claude/skills/
cp -r /path/to/cc-guide/skills/ralph-preflight .claude/skills/
```

### Step 4: Verify Installation

```bash
ls -la .claude/skills/
# Should show:
# prd/
# agent-browser/
# ralph-preflight/
```

---

## Alternative: Symlinks for Development

If working on cc-guide itself or wanting live updates:

```bash
mkdir -p .claude/skills
ln -s /path/to/cc-guide/skills/prd .claude/skills/prd
ln -s /path/to/cc-guide/skills/agent-browser .claude/skills/agent-browser
ln -s /path/to/cc-guide/skills/ralph-preflight .claude/skills/ralph-preflight
```

**Note:** Symlinks mean changes to cc-guide skills are reflected immediately.

---

## If cc-guide Not Available

If user doesn't have cc-guide:

1. **Option A: Clone cc-guide**
   ```bash
   git clone https://github.com/username/cc-guide.git ~/cc-guide
   ```

2. **Option B: Install via skills.sh (when published)**
   ```bash
   npx skills add username/cc-guide
   ```

3. **Option C: Skip for now**
   Document that these skills are recommended but not required.

---

## Verification

After installation, verify skills work:

```bash
# Check skill files exist
cat .claude/skills/prd/SKILL.md | head -5
cat .claude/skills/agent-browser/SKILL.md | head -5
cat .claude/skills/ralph-preflight/SKILL.md | head -5
```

Report:
```
Mandatory Skills Installed:

- prd
  Location: .claude/skills/prd/
  Invocation: /prd
  Status: Ready

- agent-browser
  Location: .claude/skills/agent-browser/
  Invocation: /agent-browser
  Status: Ready

- ralph-preflight
  Location: .claude/skills/ralph-preflight/
  Invocation: /ralph-preflight
  Status: Ready
```
