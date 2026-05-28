---
name: fountain-syntax
description: Use this skill when writing or editing .fountain files, validating screenplay format, converting between formats, or teaching Fountain syntax.
---

# Fountain Syntax Skill

## Overview
Fountain is a plain text markup language for writing screenplays. Files use the `.fountain` extension.

## Core Elements

### Title Page
Key-value pairs at the start of the document:
```fountain
Title: SCREENPLAY TITLE
Credit: Written by
Author: Writer Name
Draft date: January 2025
Contact: email@example.com
```
Standard keys include `Title`, `Credit`, `Author`, `Draft date`, `Contact`, and more.

### Scene Headings
```fountain
INT. COFFEE SHOP - DAY
EXT. CITY STREET - NIGHT
INT./EXT. CAR (MOVING) - CONTINUOUS
```
Must begin with `INT`, `EXT`, `EST`, `INT./EXT`, or `I/E`. Force any line as scene heading with a `.` prefix.

### Action (Description)
Plain paragraphs are action. Line breaks are preserved:
```fountain
Sarah enters the crowded coffee shop, scanning the room. She spots MIKE at a corner table.
```
Force uppercase lines as action with `!`:
```fountain
!MONTAGE - SARAH'S MORNING ROUTINE
```

### Character Names
All UPPERCASE on their own line, with a blank line before:
```fountain

SARAH
Hello, Mike. It's been a while.
```
With extensions:
```fountain
MOM (V.O.)
When I was your age...
```

### Dialogue
Text following Character or Parenthetical:
```fountain
MIKE
(surprised)
Sarah? I didn't expect to see you here.
```

### Parentheticals
Wrapped in parentheses, after Character or within Dialogue:
```fountain
SARAH
(sitting down)
We need to talk.
```

### Dual Dialogue (Simultaneous)
Add `^` after the second character:
```fountain
SARAH
I can't believe you—

MIKE ^
Let me explain—
```

### Transitions
Uppercase ending in `TO:`, or forced with `>`:
```fountain
CUT TO:

> FADE OUT.
```

### Centered Text
Bracket with `>` and `<`:
```fountain
>THE END<
```

### Emphasis (Formatting)
```fountain
*italics*
**bold**
***bold italics***
_underline_
```

### Lyrics
Prefix with `~`:
```fountain
~Somewhere over the rainbow
```

### Page Breaks
Three or more `=` on their own line:
```fountain
===
```

### Notes (Writer Comments)
Double brackets, won't appear in output:
```fountain
[[This is a note to myself about the scene.]]
```

### Boneyard (Archived Content)
Content between `/*` and `*/` is ignored:
```fountain
/*
CUT SCENE - keeping for reference
*/
```

### Sections (Structural, Hidden)
Pound signs for outline hierarchy:
```fountain
# Act One
## Sequence 1
### Scene Group
```

### Synopses (Scene Summaries, Hidden)
Prefix with `=`:
```fountain
= Sarah discovers the truth about her father.
```

## Validation Rules

### Required Elements
- Title page (for complete scripts)
- Scene headings with location and time
- Proper character/dialogue structure

### Common Errors
1. Missing blank line before character names
2. Scene heading missing time of day
3. Parenthetical not on own line
4. Unescaped special characters triggering wrong format

### Syntax Validation Checklist
- [ ] Title page has required fields
- [ ] Scene headings start with INT/EXT
- [ ] Character names are UPPERCASE
- [ ] Parentheticals are in (parentheses)
- [ ] Dual dialogue uses ^ correctly
- [ ] Notes use [[double brackets]]
- [ ] Boneyard uses /* */ correctly