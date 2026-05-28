---
name: fountain-syntax
description: Use this skill when writing or editing .fountain files, validating screenplay format, converting between formats, or teaching Fountain syntax.
---

# Fountain Syntax Skill

## Overview
Fountain is a plain text markup language for writing screenplays. Files use the `.fountain` extension and support various formatting elements.

## Invocation Triggers
Apply this skill when:
- Writing or editing .fountain files
- Validating screenplay format
- Converting between formats
- Teaching Fountain syntax

## Complete Fountain Syntax Reference

### Title Page
Key-value pairs at the start of the document:
```fountain
Title: SCREENPLAY TITLE
Credit: Written by
Author: Writer Name
Draft date: January 2025
Contact: email@example.com
```
Standard keys: `Title`, `Credit`, `Author`, `Source`, `Draft date`, `Contact`, `Copyright`, `Notes`.

### Scene Headings
Must begin with `INT`, `EXT`, `EST`, `INT./EXT`, or `I/E`:
```fountain
INT. COFFEE SHOP - DAY
EXT. CITY STREET - NIGHT
INT./EXT. CAR (MOVING) - CONTINUOUS
```
Force any line as scene heading with `.` prefix:
```fountain
.FLASHBACK - TWENTY YEARS EARLIER
```
Optional scene numbers:
```fountain
INT. OFFICE - DAY #1#
```

### Action (Description)
Plain paragraphs are action. Line breaks are preserved:
```fountain
The room is dark. A FIGURE moves in the shadows.
```
Force uppercase lines as action with `!`:
```fountain
!MONTAGE - SARAH'S MORNING ROUTINE
```

### Character Names
All UPPERCASE on their own line, with a blank line before:
```fountain

SARAH
I don't understand.
```
With extensions:
```fountain
MOM (V.O.)
When I was your age...

JOHN (O.S.)
I'm in the kitchen!
```
Force mixed-case with `@`:
```fountain
@McCLANE
Yippee ki-yay.
```

### Dialogue
Text following Character or Parenthetical:
```fountain
JOHN
This is dialogue. It can span
multiple lines without a problem.
```

### Parentheticals
Wrapped in parentheses, after Character or within Dialogue:
```fountain
SARAH
(looking away)
I never said that.
```

### Dual Dialogue (Simultaneous)
Add `^` after the second character:
```fountain
JACK
I love you!

JILL ^
I hate you!
```

### Transitions
Uppercase ending in `TO:`, or forced with `>`:
```fountain
CUT TO:

>FADE TO BLACK.
```

### Notes
Production notes can be added as:
```fountain
[[This is a production note]]

/* This is a hidden comment */
```

### Emphasis
Use asterisks for emphasis:
```fountain
*italics*
**bold**
***bold italics***
_underline_
```

### Page Breaks
Indicate page breaks with three or more equal signs:
```fountain
===
```