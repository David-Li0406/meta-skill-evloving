# Goreleaser Integration with tagpr

When using tagpr with goreleaser for Go projects, configure both tools for immutable releases.

## Why Immutable Releases?

GitHub's immutable releases feature prevents modification of release assets after publication. Without proper configuration:

- tagpr creates a release → becomes immutable immediately
- goreleaser cannot upload binaries to an immutable release

The solution: tagpr creates a **draft** release, goreleaser uploads to the draft, then publishes it.

## Required Configuration

### 1. .tagpr Configuration

```gitconfig
[tagpr]
    releaseBranch = main
    versionFile = version.go
    vPrefix = true
    release = draft
```

The `release = draft` setting is critical - it creates the GitHub Release as a draft.

For `versionFile`, you can use:
- `version.go` - A Go file containing version constant
- `-` - Use git tags only (no version file)

### 2. .goreleaser.yaml Configuration

Add to your `.goreleaser.yaml`:

```yaml
release:
  use_existing_draft: true
```

This tells goreleaser to reuse tagpr's draft release instead of creating a new one.

## Recommended: Separate Workflow Files

For better maintainability, use separate workflow files:

### .github/workflows/tagpr.yml

```yaml
name: tagpr
on:
  push:
    branches:
      - main

jobs:
  tagpr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_PAT }}
      - uses: Songmu/tagpr@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}
```

### .github/workflows/release.yml

```yaml
name: release
on:
  push:
    branches:
      - "!**"
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+"
  workflow_dispatch: ~

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-go@v5
        with:
          cache-dependency-path: '**/go.sum'
          go-version: "stable"

      - uses: goreleaser/goreleaser-action@v6
        with:
          version: latest
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}
```

Key points:
- `branches: "!**"` prevents the workflow from running on branch pushes
- `tags: "v[0-9]+.[0-9]+.[0-9]+"` matches semantic version tags
- `workflow_dispatch` allows manual triggering
- `fetch-depth: 0` is required for goreleaser to access git history

### Flow Explanation

1. **Push to main branch**:
   - tagpr.yml runs
   - Creates/updates release PR
   - When PR is merged, tagpr creates a draft release and pushes a tag

2. **Tag push** (triggered by tagpr):
   - release.yml runs
   - goreleaser builds binaries for multiple platforms
   - Uploads to the existing draft release
   - Publishes the release

## Alternative: Combined Workflow

If you prefer a single file:

```yaml
name: release
on:
  push:
    branches:
      - main
    tags:
      - "v*"

jobs:
  tagpr:
    if: github.ref_type != 'tag'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_PAT }}
      - uses: Songmu/tagpr@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}

  goreleaser:
    if: github.ref_type == 'tag'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod

      - uses: goreleaser/goreleaser-action@v6
        with:
          version: latest
          args: release --clean
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}
```

## Minimal .goreleaser.yaml Example

```yaml
version: 2

builds:
  - env:
      - CGO_ENABLED=0
    main: ./cmd/myapp

release:
  use_existing_draft: true
```

For more complex builds:

```yaml
version: 2

before:
  hooks:
    - go mod tidy

builds:
  - env:
      - CGO_ENABLED=0
    goos:
      - linux
      - darwin
      - windows
    goarch:
      - amd64
      - arm64

archives:
  - format: tar.gz
    format_overrides:
      - goos: windows
        format: zip

checksum:
  name_template: "checksums.txt"

release:
  use_existing_draft: true
```

## Troubleshooting

### goreleaser creates a separate release

**Cause**: Missing `use_existing_draft: true` in `.goreleaser.yaml`

**Solution**: Add the configuration under the `release` section

### goreleaser fails with "release is immutable"

**Cause**: Missing `release = draft` in `.tagpr`

**Solution**: Add `release = draft` to your `.tagpr` configuration

### Workflow doesn't trigger on tag push

**Cause**: Using `GITHUB_TOKEN` instead of `GH_PAT`, or workflow trigger doesn't include tags

**Solution**:
1. Use `GH_PAT` (Personal Access Token) for tagpr
2. Ensure your workflow includes:
```yaml
on:
  push:
    tags:
      - "v*"
```

### Tag is pushed but release workflow doesn't run

**Cause**: `GITHUB_TOKEN` was used in tagpr, which cannot trigger other workflows

**Solution**: Create a Personal Access Token with `repo` and `workflow` permissions, add it as `GH_PAT` secret
