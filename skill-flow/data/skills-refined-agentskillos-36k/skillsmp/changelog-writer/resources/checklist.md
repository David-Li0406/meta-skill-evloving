# Changelog Pre-Publish Checklist

Quick checklist before publishing. 2 minutes max.

## 1. Fact Check (Critical)

Compare against `docs/architecture/implementation-status/README.md`:

- [ ] Every feature mentioned is actually complete
- [ ] Incomplete features marked "Not yet" or "when N+ customers request"
- [ ] No overselling (e.g., "GitHub Integration" → "GitHub File Sync (File Contents)")
- [ ] Limitations disclosed (what's NOT included)

## 2. Frontmatter Validation (Required)

- [ ] `title`: 2-3 key features, clear and specific
- [ ] `slug`: URL-safe, matches version or feature theme
- [ ] `description`: 150-160 characters (count: ___)
- [ ] `date`: Valid ISO date format
- [ ] `status`: Set to `draft`
- [ ] `source_prs`: All source PRs/commits listed
- [ ] `excerpt`: Max 300 characters, distinct from description
- [ ] `tldr`: 50-100 words, self-contained summary
- [ ] `focusKeyword`: Selected from target keywords list

## 3. Optional SEO Fields

- [ ] `secondaryKeywords`: Relevant secondary keyword (if applicable)
- [ ] `faq`: 2-4 Q&A pairs with search-optimized questions

## 4. SEO Content

- [ ] 3+ internal links to docs
- [ ] At least 1 code example per major feature
- [ ] Technical specifics present (not just marketing fluff)

## 5. Style

- [ ] 1-3 sentences per feature (not long paragraphs)
- [ ] "You can now..." not "Users are able to..."
- [ ] No emoji
- [ ] Professional tone throughout

## 6. Red Flags

**DO NOT PUBLISH if you see:**

- "Coming soon: Linear, Notion" (use "when 3+ customers request")
- "GitHub Integration" without specifying what (files/PRs/issues)
- Claims about features at 0% in implementation docs
- No limitations disclosed for partial features
- Meta description missing or >160 chars
- No code examples
- `tldr` is missing or too short (< 50 words)
- `excerpt` is identical to `description`
- `focusKeyword` not present in body text
- `faq` questions don't match real search queries

## Quick Reference

### Bad → Good

| Bad | Good |
|-----|------|
| "Plans for Linear, Notion, and Slack!" | "When 3+ customers request: Linear (1-2 week implementation)" |
| "GitHub Integration is live" | "GitHub Repository Sync (File Contents). Not yet: PR metadata (v0.2)" |
| Long paragraph describing feature | 1-3 sentences with bullet points |
| "Users are able to search" | "You can now search" |

## Transparency Questions

For every feature, ask:

- [ ] Is this 100% complete and in production?
- [ ] Are there limitations users should know?
- [ ] Is this beta/rolling out?
- [ ] Did I verify against implementation docs?
- [ ] Would a developer hit any surprises?
