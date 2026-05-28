# VS Code Extension Publishing

## Prerequisites

1. Azure DevOps account
2. Personal Access Token (PAT) with Marketplace scope
3. Publisher ID on VS Code Marketplace

## Setup

```bash
# Install vsce
npm install -g @vscode/vsce

# Create publisher (first time)
vsce create-publisher <publisher-name>

# Login
vsce login <publisher-name>
```

## Package.json Requirements

```json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "description": "Description for marketplace",
  "version": "1.0.0",
  "publisher": "your-publisher-id",
  "engines": {
    "vscode": "^1.80.0"
  },
  "categories": ["Programming Languages"],
  "keywords": ["keyword1", "keyword2"],
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo"
  },
  "icon": "images/icon.png",
  "galleryBanner": {
    "color": "#1e1e1e",
    "theme": "dark"
  }
}
```

## Categories

- `Programming Languages`
- `Snippets`
- `Linters`
- `Themes`
- `Debuggers`
- `Formatters`
- `Language Packs`
- `Other`

## Publishing Commands

```bash
# Package extension
vsce package

# Publish to marketplace
vsce publish

# Publish with version bump
vsce publish minor  # 1.0.0 -> 1.1.0
vsce publish patch  # 1.0.0 -> 1.0.1
vsce publish major  # 1.0.0 -> 2.0.0

# Publish specific version
vsce publish 1.2.3

# Unpublish (use carefully!)
vsce unpublish <publisher>.<extension>
```

## .vscodeignore

Exclude files from package:

```
.vscode/**
.vscode-test/**
src/**
**/*.ts
**/tsconfig.json
**/test/**
.gitignore
.eslintrc*
```

## README.md for Marketplace

The README becomes the extension's marketplace page:

```markdown
# Extension Name

Short description.

## Features

- Feature 1
- Feature 2

## Requirements

- Dependency 1

## Extension Settings

- `extension.setting1`: Description

## Known Issues

- Issue 1

## Release Notes

### 1.0.0

Initial release
```

## Pre-release Versions

```bash
vsce publish --pre-release
```

## CI/CD Publishing

```yaml
# GitHub Actions example
- name: Publish Extension
  run: |
    npm install -g @vscode/vsce
    vsce publish -p ${{ secrets.VSCE_PAT }}
```

## Verification Checklist

1. `vsce ls` - List files to be packaged
2. `vsce package` - Create .vsix and inspect
3. Install .vsix locally to test
4. Check README renders correctly
5. Verify icon displays properly
