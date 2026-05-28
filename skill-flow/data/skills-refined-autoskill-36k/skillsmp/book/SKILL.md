---
name: book
description: Manage book projects - create/edit parts, chapters, sections. Use when user wants to add, rename, delete, or reorganize book structure elements. Triggers on "new chapter", "add section", "rename part", "delete appendix", "move chapter".
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, AskUserQuestion
---
# Book Skill

Manage structured book projects with parts, chapters, sections, and appendices.

## Config Requirement

**Always read `config.yaml` first** to determine the active filetype (latex, markdown, html).

```
./config.yaml
```

The `types` field specifies active formats. Load the corresponding implementation from `commands/<type>/`.

## CLI Commands

### Compile

```bash
python .claude/skills/book/cli/windows/compile_latex.py [filename]
```

- No filename: compiles `main.tex`
- With filename: compiles specified file

### Initialize Project

```bash
python .claude/skills/book/cli/windows/init_book.py <type>
```

- Creates project structure for specified type (latex, markdown, html)

### Image Generation

```bash
python .claude/skills/book/cli/windows/image_gen.py new --path "path/to/output.png" "prompt describing the image"
python .claude/skills/book/cli/windows/image_gen.py edit --path "path/to/image.png" "prompt describing changes"
```

## Structure Commands

For structural operations, load the command file from `commands/`:

| Operation          | Command File                                                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Part**     | `new-part.md`, `insert-part.md`, `rename-part.md`, `delete-part.md`                                                        |
| **Chapter**  | `new-chapter.md`, `insert-chapter.md`, `rename-chapter.md`, `delete-chapter.md`, `move-chapter.md`, `swap-chapters.md` |
| **Section**  | `new-section.md`, `insert-section.md`, `rename-section.md`, `delete-section.md`, `move-section.md`, `swap-sections.md` |
| **Appendix** | `new-appendix.md`, `insert-appendix.md`, `rename-appendix.md`, `delete-appendix.md`                                        |

Each command file specifies:

1. Required information to gather
2. Type-agnostic workflow steps
3. Reference to type-specific implementation in `commands/<type>/`

## Missing Arguments Rule

**Always use `AskUserQuestion`** when required information is missing:

- **Part/Chapter/Section/Appendix operations**: Ask for slug and title if not provided
- **Insert operations**: Ask for position if not specified
- **Move operations**: Ask for target location if not provided

## Reference Documents

- `templates/structure.md` - Folder/file naming conventions
- `filetypes/<type>.md` - Type-specific templates and patterns
- `docs/` - Additional reference documentation
