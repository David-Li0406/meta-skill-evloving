# Validation Checks

## Automated Checks

### 0. Auto-Fix Capability (New in 2026)

Quick fixes for common issues before manual review.

**Usage:**
```bash
# Safe auto-fixes (non-destructive)
python skills/julien-skill-reviewer/scripts/auto-fix.py path/to/skill/ --mode safe

# Interactive (requires approval)
python skills/julien-skill-reviewer/scripts/auto-fix.py path/to/skill/ --mode interactive

# Preview only
python skills/julien-skill-reviewer/scripts/auto-fix.py path/to/skill/ --dry-run
```

**What Gets Auto-Fixed:**

| Issue | Fix | Mode | Backup? |
|-------|-----|------|---------|
| Missing version | Add `version: 1.0.0` | Safe | Yes |
| Missing license | Add `license: Apache-2.0` | Safe | Yes |
| Windows paths | Convert `\` to `/` | Safe | Yes |
| No TOC (>100 lines) | Generate from headings | Safe | Yes |
| < 5 triggers | Warning only | Safe | No |
| Hardcoded credentials | Detection + suggestion | Interactive | Yes |
| SKILL.md > 500 lines | Suggest splits | Interactive | Yes |
| Description vague | Suggest "what+when" | Interactive | Yes |

**Safety Features:**
- Always creates timestamped backup before changes
- Dry-run mode shows preview without modifying files
- All changes logged to console
- Safe mode requires no user input
- Interactive mode prompts for each fix

### 1. Line Count Check

```bash
wc -l SKILL.md
```

| Result | Status |
|--------|--------|
| < 300 | Excellent |
| 300-500 | Good |
| > 500 | **Fail - must refactor** |

### 2. YAML Frontmatter Validation

**Required fields:**
- `name`: present, ≤ 64 chars, lowercase + hyphens only
- `description`: present, ≤ 1024 chars, non-empty

**Check for reserved words in name:**
- Cannot contain "anthropic"
- Cannot contain "claude"

**Check description format:**
- Must be third person ("Processes..." not "I process...")
- Must include what it does AND when to use it

### 3. Path Format Check

```bash
grep -E '\\\\' SKILL.md  # Should return nothing
```

All paths must use forward slashes `/`, not Windows backslashes `\`.

### 4. Reference Depth Check

References must be one level deep from SKILL.md:

**Good:**
```
SKILL.md → references/guide.md
SKILL.md → references/api.md
```

**Bad:**
```
SKILL.md → references/guide.md → references/details.md
```

### 5. TOC Check for Long Files

Files > 100 lines must have table of contents at top.

```bash
wc -l references/*.md | awk '$1 > 100 {print $2}'
```

For each file > 100 lines, verify TOC exists.

### 6. Duplication Check

Search for same content in SKILL.md and references/:

```bash
# Extract headings from SKILL.md
grep -E '^##' SKILL.md > /tmp/skill_headings.txt

# Check if same headings in references/
for f in references/*.md; do
  grep -E '^##' "$f" >> /tmp/ref_headings.txt
done

# Compare for duplicates
sort /tmp/skill_headings.txt /tmp/ref_headings.txt | uniq -d
```

### 7. Extraneous Files Check

Should NOT exist in skill directory:
- README.md
- CHANGELOG.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md

### 8. Skill Chaining Section Check

```bash
grep -E '^## Skill Chaining|^## 🔗 Skill Chaining' SKILL.md
```

Must exist if skill interacts with others.

Required subsections:
- Skills Required Before
- Input Expected
- Output Produced
- Compatible Skills After
- Called By
- Tools Used
- Visual Workflow
- Usage Example

## Manual Checks

### Description Quality

- [ ] Uses third person
- [ ] Includes "what it does"
- [ ] Includes "when to use it"
- [ ] Contains trigger keywords
- [ ] Not vague/generic

### Examples Quality

- [ ] At least 1-2 concrete examples
- [ ] Real-world scenarios (not foo/bar)
- [ ] Copy-paste ready
- [ ] Shows expected output

### Error Handling

- [ ] Common errors documented
- [ ] Solutions provided
- [ ] Troubleshooting section exists

## Pre-Distribution Checklist

### Core Quality
- [ ] Name ≤ 64 chars, lowercase + hyphens
- [ ] Description specific with triggers
- [ ] SKILL.md < 500 lines
- [ ] Third person description
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] One-level-deep references
- [ ] Progressive disclosure used

### Structure
- [ ] SKILL.md exists
- [ ] scripts/ for code only
- [ ] references/ for docs
- [ ] assets/ for output resources
- [ ] No extraneous files
- [ ] Forward slashes only

### Quality Score
- [ ] Average ≥ 3.5/5
- [ ] No dimension < 3/5
