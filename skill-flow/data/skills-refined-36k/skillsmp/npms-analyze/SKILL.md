---
name: npms-analyze
description: Analyze npm package quality using NPMS.io scores for quality, popularity, and maintenance. Use when the user asks for package quality analysis, NPMS scores, or package evaluation metrics.
---

# Analyze npm Package Quality (NPMS.io)

Analyze an npm package using NPMS.io quality, popularity, and maintenance scores.

## Usage

```bash
npx tsx scripts/analyze.ts <package-name> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `package-name` | Yes | The exact package name (case-sensitive) |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
react - Package Analysis
-------------------------

Quality Scores:
  Overall: 98/100
  Quality: 95/100
  Popularity: 100/100
  Maintenance: 99/100

Package Information:
  Version: 18.2.0
  Description: A declarative, efficient, and flexible JavaScript library...
  Published: 2013-05-24

npm Statistics:
  Week: 2,345,678 downloads
  Month: 9,876,543 downloads
  Year: 98,765,432 downloads

GitHub Activity:
  Stars: 213,456
  Forks: 45,678
  Open Issues: 1,234
  Contributors: 1,567
  Latest Commit: 2 days ago

Project Health:
  ✓ Has contributing guide
  ✓ Has license
  ✓ Has security policy
```

## Script Execution (Preferred)

```bash
npx tsx scripts/analyze.ts <package-name> [options]
```

Options:
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npms-io plugin directory: `~/.claude/plugins/cache/npms-io/`

## Package Analysis API

```
GET https://api.npms.io/v2/package/{package}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `package` | Yes | The exact package name (case-sensitive) |

### Examples

Get package analysis:
```
https://api.npms.io/v2/package/react
```

## Response Format

The response contains comprehensive package analysis:

### Metadata
- `name`, `version`, `description`, `keywords`
- Links (npm, homepage, repository, bugs)
- Author, maintainers, publishers
- Publication date

### npm Data
- `downloads` - Download counts over time
- `weekDownloads`, `monthDownloads`, `quarterDownloads`, `yearDownloads`

### GitHub Data
- `stars`, `forks`, `subscribers`
- `issues` (open, closed, total)
- `pull requests` (open, closed, total)
- `contributors`, `commitCount`
- `latestCommit` (sha, date, message)
- `recentReleases`, `firstRelease`, `latestRelease`
- Quality flags: participatesInCoc, hasCustomCodeOfConduct, hasOpenDiscussions, hasContributingGuide, hasLicense, hasSecurityPolicy

### Score (0-100)
- `final` - Overall score
- `quality` - Code quality assessment
- `popularity` - Community adoption
- `maintenance` - Project maintenance status

## Caching

Package analysis is cached for 6 hours. NPMS.io data updates relatively infrequently, and package metrics change slowly over time.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `npms-compare` to compare multiple packages side-by-side
- Use `npms-suggest` to find similar packages by name
- Use `npm-info` for detailed package metadata
- Use `npm-downloads` for download statistics

## Error Handling

**Package not found**: The package may not exist in NPMS.io database. New packages may take time to be analyzed.

**Incomplete analysis**: Some packages may lack GitHub integration or download data, resulting in partial scores.

**Analysis pending**: Newly published packages may not have completed analysis. Check back later.

## Interpreting Scores

| Score Range | Quality Level | Recommendation |
|-------------|---------------|----------------|
| 90-100 | Excellent | Safe to use, well-maintained |
| 75-89 | Good | Generally reliable |
| 60-74 | Fair | Use with caution, review dependencies |
| 0-59 | Poor | Avoid, look for alternatives |

## Use Cases

### Package Selection
Compare alternatives before choosing:
```bash
npx tsx scripts/analyze.ts express
npx tsx scripts/analyze.ts koa
npx tsx scripts/analyze.ts fastify
```

### Dependency Health
Check your dependencies:
```bash
npx tsx scripts/analyze.ts lodash
npx tsx scripts/analyze.ts axios
```

### Research
Evaluate new packages:
```bash
npx tsx scripts/analyze.ts new-popular-package
```

## Notes

- NPMS.io is independent of npm, providing third-party quality assessment
- Analysis includes data from npm registry, GitHub, and other sources
- Scores are algorithmically calculated based on multiple factors
- Not all packages have complete GitHub integration data
- Scores update periodically as package activity changes
