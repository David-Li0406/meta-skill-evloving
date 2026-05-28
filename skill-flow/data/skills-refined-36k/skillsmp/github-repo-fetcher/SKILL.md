---
name: github-repo-fetcher
description: Skill for fetching and parsing content from GitHub repositories. Use when cloning repos, fetching raw files, parsing repository structure, and working with GitHub's API or raw content URLs.
---

# GitHub Repository Fetcher Skill

This skill provides guidance for fetching and parsing content from GitHub repositories.

## Fetching Strategies

### Strategy 1: Git Clone (Recommended for Full Repos)
```bash
# Shallow clone for efficiency
git clone --depth 1 https://github.com/<owner>/<repo>.git /tmp/<repo>

# Clone specific branch
git clone --depth 1 --branch <branch> https://github.com/<owner>/<repo>.git /tmp/<repo>
```

### Strategy 2: Raw Content URL (For Single Files)
```
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
```

Example:
```
https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md
```

### Strategy 3: GitHub API (For Metadata)
```
https://api.github.com/repos/<owner>/<repo>/contents/<path>
```

## Node.js Implementation

### Repository Fetcher Class

```javascript
import { execSync } from 'child_process';
import { existsSync, rmSync } from 'fs';
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

export class RepoFetcher {
  constructor(tempDir = '/tmp/skills-source') {
    this.tempDir = tempDir;
  }

  async clone(repo, branch = 'main') {
    if (existsSync(this.tempDir)) {
      rmSync(this.tempDir, { recursive: true });
    }
    
    const url = `https://github.com/${repo}.git`;
    execSync(`git clone --depth 1 --branch ${branch} ${url} ${this.tempDir}`, {
      stdio: 'pipe'
    });
    
    return this.tempDir;
  }

  async listSkills(skillsDir = 'skills') {
    const dir = join(this.tempDir, skillsDir);
    const entries = await readdir(dir, { withFileTypes: true });
    
    const skills = [];
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const skillMd = join(dir, entry.name, 'SKILL.md');
        if (existsSync(skillMd)) {
          const content = await readFile(skillMd, 'utf-8');
          const metadata = this.parseSkillMd(content);
          skills.push({
            name: metadata.name || entry.name,
            description: metadata.description,
            path: join(skillsDir, entry.name)
          });
        }
      }
    }
    
    return skills;
  }

  parseSkillMd(content) {
    if (!content.startsWith('---')) {
      return {};
    }
    
    const endIndex = content.indexOf('---', 3);
    if (endIndex === -1) {
      return {};
    }
    
    const frontmatter = content.slice(4, endIndex).trim();
    const result = {};
    
    for (const line of frontmatter.split('\n')) {
      const colonIndex = line.indexOf(':');
      if (colonIndex > 0) {
        const key = line.slice(0, colonIndex).trim();
        const value = line.slice(colonIndex + 1).trim();
        result[key] = value;
      }
    }
    
    return result;
  }

  cleanup() {
    if (existsSync(this.tempDir)) {
      rmSync(this.tempDir, { recursive: true });
    }
  }
}
```

### Fetch Raw File

```javascript
async function fetchRawFile(repo, branch, path) {
  const url = `https://raw.githubusercontent.com/${repo}/${branch}/${path}`;
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch ${path}: ${response.status}`);
  }
  
  return response.text();
}

// Usage
const skillMd = await fetchRawFile(
  'anthropics/skills',
  'main',
  'skills/skill-creator/SKILL.md'
);
```

### GitHub API for Directory Listing

```javascript
async function listDirectory(repo, path = '') {
  const url = `https://api.github.com/repos/${repo}/contents/${path}`;
  const response = await fetch(url, {
    headers: {
      'Accept': 'application/vnd.github.v3+json',
      // 'Authorization': `token ${process.env.GITHUB_TOKEN}` // Optional
    }
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}

// Usage
const contents = await listDirectory('anthropics/skills', 'skills');
const skillDirs = contents.filter(item => item.type === 'dir');
```

## Rate Limiting

GitHub API has rate limits:
- Unauthenticated: 60 requests/hour
- Authenticated: 5000 requests/hour

Use authentication for production:
```javascript
const headers = {
  'Accept': 'application/vnd.github.v3+json',
  'Authorization': `token ${process.env.GITHUB_TOKEN}`
};
```

## Error Handling

```javascript
async function safeClone(repo) {
  try {
    const fetcher = new RepoFetcher();
    return await fetcher.clone(repo);
  } catch (error) {
    if (error.message.includes('not found')) {
      throw new Error(`Repository ${repo} not found`);
    }
    if (error.message.includes('Authentication')) {
      throw new Error('Private repository requires authentication');
    }
    throw error;
  }
}
```

## Best Practices

1. **Use shallow clones** - `--depth 1` saves bandwidth
2. **Clean up temp files** - Remove cloned repos after use
3. **Handle rate limits** - Cache responses, use tokens
4. **Validate repo format** - Check `owner/repo` format
5. **Timeout long operations** - Set reasonable timeouts
