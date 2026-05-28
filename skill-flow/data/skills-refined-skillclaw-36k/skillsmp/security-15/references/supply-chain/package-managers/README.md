# Package Manager Patterns for SBOM Generation

This directory contains detection patterns and configuration knowledge for each supported package manager ecosystem. These patterns enable accurate SBOM generation by identifying:

- **Manifest files**: Primary dependency declarations
- **Lock files**: Resolved dependency graphs with exact versions
- **Cache locations**: Where packages are stored locally
- **SBOM generation commands**: Native and third-party tools
- **Configuration options**: Customization for SBOM output

## Supported Package Managers

### Tier 1: Full Pattern Support (Detailed RAG Documentation)

| Ecosystem | Manager | Manifest | Lock File | Native SBOM Tool | Status |
|-----------|---------|----------|-----------|------------------|--------|
| JavaScript | npm | `package.json` | `package-lock.json` | `npm sbom`, cyclonedx-npm | Complete |
| JavaScript | yarn | `package.json` | `yarn.lock` | cyclonedx-yarn, cdxgen | Complete |
| JavaScript | pnpm | `package.json` | `pnpm-lock.yaml` | cyclonedx-pnpm, cdxgen | Complete |
| Python | pip | `requirements.txt` | (pip freeze) | cyclonedx-py | Complete |
| Python | poetry | `pyproject.toml` | `poetry.lock` | cyclonedx-py, cdxgen | Complete |
| Python | uv | `pyproject.toml` | `uv.lock` | cyclonedx-py, cdxgen | Complete |
| Rust | cargo | `Cargo.toml` | `Cargo.lock` | cargo-cyclonedx, cdxgen | Complete |
| Go | go mod | `go.mod` | `go.sum` | cyclonedx-gomod, cdxgen | Complete |
| Java | maven | `pom.xml` | (effective-pom) | cyclonedx-maven-plugin | Complete |
| Java | gradle | `build.gradle` | `gradle.lockfile` | cyclonedx-gradle-plugin | Complete |
| Ruby | bundler | `Gemfile` | `Gemfile.lock` | cyclonedx-ruby, cdxgen | Complete |
| PHP | composer | `composer.json` | `composer.lock` | cyclonedx-php-composer | Complete |
| .NET | nuget | `*.csproj` | `packages.lock.json` | CycloneDX .NET tool | Complete |

### Tier 2: Basic Support (Detection Only)

| Ecosystem | Manager | Manifest | Lock File | SBOM Tool |
|-----------|---------|----------|-----------|-----------|
| JavaScript | bun | `package.json` | `bun.lockb` | cdxgen |
| Python | pipenv | `Pipfile` | `Pipfile.lock` | cdxgen |
| Python | pdm | `pyproject.toml` | `pdm.lock` | cdxgen |
| Swift | swift | `Package.swift` | `Package.resolved` | cdxgen |
| Elixir | mix | `mix.exs` | `mix.lock` | cdxgen |
| Erlang | rebar3 | `rebar.config` | `rebar.lock` | cdxgen |
| Scala | sbt | `build.sbt` | - | cdxgen |
| Haskell | cabal | `*.cabal` | `cabal.project.freeze` | cdxgen |
| Clojure | lein | `project.clj` | - | cdxgen |
| Dart | pub | `pubspec.yaml` | `pubspec.lock` | cdxgen |
| Kotlin | gradle | `build.gradle.kts` | `gradle.lockfile` | cdxgen |

## Detection Tiers

### Tier 1: Manifest Detection
Identifies the package manager by presence of manifest files.

### Tier 2: Lock File Detection
Locates lock files for accurate dependency resolution.

### Tier 3: Configuration Extraction
Extracts configuration values like:
- Registry URLs
- Private repository settings
- Dependency groups (dev, test, prod)
- Version constraints

## Pattern File Structure

Each package manager has a `patterns.md` file with comprehensive documentation:

```
package-managers/
├── README.md                    # This file
├── npm/patterns.md              # npm (JavaScript)
├── yarn/patterns.md             # Yarn Classic & Berry
├── pnpm/patterns.md             # pnpm (JavaScript)
├── pip/patterns.md              # pip (Python)
├── poetry/patterns.md           # Poetry (Python)
├── uv/patterns.md               # uv (Python, Rust-based)
├── cargo/patterns.md            # Cargo (Rust)
├── go/patterns.md               # Go Modules
├── maven/patterns.md            # Maven (Java)
├── gradle/patterns.md           # Gradle (Java/Kotlin)
├── bundler/patterns.md          # Bundler (Ruby)
├── composer/patterns.md         # Composer (PHP)
└── nuget/patterns.md            # NuGet (.NET)
```

### Pattern File Contents

Each patterns.md includes:

1. **TIER 1: Manifest Detection** - File patterns, required fields, dependency types
2. **TIER 2: Lock File Detection** - Lock file format, structure, key fields
3. **TIER 3: Configuration Extraction** - Registry URLs, authentication, environment variables
4. **SBOM Generation** - Native tools, cdxgen commands
5. **Cache Locations** - Platform-specific paths
6. **Best Practices** - Reproducible builds, security recommendations
7. **Troubleshooting** - Common issues and solutions

## Usage

These patterns are used by:
1. **SBOM Scanner**: To detect package managers and generate accurate SBOMs
2. **Technology Scanner**: To identify language/framework ecosystems
3. **Packages Scanner**: To analyze dependencies and vulnerabilities

## SBOM Generation Best Practices

1. **Always use lock files** for deterministic SBOM generation
2. **Exclude dev dependencies** in production SBOMs (`--omit=dev`)
3. **Include hashes** for integrity verification
4. **Generate during CI/CD** for consistent results
5. **Sign SBOMs** with Sigstore for provenance

See also:
- [SBOM Generation Best Practices](../sbom-generation-best-practices.md)
- [Package Manager Specifications](../package-manager-specifications.md)
