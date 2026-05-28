# npm Publishing Workflow

## Package.json Essentials

```json
{
  "name": "my-library",
  "version": "1.0.0",
  "description": "Short description",
  "keywords": ["keyword1", "keyword2"],
  "author": "Your Name <email@example.com>",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "bugs": {
    "url": "https://github.com/user/repo/issues"
  },
  "homepage": "https://github.com/user/repo#readme",
  "files": ["dist", "README.md", "LICENSE"],
  "engines": {
    "node": ">=18"
  }
}
```

## Files Field

Only these files are published:

```json
{
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ]
}
```

Always included (cannot exclude):
- package.json
- README (any case/extension)
- LICENSE/LICENCE
- CHANGELOG

## Pre-publish Checklist

```bash
# 1. Build
npm run build

# 2. Run tests
npm test

# 3. Check what will be published
npm pack --dry-run

# 4. Verify package structure
npx publint

# 5. Check exports
npx attw --pack

# 6. Test locally
npm pack
cd /tmp && npm init -y && npm i /path/to/my-library-1.0.0.tgz
```

## Publishing Commands

```bash
# Login (first time)
npm login

# Publish public package
npm publish

# Publish scoped package publicly
npm publish --access public

# Publish with tag
npm publish --tag beta

# Dry run (test without publishing)
npm publish --dry-run
```

## Version Management

```bash
# Bump version
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0

# Pre-release versions
npm version prerelease --preid=beta  # 1.0.0 -> 1.0.1-beta.0
npm version prepatch --preid=rc      # 1.0.0 -> 1.0.1-rc.0

# Custom version
npm version 2.0.0-beta.1
```

## Changesets (Recommended)

```bash
# Install
npm i -D @changesets/cli

# Initialize
npx changeset init

# Add changeset (for each PR)
npx changeset

# Version packages
npx changeset version

# Publish
npx changeset publish
```

## Scripts

```json
{
  "scripts": {
    "build": "tsup",
    "test": "vitest run",
    "prepublishOnly": "npm run build && npm test",
    "preversion": "npm test",
    "postversion": "git push && git push --tags"
  }
}
```

## Deprecation

```bash
# Deprecate version
npm deprecate my-library@1.0.0 "Use v2 instead"

# Deprecate version range
npm deprecate my-library@"< 2.0.0" "Upgrade to v2"

# Undeprecate
npm deprecate my-library@1.0.0 ""
```

## Unpublish (Use Carefully!)

```bash
# Unpublish specific version (within 72 hours)
npm unpublish my-library@1.0.0

# Unpublish entire package (within 72 hours, no dependents)
npm unpublish my-library --force
```

## CI/CD Publishing

```yaml
# GitHub Actions
name: Publish
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm test
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Provenance

Enable npm provenance for supply chain security:

```bash
npm publish --provenance
```

Or in package.json:

```json
{
  "publishConfig": {
    "provenance": true
  }
}
```
