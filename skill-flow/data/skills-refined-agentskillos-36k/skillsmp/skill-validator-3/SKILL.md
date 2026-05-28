---
name: skill-validator
description: Skill for validating SKILL.md files against the GitHub Copilot Agent Skills specification. Use when checking skill structure, YAML frontmatter, naming conventions, and format compliance.
---

# Skill Validator Skill

This skill provides validation rules and implementation for checking skills against the GitHub Copilot Agent Skills specification.

## Validation Rules

### SKILL.md Requirements

#### File Must Exist
- Path: `<skill-directory>/SKILL.md`
- Encoding: UTF-8

#### YAML Frontmatter

Required format:
```yaml
---
name: skill-name
description: What the skill does and when to use it
---
```

#### Allowed Frontmatter Properties

Per VS Code Agent Skills specification, only these are permitted:
- `name` (required)
- `description` (required)

### Name Validation

Pattern: `^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`

Rules:
- Lowercase letters, digits, and hyphens only
- Cannot start with hyphen
- Cannot end with hyphen
- Maximum 64 characters
- Minimum 1 character

Valid examples:
- `skill-creator`
- `pdf`
- `my-awesome-skill-2`

Invalid examples:
- `Skill-Creator` (uppercase)
- `-skill` (starts with hyphen)
- `skill-` (ends with hyphen)
- `skill_name` (underscore)

### Description Validation

- Must be present
- Must not be empty
- Maximum 1024 characters
- Should describe:
  - What the skill does
  - When to use it

## Implementation

### Node.js Validator

```javascript
import { readFile } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { parse as parseYaml } from 'yaml';

const NAME_PATTERN = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?$/;
// Per VS Code Agent Skills spec: only name and description are documented
const ALLOWED_PROPERTIES = new Set([
  'name',
  'description',
]);

export async function validateSkill(skillPath) {
  const errors = [];
  const warnings = [];
  
  // Check SKILL.md exists
  const skillMdPath = join(skillPath, 'SKILL.md');
  if (!existsSync(skillMdPath)) {
    return {
      valid: false,
      errors: ['SKILL.md not found'],
      warnings: []
    };
  }
  
  // Read content
  const content = await readFile(skillMdPath, 'utf-8');
  
  // Check frontmatter exists
  if (!content.startsWith('---')) {
    errors.push('No YAML frontmatter found');
    return { valid: false, errors, warnings };
  }
  
  // Extract frontmatter
  const endIndex = content.indexOf('---', 3);
  if (endIndex === -1) {
    errors.push('Invalid frontmatter format - missing closing ---');
    return { valid: false, errors, warnings };
  }
  
  const frontmatterText = content.slice(4, endIndex).trim();
  
  // Parse YAML
  let frontmatter;
  try {
    frontmatter = parseYaml(frontmatterText);
    if (typeof frontmatter !== 'object' || frontmatter === null) {
      errors.push('Frontmatter must be a YAML object');
      return { valid: false, errors, warnings };
    }
  } catch (e) {
    errors.push(`Invalid YAML: ${e.message}`);
    return { valid: false, errors, warnings };
  }
  
  // Check for unexpected properties
  for (const key of Object.keys(frontmatter)) {
    if (!ALLOWED_PROPERTIES.has(key)) {
      errors.push(`Unexpected property: ${key}`);
    }
  }
  
  // Validate name
  if (!frontmatter.name) {
    errors.push('Missing required field: name');
  } else if (typeof frontmatter.name !== 'string') {
    errors.push('Name must be a string');
  } else {
    const name = frontmatter.name.trim();
    if (!NAME_PATTERN.test(name)) {
      errors.push('Name must be lowercase with hyphens only');
    }
    if (name.length > 64) {
      errors.push('Name exceeds 64 characters');
    }
  }
  
  // Validate description
  if (!frontmatter.description) {
    errors.push('Missing required field: description');
  } else if (typeof frontmatter.description !== 'string') {
    errors.push('Description must be a string');
  } else {
    const desc = frontmatter.description.trim();
    if (desc.length === 0) {
      errors.push('Description cannot be empty');
    }
    if (desc.length > 1024) {
      errors.push('Description exceeds 1024 characters');
    }
    if (desc.length < 20) {
      warnings.push('Description is very short');
    }
  }
  
  // Check body content
  const body = content.slice(endIndex + 3).trim();
  if (body.length === 0) {
    warnings.push('SKILL.md body is empty');
  }
  
  return {
    valid: errors.length === 0,
    errors,
    warnings
  };
}
```

### Batch Validation

```javascript
import { readdir } from 'fs/promises';

export async function validateAllSkills(skillsDir) {
  const results = [];
  const entries = await readdir(skillsDir, { withFileTypes: true });
  
  for (const entry of entries) {
    if (entry.isDirectory() && !entry.name.startsWith('.')) {
      const skillPath = join(skillsDir, entry.name);
      const result = await validateSkill(skillPath);
      results.push({
        name: entry.name,
        path: skillPath,
        ...result
      });
    }
  }
  
  return results;
}
```

## CLI Output Format

```
Skill Validation Report
═══════════════════════════════════════════════════════════

✅ skill-creator
   Path: .github/skills/skill-creator
   
❌ broken-skill  
   Errors:
   - Missing required field: description
   - Name contains uppercase letters
   
⚠️  short-desc-skill
   Warnings:
   - Description is very short

═══════════════════════════════════════════════════════════
Summary: 10 valid, 1 invalid, 1 with warnings
```

## Exit Codes

- 0: All skills valid
- 1: One or more skills invalid
- 2: Error during validation
