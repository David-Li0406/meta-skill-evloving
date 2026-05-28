# Skills Discovery Component

This component handles discovering, recommending, and installing skills for the project.

## Key Concept: User-Invokable Skills

> **Skills are NOT preloaded** - They're triggered by slash commands.
> This keeps context window clean until you need the skill.

Skills are installed to `.claude/skills/` but only loaded when invoked:
- `/prd` - Loads PRD skill
- `/agent-browser` - Loads Agent Browser skill
- `/react-best-practices` - Loads React patterns

Document all skills in CLAUDE.md so users know what's available.

## Skills Discovery Approaches

Use all three approaches in combination for best results:

### 1. Auto-Detection (Based on Tech Stack)

Map detected tech stack to recommended skills using `reference/tech-stack-skills.md`.

**Detection Process:**
1. Read tech stack from Phase 3 (or detect from config files)
2. Look up recommended skills for that stack
3. Present as "recommended based on your project"

**Example:**
```
Detected: Next.js + TypeScript + Tailwind CSS

Recommended skills:
- react-best-practices (React/Next.js performance patterns)
- tailwind-shadcn (Tailwind CSS and shadcn/ui patterns)
- git-workflow (Git conventions)
```

### 2. Interview (User Preferences)

Ask about specific needs that auto-detection might miss.

```
AskUserQuestion: "What aspects of development do you want skills for?"
(Multi-select)
├── Testing (unit, integration, E2E)
├── Code review and refactoring
├── Database operations
├── API development
├── DevOps and CI/CD
└── None - Just mandatory skills
```

Map answers to relevant skills.

### 3. Popular Skills (From skills.sh)

Reference known popular skills from the community.

```
Popular skills from skills.sh:

1. anthropics/courses (Claude best practices)
2. anthropics/prompt-eng (Prompt engineering)
3. [other popular skills]

Would you like to install any of these?
```

---

## Skill Installation Methods

### Method 1: Copy from cc-guide (For Mandatory Skills)

For PRD and Agent Browser from cc-guide:

```bash
# Create skills directory if needed
mkdir -p .claude/skills

# Copy mandatory skills
cp -r ~/Documents/cc-guide/skills/prd .claude/skills/
cp -r ~/Documents/cc-guide/skills/agent-browser .claude/skills/
```

If cc-guide path unknown:
```
AskUserQuestion: "Where is cc-guide located?"
├── ~/Documents/cc-guide (default)
├── Let me specify the path
└── Skip - I'll install manually
```

### Method 2: npx skills add (For External Skills)

For skills published on GitHub/skills.sh:

```bash
npx skills add owner/repo
```

**Example:**
```bash
npx skills add anthropics/courses
npx skills add vercel/ai-sdk
```

### Method 3: Manual Copy

For local/custom skills:

```bash
# Copy skill directory
cp -r /path/to/skill .claude/skills/skill-name

# Or symlink for development
ln -s /path/to/skill .claude/skills/skill-name
```

---

## Mandatory Skills

Always install these (see `reference/mandatory-skills.md`):

### PRD Skill
- **Purpose**: Create product requirements documents for planning
- **Source**: cc-guide/skills/prd/
- **Invocation**: `/prd`
- **When to use**: Before implementing any significant feature

### Agent Browser Skill
- **Purpose**: Browser automation and E2E testing guidance
- **Source**: cc-guide/skills/agent-browser/
- **Invocation**: `/agent-browser`
- **When to use**: E2E testing, browser automation tasks

---

## Tech Stack to Skills Mapping

Quick reference for auto-detection. See `reference/tech-stack-skills.md` for complete list.

### Frontend

| Stack | Skills | Trigger |
|-------|--------|---------|
| React/Next.js | react-best-practices, nextjs-patterns | `/react-best-practices` |
| Tailwind + shadcn | tailwind-shadcn | `/tailwind-shadcn` |
| Vue | vue-patterns | `/vue-patterns` |

### Backend

| Stack | Skills | Trigger |
|-------|--------|---------|
| Node.js | node-backend-patterns | `/node-patterns` |
| Python | python-api-patterns | `/python-patterns` |
| Go | go-patterns | `/go-patterns` |

### Database

| Stack | Skills | Trigger |
|-------|--------|---------|
| Convex | convex-patterns | `/convex-patterns` |
| Prisma | prisma-patterns | `/prisma-patterns` |
| Drizzle | drizzle-patterns | `/drizzle-patterns` |

### DevOps

| Stack | Skills | Trigger |
|-------|--------|---------|
| Git | git-workflow | `/git-workflow` |
| Docker | docker-patterns | `/docker-patterns` |
| GitHub Actions | github-actions | `/github-actions` |

---

## Installation Flow

### Step 1: Gather Recommendations

Combine all sources:
```
Skills to Install:

Mandatory (always):
├── prd (/prd)
└── agent-browser (/agent-browser)

Recommended for Next.js + Convex:
├── react-best-practices (/react-best-practices)
├── convex-patterns (/convex-patterns)
├── tailwind-shadcn (/tailwind-shadcn)
└── git-workflow (/git-workflow)
```

### Step 2: Confirm with User

```
AskUserQuestion: "Install these skills?"
├── "Yes, install all recommended"
├── "Let me select individually"
└── "Just mandatory skills"
```

### Step 3: Install Each Skill

```
Installing skills to .claude/skills/

✓ prd (from cc-guide)
✓ agent-browser (from cc-guide)
✓ react-best-practices (from cc-guide)
✓ convex-patterns (from cc-guide)

Installation complete!
```

### Step 4: Document in CLAUDE.md

Add to Available Skills section:

```markdown
## Available Skills

Skills are triggered by slash commands (not preloaded).

| Skill | Trigger | Purpose |
|-------|---------|---------|
| prd | `/prd` | Create product requirements |
| agent-browser | `/agent-browser` | Browser automation |
| react-best-practices | `/react-best-practices` | React performance |
| convex-patterns | `/convex-patterns` | Convex database |
| tailwind-shadcn | `/tailwind-shadcn` | Tailwind + shadcn |
| git-workflow | `/git-workflow` | Git conventions |

### When to Use Each
- **prd**: Before implementing any significant feature
- **agent-browser**: For E2E testing or browser tasks
- **react-best-practices**: When optimizing React code
- **convex-patterns**: When writing Convex queries/mutations
```

---

## Verification

After installation:

```bash
# List installed skills
ls -la .claude/skills/

# Verify each has SKILL.md
for skill in .claude/skills/*/; do
  [ -f "$skill/SKILL.md" ] && echo "✓ $(basename $skill)" || echo "✗ $(basename $skill) - missing SKILL.md"
done
```

Report:
```
Installed Skills:
├── prd (/prd) ✓
├── agent-browser (/agent-browser) ✓
├── react-best-practices (/react-best-practices) ✓
├── convex-patterns (/convex-patterns) ✓
└── git-workflow (/git-workflow) ✓

All skills verified. Invoke with /skill-name.
```

---

## Error Handling

### Skill Not Found

```
Error: Skill 'owner/repo' not found

Possible issues:
1. Repository doesn't exist or is private
2. Skill name is incorrect

Try:
- Check the repository URL
- Install manually if needed
```

### cc-guide Not Found

```
Cannot find cc-guide at ~/Documents/cc-guide

AskUserQuestion: "Where is cc-guide located?"
├── Let me specify the path: [input]
└── Skip mandatory skills
```

### Permission Error

```
Error: Cannot write to .claude/skills/

Fix:
mkdir -p .claude/skills
chmod 755 .claude/skills
```

---

## Skills.sh Integration

### What is skills.sh?

Community leaderboard for Claude Code skills. Skills ranked by usage.

### Browsing Skills

```
AskUserQuestion: "Browse popular skills from skills.sh?"
├── Yes, show me the leaderboard
└── No, continue with current selection
```

### Publishing Your Skills

To publish skills:
1. Create skills in `skills/` directory
2. Each needs `SKILL.md` with proper frontmatter
3. Push to GitHub
4. Others install via `npx skills add your-username/repo`
