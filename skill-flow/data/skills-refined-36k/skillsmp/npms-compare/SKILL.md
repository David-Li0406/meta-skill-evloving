---
name: npms-compare
description: Compare multiple npm packages side-by-side using NPMS.io quality scores. Use when the user asks to compare packages, evaluate alternatives, or choose between multiple options.
---

# Compare npm Packages (NPMS.io)

Compare multiple npm packages side-by-side using NPMS.io quality scores.

## Usage

```bash
npx tsx scripts/compare.ts <package1> <package2> [package3...] [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `package1` | Yes | First package to compare |
| `package2` | Yes | Second package to compare |
| `package3...` | No | Additional packages to compare |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
Package Comparison: react vs vue vs angular
-------------------------------------------

┌──────────────┬──────────┬──────────┬──────────┐
│ Metric       │ react    │ vue      │ angular  │
├──────────────┼──────────┼──────────┼──────────┤
│ Overall      │ 98/100   │ 95/100   │ 92/100   │
│ Quality      │ 95/100   │ 93/100   │ 90/100   │
│ Popularity   │ 100/100  │ 97/100   │ 95/100   │
│ Maintenance  │ 99/100   │ 96/100   │ 91/100   │
├──────────────┼──────────┼──────────┼──────────┤
│ Version      │ 18.2.0   │ 3.3.4    │ 16.2.0   │
│ Stars        │ 213K     │ 204K     │ 92K      │
│ Forks        │ 45K      │ 34K      │ 25K      │
│ Issues       │ 1.2K     │ 890      │ 1.5K     │
│ Downloads/Mo │ 9.8M     │ 3.2M     │ 2.1M     │
└──────────────┴──────────┴──────────┴──────────┘
```

## Script Execution (Preferred)

```bash
npx tsx scripts/compare.ts <package1> <package2> [package3...] [options]
```

Options:
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npms-io plugin directory: `~/.claude/plugins/cache/npms-io/`

## Package Comparison API

```
POST https://api.npms.io/v2/package/mget
Content-Type: application/json

["package1", "package2", "package3"]
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `packages` | Yes | Array of package names (JSON array in POST body) |

### Examples

Compare packages:
```bash
curl -X POST https://api.npms.io/v2/package/mget \\
  -H "Content-Type: application/json" \\
  -d '["react", "vue", "angular"]'
```

## Response Format

The response contains analysis data for each requested package:

```json
{
  "react": { /* NpmsPackage */ },
  "vue": { /* NpmsPackage */ },
  "angular": { /* NpmsPackage */ }
}
```

Packages that don't exist or haven't been analyzed will have `null` values.

## Comparison Metrics

The comparison includes:

**Scores** (0-100)
- Overall, Quality, Popularity, Maintenance

**Package Info**
- Version, Description, Published date

**GitHub Stats**
- Stars, Forks, Open Issues, Contributors

**npm Stats**
- Monthly downloads

**Project Health**
- Contributing guide, License, Security policy

## Caching

Comparison results are cached for 6 hours. Package metrics change slowly, so cached data remains accurate for extended periods.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `npms-analyze` for detailed analysis of a single package
- Use `npms-suggest` to find packages by name pattern
- Use `npm-search` to find packages by keyword

## Error Handling

**Some packages not found**: The comparison will show available data for found packages and note which ones were missing.

**All packages not found**: Verify package names are correct. New packages may take time to be analyzed.

**Rate limiting**: NPMS.io may rate limit excessive requests. Cache results to reduce API calls.

## Interpreting Comparisons

### Overall Score
Choose the package with the highest overall score if all other factors are equal.

### Quality vs Popularity
- **Higher quality**: Better code, documentation, maintenance
- **Higher popularity**: More community adoption, support

### Maintenance Score
Higher scores indicate active development and recent updates.

### Download Counts
Higher downloads indicate wider adoption but not necessarily better quality.

## Use Cases

### Framework Selection
Compare JavaScript frameworks:
```bash
npx tsx scripts/compare.ts react vue angular
```

### Library Alternatives
Compare similar libraries:
```bash
npx tsx scripts/compare.ts axios got node-fetch
```

### State Management
Compare state management solutions:
```bash
npx tsx scripts/compare.ts redux zustand pinia
```

### CSS Solutions
Compare CSS-in-JS libraries:
```bash
npx tsx scripts/compare.ts styled-components emotion linaria
```

## Tips for Comparison

1. **Consider use case**: The best package depends on your specific requirements
2. **Check maintenance**: Prefer packages with higher maintenance scores
3. **Look at ecosystem**: Consider available plugins and community support
4. **Review dependencies**: Check if the package has healthy dependencies
5. **Verify licensing**: Ensure licenses are compatible with your project

## Notes

- NPMS.io provides independent, third-party analysis
- Scores are algorithmically calculated from multiple sources
- Comparison is most useful for packages serving similar purposes
- GitHub and npm data may be incomplete for some packages
- New packages may not have completed initial analysis
