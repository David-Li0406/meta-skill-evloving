# Admonitions

## Configuration

```yaml
# mkdocs.yml
markdown_extensions:
  - admonition
  - pymdownx.details      # collapsible
  - pymdownx.superfences  # nesting
```

## Basic Syntax

```markdown
!!! note
    Content indented 4 spaces.

!!! note "Custom Title"
    With custom title.

!!! note ""
    No title (empty quotes).
```

## Supported Types

| Type | Aliases | Use For |
|------|---------|---------|
| `note` | `seealso` | General information |
| `abstract` | `summary`, `tldr` | Summaries |
| `info` | `todo` | Informational |
| `tip` | `hint`, `important` | Helpful tips |
| `success` | `check`, `done` | Success states |
| `question` | `help`, `faq` | Questions |
| `warning` | `caution`, `attention` | Warnings |
| `failure` | `fail`, `missing` | Failures |
| `danger` | `error` | Critical warnings |
| `bug` | - | Bug reports |
| `example` | - | Examples |
| `quote` | `cite` | Quotations |

## Collapsible

```markdown
??? note "Collapsed by default"
    Hidden content.

???+ note "Expanded by default"
    Visible content.
```

## Inline (Float)

Must declare BEFORE adjacent content:

```markdown
!!! info inline end "Right-aligned"
    Floats right.

!!! info inline "Left-aligned"
    Floats left.

Adjacent paragraph text here.
```

## Nested

```markdown
!!! note "Outer"
    Content here.

    !!! warning "Inner"
        Nested admonition.
```
