# claude-skill-sysdoc

Claude Code skill for editing sysdoc document repositories.

## Installation

Clone to your Claude Code skills directory:

```bash
cd ~/.claude/skills
git clone https://github.com/sysdoc-rs/claude-skill-sysdoc.git sysdoc-edit
```

## What It Does

Guides Claude when editing markdown files in sysdoc repositories, enforcing:

- No section numbers in headings (auto-generated from filenames)
- Correct file naming (`XX.YY_title-slug.md`)
- One H1 per file
- Proper use of .00 parent sections
- Avoiding ambiguity between H2 headings and separate subfiles

## Related

- [sysdoc](https://github.com/sysdoc-rs/sysdoc) - The sysdoc tool
