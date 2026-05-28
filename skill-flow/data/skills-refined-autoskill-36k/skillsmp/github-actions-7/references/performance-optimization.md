# Performance Optimization for GitHub Actions

## Overview

Optimize workflow execution time, reduce costs, and improve developer experience with these performance strategies.

## Key Metrics

- **Workflow Duration:** Total execution time
- **Job Duration:** Individual job time
- **Cache Hit Rate:** Percentage of cache hits
- **Parallelization:** Number of concurrent jobs
- **Resource Usage:** Memory and CPU consumption

## Optimization Strategies

### 1. Parallelization

Run independent jobs concurrently:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest

  test:
    runs-on: ubuntu-latest

  build:
    needs: [lint, test]  # Runs after both complete
    runs-on: ubuntu-latest
```

### 2. Matrix Strategy

Run multiple configurations in parallel:

```yaml
strategy:
  fail-fast: false  # Don't cancel all if one fails
  matrix:
    node: [16, 18, 20]
    os: [ubuntu-latest, windows-latest]
    # 6 jobs run in parallel
```

### 3. Dependency Caching

See `caching-strategies.md` for detailed patterns.

### 4. Conditional Execution

Skip unnecessary work:

```yaml
on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'
      - '.github/**'

# Or within jobs
- name: Run expensive tests
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

### 5. Incremental Builds

Build only what changed:

```yaml
- name: Detect changes
  uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      backend:
        - 'backend/**'

- name: Build backend
  if: steps.filter.outputs.backend == 'true'
```

## Advanced Techniques

### Composite Actions

Reduce duplication with composite actions:

```yaml
# .github/actions/setup-node/action.yml
name: 'Setup Node Environment'
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
    - run: npm ci
      shell: bash

# Use in workflow
- uses: ./.github/actions/setup-node
  with:
    node-version: '20'
```

### Reusable Workflows

Share workflows across repositories:

```yaml
# .github/workflows/reusable-ci.yml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
```

### Docker Build Caching

Optimize Docker builds:

```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: |
      type=registry,ref=ghcr.io/myapp:buildcache
      type=gha
    cache-to: |
      type=registry,ref=ghcr.io/myapp:buildcache,mode=max
      type=gha,mode=max
```

### Self-Hosted Runners

For heavy workloads:

```yaml
jobs:
  heavy-computation:
    runs-on: [self-hosted, linux, x64]
    steps:
      - run: ./heavy-task.sh
```

## Cost Optimization

### Reduce Billable Minutes

```yaml
# Use cancellation to save minutes
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# Skip expensive jobs on forks
if: github.event_name == 'push' && github.repository == 'myorg/myrepo'

# Use cache aggressively
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Optimize Self-Hosted Runners

```yaml
# Use smaller runners when possible
runs-on: ubuntu-latest-2-cores  # 2 cores instead of default

# Scale based on workload
runs-on: ${{ matrix.runner }}
matrix:
  runner:
    - ubuntu-latest  # For most jobs
    - ubuntu-latest-16-cores  # For heavy jobs
```

## Monitoring

### Track Workflow Duration

```yaml
- name: Track workflow duration
  run: |
    echo "Workflow started: ${{ github.event.workflow_run.created_at }}"
    echo "Current time: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Cache Statistics

```yaml
- name: Cache hit rate
  run: |
    echo "Cache status: ${{ steps.cache.outputs.cache-hit }}"
```

### Custom Metrics

```yaml
- name: Send metrics
  run: |
    curl -X POST https://metrics.example.com \
      -d "workflow=${{ github.workflow }}" \
      -d "duration=${{ github.event.workflow_run.duration }}"
```

## Benchmarking

### Performance Tests

```yaml
- name: Benchmark
  run: |
    npm run benchmark

- name: Store results
  uses: benchmark-action/github-action-benchmark@v1
  with:
    tool: 'customBench'
    output-file-path: benchmark.json
```

### Regression Detection

```yaml
- name: Check for performance regression
  run: |
    if ! ./scripts/check-performance.sh; then
      echo "::warning::Performance regression detected"
    fi
```

## Troubleshooting

### Slow Workflows

1. **Check job dependencies** - Remove unnecessary `needs` chains
2. **Optimize caching** - Increase cache hit rate
3. **Reduce I/O** - Minimize file operations
4. **Use faster runners** - Consider self-hosted for specific workloads

### High Memory Usage

```yaml
- name: Reduce memory
  run: |
    export NODE_OPTIONS="--max-old-space-size=4096"
    npm run build
```

### Timeout Issues

```yaml
- name: Increase timeout
  uses: docker/build-push-action@v5
  with:
    timeout: 3600000  # 1 hour in milliseconds
```

## Best Practices

1. **Profile before optimizing** - Measure to identify bottlenecks
2. **Optimize hot paths** - Focus on frequently executed workflows
3. **Use concurrency** - Cancel in-progress runs
4. **Cache aggressively** - Cache dependencies and build outputs
5. **Parallelize** - Run independent jobs concurrently
6. **Conditional execution** - Skip unnecessary work
7. **Monitor metrics** - Track duration and cache hit rates

## Examples

See `assets/workflows/advanced/performance-test.yml` for performance testing.
