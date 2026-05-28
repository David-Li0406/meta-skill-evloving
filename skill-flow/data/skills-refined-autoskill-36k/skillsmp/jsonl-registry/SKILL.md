---
name: jsonl-registry
description: Skill for working with JSONL (JSON Lines) format registries. Use when creating, querying, updating, or managing data stored in JSONL format for skill registries, logs, or datasets.
---

# JSONL Registry Skill

This skill provides guidance for working with JSONL (JSON Lines) format for managing skill registries.

## JSONL Format Specification

JSONL (JSON Lines) is a convenient format for storing structured data:
- Each line is a valid JSON object
- Lines are separated by newline characters (`\n`)
- Files typically use `.jsonl` extension
- Easy to append, stream, and process line-by-line

### Example Registry Entry
```json
{"name": "skill-creator", "description": "Guide for creating skills", "source": "anthropics/skills", "path": ".github/skills/skill-creator", "installed_at": "2026-01-20T10:30:00Z", "tags": ["meta"]}
```

## Registry Schema

### Required Fields
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier, lowercase with hyphens |
| `description` | string | What the skill does |
| `path` | string | Local path to skill directory |
| `installed_at` | string | ISO 8601 timestamp |

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Source repository (owner/repo) |
| `version` | string | Semantic version |
| `tags` | array | Category tags for filtering |
| `author` | string | Skill author |
| `license` | string | License type |
| `checksum` | string | SHA256 hash of SKILL.md |

## Node.js Implementation

### Registry Class

```javascript
import { readFile, writeFile, appendFile } from 'fs/promises';
import { existsSync } from 'fs';

export class Registry {
  constructor(path = '.github/skills/registry.jsonl') {
    this.path = path;
  }

  async getAll() {
    if (!existsSync(this.path)) {
      return [];
    }
    const content = await readFile(this.path, 'utf-8');
    return content
      .split('\n')
      .filter(line => line.trim())
      .map(line => JSON.parse(line));
  }

  async add(skill) {
    const entry = {
      name: skill.name,
      description: skill.description,
      path: skill.path,
      source: skill.source,
      installed_at: new Date().toISOString(),
      tags: skill.tags || [],
    };
    await appendFile(this.path, JSON.stringify(entry) + '\n');
    return entry;
  }

  async remove(name) {
    const entries = await this.getAll();
    const filtered = entries.filter(e => e.name !== name);
    await writeFile(
      this.path,
      filtered.map(e => JSON.stringify(e)).join('\n') + '\n'
    );
  }

  async find(name) {
    const entries = await this.getAll();
    return entries.find(e => e.name === name);
  }

  async search(query) {
    const entries = await this.getAll();
    const q = query.toLowerCase();
    return entries.filter(e => 
      e.name.includes(q) || 
      e.description.toLowerCase().includes(q) ||
      e.tags?.some(t => t.includes(q))
    );
  }

  async rebuild(skillsDir = '.github/skills') {
    // Scan for SKILL.md files and rebuild registry
    const skills = [];
    // Implementation: scan directories, parse SKILL.md, collect metadata
    return skills;
  }
}
```

### Streaming Large Registries

For large registries, use streaming:

```javascript
import { createReadStream } from 'fs';
import { createInterface } from 'readline';

async function* streamRegistry(path) {
  const rl = createInterface({
    input: createReadStream(path),
    crlfDelay: Infinity
  });
  
  for await (const line of rl) {
    if (line.trim()) {
      yield JSON.parse(line);
    }
  }
}

// Usage
for await (const skill of streamRegistry('registry.jsonl')) {
  console.log(skill.name);
}
```

## Query Patterns

### Filter by Tags
```javascript
const devSkills = entries.filter(e => 
  e.tags?.includes('development')
);
```

### Filter by Source
```javascript
const anthropicSkills = entries.filter(e => 
  e.source === 'anthropics/skills'
);
```

### Filter by Date Range
```javascript
const recentSkills = entries.filter(e => {
  const date = new Date(e.installed_at);
  const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
  return date.getTime() > thirtyDaysAgo;
});
```

## Validation

Always validate entries before writing:

```javascript
function validateEntry(entry) {
  if (!entry.name || typeof entry.name !== 'string') {
    throw new Error('Invalid name');
  }
  if (!/^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$/.test(entry.name)) {
    throw new Error('Name must be lowercase with hyphens');
  }
  if (!entry.description || entry.description.length > 1024) {
    throw new Error('Description required, max 1024 chars');
  }
  if (!entry.path || typeof entry.path !== 'string') {
    throw new Error('Path required');
  }
  return true;
}
```

## Best Practices

1. **Atomic writes** - Write to temp file, then rename
2. **Validate before write** - Check JSON and schema
3. **Backup before modify** - Copy before destructive ops
4. **Lock for concurrency** - Use file locks if needed
5. **Consistent ordering** - Sort entries for diffability
