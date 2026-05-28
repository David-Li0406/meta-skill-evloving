# Class List Template

The CLASS-LIST.md file provides the authoritative list of students enrolled in the course. This file is used to:

1. Cross-reference PDF names with enrolled students
2. Generate file prefixes for renaming
3. Track missing submissions

## Required Format

```markdown
# Class List - [Course Name]

[First Name] [Last Name] [Campus/Class Info]
[First Name] [Last Name] [Campus/Class Info]
...
```

## Example

```markdown
# Class List - IPL25

Anna Andersson IPL25 Campus Mölndal
Erik Eriksson IPL25 Campus Mölndal
Johan Johansson IPL25 Campus Mölndal
Maria Martinez Löfgren IPL25 Campus Mölndal
```

## Parsing Rules

### Name Extraction

Each line is parsed as:
- **First name(s):** All words before the last word that isn't campus info
- **Last name:** The word(s) between first name and campus info
- **Campus info:** Typically "IPL25 Campus [Location]" at end of line

### Compound Names

| Pattern | First Name | Last Name |
|---------|------------|-----------|
| `Anna Andersson IPL25...` | Anna | Andersson |
| `Anna-Isabel Martinez IPL25...` | Anna-Isabel | Martinez |
| `Anna Martinez Löfgren IPL25...` | Anna | Martinez Löfgren |
| `Karl Johan Andersson IPL25...` | Karl Johan | Andersson |

### File Prefix Generation

From parsed name, generate prefix:

1. Take last name (all parts)
2. Take first name (first part only if compound)
3. Lowercase everything
4. Remove spaces, hyphens
5. Normalize Swedish characters (ö→o, ä→a, å→a)

| Full Name | Generated Prefix |
|-----------|------------------|
| Anna Andersson | `andersson_anna` |
| Anna-Isabel Martinez | `martinez_annaisabel` |
| Anna Martinez Löfgren | `martinezlofgren_anna` |
| Karl Johan Andersson | `andersson_karljohan` |

## Privacy Note

The CLASS-LIST.md file contains student names and MUST be:

1. Added to `.gitignore`
2. Never committed to public repositories
3. Deleted after course completion

## Creating a New Class List

1. Export student roster from learning management system
2. Format as one student per line
3. Include campus/class info for context
4. Save as `docs/assignments/CLASS-LIST.md`
5. Immediately add to `.gitignore`

```bash
echo "CLASS-LIST.md" >> docs/assignments/.gitignore
```
