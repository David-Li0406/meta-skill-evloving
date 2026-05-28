# Documentation Tracker - Detailed Examples

This reference file contains comprehensive examples and edge cases for the doc-tracker skill.

## CLAUDE_SOURCES.md Examples

### Standard Research Entries

```
[User] WebSearch("PostgreSQL INSERT INTO SELECT documentation official"): https://www.postgresql.org/docs/current/sql-insert.html
[Auto] WebFetch("https://go.dev/blog/embed", "How to use embed.FS for static files"): embed.FS embeds files at compile time, use fs.Sub to extract subdirectories
[Auto] Grep("embed.FS", "*.go"): Found implementation in embed.go:14-88 using //go:embed directive
[User] Read("/usr/share/doc/gin/routing.md", "Route ordering best practices"): Routes matched sequentially, register specific routes before wildcards
[Auto] WebSearch("Fyne GUI main thread requirements Linux"): https://developer.fyne.io/architecture/threading
```

### Local Documentation Searches

```
[Auto] Grep("CORS configuration", "api/*.go"): Found CORS setup in api/routes.go:13-23 with wildcard origin
[User] Read("go.mod", "Check Gin version"): Using gin-gonic/gin v1.9.1
[Auto] Glob("*.md"): Found README.md, CLAUDE.md, context.md in project root
```

### Web Research Patterns

```
[User] WebSearch("React useEffect cleanup function best practices 2025"): https://react.dev/reference/react/useEffect#cleanup-function
[Auto] WebFetch("https://pkg.go.dev/embed", "Check FS interface methods"): embed.FS implements fs.FS and fs.ReadDirFS interfaces
[User] WebSearch("Raspberry Pi 5 7-inch touchscreen resolution specs"): https://www.raspberrypi.com/documentation/accessories/display.html
```

## CLAUDE_PROMPTS.md Examples

### Simple Feature Implementation

```
Prompt: "init git"
Outcome: Initialized repository, created .gitignore excluding build artifacts (ui-web/dist/, app-test-arm64, node_modules/), made initial commit with 28 files

```

### Complex Multi-Step Task

```
Prompt: "Add dark mode toggle to settings"
Outcome: Implemented dark mode with context provider, CSS-in-JS theme switching, and persistent localStorage. Updated 8 components to support theming.

```

### Debugging and Optimization

```
Prompt: "Optimize the database queries causing slow dashboard load"
Outcome: Added composite indexes on user_id+timestamp columns, implemented query result caching with 5-minute TTL, reduced average load time from 3.2s to 0.4s

```

### Refactoring Work

```
Prompt: "Refactor the authentication middleware to support OAuth2"
Outcome: Extracted auth logic into separate middleware package, added OAuth2 provider interface, implemented Google and GitHub providers, maintained backward compatibility with existing JWT auth

```

### Investigation and Research

```
Prompt: "Figure out why the embedded React app returns 404 for assets"
Outcome: Discovered fs.Sub() extracts subdirectory but Gin's FileFromFS causes 301 redirects. Fixed by serving with c.Data() and manual MIME type detection using mime.TypeByExtension()

```

## Edge Cases

### Empty Files

When files don't exist yet, create with appropriate starter content:

**CLAUDE_SOURCES.md**: Create empty (no header)
```
[Auto] WebSearch("first query"): https://example.com
```

**CLAUDE_PROMPTS.md**: Create with header
```markdown
# CLAUDE_PROMPTS.md

This file tracks significant prompts and development decisions.

---

Prompt: "init git"
Outcome: Initialized repository with .gitignore

```

### File Already Exists with Content

Use Edit tool to append at the end:

**Before**:
```
[User] WebSearch("Go embed tutorial"): https://go.dev/blog/embed
```

**After Edit**:
```
[User] WebSearch("Go embed tutorial"): https://go.dev/blog/embed
[Auto] WebFetch("https://gin-gonic.com/docs/", "CORS middleware setup"): Use gin.Default() with cors middleware from gin-contrib/cors
```

### Attribution Decision Guide

**[User]** - Use when:
- User explicitly asked you to search/fetch
- User's question requires you to look up information
- User requested documentation

**[Auto]** - Use when:
- You decided to verify something
- You're researching to complete a task
- You're checking current best practices
- You're looking up syntax or API details

### Multi-Line Results

Keep results on single line using semicolons for compound information:

```
[Auto] WebFetch("https://example.com/api", "Extract rate limits"): Rate limits are 100 req/hour for free tier; 1000 req/hour for paid; uses X-RateLimit headers
```

### Failed Searches

Only track successful searches that yielded useful results. Skip tracking if:
- Search returned no useful results
- WebFetch failed with 404/timeout
- Grep found no matches

### Concurrent Tracking

If performing multiple searches in parallel, track all of them:

```
[Auto] WebSearch("React 19 new features"): https://react.dev/blog/2024/react-19
[Auto] WebSearch("Vite 5 migration guide"): https://vitejs.dev/guide/migration
[Auto] WebSearch("TypeScript 5.4 release notes"): https://devblogs.microsoft.com/typescript/announcing-typescript-5-4/
```
