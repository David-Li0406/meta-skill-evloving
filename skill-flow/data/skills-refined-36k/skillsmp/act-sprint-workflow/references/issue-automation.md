# Issue Automation Reference

## Type Detection

```typescript
const typeKeywords = {
  Enhancement: ['add', 'create', 'build', 'implement', 'update', 'improve'],
  Bug: ['fix', 'resolve', 'correct', 'broken', 'error', 'crash'],
  Task: ['document', 'research', 'investigate', 'write', 'setup']
};

function detectType(title: string): string {
  const lower = title.toLowerCase();
  for (const [type, keywords] of Object.entries(typeKeywords)) {
    if (keywords.some(k => lower.includes(k))) return type;
  }
  return 'Task'; // default
}
```

## Priority Detection

```typescript
const priorityKeywords = {
  Critical: ['critical', 'urgent', 'security', 'broken', 'down'],
  High: ['important', 'should', 'high', 'asap'],
  Low: ['nice to have', 'eventually', 'low', 'someday']
};

function detectPriority(title: string): string {
  const lower = title.toLowerCase();
  for (const [priority, keywords] of Object.entries(priorityKeywords)) {
    if (keywords.some(k => lower.includes(k))) return priority;
  }
  return 'Medium'; // default
}
```

## Effort Estimation

```typescript
function estimateEffort(title: string): string {
  const lower = title.toLowerCase();

  if (['simple', 'quick', 'small', 'typo'].some(k => lower.includes(k))) return 'S';
  if (['complex', 'major', 'refactor', 'rewrite'].some(k => lower.includes(k))) return 'L';
  if (['complete overhaul', 'full migration', 'architecture'].some(k => lower.includes(k))) return 'XL';

  return 'M'; // default
}
```

## ACT Project Detection

```typescript
function detectProject(title: string, currentDir: string): string {
  const keywords = {
    'Empathy Ledger': ['empathy', 'ledger', 'storyteller', 'story'],
    'JusticeHub': ['justice', 'contained', 'service'],
    'The Harvest': ['harvest', 'volunteer', 'community'],
    'ACT Farm': ['farm', 'residency', 'conservation'],
    'Goods': ['goods', 'asset', 'inventory'],
    'ACT Studio': ['studio', 'dashboard', 'infrastructure']
  };

  // First check title
  for (const [project, kws] of Object.entries(keywords)) {
    if (kws.some(k => title.toLowerCase().includes(k))) return project;
  }

  // Fall back to current directory
  if (currentDir.includes('empathy')) return 'Empathy Ledger';
  if (currentDir.includes('justice')) return 'JusticeHub';
  // ... etc

  return 'ACT Studio'; // default
}
```

## Issue Creation Flow

1. Detect type from title
2. Detect priority from title
3. Estimate effort from title
4. Detect project from title/directory
5. Create issue via `gh issue create`
6. Add to GitHub Project via GraphQL
7. Set field values (Sprint, Priority, etc.)
8. Webhook syncs to Notion automatically
