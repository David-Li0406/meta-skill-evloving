---
name: skill-format-converter
description: Skill for converting between different skill formats. Use when transforming skills from anthropics/skills format to GitHub Copilot format, or vice versa. Handles SKILL.md parsing, validation, and structure transformation.
---

# Skill Format Converter Skill

This skill provides guidance for converting skills between different formats for GitHub Copilot compatibility.

## Format Comparison

### Source: anthropics/skills Format
```
skills/
└── <skill-name>/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

### Target: GitHub Copilot Format
```
.github/skills/
└── <skill-name>/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

## SKILL.md Format

Both formats use the same SKILL.md structure:

```yaml
---
name: skill-name
description: Description of the skill
---

# Skill Title

Instructions and content...
```

### Required Frontmatter

Per VS Code Agent Skills specification:
- `name`: lowercase, hyphens for spaces, max 64 chars
- `description`: what it does and when to use, max 1024 chars

## Conversion Process

### Step 1: Parse Source Skill

```javascript
import { readFile, readdir, stat } from 'fs/promises';
import { join } from 'path';
import { parse as parseYaml } from 'yaml';

async function parseSkill(skillPath) {
  const skillMd = await readFile(join(skillPath, 'SKILL.md'), 'utf-8');
  
  // Extract frontmatter
  const fmMatch = skillMd.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) {
    throw new Error('Invalid SKILL.md: no frontmatter');
  }
  
  const frontmatter = parseYaml(fmMatch[1]);
  const body = skillMd.slice(fmMatch[0].length).trim();
  
  // Scan for resources
  const resources = {
    scripts: await scanDir(join(skillPath, 'scripts')),
    references: await scanDir(join(skillPath, 'references')),
    assets: await scanDir(join(skillPath, 'assets'))
  };
  
  return {
    name: frontmatter.name,
    description: frontmatter.description,
    license: frontmatter.license,
    body,
    resources
  };
}

async function scanDir(dir) {
  try {
    const entries = await readdir(dir, { withFileTypes: true });
    return entries.map(e => ({
      name: e.name,
      isDirectory: e.isDirectory()
    }));
  } catch {
    return [];
  }
}
```

### Step 2: Validate Skill

```javascript
function validateSkill(skill) {
  const errors = [];
  
  // Name validation
  if (!skill.name) {
    errors.push('Missing name');
  } else if (!/^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$/.test(skill.name)) {
    errors.push('Name must be lowercase with hyphens');
  } else if (skill.name.length > 64) {
    errors.push('Name exceeds 64 characters');
  }
  
  // Description validation
  if (!skill.description) {
    errors.push('Missing description');
  } else if (skill.description.length > 1024) {
    errors.push('Description exceeds 1024 characters');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}
```

### Step 3: Convert and Write

```javascript
import { mkdir, copyFile, writeFile } from 'fs/promises';
import { dirname } from 'path';

async function convertSkill(sourcePath, targetBase) {
  const skill = await parseSkill(sourcePath);
  const validation = validateSkill(skill);
  
  if (!validation.valid) {
    throw new Error(`Invalid skill: ${validation.errors.join(', ')}`);
  }
  
  const targetPath = join(targetBase, skill.name);
  
  // Create target directory
  await mkdir(targetPath, { recursive: true });
  
  // Write SKILL.md
  const skillMdContent = generateSkillMd(skill);
  await writeFile(join(targetPath, 'SKILL.md'), skillMdContent);
  
  // Copy resources
  await copyResources(sourcePath, targetPath, 'scripts');
  await copyResources(sourcePath, targetPath, 'references');
  await copyResources(sourcePath, targetPath, 'assets');
  
  return {
    name: skill.name,
    path: targetPath,
    description: skill.description
  };
}

function generateSkillMd(skill) {
  // Per VS Code spec: only name and description in frontmatter
  const frontmatter = ['---'];
  frontmatter.push(`name: ${skill.name}`);
  frontmatter.push(`description: ${skill.description}`);
  frontmatter.push('---');
  
  return frontmatter.join('\n') + '\n\n' + skill.body;
}

async function copyResources(source, target, resourceType) {
  const sourceDir = join(source, resourceType);
  const targetDir = join(target, resourceType);
  
  try {
    const entries = await readdir(sourceDir, { withFileTypes: true });
    await mkdir(targetDir, { recursive: true });
    
    for (const entry of entries) {
      if (entry.isFile()) {
        await copyFile(
          join(sourceDir, entry.name),
          join(targetDir, entry.name)
        );
      }
      // For directories, recursively copy
    }
  } catch {
    // Resource directory doesn't exist, skip
  }
}
```

## Batch Conversion

```javascript
async function convertAllSkills(sourceRepo, targetBase) {
  const skills = await listSkillsInRepo(sourceRepo);
  const results = [];
  
  for (const skill of skills) {
    try {
      const result = await convertSkill(skill.path, targetBase);
      results.push({ success: true, ...result });
    } catch (error) {
      results.push({
        success: false,
        name: skill.name,
        error: error.message
      });
    }
  }
  
  return results;
}
```

## Best Practices

1. **Preserve structure** - Keep resource directories intact
2. **Validate before convert** - Check format compliance
3. **Handle encoding** - Use UTF-8 consistently
4. **Preserve line endings** - Normalize to LF
5. **Log operations** - Track what was converted
