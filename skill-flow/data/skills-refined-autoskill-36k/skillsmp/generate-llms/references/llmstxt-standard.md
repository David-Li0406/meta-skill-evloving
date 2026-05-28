# llmstxt.org Standard Reference

This document summarizes the llmstxt.org standard for creating LLM-friendly documentation files.

## Overview

The llms.txt standard proposes adding a `/llms.txt` markdown file to websites to provide LLM-friendly content. This file offers brief background information, guidance, and links to detailed markdown files.

## Why llms.txt?

- **Context window limits**: LLMs can't process entire websites
- **HTML complexity**: Converting complex HTML to LLM-friendly text is difficult
- **Efficiency**: One curated file is better than crawling many pages
- **Accuracy**: Provides a "clean feed" of desired content

## File Format

The `/llms.txt` file follows this structure:

1. **H1** with the project/site name (required)
2. **Blockquote** with a short summary (optional but recommended)
3. **Zero or more markdown sections** with details (no headings)
4. **Zero or more H2 sections** containing "file lists" of URLs

### Example Structure

```markdown
# Project Name

> Brief description with key information

Optional details about the project.

## Section Name

- [Link title](url): Optional description of the link

## Optional

- [Link title](url): Links here can be skipped for shorter context
```

## The "Optional" Section

If included, URLs in the "Optional" section can be skipped when a shorter context is needed. Use for secondary information.

## llms-full.txt

The standard also proposes `/llms-full.txt`:

- **Comprehensive content**: Contains all relevant text from documentation
- **Plain markdown**: Removes HTML, CSS, JavaScript for clean data
- **Single file**: Faster for AI to ingest than crawling multiple pages
- **Complementary**: Works with llms.txt (table of contents) + llms-full.txt (content)

## Best Practices

1. **Use concise, clear language**
2. **Include brief, informative descriptions** for links
3. **Avoid ambiguous terms** or unexplained jargon
4. **Test with LLMs** to verify they can answer questions about your content
5. **Keep llms.txt curated** - it's not a sitemap
6. **Make llms-full.txt comprehensive** - include all important content

## Page-Specific llms.txt

For multi-page sites, you can have page-specific llms.txt files:

```
/llms.txt           # Homepage / site overview
/llms-full.txt      # Complete site content
/docs/llms.txt      # Documentation section
/api/llms.txt       # API reference section
```

## Relationship to Other Standards

- **robots.txt**: Controls crawler access; llms.txt provides content
- **sitemap.xml**: Lists all pages; llms.txt curates important ones
- **Structured data**: llms.txt can reference structured markup

## Tools and Integrations

- `llms_txt2ctx`: CLI for parsing llms.txt and generating LLM context
- Various plugins for VitePress, Docusaurus, Drupal
- VS Code PagePilot extension

## References

- [llmstxt.org](https://llmstxt.org/) - Official specification
- [GitHub repository](https://github.com/AnswerDotAI/llms-txt) - Spec source
