---
name: blog-writer
description: Write bilingual blog articles for the personal website. Use when creating a new blog post, article, or writing content for the blog. Handles EN/ES translations, frontmatter, and content structure.
---

# Blog Article Writer

Create bilingual (English/Spanish) blog articles for javieraguilar.ai.

## File Locations

- English: `src/content/blog/en/[slug].md`
- Spanish: `src/content/blog/es/[slug].md`
- Images: `public/blog/[image-name].png` (referenced as `/blog/[image-name].png`)

## Required Frontmatter Format

Both EN and ES files must include this exact frontmatter:

```yaml
---
title: "Article Title Here"
description: "A concise description for SEO and preview cards (1-2 sentences)."
pubDate: YYYY-MM-DD
tags: ["Tag1", "Tag2", "Tag3"]
lang: en  # or es
translationKey: article-slug
---
```

### Field Requirements

| Field | Required | Notes |
|-------|----------|-------|
| `title` | Yes | Translated per language |
| `description` | Yes | Translated, SEO-friendly, 1-2 sentences |
| `pubDate` | Yes | Same date for both languages |
| `tags` | Yes | Translated (e.g., "AI" → "IA") |
| `lang` | Yes | Must be `en` or `es` |
| `translationKey` | Yes | Same value for EN/ES pair (kebab-case) |

### LinkedIn Automation (Optional)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `linkedinImage` | string | Ruta a imagen para LinkedIn (ej: `/blog/linkedin-card.png`) |

**Notas:**
- Campo opcional
- Solo se usa para auto-publicación en LinkedIn
- Si se omite, el post en LinkedIn será solo texto
- Ruta debe apuntar a archivo en `public/blog/`
- Formatos: PNG, JPG, WEBP
- Tamaño recomendado: 1200x627px

**Ejemplo:**
```yaml
---
title: "Mi Artículo"
description: "Descripción del artículo"
pubDate: 2026-01-07
tags: ["AI", "Automation"]
lang: en
translationKey: mi-articulo
linkedinImage: /blog/linkedin-card.png  # Opcional
---
```

## Bilingual Workflow

1. **Always create both files** with matching `translationKey`
2. Use the same `pubDate` for synchronized release
3. Translate tags appropriately (common: AI→IA, Automation→Automatización)
4. Keep `translationKey` identical in both files

## Content Structure

Follow this pattern:

```markdown
Opening paragraph establishing context and the problem/topic.

## Section Heading

Content with clear explanations. Focus on "why" not just "how".

### Subsection (if needed)

- Bullet points for lists
- Keep them concise

## Another Section

Include practical examples:

```language
code block with syntax highlighting
```

## Conclusion/Next Steps

Wrap up with actionable takeaways or links.

---

*Footer with links to resources, repos, etc.*
```

## Writing Style

- **Tone**: Professional but conversational
- **Focus**: Practical value, real examples
- **Length**: 800-2000 words typically
- **Structure**: Clear headings, scannable sections
- **Code**: Include relevant code snippets with language identifiers
- **Images**: Reference as `/blog/image-name.png`

## Tag Conventions

Common tag translations:

| English | Spanish |
|---------|---------|
| AI | IA |
| Automation | Automatización |
| Machine Learning | Machine Learning |
| Development | Desarrollo |
| Architecture | Arquitectura |

## Example Frontmatter Pair

**English** (`src/content/blog/en/my-new-post.md`):
```yaml
---
title: "Building Something Cool"
description: "How I built a tool that solves a real problem."
pubDate: 2025-01-03
tags: ["AI", "Automation", "Claude"]
lang: en
translationKey: my-new-post
---
```

**Spanish** (`src/content/blog/es/my-new-post.md`):
```yaml
---
title: "Construyendo Algo Genial"
description: "Cómo construí una herramienta que resuelve un problema real."
pubDate: 2025-01-03
tags: ["IA", "Automatización", "Claude"]
lang: es
translationKey: my-new-post
---
```

## Writing from LinkedIn Posts

When repurposing a LinkedIn post into a blog article:

1. **Fetch the post** using WebFetch to extract the content
2. **Download any images** from the post to `public/blog/`
3. **Expand the content** - LinkedIn posts are short; blog articles should:
   - Add more context and background
   - Include code examples if relevant
   - Expand on points that were condensed
   - Add sections the post didn't have room for
4. **Keep the core message** but make it more comprehensive
5. **Use original post date** as `pubDate` for authenticity

### LinkedIn Image Download

Images from LinkedIn posts should be:
- Downloaded to `public/blog/[descriptive-name].png`
- Named descriptively (e.g., `azure-content-filter-demo.png`)
- Referenced in markdown as `/blog/[name].png`

## Checklist Before Publishing

- [ ] Both EN and ES files created
- [ ] Matching `translationKey` in both
- [ ] Same `pubDate` in both
- [ ] Tags translated appropriately
- [ ] `lang` field matches file location
- [ ] Images placed in `public/blog/`
- [ ] Links are valid and functional
