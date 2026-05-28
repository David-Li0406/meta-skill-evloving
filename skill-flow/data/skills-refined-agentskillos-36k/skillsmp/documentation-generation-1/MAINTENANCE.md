# Documentation Maintenance

Strategies for keeping documentation up to date, validation, and automation.

## Documentation Debt

Documentation becomes stale when:
- Code changes without doc updates
- Examples stop working
- Links break
- Dependencies change

### Signs of Documentation Debt

| Sign | Action |
|------|--------|
| Users asking obvious questions | Add to FAQ or improve README |
| Example code throws errors | Update examples |
| Links return 404 | Fix or remove links |
| Screenshots don't match UI | Update screenshots |
| API docs don't match signatures | Regenerate from code |

## Keeping Docs in Sync with Code

### Strategy 1: Documentation Tests

Test that documentation examples actually work.

#### TypeScript/JavaScript

```typescript
// tests/docs.test.ts
import { describe, test, expect } from 'bun:test';

describe('README examples', () => {
  test('quick start example works', async () => {
    // Copy the exact code from README
    const { createClient } = await import('../src');

    const client = createClient({ apiKey: 'test-key' });
    expect(client).toBeDefined();
  });

  test('configuration example works', async () => {
    const { createClient } = await import('../src');

    const client = createClient({
      apiKey: 'test-key',
      timeout: 5000,
      retries: 3,
    });

    expect(client.config.timeout).toBe(5000);
  });
});
```

#### Python

```python
# tests/test_docs.py
import doctest
import mymodule

def test_docstrings():
    """Run doctests for all module docstrings."""
    results = doctest.testmod(mymodule)
    assert results.failed == 0, f"{results.failed} doctest(s) failed"


def test_readme_examples():
    """Test examples from README."""
    # Copy exact code from README
    from mymodule import create_client

    client = create_client(api_key="test-key")
    assert client is not None
```

### Strategy 2: Extract Examples from Docs

```typescript
// scripts/extract-examples.ts
import { readFile } from 'fs/promises';
import { glob } from 'glob';

interface CodeBlock {
  language: string;
  code: string;
  file: string;
  line: number;
}

async function extractCodeBlocks(mdFile: string): Promise<CodeBlock[]> {
  const content = await readFile(mdFile, 'utf-8');
  const blocks: CodeBlock[] = [];
  const regex = /```(\w+)\n([\s\S]*?)```/g;

  let match;
  let line = 1;

  while ((match = regex.exec(content)) !== null) {
    blocks.push({
      language: match[1],
      code: match[2].trim(),
      file: mdFile,
      line: content.slice(0, match.index).split('\n').length,
    });
  }

  return blocks;
}

async function main() {
  const mdFiles = await glob('**/*.md', { ignore: 'node_modules/**' });

  for (const file of mdFiles) {
    const blocks = await extractCodeBlocks(file);
    console.log(`${file}: ${blocks.length} code blocks`);
  }
}

main();
```

### Strategy 3: Co-locate Docs with Code

Keep documentation close to the code it documents:

```
src/
├── users/
│   ├── index.ts          # Implementation
│   ├── index.test.ts     # Tests
│   ├── README.md         # Module docs
│   └── examples/         # Working examples
│       └── basic.ts
```

## Validation Tools

### Markdown Linting

```bash
# Install markdownlint
npm install -g markdownlint-cli

# Lint all markdown files
markdownlint '**/*.md' --ignore node_modules

# Fix automatically
markdownlint '**/*.md' --fix
```

Create `.markdownlint.json`:

```json
{
  "default": true,
  "MD013": false,
  "MD033": false,
  "MD041": false
}
```

### Link Checking

```bash
# Install markdown-link-check
npm install -g markdown-link-check

# Check links in a file
markdown-link-check README.md

# Check all markdown files
find . -name '*.md' -not -path './node_modules/*' | xargs -n1 markdown-link-check
```

### Spell Checking

```bash
# Install cspell
npm install -g cspell

# Check spelling
cspell '**/*.md'
```

Create `cspell.json`:

```json
{
  "version": "0.2",
  "language": "en",
  "words": [
    "tsconfig",
    "jsdoc",
    "openapi",
    "docstrings"
  ],
  "ignorePaths": [
    "node_modules/**"
  ]
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    paths:
      - '**/*.md'
      - 'docs/**'
  pull_request:
    paths:
      - '**/*.md'
      - 'docs/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint Markdown
        uses: DavidAnson/markdownlint-cli2-action@v14
        with:
          globs: '**/*.md'

      - name: Check Links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: yes
          config-file: '.markdown-link-check.json'

      - name: Check Spelling
        uses: streetsidesoftware/cspell-action@v5
        with:
          files: '**/*.md'

  test-examples:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install Dependencies
        run: bun install

      - name: Test Documentation Examples
        run: bun test tests/docs.test.ts
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.37.0
    hooks:
      - id: markdownlint
        args: ['--fix']

  - repo: https://github.com/tcort/markdown-link-check
    rev: v3.11.2
    hooks:
      - id: markdown-link-check

  - repo: https://github.com/streetsidesoftware/cspell-cli
    rev: v8.1.0
    hooks:
      - id: cspell
```

## PR Documentation Checklist

Add to `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Documentation

Please check all that apply:

- [ ] README updated (if public API changed)
- [ ] JSDoc/docstrings added for new functions
- [ ] CHANGELOG updated
- [ ] Examples updated and tested
- [ ] Migration guide updated (if breaking change)
- [ ] API documentation regenerated (if applicable)
```

## Automated Documentation Generation

### TypeDoc for TypeScript

```bash
# Install
bun add -d typedoc typedoc-plugin-markdown

# Generate HTML docs
bunx typedoc src/index.ts --out docs/api

# Generate Markdown docs (for GitHub wiki)
bunx typedoc src/index.ts --out docs/api --plugin typedoc-plugin-markdown
```

`typedoc.json`:

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "readme": "none",
  "excludePrivate": true,
  "excludeProtected": true,
  "includeVersion": true,
  "categorizeByGroup": true
}
```

### API Reference from OpenAPI

```bash
# Install redoc-cli
npm install -g redoc-cli

# Generate HTML docs
redoc-cli build openapi.yaml -o docs/api.html

# Serve for development
redoc-cli serve openapi.yaml
```

### Changelog Generation

```bash
# Install conventional-changelog
npm install -g conventional-changelog-cli

# Generate changelog from commits
conventional-changelog -p angular -i CHANGELOG.md -s
```

## Documentation Review Process

### Checklist for Reviewers

When reviewing documentation changes:

- [ ] **Accuracy**: Does the content match the code?
- [ ] **Completeness**: Are all parameters documented?
- [ ] **Examples**: Do examples work as written?
- [ ] **Clarity**: Is the language clear and concise?
- [ ] **Consistency**: Does it follow the project's style?
- [ ] **Links**: Do all links work?
- [ ] **Versioning**: Is version information correct?

### Common Review Comments

| Issue | Comment |
|-------|---------|
| Missing example | "Please add an example showing usage" |
| Outdated example | "This example uses the old API - please update" |
| Missing parameter docs | "Please document the `options` parameter" |
| Unclear description | "Could you clarify what happens when X?" |
| Missing error docs | "What errors can this throw?" |

## Version Documentation

### Documenting Breaking Changes

```markdown
## Migration Guide: v1.x to v2.x

### Breaking Changes

#### `createUser()` signature changed

**Before (v1.x):**
\`\`\`typescript
createUser(email: string, name: string): User
\`\`\`

**After (v2.x):**
\`\`\`typescript
createUser(input: CreateUserInput): User
\`\`\`

**Migration:**
\`\`\`typescript
// Before
const user = createUser('user@example.com', 'John');

// After
const user = createUser({
  email: 'user@example.com',
  name: 'John',
});
\`\`\`

#### `timeout` default changed

The default timeout changed from 30s to 10s. If you rely on the 30s timeout, explicitly set it:

\`\`\`typescript
const client = createClient({
  timeout: 30000, // Restore old default
});
\`\`\`
```

### Deprecation Notices

```typescript
/**
 * Creates a user.
 *
 * @deprecated Use {@link createUserV2} instead. Will be removed in v3.0.
 *
 * @example Migration:
 * ```typescript
 * // Old
 * createUser(email, name);
 *
 * // New
 * createUserV2({ email, name });
 * ```
 */
function createUser(email: string, name: string): User {
  console.warn('createUser is deprecated. Use createUserV2 instead.');
  return createUserV2({ email, name });
}
```

## Workflow: Monthly Documentation Audit

### Steps

1. **Check for stale content**
   - [ ] Review last modified dates
   - [ ] Compare docs to current code
   - [ ] Test all code examples

2. **Run validation tools**
   - [ ] Markdown lint
   - [ ] Link check
   - [ ] Spell check

3. **Review analytics** (if available)
   - [ ] Most visited pages
   - [ ] Search queries with no results
   - [ ] Pages with high bounce rates

4. **Update content**
   - [ ] Fix broken links
   - [ ] Update outdated examples
   - [ ] Add missing documentation

5. **Archive deprecated content**
   - [ ] Move old version docs to archive
   - [ ] Update navigation

## Metrics to Track

| Metric | Tool | Target |
|--------|------|--------|
| Docs coverage | Custom script | 100% of public APIs |
| Link validity | markdown-link-check | 0 broken links |
| Example test pass rate | Test suite | 100% |
| Time to first contribution | GitHub | Decreasing |
| Support questions | Issue tracker | Decreasing |

## Best Practices Summary

### Do

- Test documentation examples in CI
- Use linting tools
- Review docs in PRs
- Keep docs close to code
- Track documentation metrics
- Schedule regular audits

### Don't

- Skip docs in code reviews
- Let examples get out of date
- Ignore broken links
- Forget to update CHANGELOG
- Document and forget
