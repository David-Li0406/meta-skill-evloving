---
name: bib-cite-web
description: Create bibliography citations from web page URLs with automatic Wayback Machine archival and metadata extraction. Use when the user asks to cite a website, create a citation for a URL, archive and cite a web page, or generate a bibliography entry from a web address.
---

# Web Page Citation Creator

Create bibliography citations from web page URLs with automatic archival snapshot and metadata extraction.

## Features

- **Wayback Machine Integration**: Automatically submits URLs to the Internet Archive for preservation
- **Metadata Extraction**: Extracts title, author, description, site name, and publish date from semantic HTML
- **Multiple Formats**: Outputs citations in BibTeX or CSL JSON format
- **Smart Citation Keys**: Generates citation keys from domain + author + year

## Usage

```bash
npx tsx plugins/bib/scripts/cite-web.ts <url>
npx tsx plugins/bib/scripts/cite-web.ts <url> --format=bibtex
npx tsx plugins/bib/scripts/cite-web.ts <url> --no-wayback
npx tsx plugins/bib/scripts/cite-web.ts <url> --output=citations.bib
```

## Metadata Extraction

The script extracts metadata from semantic HTML tags:

### Title
- `<title>` tag
- Open Graph: `<meta property="og:title">`
- Twitter Card: `<meta name="twitter:title">`
- Standard: `<meta name="title">`

### Author
- `<meta name="author">`
- Open Graph: `<meta property="og:author">` or `<meta property="article:author">`
- Twitter Card: `<meta name="twitter:creator">`

### Description
- `<meta name="description">`
- Open Graph: `<meta property="og:description">`
- Twitter Card: `<meta name="twitter:description">`

### Site Name
- Open Graph: `<meta property="og:site_name">`
- `<meta name="application-name">`

### Published Date
- Open Graph: `<meta property="article:published_time">`
- `<meta name="publish-date">` or `<meta name="date">`

## Arguments

- **Positional argument**: URL to cite
- **`--file <path>`**: Read URL from file (uses first line)
- **`--format <format>`**: Output format (default: bibtex)
  - `bibtex` or `bib`: BibTeX format
  - `csl`, `json`, or `csl-json`: CSL JSON format
- **`--no-wayback`**: Skip Wayback Machine submission (faster, but no archive)
- **`--output <file>`**: Write output to file (default: stdout)

## Output Formats

### BibTeX

```bibtex
@online{smithexample2024,
  author = {John Smith},
  title = {Example Article Title},
  url = {https://example.com/article},
  urldate = {2024-03-15},
  year = {2024}
}
```

### CSL JSON

```json
[
  {
    "id": "smithexample2024",
    "type": "webpage",
    "title": "Example Article Title",
    "author": [{"literal": "John Smith"}],
    "URL": "https://example.com/article",
    "accessed": {"date-parts": [[2024, 3, 15]]},
    "archive-url": "https://web.archive.org/web/20240315123456/https://example.com/article"
  }
]
```

## Examples

### Basic citation

```bash
npx tsx plugins/bib/scripts/cite-web.ts "https://example.com/article"
```

Output:
```bibtex
@online{example2024,
  title = {Example Article Title},
  url = {https://example.com/article},
  urldate = {2024-03-15}
}
```

### With Wayback archival

```bash
npx tsx plugins/bib/scripts/cite-web.ts "https://blog.example.com/post"
```

Output includes archive URL:
```bibtex
@online{example2024,
  title = {Blog Post Title},
  url = {https://blog.example.com/post},
  urldate = {2024-03-15},
  note = {Archived at https://web.archive.org/web/20240315123456/...}
}
```

### CSL JSON format

```bash
npx tsx plugins/bib/scripts/cite-web.ts "https://docs.example.com" --format=csl
```

### Skip archival (faster)

```bash
npx tsx plugins/bib/scripts/cite-web.ts "https://example.com" --no-wayback
```

### Save to file

```bash
npx tsx plugins/bib/scripts/cite-web.ts "https://example.com" --output=citations.bib
```

### Batch processing

```bash
# Create file with URLs (one per line)
echo "https://example.com/article1" > urls.txt

# Cite each URL
while read url; do
  npx tsx plugins/bib/scripts/cite-web.ts "$url" >> citations.bib
done < urls.txt
```

## Citation Key Generation

Citation keys are automatically generated from:
1. **Domain name**: `example.com` → `example`
2. **Author** (if available): `John Smith` → `smith`
3. **Year**: Archive date or publish date or current year

Examples:
- `https://blog.example.com/post` by John Smith (2024) → `smithexample2024`
- `https://example.com/article` (no author, 2023) → `example2023`

## Wayback Machine Integration

By default, the script submits URLs to the Internet Archive's Wayback Machine for preservation:

1. **Submission**: Sends URL to `https://web.archive.org/save/<url>`
2. **Archive URL**: Extracts the permanent archive URL from response
3. **Archive Date**: Records the snapshot timestamp
4. **Fallback**: If submission fails, continues without archive

The archive URL is included in the citation:
- **BibTeX**: In `note` field or custom `archiveurl`/`archivedate` fields
- **CSL JSON**: In `archive-url` field

**Skip archival** with `--no-wayback` for faster execution when archiving isn't needed.

## Error Handling

The script handles various error scenarios:

- **Invalid URL**: Validates URL format before processing
- **Fetch failures**: Reports HTTP errors with status codes
- **Missing metadata**: Falls back to "Untitled" for missing titles
- **Wayback failures**: Continues without archive if submission fails
- **No author**: Omits author field if not found

Errors are written to stderr, while citations are written to stdout (or file).

## Limitations

- **JavaScript-heavy sites**: May not extract metadata from dynamically rendered content
- **Paywalls**: Cannot access content behind authentication
- **Rate limiting**: Wayback Machine may rate-limit submissions
- **No PDF support**: Only HTML pages (use separate tool for PDFs)
- **Simple parsing**: Uses regex matching, not full DOM parsing

For complex pages or JavaScript-rendered content, consider:
1. Using `--no-wayback` to skip archival
2. Manually editing the citation after generation
3. Using browser developer tools to inspect metadata tags

## Related Skills

- **bib-create**: Create bibliography entries interactively
- **bib-read**: View existing bibliography entries
- **bib-convert**: Convert between bibliography formats
- **wayback-submit**: Submit URLs to Wayback Machine without citation generation
