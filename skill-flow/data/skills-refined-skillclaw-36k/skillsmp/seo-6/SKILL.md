---
name: seo
description: SEO audit for local HTML files. Use when user wants to check SEO, analyze files for search optimization, or mentions SEO review/audit. Scans a directory for HTML files and analyzes meta tags, heading structure, images, links, and technical SEO signals. Provides severity-rated issues with fix suggestions.
---

# SEO Audit Skill

Analyze HTML files in a directory for SEO best practices. This skill scans local build output (e.g., `./dist`, `./build`, `./public`) and reports issues across 7 categories with severity ratings and actionable fixes.

## When to Use This Skill

Activate this skill when the user:

- Asks to check SEO for a directory or project
- Wants to audit HTML files for search optimization
- Mentions SEO review, SEO check, or SEO audit
- Provides a path to analyze (e.g., "./dist", "./build", "./out")
- Says things like "check my HTML for SEO", "run SEO audit", "analyze SEO"

## SEO Audit Categories

### 1. Meta Tags & Head Elements

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Title tag | 30-60 chars, present | >60 or <30 chars | Missing |
| Meta description | 120-160 chars | >160 or <120 chars | Missing |
| Viewport meta | `<meta name="viewport">` present | - | Missing |
| Charset | `<meta charset="utf-8">` or equiv | - | Missing |
| Canonical URL | `<link rel="canonical">` present | - | Missing (suggestion) |
| Open Graph | og:title, og:description, og:image | Partial (1-2 present) | All missing |
| Twitter Card | twitter:card present | - | Missing (suggestion) |

### 2. Heading Structure

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| H1 count | Exactly 1 per page | 0 or >1 | - |
| Heading hierarchy | Sequential (H1 -> H2 -> H3) | Skips levels (H1 -> H3) | No headings |
| H1 content | Text content, <70 chars | >70 chars | Empty or whitespace only |
| Heading uniqueness | All headings unique | Duplicate headings | - |

### 3. Images & Media

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Alt text | Present and descriptive | Present but empty (`alt=""`) | Missing on non-decorative |
| Image dimensions | width/height attributes set | - | Missing (CLS risk) |
| Lazy loading | `loading="lazy"` on images | - | Suggestion only |

### 4. Links & Navigation

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Anchor text | Descriptive text | Generic ("click here", "read more") | Empty links |
| External links | `rel="noopener"` on `target="_blank"` | - | Missing noopener |
| Internal links | Valid relative paths | - | Broken (file doesn't exist) |

### 5. Technical SEO Signals

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Language | `<html lang="...">` present | - | Missing |
| Robots meta | No conflicting directives | `noindex` on main pages | - |
| Structured data | Valid JSON-LD in `<script type="application/ld+json">` | Present but malformed | Suggestion only |
| Doctype | `<!DOCTYPE html>` present | - | Missing |

### 6. Performance Indicators (Static Analysis)

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Inline CSS | <14KB total | 14-50KB | >50KB |
| Render-blocking scripts | All scripts have `defer` or `async` | Some blocking | All blocking in `<head>` |
| Resource hints | `preconnect`, `prefetch` used | - | Suggestion only |

### 7. Content Quality

| Check | Good | Warning | Critical |
|-------|------|---------|----------|
| Text-to-HTML ratio | >25% text content | 10-25% | <10% |
| Word count | >300 words | 100-300 words | <100 words |
| Empty page | Has content | - | No visible text |

## Audit Process

### Step 1: Find HTML Files

```bash
# Use Glob tool to find all HTML files
Glob pattern: **/*.html
Path: [user-provided directory]
```

Handle errors:
- Directory not found: Report error with path
- No HTML files: Report "No HTML files found in [path]"
- Permission denied: Report specific file/directory

### Step 2: Analyze Each File

For each HTML file found:

1. **Read file contents** using Read tool
2. **Extract elements** for analysis:
   - `<head>` contents (meta tags, title, links, scripts)
   - All headings (`<h1>` through `<h6>`)
   - All images (`<img>` tags with src, alt, width, height, loading)
   - All links (`<a>` tags with href, rel, target, text content)
   - Structured data (`<script type="application/ld+json">`)
   - Inline styles (`<style>` tags)
   - Scripts in `<head>` without defer/async

3. **Run category checks** against thresholds
4. **Record issues** with:
   - File path (relative to scanned directory)
   - Line number (approximate based on content position)
   - Severity (CRITICAL, WARNING, SUGGESTION)
   - Description
   - Fix suggestion

### Step 3: Generate Report

Structure the report as follows:

```markdown
## SEO Audit Report

**Directory:** ./path/to/files
**Files Scanned:** N
**Issues Found:** X Critical, Y Warnings, Z Suggestions

---

### file1.html

#### Critical
- [Line N] Missing title tag
  Fix: Add `<title>Your Page Title</title>` in `<head>`

#### Warning
- [Line N] Title too long (75 chars, max 60)
  Fix: Shorten to under 60 characters

---

### file2.html
...
```

## Output Format

### Summary Section

```markdown
## SEO Audit Report

**Directory:** [scanned path]
**Files Scanned:** [count]
**Issues Found:**
- Critical: [count]
- Warning: [count]
- Suggestion: [count]
```

### Per-File Findings

For each file with issues:

```markdown
### [relative/path/to/file.html]

#### Critical
- **[Category]**: [Issue description]
  Line: [N] | Fix: [specific fix]

#### Warning
- **[Category]**: [Issue description]
  Line: [N] | Fix: [specific fix]

#### Suggestions
- **[Category]**: [Issue description]
  Fix: [specific fix]
```

### Severity Definitions

- **CRITICAL**: Blocks indexing or severely hurts rankings. Must fix.
  - Missing title tag
  - Missing meta description
  - Missing viewport meta (mobile-unfriendly)
  - No H1 heading
  - Images without alt text
  - Empty page content

- **WARNING**: Negatively impacts SEO or UX. Should fix.
  - Title/description too long or too short
  - Multiple H1 tags
  - Heading hierarchy skips levels
  - Low word count
  - Missing doctype
  - Render-blocking scripts

- **SUGGESTION**: Optimization opportunities. Nice to have.
  - Missing canonical URL
  - Missing Open Graph tags
  - Missing structured data
  - No lazy loading on images
  - No resource hints

### Clean Report

If no issues found:

```markdown
## SEO Audit Report

**Directory:** [path]
**Files Scanned:** [count]

All files pass SEO checks. No issues found.
```

## Behavior Rules

### Always

- Use Glob tool to find HTML files (not Bash find/ls)
- Use Read tool to read file contents (not Bash cat)
- Report file paths relative to the scanned directory
- Provide specific line numbers when possible
- Include actionable fix suggestions
- Group issues by file, then by severity
- Show summary counts at the top

### Never

- Auto-fix issues (report only)
- Analyze non-HTML files
- Claim to measure runtime metrics (LCP, CLS, etc.)
- Skip files due to size (analyze all HTML)
- Generate excessively long reports (prioritize critical issues)

### Error Handling

- **Directory not found**: "Error: Directory '[path]' not found"
- **No HTML files**: "No HTML files found in '[path]'. Check the path or ensure HTML files exist."
- **Read error**: Skip file, note in report: "Could not read [file]: [reason]"

## Skill Invocation Examples

This skill should activate when user says:

- "Run SEO audit on ./dist"
- "Check SEO for the build folder"
- "Analyze ./public for SEO issues"
- "SEO check my HTML files"
- "Audit ./out for SEO"
- "Check the SEO of my static site"
- "Review SEO in ./build"

### Example Session

```
User: "Run SEO audit on ./dist"

AI: [Activates skill]
    1. Uses Glob to find **/*.html in ./dist
    2. Reads each HTML file
    3. Analyzes against all 7 categories
    4. Generates report with issues grouped by file and severity
```

## Notes

- This skill analyzes static HTML only - no JavaScript execution
- Thresholds are fixed (same for all page types)
- Works with any directory containing HTML files (build output, static sites, etc.)
- Line numbers are approximate based on content position in file
