# Mutation Testing Tools by Language

## TypeScript / JavaScript

### Stryker (Recommended)

**Installation:**
```bash
npm install --save-dev @stryker-mutator/core
npx stryker init
```

**Configuration (stryker.config.json):**
```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "mutate": [
    "src/**/*.ts",
    "!src/**/*.test.ts",
    "!src/**/*.spec.ts"
  ],
  "testRunner": "vitest",
  "reporters": ["progress", "clear-text", "html"],
  "coverageAnalysis": "perTest",
  "timeoutMS": 10000,
  "concurrency": 4
}
```

**For different test runners:**
```bash
# Vitest
npm install --save-dev @stryker-mutator/vitest-runner

# Jest
npm install --save-dev @stryker-mutator/jest-runner

# Mocha
npm install --save-dev @stryker-mutator/mocha-runner
```

**Run:**
```bash
npx stryker run

# Run on specific files
npx stryker run --mutate "src/lib/auth/**/*.ts"

# Incremental (faster)
npx stryker run --incremental
```

**Output:**
```
Mutation testing  [====================] 100% (elapsed: 1m, remaining: n/a)
#1. [Killed] ArithmeticOperator
#2. [Killed] ConditionalExpression
#3. [Survived] BooleanLiteral
...

Mutation score: 87.5% (21/24)
```

---

## Python

### mutmut (Recommended)

**Installation:**
```bash
pip install mutmut
```

**Configuration (setup.cfg):**
```ini
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=pytest
```

**Run:**
```bash
# Full run
mutmut run

# Show results
mutmut results

# Show specific survivor
mutmut show 3

# Apply mutation (for debugging)
mutmut apply 3
```

**Output:**
```
Running mutmut...
⠋ 24/24  🎉 21  ⏰ 0  🤔 0  🙁 3

Survivors:
  src/auth/validate.py:45 - changed >= to >
  src/auth/validate.py:67 - changed 'guest' to 'admin'
  src/auth/validate.py:89 - changed >= to >
```

### Cosmic Ray (Alternative)

```bash
pip install cosmic-ray

# Initialize
cosmic-ray init config.toml

# Run
cosmic-ray exec config.toml
cosmic-ray report config.toml
```

---

## Go

### go-mutesting

**Installation:**
```bash
go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest
```

**Run:**
```bash
go-mutesting ./...

# Specific package
go-mutesting ./pkg/auth/...

# With verbose output
go-mutesting --verbose ./...
```

### gremlins (Alternative)

```bash
go install github.com/go-gremlins/gremlins/cmd/gremlins@latest

gremlins unleash ./...
```

---

## Rust

### cargo-mutants (Recommended)

**Installation:**
```bash
cargo install cargo-mutants
```

**Run:**
```bash
cargo mutants

# Specific files
cargo mutants -- --package mypackage

# Skip slow tests
cargo mutants --timeout 30
```

**Configuration (Cargo.toml):**
```toml
[package.metadata.cargo-mutants]
exclude = ["tests/", "benches/"]
timeout = 60
```

### mutagen (Alternative)

```bash
cargo install mutagen

# Requires annotation
#[mutagen::mutate]
fn my_function() { ... }
```

---

## Java

### PIT (PITest)

**Maven:**
```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.15.0</version>
  <configuration>
    <targetClasses>
      <param>com.example.*</param>
    </targetClasses>
    <targetTests>
      <param>com.example.*Test</param>
    </targetTests>
  </configuration>
</plugin>
```

**Run:**
```bash
mvn org.pitest:pitest-maven:mutationCoverage
```

**Gradle:**
```gradle
plugins {
    id 'info.solidsoft.pitest' version '1.15.0'
}

pitest {
    targetClasses = ['com.example.*']
    targetTests = ['com.example.*Test']
    threads = 4
}
```

```bash
gradle pitest
```

---

## C# / .NET

### Stryker.NET

**Installation:**
```bash
dotnet tool install --global dotnet-stryker
```

**Run:**
```bash
dotnet stryker

# With options
dotnet stryker --project MyProject.csproj --reporters "html,progress"
```

**Configuration (stryker-config.json):**
```json
{
  "stryker-config": {
    "project": "MyProject.csproj",
    "reporters": ["html", "progress"],
    "mutate": ["**/*.cs", "!**/*Test.cs"]
  }
}
```

---

## Integration with autonomous-dev

### Auto-detection

The mutation tester skill auto-detects the tool based on project profile:

```yaml
# .claude/project-profile.yaml
stack:
  language: "typescript/javascript"
```

Maps to:
- `typescript/javascript` → Stryker
- `python` → mutmut
- `go` → go-mutesting
- `rust` → cargo-mutants
- `java` → PIT

### Installation Check

Before running, verify tool is installed:

```bash
# TypeScript
npx stryker --version

# Python
mutmut version

# Go
go-mutesting --version

# Rust
cargo mutants --version
```

If not installed, suggest installation command.

---

## Performance Tips

### 1. Incremental Testing
Only test changed files, not the entire codebase.

### 2. Parallel Execution
All tools support parallel execution:
- Stryker: `concurrency: 4`
- mutmut: `--parallel`
- go-mutesting: `--parallel 4`

### 3. Timeout Configuration
Set reasonable timeouts to skip slow tests:
- Stryker: `timeoutMS: 10000`
- mutmut: `--test-time-base 5.0`

### 4. Focused Mutation
Only mutate critical paths:
```bash
# Stryker
npx stryker run --mutate "src/lib/auth/**/*.ts"

# mutmut
mutmut run --paths-to-mutate=src/auth/
```
