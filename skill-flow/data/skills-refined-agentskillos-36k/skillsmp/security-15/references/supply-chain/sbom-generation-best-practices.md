# SBOM Generation Best Practices and Specifications

## Executive Summary

A Software Bill of Materials (SBOM) is a comprehensive inventory of software components, dependencies, and metadata that provides transparency into software composition. This document compiles authoritative best practices, specifications, and implementation guidance for generating accurate, complete, and machine-readable SBOMs.

**Last Updated:** November 2025
**Target Audience:** Security teams, DevOps engineers, compliance officers, software developers

---

## Table of Contents

1. [SBOM Standards and Specifications](#sbom-standards-and-specifications)
2. [2025 SBOM Minimum Elements (CISA/NTIA)](#2025-sbom-minimum-elements-cisantia)
3. [Lock File Specifications by Package Manager](#lock-file-specifications-by-package-manager)
4. [Transitive Dependency Resolution](#transitive-dependency-resolution)
5. [Production vs Development Dependencies](#production-vs-development-dependencies)
6. [Reproducible Builds and Version Pinning](#reproducible-builds-and-version-pinning)
7. [SBOM Generation Tools by Ecosystem](#sbom-generation-tools-by-ecosystem)
8. [Vulnerability Correlation with VEX](#vulnerability-correlation-with-vex)
9. [SBOM Signing and Attestation](#sbom-signing-and-attestation)
10. [Common Pitfalls and Solutions](#common-pitfalls-and-solutions)
11. [Best Practices Summary](#best-practices-summary)

---

## SBOM Standards and Specifications

### CycloneDX

**Current Version:** 1.7 (Released October 21, 2025)
**Standard:** ECMA-424 (Ecma International)
**Organization:** OWASP

#### Key Features

- Full-stack Bill of Materials standard for cyber risk reduction
- Supports multiple BOM types: SBOM, SaaSBOM, HBOM, AI/ML-BOM, CBOM, OBOM, MBOM
- Includes Vulnerability Disclosure Reports (VDR) and Vulnerability Exploitability eXchange (VEX)
- Reference implementation: JSON Schema

#### Supported Formats

- **XML:** `application/vnd.cyclonedx+xml`
- **JSON:** `application/vnd.cyclonedx+json`
- **Protocol Buffer:** `application/x.vnd.cyclonedx+protobuf`

#### Component Types

CycloneDX can describe multiple types of components:
- Applications
- Containers
- Devices
- Libraries
- Files
- Firmware
- Frameworks
- Operating systems
- Services

#### Package URL (PURL) Specification

Package URLs standardize how software package metadata is represented across ecosystems.

**PURL Components:**
- **Type (required):** Package protocol (maven, npm, nuget, gem, pypi, cargo, golang, etc.)
- **Namespace (optional):** Name prefix (Maven groupId, Docker owner, GitHub org)
- **Name (required):** Package name
- **Version (optional):** Package version
- **Qualifiers (optional):** Extra data (OS, architecture, distro)

**Example PURLs:**
```
pkg:npm/express@4.18.2
pkg:maven/org.apache.commons/commons-lang3@3.12.0
pkg:pypi/requests@2.31.0
pkg:cargo/serde@1.0.152
pkg:golang/github.com/gin-gonic/gin@v1.9.1
```

#### Component Hashes

CycloneDX supports multiple hash algorithms for integrity verification:
- MD5
- SHA-1
- SHA-256 (recommended)
- SHA-384
- SHA-512
- SHA3-256
- SHA3-384
- SHA3-512

**XML Example:**
```xml
<hash alg="SHA-256">f498a8ff2dd007e29c2074f5e4b01a9a01775c3ff3aeaf6906ea503bc5791b7b</hash>
```

**JSON Example:**
```json
{
  "alg": "SHA-256",
  "content": "d88bc4e70bfb34d18b5542136639acbb26a8ae2429aa1e47489332fb389cc964"
}
```

#### Version 1.7 Highlights

- Extended formulations scope to describe how any referenceable object within the BOM came together
- Support for components, services, metadata, declarations, and the BOM itself
- Deprecated fields related to cryptographic transparency (CBOM)

**Resources:**
- Specification: https://cyclonedx.org/specification/overview/
- Documentation: https://cyclonedx.org/docs/1.5/json/
- Use Cases: https://cyclonedx.org/use-cases/

### SPDX (Software Package Data Exchange)

**Current Version:** 3.0.1 (August 2025)
**Standard:** ISO/IEC 5962:2021
**Organization:** Linux Foundation

#### Key Features

- International open standard for security, license compliance, and software supply chain artifacts
- Based on Resource Description Framework (RDF)
- Expanded scope: AI models, datasets, system lifecycle information
- Profiles for specialized use cases

#### SPDX 3.0 Profiles

Eight profiles defined in SPDX 3.0:
1. **Core** - Base functionality
2. **Software** - Software components
3. **Security** - Vulnerability data, VEX
4. **Licensing** - License information
5. **Dataset** - Data assets
6. **AI** - Artificial intelligence models
7. **Build** - Build metadata
8. **Usage** - Usage information

#### Serialization Formats

Data may be serialized in multiple RDF formats:
- **JSON-LD** (recommended for human readability)
- **Turtle** (Terse RDF Triple Language)
- **N-Triples**
- **RDF/XML**

#### JSON-LD Context

SPDX 3.0 provides a JSON-LD context file for simplified, human-readable JSON:
- Context file: `https://spdx.org/rdf/3.0.1/spdx-context.jsonld`
- Allows use of simple, locally defined terms while ensuring interoperability

#### Validation Requirements

A conformant SPDX 3.0 JSON-LD serialization must:
1. Structurally validate against the SPDX JSON Schema
2. Semantically validate against the SPDX OWL ontology

#### Relationships

SPDX 3.0 relationships enable detailed modeling:
- More expressive than previous versions
- Easier to understand
- Explicit relationships between components (dependencies, inclusion, exclusion)
- `serializedInArtifact` relationship links SpdxDocument to serialized forms

#### License List

**Current Version:** 3.27.0 (July 1, 2025)

**Resources:**
- Specification: https://spdx.github.io/spdx-spec/v3.0.1/
- License List: https://spdx.org/licenses/
- GitHub: https://github.com/spdx/spdx-spec

---

## 2025 SBOM Minimum Elements (CISA/NTIA)

### Overview

CISA released updated guidance in August 2025, building on the 2021 NTIA SBOM Minimum Elements. This update reflects:
- Advances in SBOM tooling
- Growing maturity of SBOM adoption
- Lessons learned from increased SBOM generation and use
- Improved expectations for SBOM data quality

**Public Comment Period:** Concluded October 3, 2025

### Three Main Categories

1. **Data Fields** - Essential metadata elements
2. **Automation Support** - Machine-readable capabilities
3. **Practices and Processes** - Generation and management workflows

### Core Data Field Requirements

#### 2025 Updates

| Element | 2021 NTIA | 2025 CISA | Notes |
|---------|-----------|-----------|-------|
| Supplier Name | Required | Replaced | Now "Producer Name" |
| Producer Name | - | Required | Replaces Supplier Name |
| Component Name | Required | Required | Clarified definition |
| Component Version | Required | Required | Enhanced guidance |
| Component Hash | - | Required | NEW in 2025 |
| License | - | Required | NEW in 2025 |
| SBOM Author | Required | Required | Enhanced definition |
| Timestamp | Required | Required | Date/time of assembly |
| Dependency Relationships | Required | Required | Upstream components |
| Tool Name | - | Required | NEW in 2025 |
| Generation Context | - | Required | NEW in 2025 |

#### Data Field Definitions

**Producer Name:**
- Entity that created the software
- Replaces "Supplier Name" for clarity
- Must be machine-readable

**Component Name:**
- Human-readable identifier
- Assigned by software producer
- Must be consistent across versions

**Component Version:**
- Identifier for changes from previous versions
- Must follow semantic versioning when possible
- Required for vulnerability correlation

**Component Hash (NEW):**
- Cryptographic hash of component
- SHA-256 recommended
- Enables integrity verification

**License (NEW):**
- SPDX license identifier preferred
- Custom licenses must be documented
- Essential for compliance

**SBOM Author:**
- Entity that created the SBOM (may differ from producer)
- Can be automated tool or organization
- Enables accountability

**Timestamp:**
- Date and time of SBOM assembly
- ISO 8601 format required
- Critical for SBOM lifecycle management

**Dependency Relationships:**
- Describes component interconnections
- Must include transitive dependencies
- Enables supply chain visibility

**Tool Name (NEW):**
- Name and version of SBOM generation tool
- Enables reproducibility
- Supports quality assessment

**Generation Context (NEW):**
- Build environment information
- Source code repository details
- Build configuration data

### Machine-Readable Formats

SBOMs must be generated in standardized formats:
- **SPDX** (ISO/IEC 5962:2021)
- **CycloneDX** (ECMA-424)
- **SWID** (ISO/IEC 19770-2:2015)

### Automation Support Requirements

- Machine-readable structure
- Standardized format compliance
- API accessibility
- CI/CD integration capabilities

### Practices and Processes

- Generate SBOMs automatically in build pipelines
- Treat SBOMs as living artifacts
- Update when dependencies change
- Sign and verify SBOM integrity
- Store and distribute securely

**Resources:**
- CISA Guidance: https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom
- NTIA Original: https://www.ntia.gov/page/software-bill-materials

---

## Lock File Specifications by Package Manager

Lock files are critical for accurate SBOM generation because they:
- Provide fully resolved dependency trees
- Include exact versions of all dependencies (direct and transitive)
- Contain integrity hashes for verification
- Enable reproducible builds
- Serve as source of truth for installed packages

### JavaScript/Node.js

#### npm (package-lock.json)

**Format:** JSON
**Location:** Project root
**Created by:** `npm install`

**Key Features:**
- Records exact dependency tree
- Includes integrity hashes (SHA-512)
- Supports workspaces (monorepos)
- Version-specific format (lockfileVersion)

**Structure:**
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "project-name",
      "version": "1.0.0",
      "dependencies": {
        "express": "^4.18.2"
      }
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ=="
    }
  }
}
```

**SBOM Generation:**
```bash
# Built-in npm command
npm sbom --sbom-format=cyclonedx > sbom.json
npm sbom --sbom-format=spdx > sbom.spdx.json

# Using CycloneDX
npx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Exclude dev dependencies
npx @cyclonedx/cyclonedx-npm --omit=dev --output-file sbom.json
```

**Best Practices:**
- Always commit package-lock.json to version control
- Use `npm ci` in CI/CD (installs from lock file exactly)
- Use `--package-lock-only` flag to ignore node_modules
- Run `npm audit` regularly for vulnerability scanning

#### Yarn (yarn.lock)

**Format:** Custom YAML-like format
**Location:** Project root
**Created by:** `yarn install`

**Key Features:**
- Human-readable format
- Records resolved versions
- Includes integrity checksums
- Supports Yarn workspaces

**Structure:**
```
# THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY.
# yarn lockfile v1

express@^4.18.2:
  version "4.18.2"
  resolved "https://registry.yarnpkg.com/express/-/express-4.18.2.tgz#3fabe08296e930c796c19e3c516979386ba9fd59"
  integrity sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ==
  dependencies:
    accepts "~1.3.8"
    array-flatten "1.1.1"
```

**SBOM Generation:**
```bash
# Using CycloneDX
yarn dlx @cyclonedx/cyclonedx-npm --output-file sbom.json

# Exclude dev dependencies
yarn dlx @cyclonedx/cyclonedx-npm --omit=dev
```

**Best Practices:**
- Always commit yarn.lock to version control
- Use `--frozen-lockfile` in CI/CD to prevent updates
- Never edit yarn.lock manually
- Standardize on one package manager per project (npm OR yarn, not both)

#### pnpm (pnpm-lock.yaml)

**Format:** YAML
**Location:** Project root
**Created by:** `pnpm install`

**Key Features:**
- Content-addressable storage
- Symlink-based node_modules structure
- Workspace support
- Includes integrity hashes

**Structure:**
```yaml
lockfileVersion: '6.0'
dependencies:
  express:
    specifier: ^4.18.2
    version: 4.18.2

packages:
  /express@4.18.2:
    resolution: {integrity: sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ==}
    engines: {node: '>= 0.10.0'}
    dependencies:
      accepts: 1.3.8
```

**SBOM Generation:**
```bash
# Using Snyk
snyk sbom --format=cyclonedx1.4+json --package-manager=pnpm --file=pnpm-lock.yaml > sbom.json

# Using cdxgen
cdxgen -o sbom.json
```

**Challenges:**
- pnpm has unique node_modules structure (.pnpm directory with symlinks)
- No native SBOM command like npm
- Third-party tools must understand pnpm's structure

**Best Practices:**
- Commit pnpm-lock.yaml to version control
- Use `pnpm install --frozen-lockfile` in CI/CD
- Document use of pnpm for SBOM tool selection

#### Bun (bun.lockb)

**Format:** Binary
**Location:** Project root
**Created by:** `bun install`

**Key Features:**
- Binary format (not human-readable)
- Extremely fast installation
- Can migrate from npm/yarn/pnpm lock files
- Compatible with package.json

**SBOM Generation:**
```bash
# Using cdxgen
cdxgen -o sbom.json
```

**Note:** Bun is a newer package manager with limited native SBOM tooling support. Use cdxgen for SBOM generation.

**Best Practices:**
- Commit bun.lockb to version control
- Document Bun usage for security teams
- Test SBOM generation tools for Bun compatibility

### Python

#### pip (requirements.txt)

**Format:** Plain text
**Location:** Varies (commonly project root)
**Created by:** Manual or `pip freeze`

**Structure:**
```
certifi==2023.7.22
charset-normalizer==3.3.2
idna==3.6
requests==2.31.0
urllib3==2.1.0
```

**Limitations:**
- Not a true lock file (no hashes by default)
- No transitive dependency metadata
- Multiple naming conventions (requirements_dev.txt, requirements-test.txt)

**Enhanced Format with Hashes:**
```
certifi==2023.7.22 \
    --hash=sha256:539cc1d13202e33ca466e88b2807e29f4c13049d6d87031a3c110744495cb082
requests==2.31.0 \
    --hash=sha256:942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1
```

**SBOM Generation:**
```bash
# Using CycloneDX
cyclonedx-py requirements requirements.txt -o sbom.json

# Using SPDX
spdx-sbom-generator -p requirements.txt -o sbom.spdx
```

#### Pipenv (Pipfile.lock)

**Format:** JSON
**Location:** Project root
**Created by:** `pipenv lock`

**Key Features:**
- Records exact versions
- Includes SHA-256 hashes
- Separates default and development dependencies
- Deterministic builds

**Structure:**
```json
{
    "_meta": {
        "hash": {
            "sha256": "..."
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.11"
        }
    },
    "default": {
        "requests": {
            "hashes": [
                "sha256:942c5a758f98d790eaed1a29cb6eefc7ffb0d1cf7af05c3d2791656dbd6ad1e1"
            ],
            "index": "pypi",
            "version": "==2.31.0"
        }
    },
    "develop": {}
}
```

**SBOM Generation:**
```bash
# Using CycloneDX
cyclonedx-py pipenv -o sbom.json
```

#### Poetry (poetry.lock)

**Format:** TOML
**Location:** Project root
**Created by:** `poetry lock`

**Key Features:**
- TOML format
- Complete dependency graph
- Content hashes for verification
- Supports dependency groups

**Structure:**
```toml
[[package]]
name = "requests"
version = "2.31.0"
description = "Python HTTP for Humans."
category = "main"
optional = false
python-versions = ">=3.7"

[package.dependencies]
certifi = ">=2017.4.17"
charset-normalizer = ">=2,<4"
idna = ">=2.5,<4"
urllib3 = ">=1.21.1,<3"

[[package]]
name = "certifi"
version = "2023.7.22"
```

**SBOM Generation:**
```bash
# Using CycloneDX
cyclonedx-py poetry -o sbom.json

# Using cdxgen (with poetry.lock)
cdxgen -o sbom.json
```

**Note:** Some tools have issues extracting license information from poetry.lock. Ensure license data is in pyproject.toml.

#### pyproject.toml

**Format:** TOML
**Standard:** PEP 621
**Location:** Project root

**Key Features:**
- Modern Python project configuration
- Supported by multiple tools (flit, hatch, pdm, poetry, uv)
- Declarative dependency specification
- May include or reference requirements

**Structure:**
```toml
[project]
name = "my-project"
version = "1.0.0"
dependencies = [
    "requests>=2.31.0",
    "click>=8.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0"
]
```

**Best Practices:**
- Use poetry.lock or Pipfile.lock for SBOM generation (not pyproject.toml)
- pyproject.toml specifies ranges; lock files specify exact versions
- Starting Python 3.12.2, CPython includes SBOM documents in releases

### Ruby (Gemfile.lock)

**Format:** Custom text format
**Location:** Project root
**Created by:** `bundle install`

**Key Features:**
- Records exact gem versions
- Platform-specific dependencies
- Bundler version information
- Transitive dependencies

**Structure:**
```
GEM
  remote: https://rubygems.org/
  specs:
    rack (2.2.8)
    sinatra (3.1.0)
      mustermann (~> 3.0)
      rack (~> 2.2, >= 2.2.4)
      rack-protection (= 3.1.0)
      tilt (~> 2.0)

PLATFORMS
  ruby
  x86_64-darwin-22
  x86_64-linux

DEPENDENCIES
  sinatra (~> 3.1)

BUNDLED WITH
   2.4.10
```

**SBOM Generation:**
```bash
# Using CycloneDX
cyclonedx-ruby -p ./ -o sbom.json

# Using cdxgen
cdxgen -o sbom.json
```

**Best Practices:**
- Always commit Gemfile.lock to version control
- Use `bundle install --frozen` in production
- Run `bundle audit` for vulnerability scanning

### Rust (Cargo.lock)

**Format:** TOML
**Location:** Project root
**Created by:** `cargo build` or `cargo update`

**Key Features:**
- TOML format
- Exact dependency versions
- Checksum verification
- Git dependencies support

**Structure:**
```toml
version = 3

[[package]]
name = "serde"
version = "1.0.152"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "bb7d1f0d3021d347a83e556fc4683dea2ea09d87bccdf88ff5c12545d89d5efb"
dependencies = [
 "serde_derive",
]

[[package]]
name = "serde_derive"
version = "1.0.152"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "af487d118eecd09402d70a5d72551860e788df87b464af30e5ea6a38c75c541e"
```

**SBOM Generation:**
```bash
# Using CycloneDX
cargo cyclonedx --format json --output-cdx sbom.json

# Using cargo-sbom
cargo install cargo-sbom
cargo sbom > sbom.spdx.json

# Using cdxgen
cdxgen -o sbom.json
```

**Note:** Trivy requires Cargo.lock to be available when scanning Rust binaries.

**Best Practices:**
- Commit Cargo.lock for applications (binaries)
- Do NOT commit Cargo.lock for libraries (let consumers resolve)
- Use `cargo update` to refresh dependencies

### Go (go.mod and go.sum)

**Format:** Custom text format
**Location:** Project root
**Created by:** `go mod init`, updated by Go commands

#### go.mod

**Purpose:** Declares module requirements (manifest)

**Structure:**
```go
module github.com/example/myapp

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/spf13/cobra v1.8.0
)

require (
    github.com/bytedance/sonic v1.9.1 // indirect
    github.com/spf13/pflag v1.0.5 // indirect
)
```

#### go.sum

**Purpose:** Cryptographic checksums for reproducible builds

**Structure:**
```
github.com/gin-gonic/gin v1.9.1 h1:4idEAncQnU5cB7BeOkPtxjfCSye0AAm1R0RVIqJ+Jmg=
github.com/gin-gonic/gin v1.9.1/go.mod h1:hPrL7YrpYKXt5YId3A/Tnip5kqbEAP+KLuI3SUcPTeU=
github.com/spf13/cobra v1.8.0 h1:7aJaZx1B85qltLMc546zn58BxxfZdR/W22ej9CFoEf0=
github.com/spf13/cobra v1.8.0/go.mod h1:WXLWApfZ71AjXPya3WOlMsY9yMs7YeiHhFVlvLyhcho=
```

**SBOM Generation:**
```bash
# Using CycloneDX
cyclonedx-gomod app -json -output sbom.json

# Generate for application (only included dependencies)
cyclonedx-gomod app -json -licenses -output sbom.json

# Using SPDX
spdx-sbom-generator -p ./ -o sbom.spdx

# Using cdxgen
cdxgen -o sbom.json
```

**Best Practices:**
- Both go.mod and go.sum must be committed
- go.sum provides integrity verification (like lock files)
- Use `go mod tidy` to clean up unused dependencies
- Use `go mod verify` to check integrity
- For SBOMs, prefer tools that analyze compiled binaries

### Java/Maven (pom.xml + effective-pom)

**Format:** XML
**Location:** Project root
**Created by:** Developer (pom.xml), Maven (effective-pom)

**Key Features:**
- Declarative dependency management
- Transitive dependency resolution
- Dependency scopes (compile, test, runtime, provided)
- BOM (Bill of Materials) imports

**Dependency Example:**
```xml
<project>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
      <version>3.1.5</version>
    </dependency>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.13.2</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```

**SBOM Generation:**
```bash
# Using CycloneDX Maven Plugin
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# Configure in pom.xml
<build>
  <plugins>
    <plugin>
      <groupId>org.cyclonedx</groupId>
      <artifactId>cyclonedx-maven-plugin</artifactId>
      <version>2.7.11</version>
      <executions>
        <execution>
          <phase>package</phase>
          <goals>
            <goal>makeAggregateBom</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>

# Run with build
mvn clean package
# SBOM generated at target/bom.json or target/bom.xml
```

**Spring Boot 3.3+ Automatic SBOM:**
```xml
<!-- No additional configuration needed -->
<!-- SBOM automatically generated in META-INF/sbom/ -->
```

**Best Practices:**
- Commit pom.xml to version control
- Use dependency management sections for version control
- Run `mvn dependency:tree` to view resolved dependencies
- Generate SBOM during `package` or `verify` phase

### Java/Gradle (build.gradle)

**Format:** Groovy DSL or Kotlin DSL
**Location:** Project root
**Created by:** Developer

**Dependency Example (Groovy):**
```groovy
plugins {
    id 'java'
    id 'org.cyclonedx.bom' version '1.8.2'
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web:3.1.5'
    testImplementation 'junit:junit:4.13.2'
}
```

**SBOM Generation:**
```bash
# Using CycloneDX Gradle Plugin
./gradlew cyclonedxBom

# SBOM generated at build/reports/bom.json or build/reports/bom.xml
```

**Plugin Configuration:**
```groovy
cyclonedxBom {
    includeConfigs = ["runtimeClasspath"]
    skipConfigs = ["testRuntimeClasspath"]
    destination = file("build/reports")
    outputName = "sbom"
    outputFormat = "json"
    includeLicenseText = true
}
```

**Best Practices:**
- Commit build.gradle and settings.gradle to version control
- Use Gradle lock files (`gradle.lockfile`) for deterministic builds
- Enable lock files: `./gradlew dependencies --write-locks`
- For SPDX, currently limited tool support compared to Maven

---

## Transitive Dependency Resolution

### Overview

Transitive dependencies are dependencies of your dependencies. Accurate SBOM generation requires capturing the complete dependency tree, not just direct dependencies.

### Multi-Level Dependency Trees

**Flat vs. Hierarchical SBOMs:**
- **Flat SBOM:** Lists all dependencies at one level (ineffective for understanding relationships)
- **Hierarchical SBOM:** Multi-level tree showing how each component depends on others (recommended)

**Example Dependency Tree:**
```
my-app (1.0.0)
├── express (4.18.2)
│   ├── accepts (1.3.8)
│   │   ├── mime-types (2.1.35)
│   │   │   └── mime-db (1.52.0)
│   │   └── negotiator (0.6.3)
│   ├── body-parser (1.20.1)
│   └── cookie (0.5.0)
└── lodash (4.17.21)
```

### Best Practices for Transitive Dependencies

#### 1. Use Language-Specific Tools

Single-language SBOM generation tools typically produce more reliable SBOMs with complete transitive dependency information.

**Examples:**
- **npm:** `npm sbom` or `@cyclonedx/cyclonedx-npm`
- **Maven:** CycloneDX Maven plugin
- **Go:** `cyclonedx-gomod app` (for applications)
- **Python:** `cyclonedx-py`

#### 2. Automate in CI/CD

Generate SBOMs automatically with every build to capture dependency changes.

**CI/CD Integration Points:**
- After dependency resolution
- Before compilation
- During package/build phase
- Post-build verification

**Example GitHub Actions:**
```yaml
- name: Generate SBOM
  run: |
    npm ci
    npm sbom --sbom-format=cyclonedx > sbom.json

- name: Upload SBOM
  uses: actions/upload-artifact@v3
  with:
    name: sbom
    path: sbom.json
```

#### 3. Track Dependency Relationships

Use SBOM formats that support relationship metadata:

**CycloneDX Relationships:**
```json
{
  "dependencies": [
    {
      "ref": "pkg:npm/express@4.18.2",
      "dependsOn": [
        "pkg:npm/accepts@1.3.8",
        "pkg:npm/body-parser@1.20.1",
        "pkg:npm/cookie@0.5.0"
      ]
    }
  ]
}
```

**SPDX Relationships:**
```json
{
  "spdxElementId": "SPDXRef-Package-express",
  "relationshipType": "DEPENDS_ON",
  "relatedSpdxElement": "SPDXRef-Package-accepts"
}
```

#### 4. Generate at Different SDLC Stages

**Design SBOM:**
- Planned components
- Architecture dependencies
- Third-party selections

**Build SBOM:**
- Actual resolved dependencies
- Lock file-based
- Signed and timestamped

**Runtime SBOM:**
- Actually loaded components
- Dynamic dependencies
- Container image analysis

#### 5. Validate Completeness

**Verification Checks:**
- Compare SBOM component count to package manager output
- Verify transitive dependencies against lock files
- Check for missing vulnerability data
- Validate relationship graphs

**Tools for Validation:**
```bash
# Compare npm dependencies to SBOM
npm list --all --json > npm-tree.json
# Compare counts and packages

# Validate CycloneDX SBOM
cyclonedx validate --input-file sbom.json

# Validate SPDX SBOM
spdx-tools check sbom.spdx.json
```

#### 6. Handle Version Conflicts

Package managers resolve version conflicts differently:

**npm/Yarn:** Nested dependencies (can have multiple versions)
**Maven:** Nearest definition wins
**Go:** Minimal version selection
**Cargo:** Single version per dependency

Ensure your SBOM accurately reflects the actual resolved versions.

#### 7. Cross-Validate with Multiple Tools

For critical applications, generate SBOMs with multiple tools and compare:

```bash
# Generate with multiple tools
npm sbom --sbom-format=cyclonedx > sbom-npm.json
cdxgen -t js -o sbom-cdxgen.json

# Compare results
diff <(jq -S '.components | sort_by(.name)' sbom-npm.json) \
     <(jq -S '.components | sort_by(.name)' sbom-cdxgen.json)
```

### Common Transitive Dependency Challenges

#### Challenge 1: Dependency Drift

**Problem:** Transitive dependencies update without direct dependency changes

**Solution:**
- Use lock files religiously
- Automate SBOM regeneration on any dependency change
- Monitor SBOM differences in version control

#### Challenge 2: Conditional Dependencies

**Problem:** Dependencies that are only required in specific environments (OS, architecture)

**Solution:**
- Document build environment in SBOM metadata
- Use SBOM qualifiers for platform-specific dependencies
- Generate separate SBOMs for each target platform

**Example PURL with Qualifiers:**
```
pkg:cargo/openssl@0.10.55?platform=linux-x86_64
```

#### Challenge 3: Build-Time vs Runtime Dependencies

**Problem:** Some transitive dependencies are only needed during build

**Solution:**
- Separate SBOMs for build and runtime
- Use dependency scopes (compile, runtime, test)
- For containers, generate SBOM from final image, not build stage

#### Challenge 4: Monorepo Dependencies

**Problem:** Internal packages with their own dependency trees

**Solution:**
- Use workspace-aware SBOM tools
- Generate both per-package and aggregate SBOMs
- Document internal package relationships

**Example (pnpm workspaces):**
```bash
# Per-package SBOM
cdxgen -o sbom-api.json packages/api

# Aggregate SBOM
cdxgen -o sbom-monorepo.json
```

---

## Production vs Development Dependencies

### Overview

Development dependencies are tools and libraries used during development but not included in production deployments. The inclusion or exclusion of development dependencies in SBOMs depends on use case.

### Dependency Types by Package Manager

#### npm/Yarn/pnpm

**Dependency Types:**
- **dependencies:** Required in production
- **devDependencies:** Development and testing only
- **optionalDependencies:** Optional features
- **peerDependencies:** Required by consumers

**Example package.json:**
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "eslint": "^8.54.0",
    "typescript": "^5.3.2"
  }
}
```

**SBOM Generation (Production Only):**
```bash
# npm
npm sbom --omit=dev > sbom-prod.json

# CycloneDX
npx @cyclonedx/cyclonedx-npm --omit=dev -o sbom-prod.json

# pnpm (using third-party tool)
snyk sbom --dev=false --format=cyclonedx1.4+json > sbom-prod.json
```

#### Maven

**Dependency Scopes:**
- **compile:** Available in all classpaths (default)
- **provided:** Expected from JDK or container
- **runtime:** Not needed for compilation, required at runtime
- **test:** Only available for test compilation and execution
- **system:** Similar to provided, but must explicitly provide JAR
- **import:** Import dependencies from other POMs (BOM files)

**Example:**
```xml
<dependency>
  <groupId>junit</groupId>
  <artifactId>junit</artifactId>
  <version>4.13.2</version>
  <scope>test</scope>
</dependency>
```

**SBOM Generation (Production Only):**
```bash
# CycloneDX Maven Plugin (excludes test scope by default)
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# Include specific scopes
mvn cyclonedx:makeAggregateBom -DincludeRuntimeScope=true -DincludeCompileScope=true
```

#### Gradle

**Configurations:**
- **implementation:** Compile and runtime dependencies
- **api:** Dependencies exposed to consumers
- **runtimeOnly:** Runtime-only dependencies
- **testImplementation:** Test dependencies
- **compileOnly:** Compile-time only

**SBOM Generation (Production Only):**
```groovy
cyclonedxBom {
    includeConfigs = ["runtimeClasspath", "compileClasspath"]
    skipConfigs = ["testRuntimeClasspath", "testCompileClasspath"]
}
```

#### Python

**Dependency Groups:**
- **Main dependencies:** Listed in dependencies (pyproject.toml) or requirements.txt
- **Development dependencies:** Listed in dev group or requirements-dev.txt

**Example pyproject.toml:**
```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "flask>=3.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0"
]
```

**SBOM Generation:**
```bash
# CycloneDX (production only, from poetry)
cyclonedx-py poetry --only main -o sbom-prod.json

# From requirements.txt (no dev dependencies by default)
cyclonedx-py requirements requirements.txt -o sbom.json
```

#### Cargo (Rust)

**Dependency Sections:**
- **[dependencies]:** Required for building
- **[dev-dependencies]:** Required for tests and examples
- **[build-dependencies]:** Required for build scripts

**Example Cargo.toml:**
```toml
[dependencies]
serde = "1.0"
tokio = { version = "1.35", features = ["full"] }

[dev-dependencies]
criterion = "0.5"
```

**SBOM Generation:**
```bash
# CycloneDX (production only)
cargo cyclonedx --format json --output-cdx sbom.json

# cdxgen (from source - production deps only)
cdxgen --no-include-dev -o sbom.json
```

### Best Practices for Production SBOMs

#### 1. Exclude Development Dependencies

**Rationale:**
- Development tools are not "materials" of the software
- Reduces false positives in vulnerability scanning
- Focuses security efforts on deployed code
- Reduces SBOM size and complexity

**How to Exclude:**
- Use production-only installation commands
- Configure SBOM tools to skip dev dependencies
- Generate from production builds/images, not development environments

#### 2. Use Package Manager Production Modes

**Examples:**
```bash
# npm - install production only
npm ci --omit=dev

# Python Poetry - install main group only
poetry install --only main

# Maven - skip test scope
mvn package -DskipTests

# Cargo - build release (excludes dev-dependencies)
cargo build --release
```

#### 3. Generate from Deployment Artifacts

**Best Practice:** Generate SBOMs from the actual deployment artifact:

**Container Images:**
```bash
# Generate SBOM during container build with cdxgen
cdxgen -t docker -o sbom.json .

# Or integrate into Dockerfile
# COPY --from=builder sbom.json /app/sbom.json
```

**Go/Rust Projects:**
```bash
# Generate from source before building
cdxgen -t go -o sbom.json
cdxgen -t rust -o sbom.json
```

**Java Projects:**
```bash
# Generate from pom.xml/build.gradle
cdxgen -t java -o sbom.json
```

#### 4. Document SBOM Scope

Include metadata describing what's included:

**CycloneDX Metadata:**
```json
{
  "metadata": {
    "properties": [
      {
        "name": "cdx:sbom:scope",
        "value": "production"
      },
      {
        "name": "cdx:sbom:excludes",
        "value": "devDependencies,testDependencies"
      }
    ]
  }
}
```

### When to Include Development Dependencies

**Include Development Dependencies If:**

1. **Compliance Requirements:** Regulators require complete software inventory
2. **Supply Chain Analysis:** Analyzing entire development environment
3. **Build Reproducibility:** Documenting complete build environment
4. **Internal Security Audit:** Understanding all tools in development pipeline

**Separate SBOMs Approach:**
```bash
# Production SBOM
npm sbom --omit=dev -o sbom-production.json

# Development SBOM
npm sbom -o sbom-development.json

# Build environment SBOM (includes all deps)
cdxgen -o sbom-build-env.json
```

### Debate: To Include or Not to Include

**Arguments Against Including Dev Dependencies:**
- Not part of shipped software
- Creates noise in vulnerability scanning
- Increases false positive rate
- Larger SBOM size

**Arguments For Including Dev Dependencies:**
- Complete supply chain transparency
- Build environment security matters
- Compromised dev tools can inject malicious code
- Compliance with comprehensive audit requirements

**Recommended Approach:**
- **Primary SBOM:** Production dependencies only
- **Supplementary SBOM:** Complete development environment
- **Clear Documentation:** Metadata indicating scope

---

## Reproducible Builds and Version Pinning

### Overview

Reproducible builds ensure that identical source code produces bit-for-bit identical binaries. Version pinning and lock files are critical for both reproducibility and accurate SBOM generation.

### Lock Files and Reproducibility

**Lock File Benefits:**
- Fully resolved requirements with exact versions
- Cryptographic hashes for integrity verification
- Complete dependency tree (including transitive)
- Consistent builds across environments

**Reproducibility Formula:**
```
Same Source Code + Same Lock File + Same Build Environment = Identical Binary
```

### Version Pinning Strategies

#### Semantic Versioning (SemVer)

**Format:** MAJOR.MINOR.PATCH (e.g., 2.5.3)

**Version Ranges:**
- `^1.2.3` - Compatible with 1.x.x (>= 1.2.3, < 2.0.0)
- `~1.2.3` - Approximately 1.2.x (>= 1.2.3, < 1.3.0)
- `1.2.x` - Any patch version of 1.2
- `1.2.3` - Exact version only
- `*` - Any version (dangerous!)

#### Pinning Approaches

**1. Exact Pinning (Strict)**
```json
{
  "dependencies": {
    "express": "4.18.2",
    "lodash": "4.17.21"
  }
}
```

**Pros:**
- Maximum reproducibility
- Predictable behavior
- Easier vulnerability tracking

**Cons:**
- No automatic security updates
- Requires manual updates
- Can accumulate technical debt

**2. Range Pinning (Flexible)**
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.0"
  }
}
```

**Pros:**
- Automatic patch updates
- Receive security fixes
- Less maintenance

**Cons:**
- Potential for breaking changes
- Less reproducible without lock file
- Dependency drift risk

**3. Lock File Pinning (Recommended)**

**Manifest (package.json):**
```json
{
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

**Lock File (package-lock.json):**
```json
{
  "packages": {
    "node_modules/express": {
      "version": "4.18.2",
      "integrity": "sha512-..."
    }
  }
}
```

**Pros:**
- Combines flexibility and reproducibility
- Ranges in manifest, exact versions in lock file
- Easy updates with lock file regeneration

### Best Practices by Package Manager

#### npm

```bash
# Install from lock file (exact versions)
npm ci

# Update dependencies and lock file
npm update

# Install specific version
npm install express@4.18.2 --save-exact

# Verify integrity
npm audit
```

**package.json Configuration:**
```json
{
  "scripts": {
    "preinstall": "npm config set save-exact true"
  }
}
```

#### Yarn

```bash
# Install from lock file
yarn install --frozen-lockfile

# Update dependencies
yarn upgrade

# Install exact version
yarn add express@4.18.2 --exact
```

**.yarnrc Configuration:**
```yaml
save-exact true
```

#### Python Poetry

```bash
# Install from lock file
poetry install

# Update lock file
poetry update

# Install with exact version
poetry add "requests==2.31.0"
```

**pyproject.toml:**
```toml
[tool.poetry.dependencies]
python = "^3.11"
requests = "2.31.0"  # Exact version
```

#### Maven

```xml
<!-- Use dependency management for version control -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>3.1.5</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

#### Go

```bash
# Go modules use minimal version selection
go mod tidy

# Update to latest
go get -u ./...

# Verify checksums
go mod verify

# Vendor dependencies for reproducibility
go mod vendor
```

### SBOM and Version Matching

#### Challenge: Version Ranges in Manifests

**Problem:** Manifest files specify ranges, not exact versions.

**Solution:** Always generate SBOMs from lock files, not manifest files.

**Wrong (from package.json):**
```json
{
  "name": "express",
  "version": "^4.18.2"  // Range, not exact
}
```

**Correct (from package-lock.json):**
```json
{
  "name": "express",
  "version": "4.18.2",  // Exact version
  "integrity": "sha512-..."
}
```

#### SBOM Validation Against Lock Files

**Validation Process:**
1. Generate SBOM from lock file
2. Compare SBOM versions to lock file versions
3. Verify all transitive dependencies are included
4. Check integrity hashes match

**Example Validation Script:**
```bash
#!/bin/bash
# Compare SBOM components to package-lock.json

# Extract package names and versions from SBOM
jq -r '.components[] | "\(.name)@\(.version)"' sbom.json | sort > sbom-packages.txt

# Extract from package-lock.json
jq -r '.packages | to_entries[] | select(.key != "") | "\(.key | split("/")[-1])@\(.value.version)"' package-lock.json | sort > lock-packages.txt

# Compare
diff sbom-packages.txt lock-packages.txt
```

### Reproducible Build Environments

#### Containerized Builds

**Dockerfile for Reproducible Builds:**
```dockerfile
# Pin base image with digest
FROM node:20.10.0@sha256:abc123...

# Install specific npm version
RUN npm install -g npm@10.2.5

# Copy lock file first
COPY package-lock.json ./

# Install from lock file
RUN npm ci --omit=dev

# Copy source
COPY . .

# Build
RUN npm run build

# Generate SBOM
RUN npm sbom --sbom-format=cyclonedx > /sbom.json
```

#### CI/CD Configuration

**GitHub Actions Example:**
```yaml
name: Build and Generate SBOM

on: [push]

jobs:
  build:
    runs-on: ubuntu-22.04  # Pin runner version

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.10.0'  # Exact version

      - name: Verify lock file
        run: |
          npm ci
          git diff --exit-code package-lock.json

      - name: Build
        run: npm run build

      - name: Generate SBOM
        run: npm sbom --sbom-format=cyclonedx > sbom.json

      - name: Verify SBOM
        run: |
          # Validate SBOM format
          cyclonedx validate --input-file sbom.json

      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json
```

### Trade-offs: Floating vs Pinned Versions

| Aspect | Floating Versions | Pinned Versions |
|--------|-------------------|-----------------|
| **Agility** | High - automatic updates | Low - manual updates |
| **Security** | Auto-patches available | Manual patching required |
| **Stability** | Risk of regressions | Predictable behavior |
| **Reproducibility** | Low (without lock file) | High |
| **Maintenance** | Lower effort | Higher effort |
| **SBOM Accuracy** | Requires lock file | Straightforward |
| **Audit Trail** | Harder to track | Clear version history |

**Recommended Approach:**
- Use **ranges in manifests** for flexibility
- Use **lock files** for reproducibility
- **Commit lock files** to version control
- **Update regularly** but deliberately
- **Generate SBOMs** from lock files
- **Document update policy** in README

### Handling Version Drift

**Detection:**
```bash
# Check for outdated dependencies
npm outdated
pip list --outdated
cargo outdated
```

**Regular Update Cycle:**
1. Review outdated dependencies weekly/monthly
2. Update lock file: `npm update`, `poetry update`
3. Run tests to verify compatibility
4. Generate new SBOM
5. Compare SBOMs for changes
6. Commit lock file and SBOM together

**SBOM Diff in Version Control:**
```bash
# View SBOM changes
git diff sbom.json

# Automated SBOM comparison in PR
diff <(git show main:sbom.json | jq -S '.components | sort_by(.name)') \
     <(jq -S '.components | sort_by(.name)' sbom.json)
```

---

## SBOM Generation Tools by Ecosystem

### Multi-Language Tools

#### cdxgen (OWASP) - Recommended

**Supported Formats:** CycloneDX
**Ecosystems:** 20+ languages

**Key Features:**
- Deep dependency analysis
- VEX generation
- SBOM attestation
- Rich metadata

**Installation:**
```bash
npm install -g @cyclonedx/cdxgen
```

**Usage:**
```bash
# Auto-detect project type
cdxgen -o sbom.json

# Specify type
cdxgen -t js -o sbom.json
cdxgen -t python -o sbom.json

# Include dev dependencies
cdxgen --include-dev -o sbom.json

# Generate with VEX
cdxgen --vex -o sbom.json
```

**Best For:** Rich SBOMs, multiple ecosystems, VEX support

#### Microsoft SBOM Tool

**Supported Formats:** SPDX
**Ecosystems:** Multiple

**Key Features:**
- Enterprise-focused
- SPDX 2.2 compliance
- Hash generation
- Component verification

**Installation:**
```bash
# Via dotnet
dotnet tool install -g Microsoft.Sbom.DotNetTool
```

**Usage:**
```bash
# Generate SBOM
sbom-tool generate -b . -bc . -pn MyProject -pv 1.0.0 -ps MyCompany -nsb https://mycompany.com

# Validate SBOM
sbom-tool validate -b . -o sbom.json
```

**Best For:** SPDX format, enterprise compliance, .NET projects

### JavaScript/Node.js

#### npm (Built-in)

**Supported Formats:** SPDX, CycloneDX

**Usage:**
```bash
# CycloneDX format
npm sbom --sbom-format=cyclonedx > sbom.json

# SPDX format
npm sbom --sbom-format=spdx > sbom.spdx.json

# Omit dev dependencies
npm sbom --omit=dev > sbom.json

# Use package-lock only (ignore node_modules)
npm sbom --package-lock-only > sbom.json
```

**Best For:** npm projects, built-in solution, official support

#### CycloneDX for npm/Yarn/pnpm

**Installation:**
```bash
npm install -g @cyclonedx/cyclonedx-npm
```

**Usage:**
```bash
# npm project
cyclonedx-npm --output-file sbom.json

# Exclude dev dependencies
cyclonedx-npm --omit=dev --output-file sbom.json

# Yarn project
cyclonedx-npm --output-file sbom.json

# Include license text
cyclonedx-npm --output-file sbom.json --license-text
```

**Best For:** CycloneDX format, advanced options, cross-package-manager

### Python

#### CycloneDX for Python

**Installation:**
```bash
pip install cyclonedx-bom
```

**Usage:**
```bash
# From requirements.txt
cyclonedx-py requirements requirements.txt -o sbom.json

# From Pipenv
cyclonedx-py pipenv -o sbom.json

# From Poetry (production only)
cyclonedx-py poetry --only main -o sbom.json

# From environment
cyclonedx-py environment -o sbom.json
```

**Best For:** CycloneDX format, multiple Python dependency formats

#### sbom4python

**Installation:**
```bash
pip install sbom4python
```

**Usage:**
```bash
# Generate SBOM for installed module
sbom4python --module requests --output sbom.json --format cyclonedx

# SPDX format
sbom4python --module requests --output sbom.spdx.json --format spdx
```

**Best For:** Analyzing installed Python packages

#### SPDX SBOM Generator

**Installation:**
```bash
pip install spdx-tools
```

**Usage:**
```bash
spdx-sbom-generator -p requirements.txt -o sbom.spdx.json
```

**Best For:** SPDX format for Python projects

### Java

#### CycloneDX Maven Plugin

**Configuration (pom.xml):**
```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.cyclonedx</groupId>
      <artifactId>cyclonedx-maven-plugin</artifactId>
      <version>2.7.11</version>
      <executions>
        <execution>
          <phase>package</phase>
          <goals>
            <goal>makeAggregateBom</goal>
          </goals>
        </execution>
      </executions>
      <configuration>
        <outputFormat>json</outputFormat>
        <outputName>sbom</outputName>
      </configuration>
    </plugin>
  </plugins>
</build>
```

**Usage:**
```bash
# Generate SBOM
mvn cyclonedx:makeAggregateBom

# During build
mvn clean package
# SBOM at target/sbom.json
```

**Best For:** Maven projects, automated builds, CycloneDX

#### CycloneDX Gradle Plugin

**Configuration (build.gradle):**
```groovy
plugins {
    id 'org.cyclonedx.bom' version '1.8.2'
}

cyclonedxBom {
    includeConfigs = ["runtimeClasspath"]
    outputFormat = "json"
    outputName = "sbom"
    includeLicenseText = true
}
```

**Usage:**
```bash
./gradlew cyclonedxBom
# SBOM at build/reports/sbom.json
```

**Best For:** Gradle projects, CycloneDX format

#### Spring Boot 3.3+ (Built-in)

Spring Boot 3.3 and later automatically generate SBOMs during build.

**Location:** `META-INF/sbom/`

**Configuration (pom.xml):**
```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.3.0</version>
</dependency>
```

**No additional configuration needed!**

**Best For:** Spring Boot projects, zero-configuration

### Go

#### CycloneDX for Go Modules

**Installation:**
```bash
go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest
```

**Usage:**
```bash
# Generate for application (only included deps)
cyclonedx-gomod app -json -output sbom.json

# Include license data
cyclonedx-gomod app -json -licenses -output sbom.json

# Generate for module (all deps including dev)
cyclonedx-gomod mod -json -output sbom.json
```

**Best For:** Go projects, accurate application SBOMs

#### SPDX SBOM Generator

**Installation:**
```bash
go install github.com/opensbom-generator/spdx-sbom-generator/cmd/generator@latest
```

**Usage:**
```bash
spdx-sbom-generator -p ./ -o sbom.spdx.json
```

**Best For:** SPDX format for Go projects

### Rust

#### CycloneDX for Cargo

**Installation:**
```bash
cargo install cargo-cyclonedx
```

**Usage:**
```bash
# Generate CycloneDX SBOM
cargo cyclonedx --format json --output-cdx sbom.json

# Include license text
cargo cyclonedx --format json --output-cdx sbom.json --all
```

**Best For:** Rust projects, CycloneDX format

#### cargo-sbom

**Installation:**
```bash
cargo install cargo-sbom
```

**Usage:**
```bash
cargo sbom > sbom.spdx.json
```

**Best For:** SPDX format for Rust projects

**Note:** Trivy requires Cargo.lock for accurate Rust binary scanning.

### Ruby

#### CycloneDX for Ruby

**Installation:**
```bash
gem install cyclonedx-ruby
```

**Usage:**
```bash
# From Gemfile.lock
cyclonedx-ruby -p ./ -o sbom.json
```

**Best For:** Ruby projects with Bundler

### Container Images

#### cdxgen

```bash
# Generate SBOM for container project
cdxgen -t docker -o sbom.json .

# With specific output format
cdxgen -t docker -o sbom.json --spec-version 1.5
```

#### Trivy

**Installation:**
```bash
# macOS
brew install aquasecurity/trivy/trivy

# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

**Usage:**
```bash
# Generate SBOM from image
trivy image --format cyclonedx nginx:latest > sbom.json

# SPDX format
trivy image --format spdx-json nginx:latest > sbom.spdx.json

# Scan filesystem
trivy fs --format cyclonedx . > sbom.json
```

**Best For:** Container security scanning, SBOM + vulnerabilities

---

## Vulnerability Correlation with VEX

### Overview

Vulnerability Exploitability eXchange (VEX) enriches SBOMs with vulnerability status information. VEX documents help reduce noise from false positives by indicating which vulnerabilities actually affect the software.

### SBOM + VEX Relationship

**Metaphor:** "SBOM turns on all relevant lights, VEX turns off all the unnecessary ones."

**SBOM Role:**
- Complete inventory of components
- Identifies potential vulnerabilities
- Maps to CVE database

**VEX Role:**
- Filters applicable vulnerabilities
- Reduces false positives
- Provides exploitability context
- Enables prioritization

### VEX Status Values

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| **Not Affected** | Vulnerability does not impact this product | None |
| **Affected** | Vulnerability impacts this product | Remediation needed |
| **Fixed** | Vulnerability has been remediated | Update recommended |
| **Under Investigation** | Impact is being assessed | Monitor status |

### VEX Formats

#### CycloneDX VEX (Embedded)

VEX can be directly embedded in CycloneDX 1.4+

**Example:**
```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "vulnerabilities": [
    {
      "id": "CVE-2023-12345",
      "source": {
        "name": "NVD",
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2023-12345"
      },
      "ratings": [
        {
          "score": 7.5,
          "severity": "high",
          "method": "CVSSv3",
          "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"
        }
      ],
      "affects": [
        {
          "ref": "pkg:npm/express@4.17.0",
          "versions": [
            {
              "version": "4.17.0",
              "status": "affected"
            }
          ]
        }
      ],
      "analysis": {
        "state": "not_affected",
        "justification": "code_not_reachable",
        "detail": "The vulnerable function is not called in our application."
      }
    }
  ]
}
```

#### SPDX VEX

VEX is included in the Security profile of SPDX 3.0.

**Example:**
```json
{
  "spdxVersion": "SPDX-3.0",
  "creationInfo": {
    "created": "2025-11-22T10:00:00Z"
  },
  "vulnerabilities": [
    {
      "id": "CVE-2023-12345",
      "vexStatus": "not_affected",
      "vexJustification": "vulnerable_code_not_in_execute_path",
      "statementTimestamp": "2025-11-22T10:00:00Z"
    }
  ]
}
```

#### CSAF VEX

Common Security Advisory Framework (CSAF) 2.0 includes VEX profile.

**Example:**
```json
{
  "document": {
    "category": "csaf_vex",
    "title": "VEX Document for Product X"
  },
  "product_tree": {
    "branches": [
      {
        "name": "Product X",
        "product": {
          "product_id": "PRODUCTX-1.0",
          "name": "Product X version 1.0"
        }
      }
    ]
  },
  "vulnerabilities": [
    {
      "cve": "CVE-2023-12345",
      "product_status": {
        "known_not_affected": ["PRODUCTX-1.0"]
      },
      "threats": [
        {
          "category": "impact",
          "details": "Vulnerable code not reachable"
        }
      ]
    }
  ]
}
```

### CVE and CVSS Integration

#### Common Vulnerabilities and Exposures (CVE)

**CVE Identifier Format:** CVE-YEAR-NUMBER (e.g., CVE-2023-12345)

**Data Sources:**
- **NVD (National Vulnerability Database):** https://nvd.nist.gov/
- **MITRE CVE List:** https://cve.mitre.org/
- **GitHub Advisory Database:** https://github.com/advisories
- **OSV (Open Source Vulnerabilities):** https://osv.dev/

#### Common Vulnerability Scoring System (CVSS)

**CVSS Versions:**
- **CVSS v2** (deprecated)
- **CVSS v3.0**
- **CVSS v3.1** (current standard)
- **CVSS v4.0** (latest, released 2023)

**CVSS v3.1 Metrics:**

**Base Metrics:**
- Attack Vector (AV): Network, Adjacent, Local, Physical
- Attack Complexity (AC): Low, High
- Privileges Required (PR): None, Low, High
- User Interaction (UI): None, Required
- Scope (S): Unchanged, Changed
- Confidentiality (C): None, Low, High
- Integrity (I): None, Low, High
- Availability (A): None, Low, High

**Severity Ratings:**
- **None:** 0.0
- **Low:** 0.1-3.9
- **Medium:** 4.0-6.9
- **High:** 7.0-8.9
- **Critical:** 9.0-10.0

**Example CVSS Vector:**
```
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```
Score: 9.8 (Critical)

**In CycloneDX:**
```json
{
  "ratings": [
    {
      "score": 9.8,
      "severity": "critical",
      "method": "CVSSv31",
      "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
    }
  ]
}
```

### Vulnerability Correlation Workflow

#### Step 1: Generate SBOM

```bash
# Generate SBOM with component details
npm sbom --sbom-format=cyclonedx > sbom.json
```

#### Step 2: Scan for Vulnerabilities

```bash
# Using osv-scanner (recommended)
osv-scanner --sbom=sbom.json --format json > vulnerabilities.json

# Using Trivy
trivy sbom sbom.json --format json > vulnerabilities.json

# Using OWASP Dependency-Track
# Upload SBOM to Dependency-Track for continuous monitoring
```

#### Step 3: Analyze Results

Tools match SBOM components against vulnerability databases:
- Component name + version → CVE lookup
- PURL matching for accuracy
- CPE (Common Platform Enumeration) matching

#### Step 4: Create VEX Document

Assess each vulnerability:
- Is the vulnerable code path reachable?
- Are mitigating controls in place?
- Is the component used in a safe context?

**VEX Justification Codes:**
- `component_not_present`
- `vulnerable_code_not_present`
- `vulnerable_code_not_in_execute_path`
- `vulnerable_code_cannot_be_controlled_by_adversary`
- `inline_mitigations_already_exist`

#### Step 5: Distribute SBOM + VEX

Options:
- Embedded VEX in CycloneDX SBOM
- Separate VEX document linked to SBOM
- Upload to vulnerability management platform

### Tools for Vulnerability Correlation

#### OWASP Dependency-Track

**Features:**
- SBOM ingestion (CycloneDX, SPDX)
- Continuous vulnerability monitoring
- VEX support
- Risk scoring
- Policy enforcement

**Usage:**
```bash
# Upload SBOM via API
curl -X "POST" "http://dtrack.example.com/api/v1/bom" \
  -H 'Content-Type: multipart/form-data' \
  -H 'X-API-Key: your-api-key' \
  -F "project=project-uuid" \
  -F "bom=@sbom.json"
```

**Best For:** Continuous SBOM monitoring, enterprise-scale

#### osv-scanner (Recommended)

**Installation:**
```bash
# macOS
brew install osv-scanner

# Linux/Go install
go install github.com/google/osv-scanner/cmd/osv-scanner@latest
```

**Usage:**
```bash
# Scan SBOM
osv-scanner --sbom=sbom.json

# Output as JSON
osv-scanner --sbom=sbom.json --format json

# Scan directory (lock files)
osv-scanner -r .

# Scan specific lock file
osv-scanner --lockfile=package-lock.json
```

**Best For:** CI/CD vulnerability scanning, OSV database integration

#### Trivy

```bash
# Scan SBOM for vulnerabilities
trivy sbom sbom.json

# Generate SBOM + vulnerabilities
trivy image --format cyclonedx --scanners vuln nginx:latest > sbom-with-vulns.json

# VEX filtering
trivy image --vex vex.json nginx:latest
```

**Best For:** Container scanning, SBOM + vulnerability combo

### Best Practices for Vulnerability Management

#### 1. Combine SBOM with VEX

Don't rely on SBOM alone for vulnerability assessment. Use VEX to provide context.

#### 2. Prioritize with Multiple Factors

Beyond CVSS scores, consider:
- **EPSS (Exploit Prediction Scoring System):** Likelihood of exploitation
- **SSVC (Stakeholder-Specific Vulnerability Categorization):** Decision tree for prioritization
- **Reachability Analysis:** Is vulnerable code actually executed?
- **VEX Status:** Official vendor assessment

**Prioritization Formula:**
```
Priority = f(CVSS, EPSS, Reachability, VEX Status, Business Impact)
```

#### 3. Automate Vulnerability Scanning

Integrate into CI/CD:

```yaml
# GitHub Actions example
- name: Generate SBOM
  run: npm sbom --sbom-format=cyclonedx > sbom.json

- name: Scan for vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'sbom'
    input: 'sbom.json'
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload to GitHub Security
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

#### 4. Maintain SBOM + VEX Lifecycle

- **Generate SBOM:** Every build
- **Scan for vulnerabilities:** Every build + continuous monitoring
- **Update VEX:** When vulnerabilities are assessed/remediated
- **Distribute:** Share SBOM + VEX with customers/stakeholders

#### 5. Use Package URLs (PURLs) for Accuracy

PURLs reduce false positives by providing precise component identification:

```
pkg:npm/express@4.18.2
```

is more accurate than just:
```
express 4.18.2
```

#### 6. Monitor Continuously

Don't just generate SBOMs once:
- New vulnerabilities are discovered daily
- Upload SBOMs to platforms like Dependency-Track
- Set up alerts for new CVEs affecting your components

---

## SBOM Signing and Attestation

### Overview

Signing SBOMs and creating attestations ensures:
- **Authenticity:** Verifies who created the SBOM
- **Integrity:** Detects tampering
- **Non-repudiation:** Creator cannot deny authorship
- **Trust:** Establishes chain of custody

### SBOM vs Attestations

**SBOM:**
- Inventory of components
- Metadata about software composition
- Can be signed or unsigned

**Attestation:**
- Signed document containing metadata about an artifact
- Includes provenance information (who, what, when, where, how)
- More trustworthy due to signature and metadata

**Relationship:**
An SBOM can be included within an attestation, or an SBOM itself can be signed to create an attestation.

### SLSA Provenance

**SLSA (Supply chain Levels for Software Artifacts)** is a framework for ensuring artifact integrity.

**SLSA Levels:**
- **SLSA 0:** No guarantees
- **SLSA 1:** Provenance exists
- **SLSA 2:** Tamper-resistant provenance
- **SLSA 3:** Hardened build platform
- **SLSA 4:** Hermetic, reproducible builds

**SLSA Provenance Attestation:**
Built on in-toto attestation framework, providing:
- Build platform information
- Source repository
- Build command
- Materials (inputs)
- Builder identity

**Example Provenance:**
```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://slsa.dev/provenance/v0.2",
  "subject": [
    {
      "name": "pkg:docker/myapp@sha256:abc123",
      "digest": {
        "sha256": "abc123..."
      }
    }
  ],
  "predicate": {
    "builder": {
      "id": "https://github.com/Attestations/GitHubHostedActions@v1"
    },
    "buildType": "https://github.com/Attestations/GitHubActionsWorkflow@v1",
    "materials": [
      {
        "uri": "git+https://github.com/myorg/myapp@refs/heads/main",
        "digest": {
          "sha1": "def456..."
        }
      }
    ]
  }
}
```

**SLSA + SBOM Integration:**
- SBOM hinge on accuracy and completeness
- SLSA provenance improves SBOM trustworthiness
- Combined: Verifiable software composition with build integrity

### Signing SBOMs with Sigstore/Cosign

#### Cosign Overview

**Cosign** is part of the Sigstore project, providing:
- Keyless signing (OIDC-based)
- Signature verification
- Attestation creation
- OCI registry storage

**Installation:**
```bash
# macOS
brew install cosign

# Linux
wget https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64
chmod +x cosign-linux-amd64
sudo mv cosign-linux-amd64 /usr/local/bin/cosign
```

#### Signing an SBOM

**Method 1: Keyless Signing (Recommended)**
```bash
# Sign SBOM (uses OIDC for identity)
cosign sign-blob --bundle sbom.bundle sbom.json

# This will:
# 1. Open browser for OIDC authentication
# 2. Sign the SBOM
# 3. Create transparency log entry
# 4. Save signature bundle
```

**Method 2: Key-Based Signing**
```bash
# Generate key pair
cosign generate-key-pair

# Sign SBOM
cosign sign-blob --key cosign.key sbom.json > sbom.sig

# Sign with bundle
cosign sign-blob --key cosign.key --bundle sbom.bundle sbom.json
```

#### Verifying SBOM Signature

**Keyless Verification:**
```bash
# Verify with bundle
cosign verify-blob --bundle sbom.bundle --certificate-identity=your-email@example.com --certificate-oidc-issuer=https://github.com/login/oauth sbom.json
```

**Key-Based Verification:**
```bash
# Verify with public key
cosign verify-blob --key cosign.pub --signature sbom.sig sbom.json
```

#### Creating SBOM Attestations

**Attach SBOM as Attestation to Container Image:**
```bash
# Generate SBOM with cdxgen
cdxgen -t docker -o sbom.json .

# Create attestation and attach to image
cosign attest --key cosign.key --type cyclonedx --predicate sbom.json myapp:latest

# Keyless attestation
cosign attest --type cyclonedx --predicate sbom.json myapp:latest
```

**Verify Attestation:**
```bash
# Verify attestation on image
cosign verify-attestation --key cosign.pub --type cyclonedx myapp:latest

# Keyless verification
cosign verify-attestation --certificate-identity=your-email@example.com --certificate-oidc-issuer=https://github.com/login/oauth --type cyclonedx myapp:latest
```

#### SBOM Attestation in GitHub

GitHub supports artifact attestations natively:

**Generate Attestation in GitHub Actions:**
```yaml
- name: Generate SBOM
  run: npm sbom --sbom-format=cyclonedx > sbom.json

- name: Attest SBOM
  uses: actions/attest-sbom@v1
  with:
    subject-path: 'dist/myapp.tar.gz'
    sbom-path: 'sbom.json'
```

**Verify Attestation:**
```bash
# Install GitHub CLI
gh attestation verify myapp.tar.gz --owner myorg
```

### In-Toto Attestation Framework

**in-toto** provides a framework for securing the software supply chain.

**Attestation Structure:**
```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "subject": [
    {
      "name": "myapp",
      "digest": {
        "sha256": "abc123..."
      }
    }
  ],
  "predicateType": "https://cyclonedx.org/bom",
  "predicate": {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "components": [...]
  }
}
```

### Best Practices for SBOM Signing

#### 1. Sign Every SBOM

Treat SBOMs as critical security artifacts:
- Sign during build process
- Store signatures alongside SBOMs
- Verify before consumption

#### 2. Use Keyless Signing

Advantages:
- No key management burden
- OIDC-based identity
- Transparency log provides audit trail
- Revocation through certificate transparency

#### 3. Include Provenance

Combine SBOM with build provenance:
- Source repository
- Build environment
- Builder identity
- Timestamp
- Build parameters

#### 4. Store in Transparency Logs

Sigstore's Rekor provides immutable transparency log:
- Verifiable timestamps
- Cannot be deleted
- Public audit trail

#### 5. Automate in CI/CD

**Complete Workflow:**
```yaml
name: Build, SBOM, Sign, Attest

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
      attestations: write

    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: npm run build

      - name: Generate SBOM
        run: npm sbom --sbom-format=cyclonedx > sbom.json

      - name: Sign SBOM
        run: cosign sign-blob --bundle sbom.bundle sbom.json

      - name: Attest Build
        uses: actions/attest-build-provenance@v1
        with:
          subject-path: 'dist/myapp.tar.gz'

      - name: Attest SBOM
        uses: actions/attest-sbom@v1
        with:
          subject-path: 'dist/myapp.tar.gz'
          sbom-path: 'sbom.json'

      - name: Upload Artifacts
        uses: actions/upload-artifact@v3
        with:
          name: release-artifacts
          path: |
            dist/
            sbom.json
            sbom.bundle
```

#### 6. Verify Before Use

Downstream consumers should verify:
```bash
# Verify SBOM signature
cosign verify-blob --bundle sbom.bundle --certificate-identity=builder@example.com --certificate-oidc-issuer=https://token.actions.githubusercontent.com sbom.json

# Verify container attestations
cosign verify-attestation --type slsaprovenance myapp:latest
cosign verify-attestation --type cyclonedx myapp:latest
```

---

## Common Pitfalls and Solutions

### 1. Incomplete Component Coverage

**Problem:**
- Missing transitive dependencies
- Pre-compiled binaries not analyzed
- Incomplete dependency tree

**Solution:**
- Use lock files as source of truth
- Generate SBOM from source with cdxgen
- Generate SBOMs at build time, not from source only
- Validate SBOM completeness against package manager output

**Validation Script:**
```bash
# npm example
npm list --all --json | jq '.dependencies | keys | length'
jq '.components | length' sbom.json
# Numbers should match
```

### 2. Lack of Automation

**Problem:**
- Manual SBOM generation is error-prone
- Forgotten updates when dependencies change
- Inconsistent SBOM quality

**Solution:**
- Integrate SBOM generation into CI/CD pipelines
- Generate on every build
- Automate validation and distribution
- Use pre-commit hooks for SBOM verification

**Pre-commit Hook Example:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check if package-lock.json changed
if git diff --cached --name-only | grep -q package-lock.json; then
    echo "package-lock.json changed, regenerating SBOM..."
    npm sbom --sbom-format=cyclonedx > sbom.json
    git add sbom.json
fi
```

### 3. Missing or Inaccurate Metadata

**Problem:**
- No supplier information
- Incorrect CPEs (Common Platform Enumeration)
- Missing license data
- Wrong component versions

**Solution:**
- Use tools that extract complete metadata
- Validate CPEs against NVD database
- Cross-reference with multiple data sources
- Manually enrich critical component data

**CycloneDX Metadata Example:**
```json
{
  "metadata": {
    "timestamp": "2025-11-22T10:00:00Z",
    "tools": [
      {
        "vendor": "npm",
        "name": "npm-cli",
        "version": "10.2.5"
      }
    ],
    "authors": [
      {
        "name": "Security Team",
        "email": "security@example.com"
      }
    ],
    "component": {
      "type": "application",
      "name": "myapp",
      "version": "1.0.0",
      "supplier": {
        "name": "Example Corp"
      }
    }
  }
}
```

### 4. Outdated or Inaccurate Data

**Problem:**
- SBOMs not updated when dependencies change
- Version mismatches between SBOM and actual software
- Stale SBOMs in distribution

**Solution:**
- Generate SBOM with every build
- Include SBOM timestamp
- Implement SBOM versioning/tagging
- Link SBOM to specific software version

**SBOM Versioning:**
```bash
# Tag SBOM with software version
npm sbom --sbom-format=cyclonedx > sbom-v1.2.3.json

# Include in metadata
jq '.metadata.component.version = "1.2.3"' sbom.json > sbom-v1.2.3.json

# Git tag
git tag -a v1.2.3 -m "Release v1.2.3 with SBOM"
```

### 5. Lack of Standardized Formats

**Problem:**
- Custom SBOM formats that aren't interoperable
- Tools can't consume SBOM
- Incompatible with vulnerability scanners

**Solution:**
- Use SPDX or CycloneDX exclusively
- Validate SBOMs against official schemas
- Test SBOM consumption with target tools

**Format Validation:**
```bash
# Validate CycloneDX
cyclonedx validate --input-file sbom.json

# Validate SPDX
spdx-tools check sbom.spdx.json

# Validate with schema
ajv validate -s cyclonedx-schema.json -d sbom.json
```

### 6. Poor Cross-Department Collaboration

**Problem:**
- Developers don't understand SBOM importance
- Security teams lack visibility
- Procurement doesn't request SBOMs from vendors

**Solution:**
- Educate teams on SBOM benefits
- Integrate SBOM into security policy
- Require SBOMs in vendor contracts
- Share SBOMs across organization

**Policy Example:**
```markdown
## SBOM Policy

1. All internal software MUST include an SBOM
2. SBOM MUST be generated automatically in CI/CD
3. SBOM MUST be in CycloneDX or SPDX format
4. SBOM MUST be signed with Sigstore
5. SBOM MUST be distributed with software releases
6. Third-party software MUST include vendor-provided SBOM
```

### 7. Insufficient Resources and Expertise

**Problem:**
- Lack of knowledge about SBOM generation
- Insufficient tooling budget
- No dedicated SBOM management

**Solution:**
- Use open-source tools (cdxgen, CycloneDX CLI, SPDX tools)
- Train security and DevOps teams
- Start small: one project as pilot
- Leverage community resources and documentation

### 8. Including node_modules in Scans

**Problem:**
- Scanning node_modules directory directly
- Including dev dependencies from file system
- Inaccurate dependency tree

**Solution:**
- Use `--package-lock-only` flag
- Generate from lock files, not file system
- Exclude node_modules from filesystem scans

**Correct Approach:**
```bash
# Use lock file only
npm sbom --package-lock-only > sbom.json

# cdxgen: automatically uses lock files when present
cdxgen -o sbom.json
```

### 9. Incorrect Version Resolution

**Problem:**
- Version ranges instead of exact versions
- Transitive version conflicts not reflected
- Different versions in different environments

**Solution:**
- Always use lock files for SBOM generation
- Document build environment
- Generate SBOMs from deployment artifacts

### 10. Missing Component Hashes

**Problem:**
- No integrity verification possible
- Cannot detect tampering
- Compliance requirement not met

**Solution:**
- Use tools that include hashes (SHA-256 minimum)
- Validate hashes against lock files
- Verify integrity during deployment

**Hash Validation Example:**
```bash
# Extract hash from SBOM
SBOM_HASH=$(jq -r '.components[] | select(.name=="express") | .hashes[] | select(.alg=="SHA-256") | .content' sbom.json)

# Extract from package-lock.json
LOCK_HASH=$(jq -r '.packages."node_modules/express".integrity' package-lock.json | cut -d'-' -f2)

# Compare
if [ "$SBOM_HASH" != "$LOCK_HASH" ]; then
    echo "Hash mismatch!"
    exit 1
fi
```

### 11. Ignoring Platform-Specific Dependencies

**Problem:**
- SBOMs generated on one platform (Linux) don't reflect dependencies on another (Windows)
- Native modules have different dependencies per platform

**Solution:**
- Generate SBOMs for each target platform
- Use PURL qualifiers for platform-specific dependencies
- Document platform in SBOM metadata

**Platform-Specific PURL:**
```
pkg:npm/node-sass@7.0.0?os=linux&arch=x64
pkg:npm/node-sass@7.0.0?os=win32&arch=x64
```

### 12. Not Signing SBOMs

**Problem:**
- No verification of SBOM authenticity
- Tampering undetectable
- Compliance requirements not met

**Solution:**
- Sign all SBOMs with Cosign or similar
- Use keyless signing for simplicity
- Verify signatures before consumption
- Store signatures with SBOMs

---

## Best Practices Summary

### SBOM Generation

1. **Automate Everything**
   - Generate SBOMs automatically in CI/CD
   - Trigger on dependency changes
   - Integrate with release process

2. **Use Lock Files**
   - Always generate from lock files, not manifests
   - Commit lock files to version control
   - Use `--frozen-lockfile` or equivalent in production

3. **Choose the Right Format**
   - **CycloneDX:** Rich metadata, VEX support, vulnerability data
   - **SPDX:** License compliance, ISO standard, broad tool support
   - Use both if needed for different audiences

4. **Include Complete Metadata**
   - Producer/supplier name
   - Component versions (exact, not ranges)
   - Hashes (SHA-256 minimum)
   - Licenses (SPDX identifiers)
   - Timestamps
   - Tool information
   - Dependency relationships

5. **Generate at Multiple Stages**
   - **Build SBOM:** From lock files during build
   - **Runtime SBOM:** From deployed containers/binaries
   - **Release SBOM:** Signed and distributed with software

### Dependency Management

6. **Capture Transitive Dependencies**
   - Use tools that analyze complete dependency tree
   - Validate against package manager output
   - Include dependency relationships

7. **Handle Production vs Development**
   - Primary SBOM: production dependencies only
   - Supplementary SBOM: complete environment (if needed)
   - Document scope in metadata

8. **Pin Versions for Reproducibility**
   - Use lock files for exact versions
   - Document build environment
   - Verify reproducible builds

### Quality and Validation

9. **Validate SBOMs**
   - Check against official schemas
   - Verify completeness (component count)
   - Cross-reference with multiple tools
   - Compare hashes to lock files

10. **Sign and Attest**
    - Sign all SBOMs with Sigstore/Cosign
    - Create build provenance attestations
    - Store in transparency logs
    - Verify before consumption

11. **Enrich with Vulnerability Data**
    - Scan SBOMs for vulnerabilities
    - Create VEX documents for context
    - Prioritize with CVSS, EPSS, reachability
    - Automate continuous monitoring

### Distribution and Lifecycle

12. **Treat SBOMs as Living Artifacts**
    - Update when dependencies change
    - Regenerate for each release
    - Version SBOMs with software
    - Track changes in version control

13. **Distribute SBOMs**
    - Include in software packages
    - Publish to SBOM registries
    - Share with customers/stakeholders
    - Make accessible via API

14. **Monitor Continuously**
    - Upload to platforms like Dependency-Track
    - Set up vulnerability alerts
    - Review SBOM diffs in PRs
    - Audit regularly

### Tool Selection

15. **Choose Language-Specific Tools**
    - Use native tools when available (npm, Maven plugin)
    - Language-specific tools are more accurate
    - Fall back to multi-language tools for coverage

16. **Use Multiple Tools for Critical Apps**
    - Generate with 2+ tools
    - Compare results
    - Cross-validate component lists

### Compliance and Policy

17. **Establish SBOM Policy**
    - Mandate SBOMs for all projects
    - Define format requirements
    - Specify distribution process
    - Require vendor SBOMs

18. **Educate Teams**
    - Train developers on SBOM importance
    - Provide tooling and documentation
    - Share best practices
    - Celebrate successes

### Common Patterns

**CI/CD Integration Pattern:**
```yaml
1. Checkout code
2. Install dependencies (from lock file)
3. Build software
4. Generate SBOM
5. Validate SBOM
6. Scan for vulnerabilities
7. Sign SBOM
8. Create attestation
9. Upload artifacts
10. Distribute SBOM
```

**Multi-Language Monorepo Pattern:**
```bash
# Generate per-language SBOMs with cdxgen
cdxgen -o sbom-api.json packages/api
cdxgen -o sbom-web.json packages/web

# Generate aggregate SBOM
cdxgen -o sbom-monorepo.json

# Merge SBOMs
cyclonedx merge --input-files sbom-api.json sbom-web.json --output-file sbom-combined.json
```

**Container Pattern:**
```dockerfile
# Multi-stage build
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build

# Generate SBOM from final stage only
FROM node:20-slim
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Install SBOM tool
RUN npm install -g @cyclonedx/cyclonedx-npm

# Generate SBOM
RUN cyclonedx-npm --omit=dev --output-file /sbom.json

# Include SBOM in image
COPY sbom.json /sbom.json
```

---

## Conclusion

SBOM generation is a critical component of modern software supply chain security. By following these best practices, organizations can:

- **Improve Security:** Identify and remediate vulnerabilities faster
- **Ensure Compliance:** Meet regulatory requirements (EU Cyber Resilience Act, US Executive Order 14028)
- **Enable Transparency:** Provide clear inventory of software components
- **Build Trust:** Demonstrate commitment to security through signed, verifiable SBOMs
- **Reduce Risk:** Proactively manage software supply chain risks

### Key Takeaways

1. **Automate SBOM generation** in your CI/CD pipeline
2. **Use lock files** as the source of truth
3. **Choose standardized formats** (SPDX or CycloneDX)
4. **Include complete metadata** (versions, hashes, licenses, relationships)
5. **Sign and attest** SBOMs for trustworthiness
6. **Combine with VEX** for accurate vulnerability assessment
7. **Monitor continuously** for new vulnerabilities
8. **Treat SBOMs as living artifacts** that evolve with your software

### Next Steps

- **Start Small:** Begin with one critical project
- **Pilot Tools:** Test SBOM generators for your ecosystem
- **Establish Policy:** Define SBOM requirements for your organization
- **Educate Teams:** Train developers and security staff
- **Iterate and Improve:** Refine processes based on feedback

### Additional Resources

**Standards:**
- CycloneDX: https://cyclonedx.org/
- SPDX: https://spdx.dev/
- CISA SBOM: https://www.cisa.gov/sbom
- NTIA SBOM: https://www.ntia.gov/page/software-bill-materials

**Tools:**
- cdxgen: https://github.com/CycloneDX/cdxgen
- osv-scanner: https://github.com/google/osv-scanner
- CycloneDX Tools: https://cyclonedx.org/tool-center/
- SPDX Tools: https://github.com/spdx
- Sigstore: https://www.sigstore.dev/

**Frameworks:**
- SLSA: https://slsa.dev/
- in-toto: https://in-toto.io/
- SSDF (NIST): https://csrc.nist.gov/publications/detail/sp/800-218/final

**Vulnerability Management:**
- OWASP Dependency-Track: https://dependencytrack.org/
- NVD: https://nvd.nist.gov/
- OSV: https://osv.dev/

---

## Sources

This document was compiled from authoritative sources including:

- [CISA 2025 Minimum Elements for SBOM](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom)
- [NTIA SBOM Resources](https://www.ntia.gov/page/software-bill-materials)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [SPDX Specification 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/)
- [npm SBOM Documentation](https://docs.npmjs.com/cli/v10/commands/npm-sbom/)
- [Python SBOM Standards](https://peps.python.org/pep-0770/)
- [Maven CycloneDX Plugin](https://github.com/CycloneDX/cyclonedx-maven-plugin)
- [Go SBOM Generation Guide](https://sbomgenerator.com/guides/go)
- [OWASP Dependency-Track](https://dependencytrack.org/)
- [Sigstore Documentation](https://www.sigstore.dev/)
- [SLSA Framework](https://slsa.dev/)
- [Chainguard SBOM Academy](https://edu.chainguard.dev/open-source/sbom/)
- [NVD CVSS Documentation](https://nvd.nist.gov/vuln-metrics/cvss)

---

**Document Version:** 1.0
**Last Updated:** November 22, 2025
**Maintained By:** Security Team
