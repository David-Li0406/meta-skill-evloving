# Links and images

Write links and images that are valid, consistent, and readable.

## MD011 - Reversed link syntax

Use `[text](target)`, not the reversed form.

Bad:

```markdown
(target)[text]
```

Good:

```markdown
[text](./path/to/doc.md)
```

## MD034 - Bare URL used

Avoid bare URLs in prose.
Use a normal link or an autolink.

Bad:

```markdown
See https://example.com for details.
```

Good:

```markdown
See [the docs](./docs/index.md) for details.
```

## MD039 - Spaces inside link text

Do not include leading or trailing spaces inside the brackets.

Bad:

```markdown
[ link text ](./docs/index.md)
```

Good:

```markdown
[link text](./docs/index.md)
```

## MD042 - No empty links

Do not create empty link text or empty link destinations.

Bad:

```markdown
[]()
```

Good:

```markdown
[release notes](./docs/release-notes.md)
```

## MD045 - Images should have alternate text (alt text)

Provide alt text for images.

Bad:

```markdown
![](./assets/screenshot.png)
```

Good:

```markdown
![Sign-in screen](./assets/screenshot.png)
```

## MD051 - Link fragments should be valid

Ensure fragment identifiers match real headings.

Bad:

```markdown
[Install](./docs/guide.md#not-a-real-heading)
```

Good:

```markdown
[Install](./docs/guide.md#installation)
```

## MD052 - Reference links and images should use a label that is defined

Define labels that you reference.

Bad:

```markdown
See [guide][guide].
```

Good:

```markdown
See [guide][guide].

[guide]: ./docs/guide.md
```

## MD053 - Link and image reference definitions should be needed

Remove unused reference definitions.

Bad:

```markdown
[unused]: ./docs/old.md
```

Good:

```markdown
Use [guide][guide].

[guide]: ./docs/guide.md
```

## MD054 - Link and image style

Use a consistent link style within a document.

Bad:

```markdown
Inline: [guide](./docs/guide.md)

Reference: [guide][guide]

[guide]: ./docs/guide.md
```

Good:

```markdown
[guide](./docs/guide.md)
[guide](./docs/guide.md)
```

## MD059 - Link text should be descriptive

Avoid vague link text such as "here".
Use descriptive link text.

Bad:

```markdown
Click [here](./docs/guide.md).
```

Good:

```markdown
Read the [installation guide](./docs/guide.md).
```
