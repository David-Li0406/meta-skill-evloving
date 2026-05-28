# Build and Dependency Management

## Use Appropriate Tools

Select build and dependency management tools based on your language:

### C/C++

**CMake** (Cross-platform builds):
```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject VERSION 1.0.0)

# C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Dependencies
find_package(Boost 1.75 REQUIRED COMPONENTS system filesystem)

# Executable
add_executable(myapp
    src/main.cpp
    src/module.cpp
)

target_link_libraries(myapp PRIVATE
    Boost::system
    Boost::filesystem
)

# Install rules
install(TARGETS myapp DESTINATION bin)
```

**vcpkg** (Package management):
```bash
# Install dependencies
vcpkg install boost fmt spdlog

# Use in CMakeLists.txt
find_package(fmt CONFIG REQUIRED)
target_link_libraries(myapp PRIVATE fmt::fmt)
```

**Conan** (Alternative package manager):
```ini
# conanfile.txt
[requires]
boost/1.79.0
fmt/9.0.0

[generators]
CMakeDeps
CMakeToolchain
```

### Kotlin/Java

**Gradle**:
```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "1.9.0"
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    implementation("io.ktor:ktor-server-core:2.3.4")

    testImplementation(kotlin("test"))
    testImplementation("io.mockk:mockk:1.13.7")
}

tasks.test {
    useJUnitPlatform()
}
```

**Maven**:
```xml
<!-- pom.xml -->
<project>
    <dependencies>
        <dependency>
            <groupId>org.jetbrains.kotlinx</groupId>
            <artifactId>kotlinx-coroutines-core</artifactId>
            <version>1.7.3</version>
        </dependency>
    </dependencies>
</project>
```

### TypeScript/JavaScript

**npm**:
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/**/*.ts"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.17",
    "typescript": "^5.1.6",
    "jest": "^29.6.2"
  }
}
```

**yarn**:
```bash
# Install dependencies
yarn add express
yarn add --dev typescript @types/express

# Scripts
yarn build
yarn test
```

### Python

**Poetry** (Recommended):
```toml
# pyproject.toml
[tool.poetry]
name = "my-project"
version = "1.0.0"
description = "Project description"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.103.0"
sqlalchemy = "^2.0.20"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
mypy = "^1.5.0"
```

```bash
# Commands
poetry install          # Install dependencies
poetry add requests     # Add new dependency
poetry run pytest       # Run tests
```

**pip + requirements.txt**:
```txt
# requirements.txt
fastapi==0.103.0
sqlalchemy==2.0.20
pydantic==2.3.0

# requirements-dev.txt
pytest==7.4.0
black==23.7.0
mypy==1.5.0
```

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Separate Environments

### Development vs Production

**Key differences**:

| Aspect | Development | Production |
|--------|-------------|------------|
| Debug symbols | Included | Stripped |
| Optimizations | Minimal (-O0/-O1) | Maximum (-O3) |
| Assertions | Enabled | Disabled |
| Logging | Verbose | Essential only |
| Dependencies | Include dev tools | Runtime only |

### C++ Build Types

```cmake
# CMakeLists.txt
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_compile_definitions(DEBUG_BUILD)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0")
elseif(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_definitions(NDEBUG)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -DNDEBUG")
endif()
```

```bash
# Build commands
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake -B build -DCMAKE_BUILD_TYPE=Release
```

### Python Virtual Environments

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate
deactivate
```

### Node.js Environments

```json
{
  "scripts": {
    "dev": "NODE_ENV=development nodemon src/index.ts",
    "build": "NODE_ENV=production tsc",
    "start": "NODE_ENV=production node dist/index.js"
  }
}
```

## Pin Dependency Versions

### Why Pin Versions?

- **Reproducibility**: Same build results across machines and time
- **Stability**: Avoid breaking changes from automatic updates
- **Security**: Control when to adopt updates with known vulnerabilities

### Version Pinning Strategies

**Exact version** (most strict):
```json
"dependencies": {
  "express": "4.18.2"
}
```

**Minor version range** (recommended):
```json
"dependencies": {
  "express": "~4.18.2"  // npm: 4.18.x only
}
```

**Major version range**:
```json
"dependencies": {
  "express": "^4.18.2"  // npm: 4.x.x
}
```

### Lock Files

Always commit lock files to version control:

- **npm**: `package-lock.json`
- **yarn**: `yarn.lock`
- **pip**: `requirements.txt` (with exact versions) or `poetry.lock`
- **Gradle**: `gradle.lockfile`
- **Go**: `go.sum`

### Example: Python with Poetry

```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.103.0"  # Allows minor/patch updates

# For production-critical dependencies, use exact versions
sqlalchemy = "2.0.20"  # Exact version
```

```bash
# Generate lock file
poetry lock

# Install from lock file
poetry install --no-update
```

## Build Reproducibility

### Dockerfile Example

```dockerfile
# Pin base image version
FROM python:3.11.5-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install exact versions from lock file
RUN pip install poetry==1.6.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction

# Copy application
COPY . .

CMD ["python", "main.py"]
```

### CI/CD Configuration

```yaml
# .github/workflows/build.yml
name: Build

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-22.04  # Pin OS version

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11.5'  # Pin Python version

      - name: Install dependencies
        run: |
          pip install poetry==1.6.1
          poetry install --no-interaction

      - name: Build
        run: poetry run build

      - name: Test
        run: poetry run pytest
```

## Dependency Updates

### Regular Update Strategy

1. **Monitor for updates**: Use tools like Dependabot, Renovate
2. **Review changelogs**: Understand what changed
3. **Test thoroughly**: Run full test suite after updates
4. **Update incrementally**: One or few dependencies at a time
5. **Document breaking changes**: Note required code changes

### Automated Dependency Updates

**Dependabot** (GitHub):
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

**Renovate**:
```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "updateTypes": ["minor", "patch"],
      "automerge": true
    }
  ]
}
```

## Build Optimization

### Incremental Builds

**CMake**:
```cmake
# Use ccache for faster rebuilds
find_program(CCACHE_FOUND ccache)
if(CCACHE_FOUND)
    set(CMAKE_CXX_COMPILER_LAUNCHER ccache)
endif()
```

**Gradle**:
```kotlin
// Enable build cache
org.gradle.caching=true

// Parallel builds
org.gradle.parallel=true
```

### Dependency Caching

**CI/CD Cache Example**:
```yaml
# GitHub Actions
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pip
      ~/.cache/vcpkg
    key: ${{ runner.os }}-deps-${{ hashFiles('**/requirements.txt') }}
```
