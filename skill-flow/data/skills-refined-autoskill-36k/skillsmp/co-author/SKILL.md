---
name: co-author
description: Manage co-author attribution in commits for agentconfig.org. Use when pair programming, collaborating on changes, or when the user mentions working with another contributor.
---

# Co-Author Attribution

## Contributors

| Name | Aliases | Git Trailer |
|------|---------|-------------|
| Jonathan Hoyt | jon, jonathan, jonmagic | `Jonathan Hoyt <jonmagic@gmail.com>` |
| Francis Brero | francis, francisfuzz | `francisfuzz <15894826+francisfuzz@users.noreply.github.com>` |

## How to Add Co-Authors

Add a `Co-authored-by:` trailer at the end of commit messages:

```
feat(hero): update tagline

Co-authored-by: francisfuzz <15894826+francisfuzz@users.noreply.github.com>
```

## Multiple Co-Authors

For multiple collaborators, add separate lines:

```
feat(comparison): redesign provider matrix

Co-authored-by: francisfuzz <15894826+francisfuzz@users.noreply.github.com>
Co-authored-by: Jonathan Hoyt <jonmagic@gmail.com>
```

## Rules

1. **Only human contributors** - Never add AI agents as co-authors
2. **Use exact format** - `Co-authored-by: Name <email>`
3. **Verify contributor** - Only use emails from the contributors table above
4. **Add when appropriate** - When someone contributed ideas, review, or code

## When NOT to Add Co-Authors

- Solo work with no collaboration
- AI-assisted coding (the AI is not a co-author)
- Minor suggestions from code review (use PR attribution instead)
- Rebasing or cherry-picking others' commits (original authorship preserved)
