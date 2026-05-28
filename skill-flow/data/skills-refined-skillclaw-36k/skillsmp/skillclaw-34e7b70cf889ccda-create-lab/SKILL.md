---
name: create-lab
description: Use this skill when you want to create a single Red Hat Showroom workshop module from various reference materials, ensuring proper AsciiDoc formatting and engaging storytelling.
---

# Lab Module Generator

Guide you through creating a single Red Hat Showroom workshop module from reference materials (URLs, files, docs, or text) with business storytelling and proper AsciiDoc formatting.

## When to Use

**Use this skill when you want to**:
- Create a new workshop module from scratch
- Convert documentation into hands-on lab format
- Add a module to an existing workshop
- Transform technical content into an engaging learning experience

**Don't use this for**:
- Creating demo content → use `/create-demo`
- Converting to blog posts → use `/blog-generate`
- Reviewing existing content → use `/verify-content`

## Shared Rules

**IMPORTANT**: This skill follows shared contracts defined in `.claude/docs/SKILL-COMMON-RULES.md`:
- Version pinning or attribute placeholders (REQUIRED)
- Reference enforcement (REQUIRED)
- Attribute file location (REQUIRED)
- Image path conventions (REQUIRED)
- Navigation update expectations (REQUIRED)
- Failure-mode behavior (stop if cannot proceed safely)

See SKILL-COMMON-RULES.md for complete details.

## Arguments (Optional)

This skill supports optional command-line arguments for faster workflows.

**Usage Examples**:
```bash
/create-lab                                    # Interactive mode (asks all questions)
/create-lab <directory>                        # Specify target directory
/create-lab <directory> --new                  # Create new lab in directory
/create-lab <directory> --continue <module>    # Continue from specific module
```

**Parameters**:
- `<directory>` - Target directory for module files
  - Example: `/create-lab content/modules/ROOT/pages/`
  - If not provided, defaults to `content/modules/ROOT/pages/`
- `--new` - Flag to create new lab (generates index + overview + details + module-01)
- `--continue <module-path>` - Continue from specified previous module
  - Example: `/create-lab content/modules/ROOT/pages/ --continue content/modules/ROOT/pages/03-module-01-intro.adoc`
  - Reads previous module to detect story continuity

**How Arguments Work**:
- Arguments skip certain questions (faster workflow)
- You can still use interactive mode by calling `/create-lab` with no arguments
- Arguments are validated before use