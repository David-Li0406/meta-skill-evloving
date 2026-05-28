# Overview Exploration Templates

## Output Template

Use this format for exploration results:

```markdown
## Overview Exploration Results

**Project Type**: {Next.js / Express / Go CLI / Python Library / etc.}

**Tech Stack**:
- Language: {TypeScript / Go / Python / etc.}
- Framework: {Next.js / Express / Gin / etc.}
- Database: {PostgreSQL / MongoDB / etc.} (if any)
- Test: {Jest / pytest / go test / etc.}

**Directory Structure**:
```
project/
├── src/           # {description}
├── app/           # {description}
├── lib/           # {description}
└── tests/         # {description}
```

**Key Entry Points**:
- {main entry file}
- {api routes if any}

**Existing Patterns**:
- {auth: implemented/not found}
- {database: prisma/typeorm/raw sql/not found}
- {api: rest/graphql/trpc/not found}

**Relevant Files** (based on Goal):
- {file1}: {reason}
- {file2}: {reason}
```

---

## Framework Detection Commands

### Node.js / JavaScript / TypeScript

```python
# Detect Node.js project
Glob(pattern="package.json")
Read(file_path="package.json")

# Check for frameworks
Grep(pattern="next|express|fastify|nestjs", path="package.json")

# Find entry points
Glob(pattern="src/index.{ts,js}")
Glob(pattern="app/**/*.{ts,tsx}")
```

### Go

```python
# Detect Go project
Glob(pattern="go.mod")
Read(file_path="go.mod")

# Find main packages
Glob(pattern="cmd/**/*.go")
Glob(pattern="main.go")

# Check for frameworks
Grep(pattern="gin|echo|fiber|chi", path="go.mod")
```

### Python

```python
# Detect Python project
Glob(pattern="requirements.txt")
Glob(pattern="pyproject.toml")
Glob(pattern="setup.py")

# Check for frameworks
Grep(pattern="django|flask|fastapi", path="requirements.txt")

# Find entry points
Glob(pattern="manage.py")      # Django
Glob(pattern="app.py")         # Flask
Glob(pattern="main.py")        # FastAPI
```

### Rust

```python
# Detect Rust project
Glob(pattern="Cargo.toml")
Read(file_path="Cargo.toml")

# Find main entry
Glob(pattern="src/main.rs")
Glob(pattern="src/lib.rs")
```

### Java / Kotlin

```python
# Maven
Glob(pattern="pom.xml")

# Gradle
Glob(pattern="build.gradle")
Glob(pattern="build.gradle.kts")

# Find entry points
Grep(pattern="@SpringBootApplication|main\(", type="java")
```

---

## Directory Structure Exploration

### Generic approach

```python
# Top-level structure
Glob(pattern="*", path=".")

# Main source directories (try common patterns)
Glob(pattern="src/*")
Glob(pattern="app/*")
Glob(pattern="lib/*")
Glob(pattern="internal/*")
Glob(pattern="cmd/*")
Glob(pattern="pkg/*")
```

### Config file discovery

```python
# Config files
Glob(pattern="**/*.config.*")
Glob(pattern="**/.*rc")
Glob(pattern="**/*.json", path=".")
Glob(pattern="**/*.yaml")
Glob(pattern="**/*.toml")
```

### Test structure discovery

```python
# Test files
Glob(pattern="**/*_test.*")
Glob(pattern="**/*.test.*")
Glob(pattern="**/*.spec.*")
Glob(pattern="**/test/**/*")
Glob(pattern="**/__tests__/**/*")
```

---

## Session Integration Commands

### Update exploration stage

```bash
bun "${CLAUDE_PLUGIN_ROOT}/src/scripts/session-update.js" \
  --session ${CLAUDE_SESSION_ID} \
  --exploration-stage overview
```

### Save overview.md

```bash
# Get session directory
SESSION_DIR=~/.claude/ultrawork/sessions/${CLAUDE_SESSION_ID}

# Write overview.md
Write(
  file_path="$SESSION_DIR/exploration/overview.md",
  content="{exploration results in above format}"
)
```

### Add to context.json

```bash
bun "${CLAUDE_PLUGIN_ROOT}/src/scripts/context-add.js" \
  --session ${CLAUDE_SESSION_ID} \
  --explorer-id "overview" \
  --file "exploration/overview.md" \
  --summary "{brief summary of overview findings}" \
  --key-files "{comma-separated key files}" \
  --patterns "{comma-separated patterns found}"
```

### Advance to analyzing stage

```bash
bun "${CLAUDE_PLUGIN_ROOT}/src/scripts/session-update.js" \
  --session ${CLAUDE_SESSION_ID} \
  --exploration-stage analyzing
```
