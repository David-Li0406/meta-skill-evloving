# Audit Report Parsing Guide

## axe-results.json

```typescript
interface AxeResults {
  violations: AxeViolation[];
  passes: AxePass[];
  incomplete: AxeIncomplete[];
  inapplicable: any[];
}

interface AxeViolation {
  id: string;           // e.g., "color-contrast"
  impact: "critical" | "serious" | "moderate" | "minor";
  description: string;
  help: string;
  helpUrl: string;
  tags: string[];       // WCAG criteria like "wcag2aa", "wcag143"
  nodes: AxeNode[];
}

interface AxeNode {
  target: string[];     // CSS selectors
  html: string;         // HTML snippet
  failureSummary: string;
}
```

**Extraction:**
```typescript
const axeData = JSON.parse(fs.readFileSync('docs/audits/raw/axe-results.json', 'utf-8'));

for (const violation of axeData.violations) {
  const issue = {
    id: violation.id,
    priority: impactToPriority(violation.impact),
    description: violation.description,
    help: violation.help,
    wcag: extractWcagCriteria(violation.tags),
    selectors: violation.nodes.map(n => n.target.join(' ')),
    source: 'axe',
  };
}

function impactToPriority(impact: string): number {
  return { critical: 1, serious: 2, moderate: 3, minor: 4 }[impact] ?? 4;
}

function extractWcagCriteria(tags: string[]): string[] {
  return tags
    .filter(t => t.startsWith('wcag'))
    .map(t => t.replace('wcag', '').replace(/(\d)(\d)(\d)/, '$1.$2.$3'));
}
```

## pa11y-results.json

Pa11y outputs an array of issues:

```typescript
interface Pa11yIssue {
  code: string;         // e.g., "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail"
  type: "error" | "warning" | "notice";
  typeCode: number;
  message: string;
  context: string;      // HTML snippet
  selector: string;     // CSS selector
  runner: string;
  runnerExtras: any;
}
```

**Extraction:**
```typescript
const pa11yData = JSON.parse(fs.readFileSync('docs/audits/raw/pa11y-results.json', 'utf-8'));

// Pa11y returns array directly
const issues = Array.isArray(pa11yData) ? pa11yData : pa11yData.issues ?? [];

for (const issue of issues) {
  const parsed = {
    id: extractPa11yId(issue.code),
    priority: typeToPriority(issue.type),
    description: issue.message,
    wcag: extractWcagFromCode(issue.code),
    selectors: [issue.selector],
    context: issue.context,
    source: 'pa11y',
  };
}

function typeToPriority(type: string): number {
  return { error: 2, warning: 3, notice: 4 }[type] ?? 4;
}

function extractPa11yId(code: string): string {
  // "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail" -> "color-contrast"
  const mapping: Record<string, string> = {
    '1_4_3': 'color-contrast',
    '1_1_1': 'image-alt',
    '2_4_4': 'link-name',
    '4_1_2': 'aria-valid',
  };
  const match = code.match(/(\d+_\d+_\d+)/);
  return match ? mapping[match[1]] ?? code : code;
}

function extractWcagFromCode(code: string): string[] {
  const match = code.match(/(\d+)_(\d+)_(\d+)/);
  return match ? [`${match[1]}.${match[2]}.${match[3]}`] : [];
}
```

## lighthouse-results.json

```typescript
interface LighthouseResults {
  categories: {
    accessibility?: LighthouseCategory;
    seo?: LighthouseCategory;
    performance?: LighthouseCategory;
    'best-practices'?: LighthouseCategory;
  };
  audits: Record<string, LighthouseAudit>;
}

interface LighthouseCategory {
  id: string;
  title: string;
  score: number;        // 0-1
  auditRefs: { id: string; weight: number }[];
}

interface LighthouseAudit {
  id: string;
  title: string;
  description: string;
  score: number | null;
  scoreDisplayMode: string;
  details?: {
    type: string;
    items?: any[];
    headings?: any[];
  };
}
```

**Extraction:**
```typescript
const lhData = JSON.parse(fs.readFileSync('docs/audits/raw/lighthouse-results.json', 'utf-8'));

// Focus on accessibility and SEO categories
const categories = ['accessibility', 'seo'];

for (const catId of categories) {
  const category = lhData.categories[catId];
  if (!category) continue;

  for (const auditRef of category.auditRefs) {
    const audit = lhData.audits[auditRef.id];
    if (!audit || audit.score === null || audit.score === 1) continue;

    const issue = {
      id: audit.id,
      priority: scoreToPriority(audit.score),
      description: audit.title,
      help: audit.description,
      details: audit.details?.items ?? [],
      category: catId,
      source: 'lighthouse',
    };
  }
}

function scoreToPriority(score: number): number {
  if (score === 0) return 1;
  if (score < 0.5) return 2;
  if (score < 0.9) return 3;
  return 4;
}
```

## Deduplication Strategy

Issues from different tools often overlap. Deduplicate by:

1. **Normalize selectors:**
   ```typescript
   function normalizeSelector(selector: string): string {
     return selector
       .toLowerCase()
       .replace(/\s+/g, ' ')
       .trim();
   }
   ```

2. **Map to canonical issue types:**
   ```typescript
   const ISSUE_TYPES = {
     'color-contrast': ['color-contrast', '1_4_3', 'contrast'],
     'image-alt': ['image-alt', '1_1_1', 'alt-text'],
     'link-name': ['link-name', '2_4_4', 'link-text'],
     // ... etc
   };
   ```

3. **Group by (issue_type, normalized_selector):**
   - Keep the report with most detail (longest description, most context)
   - Merge all source tools into `source_tools` array
   - Combine all affected elements

4. **Priority:**
   - Use the highest priority (lowest number) from any source
