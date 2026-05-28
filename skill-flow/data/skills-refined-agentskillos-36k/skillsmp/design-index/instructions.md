# Design Index Detailed Instructions

Complete step-by-step workflow for generating design documentation indexes.

## Detailed Workflow

### 1. Parse Parameters

Extract parameters from the user's request.

**Required:**

- `module`: Module name to index (or "all" for all modules)

**Optional:**

- `format`: Output format (default: markdown)
  - `markdown` - Markdown index
  - `html` - HTML navigation
  - `json` - Structured JSON
- `organize-by`: Organization method (default: category)
  - `category` - Group by category
  - `status` - Group by status
  - `alphabetical` - Alphabetical order
  - `date` - By creation/update date
- `output`: Output file path (default: stdout or INDEX.md)
- `include-sections`: Include document sections (default: false)
- `depth`: Heading depth to include (default: 2)

**Parameter parsing examples:**

- "Generate index for effect-type-registry"
  - module: `effect-type-registry`, format: `markdown`, organize-by: `category`

- "Create HTML navigation for all design docs"
  - module: `all`, format: `html`, organize-by: `status`

- "Index rspress-plugin-api-extractor by date"
  - module: `rspress-plugin-api-extractor`, organize-by: `date`

### 2. Load Configuration

Read `.claude/design/design.config.json` to:

- Get module paths
- Get design docs locations
- Understand module structure

**Configuration structure:**

```json
{
  "modules": {
    "module-name": {
      "path": ".claude/design/module-name",
      "description": "..."
    }
  }
}
```

### 3. Scan Documentation Files

Use Glob to find all design docs:

**Single module:**

```bash
glob "*.md" --path=".claude/design/{module}"
```

**All modules:**

```bash
for module in ${modules[@]}; do
  glob "*.md" --path=".claude/design/${module}"
done
```

**For each file:**

- Read frontmatter
- Extract metadata
- Parse headings (up to specified depth)
- Calculate statistics (lines, words, sections, code blocks)

### 4. Extract Document Metadata

For each design document, extract comprehensive metadata.

#### Parse Frontmatter

Extract fields from YAML frontmatter:

```yaml
status: current
module: effect-type-registry
category: architecture
created: 2026-01-15
updated: 2026-01-17
completeness: 85
```

**Frontmatter parsing algorithm:**

1. Read first 30 lines of document
2. Find YAML between `---` markers
3. Parse YAML structure
4. Extract standard fields
5. Validate field values

#### Extract Headings

Parse markdown headings up to specified depth:

**Heading extraction:**

```bash
# Extract headings (H1-H3)
grep -E '^#{1,3} ' file.md
```

**Parsing algorithm:**

1. Read entire document
2. Find lines starting with `#`
3. Count `#` characters to determine level
4. Extract heading text
5. Build hierarchical structure

**Heading structure example:**

```text
# Main Document Title (H1)
## Overview (H2)
## Current State (H2)
### Implementation Details (H3)
### Performance (H3)
## Rationale (H2)
```

#### Calculate Statistics

For each document, calculate:

**Line count:**

```bash
wc -l file.md
```

**Word count:**

```bash
wc -w file.md  # Approximate
```

**Number of sections:**

Count H2 headings (major sections).

**Number of code blocks:**

```bash
grep -c '^```' file.md | awk '{print $1/2}'  # Divide by 2 (open+close)
```

**Last updated:**

Extract from frontmatter `updated` field.

### 5. Organize Documents

Group documents based on `organize-by` parameter.

#### By Category

Group by document category field.

**Algorithm:**

```javascript
const byCategory = {}

for (doc of documents) {
  const category = doc.frontmatter.category || 'uncategorized'
  if (!byCategory[category]) {
    byCategory[category] = []
  }
  byCategory[category].push(doc)
}

// Sort categories alphabetically
// Sort docs within category by title
```

**Output structure:**

```text
Architecture:
  - observability.md
  - system-design.md

Performance:
  - cache-optimization.md
  - benchmarking.md

Observability:
  - logging.md
  - metrics.md
```

#### By Status

Group by document status field.

**Status order:**

1. Current (production-ready)
2. Draft (work in progress)
3. Needs Review
4. Stub (planned)
5. Archived (outdated)

**Algorithm:**

```javascript
const byStatus = {
  current: [],
  draft: [],
  'needs-review': [],
  stub: [],
  archived: []
}

for (doc of documents) {
  const status = doc.frontmatter.status || 'draft'
  byStatus[status].push(doc)
}
```

#### Alphabetical

Sort alphabetically by filename or title.

**Algorithm:**

```javascript
const sorted = documents.sort((a, b) => {
  return a.title.localeCompare(b.title)
})

// Group into letter ranges for large sets
const byLetter = {}
for (doc of sorted) {
  const firstLetter = doc.title[0].toUpperCase()
  const range = getLetterRange(firstLetter)  // A-C, D-F, etc.
  if (!byLetter[range]) {
    byLetter[range] = []
  }
  byLetter[range].push(doc)
}
```

#### By Date

Sort by creation or update date.

**Time buckets:**

- Recently Updated (Last 7 days)
- This Month
- This Quarter
- Older

**Algorithm:**

```javascript
const now = new Date()
const byDate = {
  recent: [],      // Last 7 days
  thisMonth: [],
  thisQuarter: [],
  older: []
}

for (doc of documents) {
  const updated = new Date(doc.frontmatter.updated)
  const daysSince = (now - updated) / (1000 * 60 * 60 * 24)

  if (daysSince <= 7) {
    byDate.recent.push(doc)
  } else if (daysSince <= 30) {
    byDate.thisMonth.push(doc)
  } else if (daysSince <= 90) {
    byDate.thisQuarter.push(doc)
  } else {
    byDate.older.push(doc)
  }
}

// Sort within each bucket by date (newest first)
```

### 6. Generate Index

Create index in specified format.

#### Format: Markdown

See [templates.md](templates.md) for full markdown templates (minimal, standard,
detailed).

**Generation algorithm:**

```javascript
function generateMarkdownIndex(documents, organization) {
  let md = []

  // Header
  md.push(`# Design Documentation Index - ${module}`)
  md.push('')
  md.push(`**Module:** ${module}`)
  md.push(`**Last Updated:** ${new Date().toISOString().split('T')[0]}`)
  md.push(`**Total Documents:** ${documents.length}`)
  md.push(`**Organization:** By ${organization}`)
  md.push('')
  md.push('---')
  md.push('')

  // Groups
  for (group in organizedDocs) {
    md.push(`## ${group}`)
    md.push('')

    for (doc of organizedDocs[group]) {
      md.push(`### [${doc.title}](${doc.relativePath})`)
      md.push('')
      md.push(
        `**Status:** ${doc.status} | ` +
        `**Completeness:** ${doc.completeness}% | ` +
        `**Updated:** ${doc.updated}`
      )
      md.push('')

      if (doc.summary) {
        md.push(doc.summary)
        md.push('')
      }

      if (includeSections && doc.sections) {
        md.push('**Sections:**')
        for (section of doc.sections) {
          md.push(`- ${section}`)
        }
        md.push('')
      }

      md.push('---')
      md.push('')
    }
  }

  // Statistics
  md.push('## Document Statistics')
  md.push('')
  md.push(generateStatistics(documents))

  // Footer
  md.push(`**Generated:** ${new Date().toISOString()} by design-index skill`)

  return md.join('\n')
}
```

#### Format: HTML

Generate HTML navigation structure with embedded CSS.

See [templates.md](templates.md) for full HTML template.

**Generation algorithm:**

```javascript
function generateHTMLIndex(documents, organization) {
  return `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Design Documentation Index - ${module}</title>
    <style>${getCSS()}</style>
</head>
<body>
    ${generateHTMLHeader(module, documents)}
    ${generateHTMLCategories(organizedDocs)}
    ${generateHTMLStatistics(documents)}
    ${generateHTMLFooter()}
</body>
</html>
  `
}
```

#### Format: JSON

Generate structured JSON index.

**JSON schema:**

```json
{
  "module": "string",
  "generated": "ISO8601 date",
  "organization": "category|status|alphabetical|date",
  "statistics": {
    "total": 0,
    "by_status": {},
    "average_completeness": 0
  },
  "categories": {
    "category-name": [
      {
        "title": "string",
        "file": "string",
        "path": "string",
        "status": "string",
        "category": "string",
        "completeness": 0,
        "created": "ISO8601 date",
        "updated": "ISO8601 date",
        "summary": "string",
        "sections": [],
        "statistics": {
          "lines": 0,
          "words": 0,
          "sections": 0,
          "code_blocks": 0
        }
      }
    ]
  }
}
```

### 7. Generate Summary Statistics

Include overall statistics in index.

**Statistics to calculate:**

#### Status Distribution

```javascript
const statusCounts = {
  current: 0,
  draft: 0,
  stub: 0,
  archived: 0
}

for (doc of documents) {
  statusCounts[doc.status]++
}

const statusPercentages = {}
for (status in statusCounts) {
  statusPercentages[status] = (statusCounts[status] / documents.length) * 100
}
```

#### Completeness Metrics

```javascript
const completenessScores = documents.map(d => d.completeness)

const metrics = {
  average: sum(completenessScores) / completenessScores.length,
  highest: Math.max(...completenessScores),
  lowest: Math.min(...completenessScores),
  needsAttention: documents.filter(d => d.completeness < 50).length
}
```

#### Recent Activity

```javascript
const now = new Date()

const activity = {
  updatedToday: documents.filter(d => daysSince(d.updated) === 0).length,
  updatedThisWeek: documents.filter(d => daysSince(d.updated) <= 7).length,
  stale: documents.filter(d => daysSince(d.updated) > 30).length
}
```

#### Coverage by Category

```javascript
const coverageByCategory = {}

for (doc of documents) {
  const category = doc.category || 'uncategorized'
  if (!coverageByCategory[category]) {
    coverageByCategory[category] = 0
  }
  coverageByCategory[category]++
}
```

### 8. Output Index

Write index to file or stdout.

**To file:**

```bash
echo "$index_content" > .claude/design/{module}/INDEX.md
```

**To custom path:**

```bash
echo "$index_content" > "$output_path"
```

**To stdout:**

Display in terminal for immediate viewing.

**Output decision tree:**

1. If `output` parameter specified → write to that path
2. If module-specific index → write to `.claude/design/{module}/INDEX.md`
3. If all-modules index → write to `.claude/design/INDEX.md`
4. If no output preference → print to stdout

### 9. Report Results

Generate summary of what was done.

**Report format:**

```markdown
# Index Generated

**Module:** {module}
**Format:** {format}
**Organization:** By {organization}
**Output:** {output_path}

## Index Details

- **Documents indexed:** {count}
- **Categories/Groups:** {group_count}
- **Total sections:** {section_count}
- **Index size:** {file_size} KB

## Index Structure

{visual tree of index}

## Next Steps

1. Review generated index
2. Link from README or main documentation
3. Regenerate when docs change
```

## Organization Method Details

### Organization by Category

**Best for:**

- Technical organization
- Finding docs by domain
- Standard documentation structure

**Example groupings:**

```text
Architecture
Performance
Observability
Testing
Deployment
Security
```

### Organization by Status

**Best for:**

- Project management
- Tracking completion
- Identifying work needed

**Status order:**

1. Current (production-ready)
2. Draft (in progress)
3. Needs Review
4. Stub (planned)
5. Archived (outdated)

### Organization Alphabetically

**Best for:**

- Quick lookup
- Large documentation sets
- Reference-style docs

**Letter ranges:**

- A-D
- E-L
- M-R
- S-Z

### Organization by Date

**Best for:**

- Recent changes tracking
- Documentation maintenance
- Version history

**Time buckets:**

- This Week (Last 7 days)
- This Month (Last 30 days)
- This Quarter (Last 90 days)
- Older (>90 days)

## Advanced Features

### Cross-Module Indexes

Generate index spanning multiple modules:

```javascript
function generateAllModulesIndex() {
  const allDocs = []

  for (module of modules) {
    const moduleDocs = scanModule(module)
    allDocs.push(...moduleDocs)
  }

  // Organize by module first, then by category
  return generateIndex(allDocs, 'module-category')
}
```

### Filtered Indexes

Generate index with filters:

```javascript
function generateFilteredIndex(filter) {
  const filtered = documents.filter(doc => {
    if (filter.status) return doc.status === filter.status
    if (filter.category) return doc.category === filter.category
    if (filter.minCompleteness) return doc.completeness >= filter.minCompleteness
    return true
  })

  return generateIndex(filtered, organization)
}
```

### Auto-Regeneration

Monitor docs and auto-regenerate:

```bash
# Watch for changes
inotifywait -m .claude/design/ -e modify,create,delete |
while read path action file; do
  /design-index ${module}
done
```
