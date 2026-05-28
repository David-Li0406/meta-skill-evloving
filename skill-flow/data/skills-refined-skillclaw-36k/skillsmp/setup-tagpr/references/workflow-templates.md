# GitHub Actions Workflow Templates for tagpr

## Important: Token Configuration

All workflows use `GH_PAT` (Personal Access Token) instead of `GITHUB_TOKEN`. This is required because:
- `GITHUB_TOKEN` cannot trigger other workflows when pushing tags
- tagpr needs to push tags that trigger release workflows

For `actions/checkout`, pass the token to enable tag pushing:
```yaml
- uses: actions/checkout@v4
  with:
    token: ${{ secrets.GH_PAT }}
```

## Basic tagpr Workflow

For projects that only need tagpr (no separate release workflow):

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

## tagpr with Asset Upload (TypeScript/Node.js)

For projects that build and upload release assets within the same workflow:

```yaml
name: tagpr
on:
  push:
    branches:
      - main

jobs:
  tagpr:
    runs-on: ubuntu-latest
    outputs:
      tag: ${{ steps.tagpr.outputs.tag }}
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GH_PAT }}

      - name: Run tagpr
        id: tagpr
        uses: Songmu/tagpr@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}

      - name: Setup Node.js
        if: steps.tagpr.outputs.tag != ''
        uses: actions/setup-node@v4
        with:
          node-version: "22"

      - name: Install dependencies
        if: steps.tagpr.outputs.tag != ''
        run: npm ci

      - name: Build
        if: steps.tagpr.outputs.tag != ''
        run: npm run build

      - name: Upload release assets
        if: steps.tagpr.outputs.tag != ''
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}
        run: |
          gh release upload ${{ steps.tagpr.outputs.tag }} \
            dist/* \
            --clobber

      - name: Publish release
        if: steps.tagpr.outputs.tag != ''
        env:
          GITHUB_TOKEN: ${{ secrets.GH_PAT }}
        run: |
          gh release edit ${{ steps.tagpr.outputs.tag }} --draft=false
```

### tagpr Outputs

| Output | Description |
|--------|-------------|
| `tag` | The created tag (empty if no tag was created) |
| `pull_request` | JSON-formatted PR information |

## Separate Workflows: tagpr + Release

For projects where tagpr and release are in separate workflow files (recommended for Go + goreleaser):

### tagpr.yml

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

### release.yml (triggered by tag)

```yaml
name: release
on:
  push:
    branches:
      - "!**"
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+"

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      # Add your release steps here
```

The `branches: "!**"` prevents the workflow from running on branch pushes.

## Combined Workflow: tagpr + goreleaser

For Go projects using both tagpr and goreleaser in a single file:

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

## GitHub Enterprise

For GitHub Enterprise instances, use `GH_ENTERPRISE_TOKEN`:

```yaml
- uses: Songmu/tagpr@v1
  env:
    GH_ENTERPRISE_TOKEN: ${{ secrets.GH_ENTERPRISE_TOKEN }}
```

## Custom Release Branch

For repositories with different default branches:

```yaml
name: tagpr
on:
  push:
    branches:
      - develop  # Change to your release branch

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

Remember to also set `releaseBranch = develop` in your `.tagpr` file.

## Workflow with npm Publishing

For Node.js projects that publish to npm:

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

  publish:
    if: github.ref_type == 'tag'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          registry-url: "https://registry.npmjs.org"

      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```
