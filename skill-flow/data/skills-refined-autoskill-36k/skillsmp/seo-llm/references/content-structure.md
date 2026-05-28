# LLM-Friendly Content Structure

## Core Principles

1. **Lead with the answer** - Put the most important information first
2. **Use clear hierarchy** - Logical heading structure (H1→H2→H3)
3. **One idea per paragraph** - Short, focused paragraphs
4. **Define terms explicitly** - Don't assume knowledge
5. **Structure data visually** - Use tables and lists for facts

## Document Structure

### Optimal Layout

```markdown
# Clear, Descriptive Title

**Summary/TL;DR:** One paragraph that directly answers the main question
or describes the key takeaway. This should stand alone.

## What is [Topic]?

Clear definition in the first sentence. Additional context follows.
No assumed knowledge - define all terms.

## Key Concepts

| Concept | Definition | Example |
|---------|------------|---------|
| Term 1 | Clear explanation | Practical example |
| Term 2 | Clear explanation | Practical example |

## How to [Action]

Step-by-step instructions:

1. **First step** - Explanation of what to do and why
2. **Second step** - Explanation of what to do and why
3. **Third step** - Explanation of what to do and why

## Common Questions

### Question 1?

Direct answer in the first sentence. Then elaborate with context.

### Question 2?

Direct answer in the first sentence. Then elaborate with context.

## Related Topics

- [Related Topic 1](/link) - Brief description
- [Related Topic 2](/link) - Brief description
```

## Heading Best Practices

### Good Headings

```markdown
## What is React? (Clear question format)
## Installing Node.js (Action-oriented)
## Common React Mistakes (Topic + qualifier)
## React vs Vue: Key Differences (Comparative)
```

### Bad Headings

```markdown
## Introduction (Too vague)
## More Info (Meaningless)
## Part 1 (No content indication)
## Stuff to Know (Informal, vague)
```

### Heading Hierarchy

```markdown
# Page Title (One per page)
  ## Main Section 1
    ### Subsection 1.1
    ### Subsection 1.2
  ## Main Section 2
    ### Subsection 2.1
```

Never skip levels (H1→H3 without H2).

## Lists and Tables

### When to Use Lists

- Steps in a process
- Features or benefits
- Requirements
- Options or alternatives
- Simple comparisons

```markdown
**Do use lists for:**
- Related items
- Scannable content
- Steps or sequences

**Don't use lists for:**
- Single items
- Narrative content
- Complex explanations
```

### When to Use Tables

- Comparing multiple items across attributes
- Reference data (commands, options)
- Structured facts

```markdown
| Framework | Language | Learning Curve | Use Case |
|-----------|----------|----------------|----------|
| React | JavaScript | Moderate | SPAs, UI components |
| Django | Python | Steep | Full-stack web apps |
| Express | JavaScript | Gentle | APIs, backends |
```

## Writing for Extraction

### Explicit Definitions

```markdown
<!-- Bad: Assumes knowledge -->
HMR significantly improves DX during development.

<!-- Good: Defines terms -->
Hot Module Replacement (HMR) updates code in the browser
without a full page reload. This improves developer experience (DX)
by preserving application state during development.
```

### Concrete Examples

```markdown
<!-- Bad: Abstract -->
Authentication tokens should be stored securely.

<!-- Good: Concrete -->
Store JWT tokens in HttpOnly cookies, not localStorage.
HttpOnly cookies cannot be accessed by JavaScript,
preventing XSS attacks from stealing tokens.
```

### Numbered Facts

```markdown
Key React performance metrics:
1. First Contentful Paint (FCP): under 1.8 seconds
2. Time to Interactive (TTI): under 3.8 seconds
3. Cumulative Layout Shift (CLS): under 0.1
```

## FAQ Optimization

### For Rich Results

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is the difference between React and Vue?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "React uses JSX and a virtual DOM with one-way data flow. Vue uses templates with two-way data binding. React has a larger ecosystem; Vue has gentler learning curve."
    }
  }]
}
</script>
```

### In Content

```markdown
## Frequently Asked Questions

### What is the difference between React and Vue?

React uses JSX and a virtual DOM with one-way data flow.
Vue uses templates with two-way data binding.
React has a larger ecosystem; Vue has a gentler learning curve.
```

## Avoiding Anti-Patterns

### Don't Hide Information

```markdown
<!-- Bad: Important info buried -->
There are many ways to authenticate users.
After much research and consideration of various factors,
we've found that JWT tokens work well. [paragraph continues...]
The tokens should be stored in HttpOnly cookies.

<!-- Good: Key info upfront -->
Store JWT tokens in HttpOnly cookies for authentication.
This prevents XSS attacks from accessing tokens via JavaScript.
```

### Don't Use Images for Text

```markdown
<!-- Bad -->
<img src="pricing-table.png" alt="pricing">

<!-- Good -->
| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 100 requests |
| Pro | $29 | 10,000 requests |
```

### Don't Assume Context

```markdown
<!-- Bad: Context-dependent -->
As mentioned above, you should use this approach.
The previous section explained why.

<!-- Good: Self-contained -->
Use environment variables for configuration.
This keeps secrets out of code and allows
different settings per environment.
```

## Content Audit Checklist

- [ ] Title clearly describes content
- [ ] Summary/TL;DR at the top
- [ ] Single H1, logical heading hierarchy
- [ ] Terms defined on first use
- [ ] Key facts in tables or lists
- [ ] No text-heavy images
- [ ] Paragraphs under 4 sentences
- [ ] Each section stands alone
- [ ] FAQ section with direct answers
- [ ] Examples are concrete, not abstract

## Tools

```bash
# Check heading structure
npx markdownlint "**/*.md"

# Check reading level
npx textstat-cli file.md

# Validate HTML structure
npx html-validate index.html
```
