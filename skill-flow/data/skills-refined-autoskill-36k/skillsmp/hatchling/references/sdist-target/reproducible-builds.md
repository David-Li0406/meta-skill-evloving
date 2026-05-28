---
name: sdist-reproducible-builds
description: Complete guide to creating byte-for-byte identical source distributions using SOURCE_DATE_EPOCH, including verification methods, CI/CD integration, and security benefits
---

# Reproducible Builds for Sdist

Configure reproducible builds to create byte-for-byte identical distributions when built from the same source code. This capability is essential for security auditing, compliance verification, and maintaining software supply chain integrity.

## What Are Reproducible Builds?

A reproducible build produces identical output binaries/archives when:

- Built at different times
- Built on different machines
- Built by different users
- Built in different directories
- Built in different environments (within reason)

For source distributions, reproducibility ensures identical `.tar.gz` archives with:

- Same file content
- Same file metadata
- Same compression
- Same archive structure
- Same timestamps

## Why Reproducible Builds Matter

### Security

**Verify Authenticity:** Users can rebuild the sdist and compare checksums:

```bash
# Official distribution
sha256sum official-package-1.0.0.tar.gz
# abc123...

# User rebuilds from source
hatch build -t sdist
sha256sum dist/package-1.0.0.tar.gz
# abc123... (matches!)

# Checksums match = No tampering detected
```

### Compliance

- **License Verification:** Auditors can verify included files
- **Dependency Tracking:** Build reproducibility aids in tracking dependencies
- **Regulatory Requirements:** Some regulations require build reproducibility

### Trust

- **Supply Chain Security:** Reduces risk of backdoors or modifications
- **Community Verification:** Multiple people can verify the same hash
- **Transparency:** Builds are verifiable without special tools

## Hatchling's Reproducible Builds

Hatchling creates reproducible sdists by default when `SOURCE_DATE_EPOCH` is set.

### How It Works

Hatchling normalizes time-dependent values:

1. **File Modification Times:** Set to `SOURCE_DATE_EPOCH`
2. **Archive Timestamps:** Normalized in tar header
3. **Metadata:** All time-dependent fields normalized
4. **Compression:** Deterministic (gzip with no metadata)

Result: Identical archive bytes across builds.

## Enabling Reproducible Builds

### Using SOURCE_DATE_EPOCH

Set the environment variable before building:

```bash
# Method 1: Use current time
export SOURCE_DATE_EPOCH=$(date +%s)
hatch build -t sdist

# Method 2: Use specific timestamp
export SOURCE_DATE_EPOCH=1234567890
hatch build -t sdist

# Method 3: Use Git commit timestamp (for releases)
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
hatch build -t sdist
```

### What SOURCE_DATE_EPOCH Does

The value is:

- **Seconds since Unix epoch** (January 1, 1970)
- **Integer value** (no fractional seconds)
- **Applied to all file timestamps** in the sdist

Example values:

```bash
# Current time
date +%s
# 1730000000

# Specific date
date -d "2024-10-01" +%s
# 1727740800

# Git commit
git log -1 --format=%ct
# 1729531234
```

## Reproducible Build in CI/CD

### GitHub Actions Example

```yaml
name: Build and Release

on:
  push:
    tags:
      - "v*"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0 # Need full history for git log

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install Hatch
        run: pip install hatch

      - name: Build distributions (reproducibly)
        run: |
          export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
          hatch build
        env:
          SOURCE_DATE_EPOCH: ${{ env.SOURCE_DATE_EPOCH }}

      - name: Calculate checksums
        run: |
          cd dist
          sha256sum * > SHA256SUMS
          cat SHA256SUMS

      - name: Upload to PyPI
        run: |
          pip install twine
          twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

### GitLab CI Example

```yaml
build:
  stage: build
  script:
    - export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
    - hatch build
    - sha256sum dist/* > dist/SHA256SUMS
  artifacts:
    paths:
      - dist/
```

## Verifying Reproducibility

### Generate Two Builds

```bash
# Build 1
export SOURCE_DATE_EPOCH=1234567890
hatch build -t sdist
cp dist/my-package-1.0.0.tar.gz dist/my-package-1.0.0.tar.gz.1
rm dist/my-package-1.0.0.tar.gz

# Build 2 (same SOURCE_DATE_EPOCH)
export SOURCE_DATE_EPOCH=1234567890
hatch build -t sdist
cp dist/my-package-1.0.0.tar.gz dist/my-package-1.0.0.tar.gz.2
```

### Compare Checksums

```bash
# SHA256
sha256sum dist/my-package-1.0.0.tar.gz.1 dist/my-package-1.0.0.tar.gz.2

# Should show identical checksums
# abc123... dist/my-package-1.0.0.tar.gz.1
# abc123... dist/my-package-1.0.0.tar.gz.2

# Binary comparison
cmp dist/my-package-1.0.0.tar.gz.1 dist/my-package-1.0.0.tar.gz.2
echo $?
# 0 = files are identical
```

### Detailed Comparison

```bash
# Extract both and compare
mkdir -p build1 build2
tar -xzf dist/my-package-1.0.0.tar.gz.1 -C build1
tar -xzf dist/my-package-1.0.0.tar.gz.2 -C build2

# Recursive comparison
diff -r build1 build2
# No output = directories are identical
```

## Configuration

### Default Reproducibility

Hatchling builds reproducibly by default when `SOURCE_DATE_EPOCH` is set:

```toml
# No configuration needed
[tool.hatch.build.targets.sdist]
# Reproducibility enabled automatically
```

### Disabling Reproducibility

To disable reproducible builds (not recommended):

```toml
[tool.hatch.build]
reproducible = false
```

When disabled:

- Current system time is used for file timestamps
- Each build has different timestamps
- Archives will have different checksums even with same content

### When to Disable Reproducibility

Disable only when:

- Testing features that require current timestamps
- Debugging timestamp-related issues
- Special development scenarios

Never disable for releases or CI/CD builds.

## What Gets Normalized

### Normalized in Sdist

With `SOURCE_DATE_EPOCH` set, these are normalized:

```text
File timestamps:       Set to SOURCE_DATE_EPOCH
Directory timestamps:  Set to SOURCE_DATE_EPOCH
Tar header times:      Set to SOURCE_DATE_EPOCH
File permissions:      Preserved as-is (not normalized)
File ownership:        Not stored in tar (uses numeric UID/GID)
Compression metadata:  Deterministic gzip
```

### Not Normalized (and why)

```text
Source code content:   No changes (as expected)
File permissions:      Preserved for correctness (executable bits matter)
File ordering:         Sorted consistently
Directory structure:   Preserved exactly
```

## Troubleshooting Reproducibility

### Builds Not Matching

If two builds don't match despite same `SOURCE_DATE_EPOCH`:

1. **Check SOURCE_DATE_EPOCH is set:**

   ```bash
   echo $SOURCE_DATE_EPOCH
   # Should print a number
   ```

2. **Verify Hatchling version:**

   ```bash
   pip show hatchling | grep Version
   # Should be >= 1.0
   ```

3. **Check source hasn't changed:**

   ```bash
   git status
   # Should be clean (no uncommitted changes)
   ```

4. **Check environment:**

   ```bash
   # Same OS/Python/Hatchling version
   python --version
   hatch --version
   uname -a
   ```

5. **Check for non-deterministic files:**
   ```bash
   # Files that might have timestamp metadata
   find . -name "*.pyc" -o -name "*.so"
   # These shouldn't be in source repository
   ```

### Different Checksums with Same SOURCE_DATE_EPOCH

Possible causes:

1. **Source files changed:** Check git status
2. **Different Python version:** Bytecode differs
3. **Different Hatchling version:** Build process may differ
4. **Local modifications:** Uncomitted changes in files
5. **Dependencies differ:** If build has dynamic dependencies

Resolution:

```bash
# Clean slate
git clean -fdx
rm -rf dist build

# Fresh build
export SOURCE_DATE_EPOCH=1234567890
hatch build -t sdist
```

### Verification Script

Create a reproducibility test script:

```bash
#!/bin/bash
# test_reproducibility.sh

set -e

REPO_DIR=$(git rev-parse --show-toplevel)
cd "$REPO_DIR"

# Use git commit timestamp
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
export SOURCE_DATE_EPOCH

echo "Testing reproducibility with SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH"

# Clean
rm -rf dist build dist_1 dist_2

# Build 1
hatch build -t sdist
mkdir -p dist_1
mv dist/my-package-*.tar.gz dist_1/

# Build 2
hatch build -t sdist
mkdir -p dist_2
mv dist/my-package-*.tar.gz dist_2/

# Compare
SHA1=$(sha256sum dist_1/* | awk '{print $1}')
SHA2=$(sha256sum dist_2/* | awk '{print $1}')

echo "Build 1: $SHA1"
echo "Build 2: $SHA2"

if [ "$SHA1" = "$SHA2" ]; then
    echo "SUCCESS: Builds are reproducible!"
    exit 0
else
    echo "FAILURE: Builds differ!"
    exit 1
fi
```

Run the test:

```bash
chmod +x test_reproducibility.sh
./test_reproducibility.sh
```

## Best Practices

### For Releases

```bash
# Use commit timestamp for the release tag
git tag v1.0.0
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)

# Build
hatch build

# Publish checksums
sha256sum dist/* | tee dist/SHA256SUMS

# Sign checksums (optional but recommended)
gpg --armor --detach-sign dist/SHA256SUMS
```

### For CI/CD

```bash
# Always set SOURCE_DATE_EPOCH in CI
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
hatch build

# Save checksums as artifact
sha256sum dist/* > checksums.txt
```

### For Users

```bash
# Verify downloaded distribution
sha256sum -c SHA256SUMS
# If all match: "OK" output for each file

# Verify against known checksums
echo "expected_hash  dist/my-package-1.0.0.tar.gz" | sha256sum -c
```

## See Also

- [Reproducible Builds Project](https://reproducible-builds.org/)
- [PEP 517 - Build System Interface](https://www.python.org/dev/peps/pep-0517/)
- [SOURCE_DATE_EPOCH Specification](https://reproducible-builds.org/docs/source-date-epoch/)
- [Tar Format Specification](https://www.gnu.org/software/tar/manual/tar.html#SEC39)
