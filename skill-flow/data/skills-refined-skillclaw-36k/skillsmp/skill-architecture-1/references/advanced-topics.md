## Part 2.5: Critical Formatting Bugs (MUST READ)

### 🚨 BUG #9817: Multiline Description Footgun

**CRITICAL**: Skills with multiline descriptions are **silently ignored** - no error message!

**What breaks** (silently ignored):
```yaml
---
name: my-skill
description:
  This description wraps to multiple lines
  and will be silently ignored by Claude
---
```

**What works** (single line):
```yaml
---
name: my-skill
description: This description stays on one line and works correctly.
---
```

**How to prevent**:
- ✅ Keep description under 200 characters (safe from Prettier wrapping)
- ✅ Use third person ("Reads files...") not imperative ("Read files...")
- ✅ Test with `/clear` and trigger keywords after creating skill
- ✅ If skill doesn't activate, check description length/format first

**Why it happens**: Prettier with `proseWrap: true` reformats long descriptions to wrap across lines. Claude Code's YAML parser silently fails on multiline descriptions. This is a known footgun tracked in Issue #9817.

**Validation checklist**:
- [ ] Description is single line (check with `head -5 SKILL.md`)
- [ ] Description uses third person ("Does X", not "Do X")
- [ ] Description under 200 chars (CLI max is 1024 but Prettier wraps ~80)
- [ ] Test activation with `/clear` and trigger keywords


## Part 4: Content Sections (Recommended)

After YAML frontmatter, organize content:

````markdown
# Agent Skill Name

Brief introduction (1-2 sentences).

## Instructions

Step-by-step guidance in **imperative mood**:

1. Read the file using Read tool
2. Process content with scripts/helper.py
3. Verify output

## Examples

Concrete usage:

```
Input: process_data.csv
Action: Run scripts/validate.py && scripts/process.py
Output: cleaned_data.csv with 1000 rows
```

## References

For detailed API specs, see reference.md.
For advanced examples, see examples.md.
````

**Writing style**:

- ✅ **Imperative**: "Read the file", "Run the script"
- ❌ **Suggestive**: "You should read", "Maybe try"

______________________________________________________________________

## Part 5: Agent Skill Composition & Limitations

### What Agent Skills CAN'T Do

❌ **Explicitly reference other Agent Skills**:

```markdown
# ❌ WRONG - Agent Skills can't call each other directly

"First use the api-auth skill, then use api-client skill"
```

### What Agent Skills CAN Do

✅ **Claude uses multiple Agent Skills automatically**:

- If both `api-auth` and `api-client` are relevant, Claude loads both
- No explicit coordination needed
- Agent Skills work together organically based on descriptions

______________________________________________________________________

## Part 6: CLI vs API Differences

| Feature           | Claude Code CLI        | Claude.ai API            |
| ----------------- | ---------------------- | ------------------------ |
| File name         | `SKILL.md` (uppercase) | `Skill.md` (capitalized) |
| Location          | `~/.claude/skills/`    | ZIP upload               |
| Description limit | 1024 characters        | 200 characters           |
| `allowed-tools`   | ✅ Supported           | ❌ Not supported         |
| Privacy           | Personal or project    | Individual account only  |
| Package install   | Pre-installed only     | Pre-installed only       |

**This Agent Skill teaches CLI format only.**
