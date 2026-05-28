# Navigation in Monorepos

Strategies for efficiently navigating large monorepo codebases with Claude Code.

## Understanding Monorepo Structure

### Step 1: Identify the Layout

```bash
# Check root structure
ls -la

# Common structures
ls packages/ apps/ libs/ modules/ services/ 2>/dev/null

# Check workspace configuration
cat package.json | grep -A10 "workspaces"
```

### Common Layouts Reference

| Layout | Structure | Use Case |
|--------|-----------|----------|
| Packages | `packages/*` | Libraries and shared code |
| Apps + Packages | `apps/` + `packages/` | Apps with shared libraries |
| Domain | `domains/*/` | Domain-driven design |
| Service | `services/*/` | Microservices |

## Package Discovery

### Finding All Packages

```bash
# List workspace packages
cat package.json | grep -A20 "workspaces"

# Find all package.json files
find . -name "package.json" -not -path "*/node_modules/*" | head -30

# List packages with their names
for pkg in packages/*/package.json; do
  echo "$(dirname $pkg): $(cat $pkg | grep '"name"' | head -1)"
done
```

### Finding a Specific Package

```bash
# By package name
rg -l '"name".*"@org/package-name"' --type json

# By exported function
rg -l "export.*functionName" --type ts

# By file content
rg -l "UniqueIdentifier" packages/
```

### Understanding Package Purpose

```bash
# Read package.json for description
cat packages/target/package.json | grep -A2 '"description"'

# Check main entry point
cat packages/target/package.json | grep '"main"'

# List exports
cat packages/target/package.json | grep -A20 '"exports"'

# Read README if available
cat packages/target/README.md 2>/dev/null | head -50
```

## Dependency Mapping

### Internal Dependencies

```bash
# Find what a package depends on (internal)
cat packages/target/package.json | grep "@org/"

# Find what depends on a package
rg '"@org/target"' packages/*/package.json

# Build complete dependency tree
turbo run build --dry-run --graph 2>&1 | head -50
```

### Dependency Order Visualization

```
Level 0 (No deps):     shared-types
                           |
Level 1:          utils    schemas
                    \       /
Level 2:             core-lib
                    /   |   \
Level 3:        api    web    cli
```

### Finding Circular Dependencies

```bash
# Check for circular imports
npx madge --circular packages/*/src/index.ts

# Nx provides this
nx graph --affected
```

## Context Scoping Strategies

### Strategy 1: Single Package Focus

When working on a specific feature in one package:

```bash
# Scope to single package
SCOPE="packages/target"

# Read only relevant files
cat $SCOPE/package.json
ls $SCOPE/src/
cat $SCOPE/src/index.ts
```

### Strategy 2: Vertical Slice

When a feature spans multiple packages:

```bash
# Identify the slice
rg -l "featureName" packages/*/src/

# Read each affected file
cat packages/types/src/feature.ts
cat packages/core/src/feature.ts
cat packages/api/src/routes/feature.ts
```

### Strategy 3: Dependency Chain

When modifying shared code:

```bash
# Find what you're modifying
rg -l "SharedComponent" packages/

# Find all consumers
rg '"@org/shared"' packages/*/package.json

# Read the chain
cat packages/shared/src/component.ts
cat packages/consumer/src/usage.ts
```

## Efficient File Discovery

### Finding Entry Points

```bash
# Package entry points
cat packages/*/src/index.ts 2>/dev/null | head -100

# Route definitions
rg -l "router\." apps/api/src/routes/

# Component exports
rg "export.*from" packages/ui/src/index.ts
```

### Finding Tests

```bash
# Find tests for a module
rg -l "describe.*ModuleName" packages/

# Find test file for source
ls packages/core/src/module.test.ts
ls packages/core/tests/module.test.ts

# Find all test files
find packages/ -name "*.test.ts" -o -name "*.spec.ts" | head -20
```

### Finding Configuration

```bash
# Package configs
cat packages/target/tsconfig.json
cat packages/target/.eslintrc.json 2>/dev/null

# Root configs that apply
cat tsconfig.base.json
cat .eslintrc.json
```

## Search Patterns

### Searching Within Package Boundary

```bash
# Search in single package
rg "pattern" packages/target/

# Search in multiple specific packages
rg "pattern" packages/core/ packages/utils/

# Exclude test files
rg "pattern" packages/target/src/ --glob '!*.test.ts'
```

### Finding Cross-Package References

```bash
# Find all imports of a package
rg "from '@org/target'" packages/

# Find all usages of an export
rg "import.*{ TargetExport }" packages/

# Find re-exports
rg "export.*from '@org/target'" packages/
```

### Finding Type Definitions

```bash
# Find interface definition
rg "interface TargetInterface" packages/ --type ts

# Find type usage
rg ": TargetType" packages/ --type ts

# Find generic usage
rg "TargetType<" packages/ --type ts
```

## Navigation Workflow

### Starting a New Task

1. **Understand the request** - What feature/file needs modification?

2. **Find the relevant package**
   ```bash
   rg -l "relevantCode" packages/
   ```

3. **Read package context**
   ```bash
   cat packages/found/package.json
   cat packages/found/src/index.ts
   ```

4. **Map dependencies**
   ```bash
   cat packages/found/package.json | grep "@org/"
   ```

5. **Scope your reading** - Only read files within this package and its direct dependencies

### Exploring Unknown Codebase

```bash
# Step 1: Understand structure
ls -la && cat package.json | head -30

# Step 2: List all packages
ls packages/ apps/ 2>/dev/null

# Step 3: Check for documentation
cat README.md | head -50
cat ARCHITECTURE.md 2>/dev/null | head -50

# Step 4: Read workspace config
cat turbo.json nx.json lerna.json pnpm-workspace.yaml 2>/dev/null

# Step 5: Identify entry points
ls apps/*/src/main.ts apps/*/src/index.ts 2>/dev/null
```

## IDE-Like Navigation

### Go to Definition Equivalent

```bash
# Find where something is defined
rg "export (const|function|class|interface) TargetName" packages/ --type ts

# Find the source file
rg -l "export.*TargetName" packages/*/src/
```

### Find All References

```bash
# All usages of a symbol
rg "TargetName" packages/ --type ts

# Only imports
rg "import.*TargetName" packages/ --type ts

# Only usages (exclude imports/exports)
rg "TargetName" packages/ --type ts | grep -v "import\|export"
```

### Find Implementations

```bash
# Find class implementing interface
rg "implements TargetInterface" packages/ --type ts

# Find function implementing type
rg ": TargetType.*=>" packages/ --type ts
```

## Performance Tips

### Limit Search Scope

```bash
# Good: Scoped search
rg "pattern" packages/target/src/

# Avoid: Unscoped search
rg "pattern"  # Searches everything
```

### Use Type Filters

```bash
# Only TypeScript
rg "pattern" --type ts

# Only JSON configs
rg "pattern" --type json

# Exclude patterns
rg "pattern" --glob '!*.test.ts' --glob '!*.spec.ts'
```

### Cache Discovery Results

When working on a task, note down:
- Package locations
- Key file paths
- Dependency relationships

This avoids re-searching during the session.

## Common Navigation Scenarios

### Scenario: Find Where API Endpoint is Defined

```bash
# Find route definition
rg "router\.(get|post|put|delete).*'/api/target'" apps/api/

# Or with path pattern
rg "/target" apps/api/src/routes/ --type ts
```

### Scenario: Find Component Usage

```bash
# Find where component is used
rg "<TargetComponent" packages/ --type tsx

# Find import statements
rg "import.*TargetComponent" packages/
```

### Scenario: Trace Data Flow

```bash
# Find type definition
rg "interface UserData" packages/types/

# Find where it's created
rg "UserData.*=" packages/

# Find where it's consumed
rg ": UserData" packages/
```

## Troubleshooting Navigation

### Issue: Can't Find File

```bash
# Check if file exists
find . -name "target.ts" -not -path "*/node_modules/*"

# Check for different extensions
find . -name "target.*" -not -path "*/node_modules/*"

# Check for case sensitivity
find . -iname "target.ts" -not -path "*/node_modules/*"
```

### Issue: Too Many Results

```bash
# Add more specificity
rg "exact phrase" packages/

# Limit to specific package
rg "pattern" packages/specific/

# Exclude generated files
rg "pattern" --glob '!*.generated.ts' --glob '!dist/'
```

### Issue: Missing Context

```bash
# Get more lines of context
rg "pattern" -C 5 packages/

# Read the whole file section
rg "pattern" -B 10 -A 20 packages/target/src/file.ts
```
