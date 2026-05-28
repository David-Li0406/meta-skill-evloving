# Documentation Review Instructions

Detailed step-by-step instructions for reviewing user documentation quality.

## Implementation Steps

### Step 1: Parse Parameters

```bash
# Parse command line arguments
# Usage: /docs-review <module> [--level=<1|2|3>] [--strict]
```

Parameters:

- `module`: Module name (REQUIRED)
- `--level`: Review specific level only (1=README, 2=repo, 3=site)
- `--strict`: Treat warnings as errors

### Step 2: Load Configuration

```bash
# Read design configuration
cat .claude/design/design.config.json
```

Extract for the specified module:

- Module path and package location
- Design docs path
- User docs configuration (readme, repoDocs, siteDocs)
- Quality standards for each level

### Step 3: Identify Documentation Files

Find all user documentation files to review:

**Level 1 (README):**

```bash
# Find README file
ls -la {module.userDocs.readme}
```

**Level 2 (Repository docs):**

```bash
# Find all repository documentation
find {module.userDocs.repoDocs} -name "*.md" -type f
```

**Level 3 (Site docs):**

```bash
# Find all site documentation
find {module.userDocs.siteDocs} \( -name "*.md" -o -name "*.mdx" \) -type f
```

### Step 4: Check Readability

Analyze text readability for each document:

**Calculate Flesch Reading Ease score:**

- Formula: 206.835 - 1.015 × (words/sentences) - 84.6 × (syllables/words)
- Target score: >60 for Level 1, >50 for Level 2/3
- 90-100: Very easy (5th grade)
- 60-70: Plain English (8th-9th grade)
- 30-50: Difficult (college level)
- 0-30: Very difficult (professional)

**Check sentence length:**

```bash
# Find long sentences (>25 words)
grep -n '[^.!?]\{200,\}[.!?]' {doc-file}
```

**Identify passive voice:**

```bash
# Find passive constructions (rough heuristic)
grep -E 'was|were|been|being' {doc-file} | grep -c 'by'
```

**Detect jargon:**

- Identify technical terms without explanations
- Flag acronyms not defined on first use
- Check for internal terminology (Layer, Effect, Pipe)

### Step 5: Validate Code Examples

For each code block in the documentation:

**Extract code blocks:**

```bash
# Find all code blocks
awk '/```typescript/,/```/' {doc-file}
```

**Check completeness:**

- All imports included
- No undefined variables
- Copy-paste ready

**Validate syntax:**

- Check for TypeScript syntax errors (if possible)
- Verify balanced braces, parentheses
- Check for common typos

**Check comments:**

- Non-obvious code has comments
- Comments explain "why" not "what"
- No commented-out code

### Step 6: Assess Coverage

Compare user docs against design docs to ensure completeness:

**Level 1 (README) coverage:**

- All major features from design docs documented
- Quick start example present
- API overview present
- Installation instructions clear

**Level 2 (Repository docs) coverage:**

- Each design doc topic has corresponding guide
- Architecture documented
- Integration points explained
- Troubleshooting section exists

**Level 3 (Site docs) coverage:**

- Getting started guide present
- Concept docs for all major topics
- How-to guides for common tasks
- API reference linked or included

**Coverage calculation:**

```text
Coverage = (Documented topics / Total topics in design docs) × 100
```

### Step 7: Validate Links

Check all links in documentation:

**Internal links:**

```bash
# Extract internal links
grep -oE '\[.*\]\(\..*\.md\)' {doc-file}

# Verify each link resolves
for link in $links; do
  test -f $(dirname {doc-file})/$link || echo "Broken: $link"
done
```

**External links:**

```bash
# Extract external links
grep -oE '\[.*\]\(https?://.*\)' {doc-file}

# Check each URL (optional, can be slow)
for url in $urls; do
  curl -s -o /dev/null -w "%{http_code}" $url
done
```

**Anchor links:**

```bash
# Extract anchor references
grep -oE '\[.*\]\(#.*\)' {doc-file}

# Verify anchors exist in document
for anchor in $anchors; do
  grep -q "^#.*${anchor#\#}" {doc-file} || echo "Missing: $anchor"
done
```

### Step 8: Check Framework Syntax (Level 3)

For site docs using RSPress, Docusaurus, or VitePress:

**Validate frontmatter:**

```bash
# Extract and validate YAML frontmatter
awk '/^---$/,/^---$/ { if (NR>1) print }' {doc-file} | yq validate
```

**Check MDX syntax:**

```bash
# Look for unclosed JSX tags
grep -E '<[A-Z][^>]*>' {doc-file} | grep -v '/>'
```

**Verify framework components:**

- RSPress: Tabs, Badge, Steps, PackageManagerTabs
- Docusaurus: Admonitions, CodeBlock, Tabs
- VitePress: Custom containers, code groups

**Check for common errors:**

- Mixing markdown and HTML syntax
- Unclosed JSX components
- Invalid frontmatter fields

### Step 9: Calculate Quality Scores

Generate quality scores for each aspect:

**Readability score (0-100):**

- Based on Flesch reading ease
- Penalize long sentences
- Penalize passive voice
- Bonus for code examples

**Completeness score (0-100):**

- Percentage of design doc topics covered
- Presence of required sections
- Code examples for major features

**Accuracy score (0-100):**

- No broken links (100% = perfect)
- Code examples validate
- Framework syntax correct

**Overall quality score:**

```text
Overall = (Readability × 0.3) + (Completeness × 0.4) + (Accuracy × 0.3)
```

### Step 10: Generate Review Report

Create comprehensive quality report:

**Summary section:**

```text
Documentation Review: effect-type-registry

Overall Quality: 85/100 (Good)
- Readability: 78/100
- Completeness: 92/100
- Accuracy: 85/100
```

**Issues by severity:**

- Critical: Broken functionality, missing required sections
- Warning: Suboptimal quality, minor issues
- Info: Suggestions for improvement

**Specific recommendations:**

- Actionable items to improve quality
- Examples of good practices
- Links to relevant documentation

### Step 11: Output Results

Format and display the review report:

**Console output:**

```text
=== Documentation Quality Report ===

Module: effect-type-registry
Files reviewed: 1 (README.md)

Readability
-----------
Flesch score: 68 (Plain English) ✅
Average sentence length: 18 words ✅
Passive voice: 12% (target: <20%) ✅

Completeness
------------
Coverage: 92% (11/12 topics) ⚠️
Missing topics: Advanced configuration
Required sections: ✅ All present

Code Examples
-------------
Total examples: 3
Valid syntax: 3/3 ✅
Copy-paste ready: 3/3 ✅

Links
-----
Internal links: 5 (all valid) ✅
External links: 2 (all valid) ✅
```

**Strict mode:**

If `--strict` flag is provided:

- Treat warnings as errors
- Exit with non-zero code if warnings exist
- Fail CI/CD pipelines on quality issues

## Quality Standards by Level

### Level 1: README

From `.claude/design/design.config.json`:

```json
"userDocs": {
  "level1": {
    "targetWordCount": [200, 500],
    "maxLineLength": 80,
    "requireSections": ["Features", "Installation", "Usage"]
  }
}
```

**Validation checks:**

- Word count: 200-500 (warn if <200 or >800)
- Line length: ≤80 characters
- Required sections present
- At least 1 code example
- Flesch score >60

### Level 2: Repository Docs

```json
"userDocs": {
  "level2": {
    "maxLineLength": 120,
    "requireNavigation": true
  }
}
```

**Validation checks:**

- Each major topic has a guide
- Navigation structure exists
- Cross-references between guides
- Troubleshooting section present
- Flesch score >50

### Level 3: Site Documentation

```json
"userDocs": {
  "level3": {
    "framework": "rspress",
    "requireMetadata": true,
    "requireCodeExamples": true
  }
}
```

**Validation checks:**

- Valid frontmatter metadata
- Framework-specific components used correctly
- Progressive navigation structure
- Interactive elements (tabs, callouts)
- Code examples present
- Mobile responsive

## Readability Analysis Details

### Flesch Reading Ease Formula

```text
Score = 206.835 - 1.015 × (total words / total sentences)
                - 84.6 × (total syllables / total words)
```

**Implementation:**

```bash
# Count words
words=$(wc -w < {doc-file})

# Count sentences (rough heuristic)
sentences=$(grep -o '[.!?]' {doc-file} | wc -l)

# Estimate syllables (rough heuristic)
# Each word averages 1.5 syllables in technical docs
syllables=$((words * 3 / 2))

# Calculate score
score=$(echo "206.835 - 1.015 * ($words / $sentences) - 84.6 * \
  ($syllables / $words)" | bc -l)
```

### Sentence Length Analysis

**Target:** Average 15-20 words per sentence

```bash
# Find sentences longer than 25 words
awk 'BEGIN{RS="[.!?]"} {if(NF>25) print NR": "$0}' {doc-file}
```

### Passive Voice Detection

**Target:** <20% passive voice

```bash
# Simple heuristic: count "was/were/been/being" + "by"
passive=$(grep -E '(was|were|been|being).{1,50}by' {doc-file} | wc -l)
total=$(grep -o '[.!?]' {doc-file} | wc -l)
percentage=$((passive * 100 / total))
```

## Code Example Validation

### Completeness Checklist

For each code example:

- [ ] All imports included
- [ ] No undefined variables
- [ ] Return types clear
- [ ] Error handling shown (if relevant)
- [ ] Comments for non-obvious parts

### Common Issues

**Missing imports:**

```typescript
// Bad: Missing imports
const registry = createRegistry();

// Good: Complete example
import { createRegistry } from 'effect-type-registry';

const registry = createRegistry();
```

**Undefined variables:**

```typescript
// Bad: Where does 'config' come from?
const registry = createRegistry(config);

// Good: Define all variables
const config = { cacheDir: '~/.cache' };
const registry = createRegistry(config);
```

**No error handling:**

```typescript
// Acceptable for quick start
const data = await fetchData();

// Better for guides
try {
  const data = await fetchData();
} catch (error) {
  console.error('Failed to fetch:', error);
}
```

## Link Validation

### Internal Links

```bash
# Example: Validate link in README
# Link: [Architecture](./docs/architecture.md)
# Check: Does ./docs/architecture.md exist relative to README?

doc_dir=$(dirname {readme-path})
target="$doc_dir/docs/architecture.md"
test -f "$target" || echo "Broken link: $target"
```

### External Links

```bash
# Check HTTP status code
status=$(curl -s -o /dev/null -w "%{http_code}" https://example.com)
if [ "$status" != "200" ]; then
  echo "Broken link: https://example.com (status: $status)"
fi
```

### Anchor Links

```bash
# Example: Validate [Quick Start](#quick-start)
# Check: Does heading exist in same file?

grep -q '^## Quick Start' {doc-file} || echo "Missing anchor: #quick-start"
```

## Error Handling

### Missing Documentation

```text
Error: No user documentation found for module 'xyz'

Expected files:
- README.md at pkgs/xyz/README.md
- Repository docs at pkgs/xyz/docs
- Site docs at website/docs/en/packages/xyz

Create documentation before running review.
```

### Invalid Module

```text
Error: Module 'xyz' not found in design.config.json
Available modules: effect-type-registry, rspress-plugin-api-extractor, website
```

### Quality Below Threshold

```text
Error: Documentation quality below acceptable threshold

Overall score: 45/100 (Threshold: 70)

Critical issues:
- Missing required section: Installation
- 3 broken links found
- No code examples

Fix critical issues before proceeding.
```

## Integration Points

- Uses `.claude/design/design.config.json` for configuration
- Reads user docs from `userDocs` paths
- Validates against `quality.userDocs` standards
- May suggest running `/docs-sync` if docs are stale
- May suggest running `/docs-generate-*` to fix issues

## Related Skills

- `/docs-sync` - Sync docs after fixes
- `/docs-generate-readme` - Regenerate README
- `/docs-generate-repo` - Regenerate repo docs
- `/docs-generate-site` - Regenerate site docs
