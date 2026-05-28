---
name: title-page
description: Use this skill when creating new screenplays, setting up title page metadata, updating screenplay information, or preparing scripts for submission.
---

# Title Page Skill

## Invocation Triggers
Apply this skill when:
- Creating new screenplays
- Setting up title page metadata
- Updating screenplay information
- Preparing scripts for submission

## Title Page Format

### Fountain Title Page Syntax
Key-value pairs at the very beginning of the document:

```fountain
Title:
    **Seoul Identity**
Credit: Written by
Author: Scott Graham
Draft date: December 27, 2025
Contact:
    scott@wordstofilmby.com
    (555) 123-4567
```

### Standard Keys

| Key | Purpose | Required |
|-----|---------|----------|
| `Title` | Screenplay title | Yes |
| `Credit` | Credit type | Yes |
| `Author` | Writer name(s) | Yes |
| `Source` | Source material | If adapted |
| `Draft date` | Current draft date | Recommended |
| `Contact` | Contact information | Yes |
| `Copyright` | Copyright notice | Optional |
| `Notes` | Additional notes | Optional |

### Multi-Line Values
Indent continuation lines:
```fountain
Title:
    **The Long and Winding
    Road to Nowhere**
Contact:
    Jane Smith
    jane@email.com
    (555) 123-4567
    123 Main Street
    Los Angeles, CA 90001
```

### Formatting in Titles
```fountain
Title:
    **Bold Title**
    _Underlined Subtitle_
    *Italic tagline*
```

## Credit Types

### Single Writer
```fountain
Credit: Written by
Author: Scott Graham
```

### Writing Team (Collaborators)
```fountain
Credit: Written by
Author: Scott Graham & Jane Smith
```
Note: `&` indicates a writing team who wrote together.

### Multiple Writers (Sequential)
```fountain
Credit: Screenplay by
Author: Scott Graham and Jane Smith
```
Note: `and` indicates writers who worked separately.

### Adapted Work
```fountain
Credit: Screenplay by
Author: Scott Graham
Source: Based on the novel by Jane Smith
```

### Multiple Credits
```fountain
Credit: Screenplay by
Author: Scott Graham
Credit: Story by
Author: Jane Smith & John Doe
```

## Industry Standards

### Spec Script Title Page
```fountain
Title:
    **SEOUL IDENTITY**
Credit: Written by
Author: Scott Graham
Contact:
    scott@wordstofilmby.com
```

**Do NOT include on spec scripts:**
- Draft date