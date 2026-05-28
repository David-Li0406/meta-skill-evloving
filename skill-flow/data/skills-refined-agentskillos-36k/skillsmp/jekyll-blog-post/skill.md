---
name: jekyll-blog-post
description: Create and format blog posts for 11h.dev following Jekyll conventions and existing patterns
tags: [jekyll, blog, format, structure]
---

# Jekyll Blog Post Skill

You are an expert in creating properly formatted Jekyll blog posts for the 11h.dev blog, following established conventions and technical requirements.

## Core Responsibilities

When creating or formatting a blog post:
1. **Analyze existing posts** to extract current patterns
2. **Generate proper front matter** following Jekyll conventions
3. **Ensure filename compliance** with Jekyll requirements
4. **Validate category consistency** with existing posts
5. **Format markdown correctly** for GitHub Pages
6. **Integrate links and references** properly

## Front Matter Structure

Every post MUST start with YAML front matter:

```yaml
---
layout: post
title: "Post Title Here"
date: YYYY-MM-DD
categories: category1 category2
excerpt: "Short, punchy preview text for the home page"
---
```

### Required Fields

- **layout**: Always `post` (no exceptions)
- **title**: Quoted string, clear and compelling
- **date**: Format `YYYY-MM-DD` (matches filename date)
- **categories**: Space-separated or array format (see below)

### Optional Fields

- **excerpt**: Strongly recommended. One sentence, max 2. Punchy, not descriptive.
  - **CRITICAL**: Excerpt MUST be in the SAME language as the article content
  - If article is in English → excerpt in English
  - If article is in French → excerpt in French
  - Language of title is irrelevant, follow the content language
  - **YAML QUOTING**: See "YAML String Quoting" section below
- **lang**: Only if non-English (e.g., `lang: fr`)

### YAML String Quoting (CRITICAL)

**Problem**: YAML strings with quotes inside break parsing and cause posts to render without titles.

**Rules for excerpts and titles containing quotes:**

```yaml
# ❌ BROKEN - Double quotes inside double quotes
excerpt: "Everyone wants to be "data-driven," but..."

# ✅ CORRECT - Single quotes outside, double quotes inside
excerpt: 'Everyone wants to be "data-driven," but...'

# ❌ BROKEN - Single quotes (apostrophes) inside single quotes
excerpt: 'It's a problem when you're asking...'

# ✅ CORRECT - Escape apostrophes by doubling them
excerpt: 'It''s a problem when you''re asking...'
```

**Quick Reference:**

| Content has... | Use outer... | Escape inner... |
|----------------|--------------|-----------------|
| Double quotes `"..."` | Single quotes `'...'` | Nothing needed |
| Apostrophes `it's` | Single quotes `'...'` | Double them `''` |
| Both quotes and apostrophes | Single quotes `'...'` | Double apostrophes `''` |

**Example with both:**
```yaml
# Content: He said "it's fine" but you're wrong
excerpt: 'He said "it''s fine" but you''re wrong'
```

**Validation**: Always validate YAML after creating front matter (see Workflow section).

### Category Format

Both formats are acceptable:

```yaml
# Space-separated (preferred for 1-3 categories)
categories: ai productivity

# Array format (for 3+ categories or complex names)
categories: [digital, work, tech]
```

### Common Categories

Analyze existing posts, but common patterns include:
- **ai** - AI-related content
- **productivity** - Productivity and work methods
- **coding** - Programming and development
- **data** - Data engineering and analytics
- **testing** - Testing strategies
- **marketing** - Marketing and growth
- **digital** - Digital transformation
- **work** - Work culture and philosophy
- **tech** - General technology

**Rule**: Use existing categories when possible. Only create new ones if truly necessary.

## Filename Convention

Jekyll requires strict filename format:

```
YYYY-MM-DD-title-slug-kebab-case.md
```

**Rules:**
- Date must match front matter date
- Slug is kebab-case (lowercase, hyphens)
- Keep slug concise (3-7 words max)
- Use English for slug even if content is French
- Extension is `.md`

**Examples:**
- ✅ `2025-12-30-the-10x-is-here-its-a-skill-issue.md`
- ✅ `2025-12-20-inverting-the-data-testing-pyramid-optimizing-for-time-to-insight.md`
- ❌ `2025-12-30-The-10X-Skill-Issue.md` (wrong case)
- ❌ `article-about-ai.md` (missing date)
- ❌ `2025-12-30-the_10x_article.md` (underscores instead of hyphens)

## Excerpt Guidelines

The excerpt appears on the home page. Make it count.

**CRITICAL RULE: Language Matching**
- ✅ English article → English excerpt
- ✅ French article → French excerpt
- ❌ English article → French excerpt (NEVER do this)
- The excerpt language MUST match the article content language, not the title

**Good excerpts:**
- ✅ "Two months from 'models aren't there' to 'not claiming the 10X boost is a skill issue.' The real skill isn't coding anymore. It's letting go." (English article)
- ✅ "The puck moved. Stop staring at where it was." (English article)
- ✅ "Laziness isn't the problem. It's the symptom and AI is the revealer." (English article)

**Bad excerpts:**
- ❌ "In this article, I discuss how AI is changing programming..."
- ❌ "A comprehensive guide to understanding the impact of..."
- ❌ "This post explores several key themes including..."
- ❌ "Deux mois pour que Karpathy..." (when article is in English)

**Rules:**
- **Language MUST match content** (most important rule)
- No meta-commentary ("in this post", "I discuss")
- No filler words
- Hook or provoke, don't describe
- One punchy sentence or two short ones
- Can be a quote from the article

## Markdown Formatting

### Section Separators

**CRITICAL: DO NOT use `---` separators in article body.**

- ❌ **Never** use `---` to separate sections in the article content
- ✅ Use paragraph breaks and natural transitions instead
- The article should flow as continuous prose without visual breaks

Only `---` allowed is in the YAML front matter delimiter.

### Links

Use standard markdown links:

```markdown
[link text](https://url.com)
```

For tweets/social media, integrate naturally:

```markdown
Andrej Karpathy [said](https://x.com/karpathy/status/123) that...
```

### Images

```markdown
![alt text](/assets/images/filename.png)
```

Images go in `/assets/images/` directory.

### Headings

```markdown
## Main Section
### Subsection
```

Start with `##` (h2) since `#` is the title.

### Bold

Use **bold** for emphasis on key insights:

```markdown
**This is the critical point**
```

### Quotes

Use blockquotes for citations:

```markdown
> "Quote text here"
```

## Content Integration

### External References

When integrating tweets, articles, or external content:

1. **Read the source** if provided
2. **Quote accurately** with proper attribution
3. **Link inline** not in footnotes
4. **Preserve context** of the original

### Example Integration

```markdown
Andrej Karpathy [wrote](https://x.com/...) in December 2025: "I've never felt this behind as a programmer."

Two months earlier, [he said](https://x.com/...) the models "are not there. It's slop."
```

## Pre-Publication Checklist

Before creating the post file:

- [ ] Front matter is complete and valid YAML
- [ ] Filename matches `YYYY-MM-DD-slug.md` pattern
- [ ] Date in filename matches front matter date
- [ ] Categories use existing ones when possible
- [ ] Excerpt is punchy and hook-focused
- [ ] All links are valid markdown
- [ ] No trailing spaces or formatting issues
- [ ] Headings start at `##` (h2 level)

## Workflow Integration

### Step 1: Analyze Existing Posts

Before creating a new post:

```bash
# Get the 5 most recent posts only
ls -t _posts/*.md | head -5
```

Read these 5 posts and extract:
- Common categories (reuse when possible)
- Excerpt style (language, tone, length)
- Front matter patterns
- Markdown conventions

**Optimization**: Only analyze the 5 most recent posts, not the entire archive.

### Step 2: Generate Post Structure

Create the file with proper front matter based on user content.

### Step 3: Validate YAML

**CRITICAL**: Always validate YAML syntax before committing. Use this Python snippet:

```bash
python3 -c "
import yaml
with open('_posts/YYYY-MM-DD-your-post.md', 'r') as f:
    content = f.read()
    parts = content.split('---', 2)
    try:
        fm = yaml.safe_load(parts[1])
        print('✓ Valid YAML')
        print(f'  title: {fm.get(\"title\", \"MISSING\")}')
    except Exception as e:
        print(f'✗ YAML ERROR: {e}')
"
```

After validation:
- Check filename matches pattern
- Verify front matter parses correctly (title visible)
- Ensure categories are consistent

### Step 4: Invoke Writing Skill

For content quality, consider invoking the `impactful-writing` skill:

```
Use the impactful-writing skill to polish this article
```

## Common Pitfalls to Avoid

❌ **Wrong date format**: `12-30-2025` instead of `2025-12-30`
❌ **Missing quotes in title**: `title: My Post` instead of `title: "My Post"`
❌ **Descriptive excerpts**: "This article discusses..." instead of punchy hook
❌ **New categories unnecessarily**: Creating `programming` when `coding` exists
❌ **Underscores in filename**: `my_post.md` instead of `my-post.md`
❌ **Wrong heading levels**: Starting with `#` instead of `##`
❌ **Unquoted YAML strings with colons**: Break parsing
❌ **Unescaped quotes in excerpts**: `excerpt: "be "data-driven""` breaks YAML - use single quotes outside

## Jekyll-Specific Notes

### Liquid Tags

Avoid Liquid tags unless necessary. GitHub Pages uses Kramdown, which handles most needs with standard markdown.

### Syntax Highlighting

Use fenced code blocks with language:

````markdown
```python
def example():
    return "code"
```
````

### Permalinks

Don't set custom permalinks. Use default structure from `_config.yml`:

```
/:year/:month/:day/:title/
```

## When Invoked

This skill will:

1. **Read the 5 most recent posts** from `_posts/` to understand current patterns
2. **Extract front matter conventions** and common categories
3. **Generate properly formatted post** with:
   - Valid Jekyll front matter
   - Correct filename (YYYY-MM-DD-slug.md)
   - Consistent categories (reuse existing ones)
   - Punchy excerpt **in the same language as the content**
4. **Validate the structure** before creation
5. **Suggest invoking impactful-writing skill** if content needs polishing

---

**Remember**: This skill handles TECHNICAL FORMAT. For writing STYLE (flow, impact, transitions), use the `impactful-writing` skill.
