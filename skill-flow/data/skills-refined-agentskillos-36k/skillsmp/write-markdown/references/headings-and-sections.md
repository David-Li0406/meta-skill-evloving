# Headings and sections

Use headings to communicate structure.
Prefer a clear hierarchy and consistent heading syntax.

## MD001 - Heading levels should only increment by one level at a time

Do not skip heading levels.
Move one level at a time to keep structure predictable.

Bad:

```markdown
# Title

### Skipped level
```

Good:

```markdown
# Title

## Section

### Subsection
```

## MD002 - First heading should be a top level heading

Start a document with a top-level heading to establish the title.
If a repository uses a different convention, follow that convention.

Bad:

```markdown
## Starts at level 2
```

Good:

```markdown
# Title

## Section
```

## MD003 - Heading style

Use one heading style consistently in a file.
A common choice is ATX headings (`#`).

Bad:

```markdown
# ATX title

Setext heading
--------------
```

Good:

```markdown
# ATX title

## ATX section
```

## MD018 - No space after hash on atx style heading

Put a single space after the `#` characters in ATX headings.

Bad:

```markdown
##No space
```

Good:

```markdown
## With space
```

## MD019 - Multiple spaces after hash on atx style heading

Do not use multiple spaces after the `#` characters.

Bad:

```markdown
##  Too many spaces
```

Good:

```markdown
## One space
```

## MD020 - No space inside hashes on closed atx style heading

For closed ATX headings, keep the closing `#` tight.
Do not place spaces just inside the closing hashes.

Bad:

```markdown
## Closed heading #
```

Good:

```markdown
## Closed heading##
```

## MD021 - Multiple spaces inside hashes on closed atx style heading

For closed ATX headings, do not add multiple spaces around the closing hashes.

Bad:

```markdown
## Closed heading  ##
```

Good:

```markdown
## Closed heading##
```

## MD022 - Headings should be surrounded by blank lines

Surround headings with blank lines.
This reduces ambiguity and improves readability.

Bad:

```markdown
Paragraph.
## Heading
More text.
```

Good:

```markdown
Paragraph.

## Heading

More text.
```

## MD023 - Headings must start at the beginning of the line

Do not indent headings.
Headings should start at column 1.

Bad:

```markdown
  ## Indented heading
```

Good:

```markdown
## Heading
```

## MD024 - Multiple headings with the same content

Avoid duplicate heading text.
Duplicate headings can create confusing navigation and ambiguous anchors.

Bad:

```markdown
## Setup

Text.

## Setup

More text.
```

Good:

```markdown
## Setup

Text.

## Setup on macOS

More text.
```

## MD025 - Multiple top-level headings in the same document

Use a single top-level heading as the document title.

Bad:

```markdown
# Title

# Another title
```

Good:

```markdown
# Title

## Another section
```

## MD026 - Trailing punctuation in heading

Avoid trailing punctuation in headings.

Bad:

```markdown
## Overview:
```

Good:

```markdown
## Overview
```

## MD036 - Emphasis used instead of a heading

Do not use emphasis-only lines as headings.
Use a real heading marker.

Bad:

```markdown
**Installation**

Steps follow.
```

Good:

```markdown
## Installation

Steps follow.
```

## MD041 - First line in file should be a top level heading

Put a top-level heading at the start of the file.
If the file begins with front matter, put the top-level heading right after
it.

Bad:

```markdown
Intro text.

# Title
```

Good:

```markdown
# Title

Intro text.
```

## MD043 - Required heading structure

Some projects require a specific set of headings in certain documents.
Match the required heading structure when it is defined.

Bad:

```markdown
# Design

## Random section
```

Good:

```markdown
# Design

## Overview

## Details

## Checklist
```
