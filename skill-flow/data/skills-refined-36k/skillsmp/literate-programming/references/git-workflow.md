# Git Workflow for Literate Programming Projects

This reference describes best practices for version control in literate programming projects.

## Table of Contents

1. [Core Rule](#core-rule)
2. [Setting Up .gitignore](#setting-up-gitignore)
3. [Removing Accidentally Tracked Files](#removing-accidentally-tracked-files)
4. [Pre-commit Verification](#pre-commit-verification)
5. [Identifying Generated Files](#identifying-generated-files)
6. [Development Workflow](#development-workflow)

---

## Core Rule

**CRITICAL**: Generated `.py` and `.tex` files from `.nw` sources must NEVER be committed to version control.

The `.nw` file is the single source of truth. Generated files are build artifacts.

---

## Setting Up .gitignore

When starting a literate programming project, create .gitignore patterns for all generated files:

### Example .gitignore

```gitignore
# Generated from literate programming (.nw files)
src/**/*.py
src/**/*.tex

# LaTeX build artifacts
*.aux
*.log
*.out
*.toc
*.pdf

# Test extraction
tests/test_*.py

# Exceptions for hand-written files (if any)
!src/specific_handwritten.py
```

### Pattern for Poetry Projects

```gitignore
# Generated code from .nw files
src/packagename/**/*.py
!src/packagename/__init__.py  # If hand-written

# Generated documentation
src/**/*.tex
doc/*.pdf

# Test files
tests/test_*.py
```

---

## Removing Accidentally Tracked Files

If generated files are already in git:

```bash
# Untrack but keep in working directory
git rm --cached path/to/generated.py
git rm --cached path/to/generated.tex

# Add to .gitignore
echo "path/to/generated.py" >> .gitignore
echo "path/to/generated.tex" >> .gitignore

# Regenerate fresh files from .nw source
make

# Commit the .gitignore changes
git add .gitignore
git commit -m "Remove generated files from version control"
```

### Bulk Removal

For many files:

```bash
# Find and untrack all .py files that have corresponding .nw
for nw in $(find src -name "*.nw"); do
    py="${nw%.nw}.py"
    tex="${nw%.nw}.tex"
    [ -f "$py" ] && git rm --cached "$py" 2>/dev/null
    [ -f "$tex" ] && git rm --cached "$tex" 2>/dev/null
done
```

---

## Pre-commit Verification

Before committing, verify no generated files are staged:

### Manual Check

```bash
# List staged files
git diff --cached --name-only

# Check for .py files in src that might be generated
git diff --cached --name-only | grep 'src/.*\.py$'

# Check for .tex files that might be generated
git diff --cached --name-only | grep '\.tex$'
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for generated files being committed
generated=0

for nw in $(find src -name "*.nw"); do
    base="${nw%.nw}"
    py="$base.py"
    tex="$base.tex"

    if git diff --cached --name-only | grep -q "^$py$"; then
        echo "ERROR: Attempting to commit generated file: $py"
        echo "       Source file: $nw"
        generated=1
    fi

    if git diff --cached --name-only | grep -q "^$tex$"; then
        echo "ERROR: Attempting to commit generated file: $tex"
        echo "       Source file: $nw"
        generated=1
    fi
done

if [ $generated -eq 1 ]; then
    echo ""
    echo "Generated files should not be committed."
    echo "Unstage them with: git reset HEAD <file>"
    exit 1
fi

exit 0
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

## Identifying Generated Files

### A File Is GENERATED (Do NOT Commit) If:

- A corresponding `.nw` file exists with the same base name
- The file is listed as a target in a Makefile that uses notangle/noweave
- The file contains patterns typical of noweb output (e.g., line number comments)

### A File Is HAND-WRITTEN (OK to Commit) If:

- No `.nw` source file exists
- It's explicitly marked as an exception in .gitignore
- It's a special file like `__init__.py` that's not generated from `.nw`
- It's in a non-literate part of the project

### Quick Test

```bash
# Is module.py generated?
ls module.nw 2>/dev/null && echo "GENERATED - do not commit" || echo "Hand-written - OK to commit"
```

---

## Development Workflow

### Standard Workflow

1. **Edit the `.nw` file** (the source of truth)
2. **Regenerate code**: `make` in the directory
3. **Run tests**: `make test` or `pytest`
4. **Stage only `.nw` files**: `git add *.nw`
5. **Commit**: `git commit -m "Description of changes"`

### After Checkout/Pull

Always regenerate after getting new `.nw` files:

```bash
git pull
make clean
make all
```

### Viewing Changes

To see what changed in the actual code:

```bash
# Regenerate to see current state
make

# Compare generated code to what's in git (if accidentally tracked)
git diff path/to/generated.py

# Better: look at .nw diff
git diff path/to/source.nw
```

### Debugging Generated Code

When debugging issues in generated code:

1. **Find the source**: `module.py` → `module.nw`
2. **Fix in `.nw` file** (NOT the generated file)
3. **Regenerate**: `make`
4. **Test**: `pytest`
5. **Commit**: only the `.nw` file

---

## Integration with Development Tools

### Version Control

- **CRITICAL**: Only commit `.nw` files
- Add generated files to `.gitignore` immediately
- Regenerate code with `make` after checkout/pull

### IDEs

- Configure to run notangle on save
- Set up file watchers for `.nw` files
- Point IDE to generated files for syntax highlighting

### CI/CD

Add tangle step before build/test:

```yaml
# GitHub Actions example
jobs:
  build:
    steps:
      - uses: actions/checkout@v3
      - name: Install noweb
        run: sudo apt-get install -y noweb
      - name: Generate code
        run: make all
      - name: Run tests
        run: make test
```

### Code Review

Review `.nw` files for both:
- **Code quality**: Does the implementation work?
- **Explanation quality**: Is the documentation clear?

Generated files should never appear in pull requests.
