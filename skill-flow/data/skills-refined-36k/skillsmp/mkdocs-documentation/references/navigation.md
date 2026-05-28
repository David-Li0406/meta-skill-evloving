# Navigation & Linking

## Nav Configuration

```yaml
# mkdocs.yml
nav:
  - Home: index.md
  - Getting Started:
    - Installation: getting-started/install.md
    - Configuration: getting-started/config.md
  - API Reference:
    - api/index.md  # section index
    - Users: api/users.md
    - Posts: api/posts.md
```

## Navigation Features

```yaml
# mkdocs.yml
theme:
  features:
    - navigation.tabs        # top-level as tabs
    - navigation.sections    # group in sidebar
    - navigation.expand      # auto-expand subsections
    - navigation.indexes     # section index pages
    - navigation.path        # breadcrumbs (experimental)
    - navigation.tracking    # anchor in URL
    - toc.integrate          # TOC in sidebar
```

**Mutually exclusive:** `navigation.indexes` + `toc.integrate`

## Internal Links

Relative paths from current file:

```markdown
<!-- Same directory -->
[Link](other-page.md)

<!-- Subdirectory -->
[Link](subdir/page.md)

<!-- Parent directory -->
[Link](../sibling/page.md)

<!-- Anchor -->
[Link](page.md#section-heading)

<!-- Same page anchor -->
[Link](#section-heading)
```

## Section Index Pages

Create `index.md` in section folder:

```
docs/
  api/
    index.md      # Section landing page
    users.md
    posts.md
```

```yaml
nav:
  - API:
    - api/index.md
    - api/users.md
```

## Cross-References

Reference headings by slug (lowercase, hyphens):

```markdown
## My Section Heading

...

See [My Section Heading](#my-section-heading).
```

## External Links

```markdown
[External Site](https://example.com)
[External with title](https://example.com "Hover text")
```
