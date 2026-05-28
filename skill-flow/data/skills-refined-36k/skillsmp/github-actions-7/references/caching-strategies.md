# Caching Strategies for GitHub Actions

## Overview

Effective caching is critical for reducing GitHub Actions workflow execution time and cost. This reference covers advanced caching strategies for common scenarios.

## Dependency Caching

### npm/pnpm/yarn

```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### Python pip

```yaml
- name: Cache pip packages
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Go modules

```yaml
- name: Cache Go modules
  uses: actions/cache@v4
  with:
    path: |
      ~/.cache/go-build
      ~/go/pkg/mod
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
    restore-keys: |
      ${{ runner.os }}-go-
```

## Build Output Caching

### Next.js

```yaml
- name: Cache Next.js build
  uses: actions/cache@v4
  with:
    path: |
      .next/cache
    key: ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-nextjs-${{ hashFiles('**/package-lock.json') }}-
      ${{ runner.os }}-nextjs-
```

### Docker Layer Caching

```yaml
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: false
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Advanced Patterns

### Multi-level Caching

```yaml
- name: Cache dependencies
  uses: actions/cache@v4
  id: cache-deps
  with:
    path: node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}

- name: Install dependencies
  if: steps.cache-deps.outputs.cache-hit != 'true'
  run: npm ci
```

### Cache Save on Success

```yaml
- name: Build
  id: build
  run: npm run build

- name: Save build cache
  if: success()
  uses: actions/cache/save@v4
  with:
    path: dist
    key: ${{ runner.os }}-build-${{ github.sha }}
```

## Monorepo Caching

```yaml
- name: Cache Turborepo
  uses: actions/cache@v4
  with:
    path: |
      .turbo
      node_modules/.cache
    key: ${{ runner.os }}-turbo-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-turbo-
```

## Best Practices

1. **Use specific cache keys** - Include file hashes for precision
2. **Provide restore keys** - Allow partial cache hits
3. **Cache frequently changing items separately** - Dependencies vs build outputs
4. **Set appropriate retention** - Use GitHub's default 7 days or custom
5. **Monitor cache hit rates** - Check Actions logs for effectiveness

## Troubleshooting

### Low cache hit rate

```yaml
# Bad: Too specific
key: ${{ runner.os }}-node-${{ github.sha }}

# Good: Balance specificity and reusability
key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-node-
```

### Cache size too large

```yaml
# Split caches by type
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: node_modules
    key: deps-${{ hashFiles('**/package-lock.json') }}

- name: Cache build output
  uses: actions/cache@v4
  with:
    path: dist
    key: build-${{ github.sha }}
```

## Examples

See `assets/workflows/advanced/cache-optimization.yml` for a complete example.
