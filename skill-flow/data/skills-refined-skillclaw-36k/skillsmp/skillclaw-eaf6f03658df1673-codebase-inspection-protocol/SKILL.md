---
name: codebase-inspection-protocol
description: Use this skill when you need to inspect a Rails codebase structure before writing any code, ensuring you understand existing patterns, conventions, dependencies, and file organization.
---

# Codebase Inspection Protocol Skill

This skill provides mandatory inspection procedures that MUST be followed before any code generation or architectural decisions in a Rails project.

## When to Use This Skill

- **ALWAYS** before writing any new code
- Before making architectural decisions
- Before suggesting any pattern
- When assumptions are made about existing code
- Before creating any new file

## Core Rule

> **"Inspect before you suggest"**
>
> No planning decisions without codebase inspection. Every recommendation must cite observed file paths. Never assume a pattern exists—verify it first.

## Mandatory Inspection Checks

### 1. Project Structure

```bash
# Primary structure check
tree app -L 2 -I 'assets|javascript' 2>/dev/null || find app -type d -maxdepth 2

# List all app directories
ls -la app/*/ 2>/dev/null

# Count Ruby files
find app -type f -name '*.rb' | wc -l
```

**Answers**: What is the current project structure?

### 2. Existing Patterns

```bash
# Check for services directory
ls app/services/ 2>/dev/null || echo 'No services directory'

# Check for service subdirectories (namespace pattern)
ls app/services/*/ 2>/dev/null || echo 'No service subdirectories'

# Find service classes
grep -r 'class.*Service' app/ --include='*.rb' -l 2>/dev/null | head -10

# Find command classes
grep -r 'class.*Command' app/ --include='*.rb' -l 2>/dev/null | head -5

# Find query objects
grep -r 'class.*Query' app/ --include='*.rb' -l 2>/dev/null | head -5
```

**Answers**: What patterns are already in use?

### 3. Naming Conventions

```bash
# Sample a service file
head -30 $(find app/services -name '*.rb' 2>/dev/null | head -1) 2>/dev/null || echo 'No service files'

# Sample a model file
head -30 $(find app/models -name '*.rb' 2>/dev/null | head -1) 2>/dev/null

# List module/class definitions in services
grep -r 'module\|class' app/services/ --include='*.rb' 2>/dev/null | head -20
```

**Answers**: What naming and style conventions exist?

### 4. Dependencies

```bash
# Check Gemfile
cat Gemfile 2>/dev/null | grep -v '^#' | grep -v '^$' | head -60

# Check Ruby version
cat Gemfile.lock 2>/dev/null | grep -A1 'RUBY VERSION' || ru
```

**Answers**: What dependencies are in use?