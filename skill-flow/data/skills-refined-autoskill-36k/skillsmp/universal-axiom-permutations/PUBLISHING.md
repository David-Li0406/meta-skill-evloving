# Publishing Guide for The Universal Axiom

This guide covers publishing The Universal Axiom to NPM, PyPI, and Crates.io.

## Table of Contents

- [NPM Publishing (@universal-axiom/core)](#npm-publishing)
- [PyPI Publishing (universal-axiom)](#pypi-publishing)
- [Crates.io Publishing (universal-axiom)](#cratesio-publishing)
- [Pre-Publishing Checklist](#pre-publishing-checklist)
- [Version Management](#version-management)

---

## NPM Publishing (@universal-axiom/core)

### Prerequisites

1. **NPM Account**: Create an account at [npmjs.com](https://www.npmjs.com/)
2. **Login to NPM**:
   ```bash
   npm login
   ```
3. **Verify Authentication**:
   ```bash
   npm whoami
   ```

### Publishing Steps

1. **Ensure all tests pass**:
   ```bash
   npm test
   npm run type-check
   npm run lint
   ```

2. **Build TypeScript**:
   ```bash
   npm run build
   ```

3. **Verify package contents**:
   ```bash
   npm pack --dry-run
   ```

   This shows what files will be included in the package.

4. **Publish to NPM**:
   ```bash
   # For first-time publishing
   npm publish --access public

   # For subsequent updates
   npm publish
   ```

5. **Verify publication**:
   ```bash
   npm view @universal-axiom/core
   ```

### Installing Published Package

Users can install with:
```bash
npm install @universal-axiom/core
```

### Usage Example

```javascript
import { UniversalAxiom } from '@universal-axiom/core';

const axiom = new UniversalAxiom({
  impulses: [1.0, 0.8],
  elements: [0.9, 0.7],
  pressure: 1.2
});

const intelligence = axiom.computeIntelligence({
  n: 5,
  subjectivity: 6,
  why: 0.9,
  time: 1.0
});

console.log(`Intelligence: ${intelligence}`);
```

---

## PyPI Publishing (universal-axiom)

### Prerequisites

1. **PyPI Account**: Create accounts at:
   - [PyPI](https://pypi.org/account/register/) (production)
   - [TestPyPI](https://test.pypi.org/account/register/) (testing)

2. **Install Build Tools**:
   ```bash
   pip install --upgrade pip build twine
   ```

3. **Create API Token**:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Create API token with "Entire account" scope
   - Save token securely (starts with `pypi-`)

4. **Configure PyPI Credentials**:
   Create `~/.pypirc`:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE

   [testpypi]
   username = __token__
   password = pypi-YOUR_TESTPYPI_TOKEN_HERE
   ```

### Publishing Steps

1. **Run Tests**:
   ```bash
   python -m pytest tests/
   python verify_outputs.py --language python
   ```

2. **Clean Previous Builds**:
   ```bash
   rm -rf build/ dist/ *.egg-info
   ```

3. **Build Distribution**:
   ```bash
   python -m build
   ```

   This creates both wheel (`.whl`) and source distribution (`.tar.gz`) in `dist/`.

4. **Check Distribution**:
   ```bash
   twine check dist/*
   ```

5. **Test on TestPyPI** (recommended first time):
   ```bash
   twine upload --repository testpypi dist/*
   ```

   Verify at: https://test.pypi.org/project/universal-axiom/

6. **Publish to PyPI**:
   ```bash
   twine upload dist/*
   ```

7. **Verify Publication**:
   ```bash
   pip index versions universal-axiom
   ```

### Installing Published Package

Users can install with:
```bash
pip install universal-axiom
```

### Usage Example

```python
from universal_axiom import UniversalAxiom

axiom = UniversalAxiom(
    impulses=[1.0, 0.8],
    elements=[0.9, 0.7],
    pressure=1.2
)

intelligence = axiom.compute_intelligence(
    n=5,
    subjectivity=6,
    why=0.9,
    time=1.0
)

print(f"Intelligence: {intelligence}")
```

---

## Crates.io Publishing (universal-axiom)

### Prerequisites

1. **Crates.io Account**:
   - Login at [crates.io](https://crates.io/) using GitHub

2. **Get API Token**:
   - Go to [Account Settings](https://crates.io/settings/tokens)
   - Create new token
   - Save token securely

3. **Login to Cargo**:
   ```bash
   cargo login YOUR_TOKEN_HERE
   ```

   Token is stored in `~/.cargo/credentials.toml`

### Publishing Steps

1. **Run Tests**:
   ```bash
   cd src/rust
   cargo test
   cargo clippy -- -D warnings
   cargo fmt -- --check
   ```

2. **Verify Package**:
   ```bash
   cargo package --list
   ```

   This shows all files that will be included.

3. **Dry Run**:
   ```bash
   cargo publish --dry-run
   ```

   This verifies the package can be published without actually publishing.

4. **Publish to Crates.io**:
   ```bash
   cargo publish
   ```

5. **Verify Publication**:
   - Check [crates.io/crates/universal-axiom](https://crates.io/crates/universal-axiom)
   - Or run: `cargo search universal-axiom`

### Installing Published Package

Users add to `Cargo.toml`:
```toml
[dependencies]
universal-axiom = "0.1.0"
```

Then:
```bash
cargo build
```

### Usage Example

```rust
use universal_axiom::UniversalAxiom;

fn main() {
    let axiom = UniversalAxiom::new(
        vec![1.0, 0.8],
        vec![0.9, 0.7],
        1.2,
    );

    let intelligence = axiom.compute_intelligence(5, 6, 0.9, 1.0);
    println!("Intelligence: {}", intelligence);
}
```

---

## Pre-Publishing Checklist

Before publishing to any registry, ensure:

### Code Quality
- [ ] All tests pass (`make test`)
- [ ] Cross-language verification passes (`python verify_outputs.py`)
- [ ] No linter warnings (`make lint`)
- [ ] Type checking passes (`npm run type-check` for TypeScript)
- [ ] Code formatted (`make format`)

### Documentation
- [ ] README.md is up to date
- [ ] CHANGELOG.md updated with version changes
- [ ] API documentation is complete
- [ ] Examples work with new version

### Version Management
- [ ] Version bumped in all package files:
  - `package.json`
  - `pyproject.toml`
  - `setup.py`
  - `src/rust/Cargo.toml`
  - `src/python/__init__.py`
- [ ] Git tag created: `git tag v0.1.0`
- [ ] Git tag pushed: `git push origin v0.1.0`

### Legal & Licensing
- [ ] LICENSE file included
- [ ] All source files have proper headers
- [ ] Third-party dependencies reviewed
- [ ] No sensitive information in published files

### Security
- [ ] No API keys, tokens, or secrets in code
- [ ] Dependencies scanned for vulnerabilities
- [ ] `.npmignore`, `.gitignore` properly configured

---

## Version Management

### Semantic Versioning

The Universal Axiom follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes, backwards compatible

### Updating Versions

Use the provided script to update all package versions at once:

```bash
# Bump patch version (0.1.0 -> 0.1.1)
make version-patch

# Bump minor version (0.1.0 -> 0.2.0)
make version-minor

# Bump major version (0.1.0 -> 1.0.0)
make version-major
```

Or manually update in these files:
1. `package.json` → `"version"`
2. `pyproject.toml` → `[project] version`
3. `setup.py` → `version=`
4. `src/rust/Cargo.toml` → `[package] version`
5. `src/python/__init__.py` → `__version__`

### Creating a Release

1. **Update version** in all files
2. **Update CHANGELOG.md** with changes
3. **Commit changes**:
   ```bash
   git add .
   git commit -m "Bump version to 0.2.0"
   ```
4. **Create git tag**:
   ```bash
   git tag -a v0.2.0 -m "Release version 0.2.0"
   ```
5. **Push changes and tags**:
   ```bash
   git push origin main
   git push origin v0.2.0
   ```
6. **Publish packages** (see platform-specific instructions above)
7. **Create GitHub Release** (optional):
   - Go to repository → Releases → Draft new release
   - Choose the tag (v0.2.0)
   - Add release notes
   - Publish

---

## Publishing to All Platforms (One Command)

For convenience, publish to all platforms with:

```bash
make publish-all
```

This will:
1. Run all tests
2. Build all packages
3. Publish to NPM
4. Publish to PyPI
5. Publish to Crates.io

**Note**: This requires all credentials to be configured.

---

## Troubleshooting

### NPM: "You do not have permission to publish"
- Ensure you're logged in: `npm whoami`
- Check package name isn't taken
- Verify scoped package: must use `--access public` for first publish

### PyPI: "Invalid username/password"
- Use `__token__` as username
- Ensure token starts with `pypi-`
- Check `~/.pypirc` configuration

### Crates.io: "failed to verify package tarball"
- Ensure all files referenced exist
- Check `Cargo.toml` paths are correct
- Run `cargo package --list` to see included files

### Version Conflicts
- Ensure version is higher than published version
- Check all package files have same version
- Cannot republish same version (must bump)

---

## Support

For issues with publishing:
- NPM: https://docs.npmjs.com/
- PyPI: https://pypi.org/help/
- Crates.io: https://doc.rust-lang.org/cargo/reference/publishing.html

For project-specific help:
- Issues: https://github.com/TheUniversalAxiom/pointy-stick/issues
- Website: https://www.epiphanyengine.ai
