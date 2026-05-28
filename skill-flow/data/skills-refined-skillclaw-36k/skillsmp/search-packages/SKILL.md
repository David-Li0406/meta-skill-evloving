---
name: search-packages
description:
  Search for the best modern library for a given purpose. Use when the user asks to find the best library for [purpose].
model: claude-haiku-4-5
allowed-tools:
  - ListMcpResourcesTool
  - ReadMcpResourceTool
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - WebSearch
  - WebFetch
---

# Package Evaluation (Finding the Best Modern Library)

When the task involves choosing a library (e.g., "what's the best PDF library",
"recommend a date picker"), use this workflow:

### Step 1: Check Org Docs First

A best library may have already been found and documented! Query the "docs" MCP
server for library-specific documentation:

1. Use `ListMcpResourcesTool` with `server: "docs"` to list available resources
2. Look for matching library docs in `org://docs/libraries/` (e.g.,
   `org://docs/libraries/tanstack-query.md`) or docs that have a similar
   category to the user prompt.
3. Use `ReadMcpResourceTool` to read the org docs and see if there is a
   preferred library mentioned.

### Step 2: Search Community Forums

Use `WebSearch` with queries like:

- `"best [purpose] library typescript reddit 2024"` or current year
- `"[purpose] npm package recommendations reddit"`
- `"[library-name] vs [alternative] typescript"`

Reddit and forums reveal real-world issues that docs won't show—maintenance
problems, hidden gotchas, and migration pain.

### Step 3: Verify Library Health

**ALWAYS fetch and include these metrics for each candidate** (use `WebFetch` on
GitHub repo and npm pages):

1. **GitHub Stars**: Indicates community adoption and trust
2. **Last Update Date**: When the library was last published/committed
3. **Weekly Downloads**: npm download count (indicates active usage)

For each candidate, also check:

4. **Last Update Health**:
   - **Red flag**: >2 years ago (likely abandoned)
   - **Yellow flag**: 6-24 months ago
   - **Green flag**: Within 6 months

5. **TypeScript Support**:
   - Built-in types (best): Ships with the package
   - `@types/` package: Acceptable but may lag
   - No types: Avoid for TypeScript projects

6. **Maintenance Signals**: Open issues, response time, release frequency

### Step 4: Check for Modern Alternatives

- Search `"[old-library] alternative 2024"` or `"modern [purpose] library"`
- Check for deprecation notices
- Prefer libraries with ESM support and tree-shaking

### Library Recommendation Output

```markdown
## Library Recommendation: [Purpose]

### Recommended [library-name]

- GitHub Stars: [count]
- Last updated: [date]
- TypeScript: [Built-in / @types / None]
- Weekly downloads: [count]
- Why: [1-2 sentence justification]

### Alternatives Considered

- [alt-1]: [why not - e.g., "last updated 2019"]
- [alt-2]: [why not - e.g., "no TypeScript support"]

### Community Sentiment

**Summary of Forum 1 (XXX upvotes)**\
https://reddit.com/r/foo/bar.md

**Summary of Forum 2 (XXX upvotes)**\
https://reddit.com/r/foo/baz.md

<answer-goes-here>
```

## Examples

### Example 1: User needs to choose a library

**Query**: "What's the best PDF generation library for TypeScript?"

**Process**:

1. Check org docs → Not found in any docs in `org://docs/libraries/`
2. Search Reddit/forums → `WebSearch: "best pdf library typescript reddit 2024"`
3. Identify candidates (e.g., pdf-lib, pdfkit, jspdf, puppeteer)
4. Verify each candidate:
   - Check npm for last update date
   - Check for built-in TypeScript types
   - Look at GitHub stars/issues
5. Return:

```markdown
### Library Recommendation: PDF Generation

**Recommended**: pdf-lib

- Last updated: 2024-01
- TypeScript: Built-in
- Weekly downloads: 1.2M
- Why: Pure JS, no native deps, great TS support, actively maintained

**Alternatives Considered**:

- pdfkit: Good but requires @types package, less TS-native
- jspdf: Last major update 2022, community reports maintenance slowdown
- puppeteer: Overkill for simple PDF generation, heavy dependency

**Community Sentiment**: Reddit consensus favors pdf-lib for new TypeScript
projects due to modern API and zero native dependencies.
```
