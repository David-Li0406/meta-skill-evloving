# Multi-Directory Literate Programming Projects

This reference document provides detailed patterns and examples for organizing large-scale literate programming projects across multiple directories.

## Table of Contents

1. [Repository Structure Patterns](#repository-structure-patterns)
2. [Hierarchical Build Systems](#hierarchical-build-systems)
3. [Documentation Composition](#documentation-composition)
4. [Test Organization](#test-organization)
5. [Navigation Strategies](#navigation-strategies)
6. [Complete Example: The nytid Repository](#complete-example-the-nytid-repository)

---

## Repository Structure Patterns

### The Three-Directory Separation Pattern

For large projects, separate literate sources, documentation builds, and tests into distinct directories:

```
project/
├── src/              # Literate source files (.nw)
│   └── package/
│       ├── module1.nw
│       ├── module2.nw
│       └── subpackage/
│           └── module3.nw
├── doc/              # Documentation build directory
│   ├── Makefile
│   ├── main.tex      # Master document
│   └── main.pdf      # Generated documentation
├── tests/            # Extracted test files
│   ├── Makefile
│   ├── test_module1.py (generated)
│   └── test_module2.py (generated)
└── makefiles/        # Shared build infrastructure
    ├── noweb.mk
    └── subdir.mk
```

### When to Use This Pattern

**Use three-directory separation when:**
- Project has 5+ .nw files
- Multiple developers need clear separation of concerns
- Documentation needs different organization than code
- Tests should be cleanly separated for CI/CD

**Use flat structure when:**
- Single-file or small projects (1-3 .nw files)
- Documentation and code naturally align
- Simpler is better for the use case

### Key Insight

The .nw files in `/src` are the single source of truth. They generate:
- **Code** → tangled back into `/src` alongside the .nw files
- **Documentation** → woven to .tex in `/src`, then included in `/doc` master document
- **Tests** → extracted to `/tests` directory

---

## Hierarchical Build Systems

### The noweb.mk + subdir.mk Pattern

For projects with nested directories, use reusable Makefiles:

**Directory structure:**
```
src/package/
├── Makefile          # This directory's build rules
├── module1.nw
├── module2.nw
└── subpackage/
    ├── Makefile      # Subdirectory's build rules
    └── module3.nw
```

**Parent Makefile** (`src/package/Makefile`):
```makefile
# Declare what to build in this directory
MODULES+=   module1.py
MODULES+=   module2.py

# Declare subdirectories to recurse into
SUBDIR+=    subpackage

# Targets that should propagate to subdirectories
SUBDIR_GOALS=   all clean distclean

# Build everything in this directory
.PHONY: all
all: ${MODULES}

# Include shared build rules
INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/subdir.mk
```

**Child Makefile** (`src/package/subpackage/Makefile`):
```makefile
MODULES+=   module3.py

.PHONY: all
all: ${MODULES}

# Point to parent's makefiles directory (one level deeper)
INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/subdir.mk
```

### The noweb.mk Build Rules

The `noweb.mk` file provides suffix rules for tangling and weaving:

```makefile
# Weaving: .nw → .tex
NOWEAVE.tex?= noweave ${NOWEAVEFLAGS.tex} $< > $@
NOWEAVEFLAGS.tex?= ${NOWEAVEFLAGS} -x -n -delay -t2

.SUFFIXES: .nw .tex
.nw.tex:
    ${NOWEAVE.tex}

# Tangling: .nw → .py
NOTANGLE.py?= notangle ${NOTANGLEFLAGS.py} -R$(notdir $@) \
              $(filter %.nw,$^) > $@ && noroots $(filter %.nw,$^)
NOTANGLE.py+= && ${NOWEB_PYCODEFMT}
NOWEB_PYCODEFMT?= black $@

.SUFFIXES: .nw .py
.nw.py:
    ${NOTANGLE.py}
```

### The subdir.mk Recursion Rules

The `subdir.mk` file enables recursive builds:

```makefile
# Default goals to propagate to subdirectories
SUBDIR_GOALS?=${MAKECMDGOALS}

# For each subdirectory, call make with the current goals
${SUBDIR}::
    ${MAKE} -C $@ ${actual_goals}

# Make subdirectories dependencies of the goals
${actual_goals}: ${SUBDIR}
```

### Special Pattern: Python __init__.py

Python modules need `__init__.py`, but noweb tangles to the chunk name. Use this pattern:

```makefile
# Declare init.py as intermediate (won't be kept)
.INTERMEDIATE: init.py

# Tangle init.nw to init.py, then rename to __init__.py
__init__.py: init.py
    ${MV} $< $@

# Standard tangling rule still applies for init.nw → init.py
```

### Self-Documenting Build Systems

The build system itself can be literate! Store Makefiles as `.mk.nw`:

```
makefiles/
├── Makefile          # Builds the .mk files
├── noweb.mk.nw       # Literate build rules
├── noweb.mk          # Generated
├── subdir.mk.nw      # Literate recursion rules
├── subdir.mk         # Generated
└── makefiles.pdf     # Documentation of build system
```

---

## Documentation Composition

### Master Document Pattern

Create a master document in `/doc` that includes generated .tex from `/src`:

**Directory structure:**
```
project/
├── src/package/
│   ├── module1.nw → module1.py + module1.tex
│   ├── module2.nw → module2.py + module2.tex
│   └── subpackage/
│       └── module3.nw → module3.py + module3.tex
└── doc/
    ├── Makefile
    ├── main.tex       # Master document (source, committed to git)
    ├── preamble.tex   # Shared LaTeX preamble (source, committed to git)
    └── main.pdf       # Generated (gitignored)
```

**Key principle**: `main.tex` and `preamble.tex` are **source files** committed to git.
They are NOT generated from .nw files. Only the woven .tex files in `/src` are generated.

### The Separate Preamble Pattern

**ALWAYS use a separate preamble.tex** that the main document inputs via `\input{preamble}`.
This standard preamble is used consistently across all literate programming projects.

Copy the preamble from the `literate-programming` skill's `references/preamble.tex` file.

**Master document** (`doc/main.tex`):
```latex
\documentclass[a4paper,oneside]{memoir}
\input{preamble}

\usepackage{noweb}
\noweboptions{shift,breakcode,longxref,longchunks}

\title{Project Name}
\author{Author Name}
\date{\today}

\begin{document}
\frontmatter
\maketitle

\begin{abstract}
Brief description of the project.
\end{abstract}

\tableofcontents

\mainmatter

\part{Core Modules}
\input{../src/package/module1.tex}
\input{../src/package/module2.tex}

\part{Extensions}
\input{../src/package/subpackage/module3.tex}

\backmatter
\end{document}
```

### .nw Files as Chapters

Each .nw file should be structured as a **chapter** (not a complete document):

```noweb
\chapter{Module Name}
\label{module-name}

\section{Introduction}
...
```

**Key points:**
- Start with `\chapter{...}` and `\label{...}`
- NO `\documentclass`, `\begin{document}`, `\end{document}`
- NO `\input{preamble}` or `\maketitle`
- The main document provides the document wrapper

### Build Dependencies

The `/doc/Makefile` must declare dependencies on generated .tex files:

```makefile
# Main target
all: main.pdf

# PDF depends on all .tex files from src
main.pdf: ../src/package/module1.tex
main.pdf: ../src/package/module2.tex
main.pdf: ../src/package/subpackage/module3.tex

# Pattern rule: if .tex doesn't exist, make it in src
../src/%::
    ${MAKE} -C $(dir $@) $(notdir $@)

# Compile with LaTeX
main.pdf: main.tex preamble.tex
    latexmk -xelatex -shell-escape main.tex
```

### How It Works

1. `make all` in `/doc` requires `main.pdf`
2. `main.pdf` depends on .tex files from `/src`
3. Those .tex files don't exist yet
4. Pattern rule invokes `make` in the appropriate `/src` subdirectories
5. Subdirectory Makefiles weave .nw → .tex using noweb.mk rules
6. Once all .tex files exist, latexmk compiles the master document

### Benefits

- **Narrative control**: Organize documentation pedagogically, not by implementation order
- **Modular content**: Each .nw contributes a chapter/section
- **Automatic dependencies**: Make tracks .tex changes and rebuilds as needed
- **Separation of concerns**: Code structure vs. documentation structure

---

## Test Organization

### Test Extraction Pattern

Tests are defined IN the .nw files alongside implementation, but extracted to a separate `/tests` directory.

### Chunk Naming Convention

Use this specific format for test chunks (note the space, not underscore):

```noweb
<<test modulename.py>>=
import pytest
from package.modulename import *

def test_feature():
    <<test code>>
@
```

The chunk name is `<<test modulename.py>>` with a **space** between "test" and the filename.

### Discovery and Extraction Makefile

The `/tests/Makefile` automatically discovers and extracts tests:

```makefile
# Function to find all test chunks in .nw files
define find_tests
find ../src -type f -name "*.nw" | \
    xargs grep "<<test [^.-]*\.py>>" | \
    sed -En "s/^(.*):.*<<test ([^.-]*).py>>.*/test_\2.py:\1/p" | \
    sort -u
endef

# Function to create a make rule for each test file
define def_target
$(shell echo $1 | cut -d: -f1): $(shell echo $1 | cut -d: -f2)
	notangle ${NOTANGLEFLAGS.py} "-R$$(shell echo $$@ | sed 's/_/ /')" $$^ > $$@
endef

# Get list of all tests
TESTS= $(shell ${find_tests})

# Build all test files
.PHONY: all
all: $(foreach files,${TESTS},$(shell echo ${files} | cut -d: -f1))

# Generate make rules for each test
$(foreach files,${TESTS},$(eval $(call def_target, ${files})))

# Run tests with pytest
.PHONY: test
test: all
    pytest ${PYTEST_FLAGS}
```

### How It Works

1. `find_tests` searches all .nw files for `<<test *.py>>` chunks
2. Extracts mapping: `test_modulename.py: ../src/package/modulename.nw`
3. `def_target` creates a rule that:
   - Depends on the source .nw file
   - Uses `notangle -R"test modulename.py"` to extract the chunk
   - Transforms filename: `test_modulename.py` → chunk `<<test modulename.py>>`
4. `make test` extracts all tests then runs pytest

### Benefits

- **Co-location**: Tests documented alongside implementation
- **Clean separation**: Tests in dedicated directory for CI/CD
- **Automatic discovery**: Adding a test chunk automatically includes it
- **No test pollution**: Source tree stays clean of test files

---

## Navigation Strategies

### Finding Source Code

**Question**: Where is function X defined?

**Answer**: Search in .nw files:
```bash
grep -r "def function_name" src/**/*.nw
```

### Reading Documentation

**Question**: Where can I read the documentation?

**Answer**: Build and view the PDF:
```bash
cd doc
make all
open main.pdf  # or xdg-open main.pdf on Linux
```

The content comes from .tex files generated from .nw in `/src`, but the presentation is organized in `/doc`.

### Running Tests

**Question**: How do I run tests?

**Answer**: Tests are in `/tests`:
```bash
cd tests
make test
```

Or use pytest directly (after extracting):
```bash
cd tests
make all    # Extract tests from .nw files
pytest
```

### Tracing Generated Code

**Question**: This generated .py file has a bug. Where's the source?

**Answer**:
1. Check for corresponding .nw file: `modulename.py` → `modulename.nw`
2. Search for the problematic code in the .nw file
3. Fix the .nw source (NOT the generated .py)
4. Regenerate: `make` in the directory

**Tip**: Generated files should be in .gitignore, so you can delete them and regenerate:
```bash
rm *.py *.tex
make all
```

### Understanding Dependencies

**Question**: What gets generated from what?

**Answer**: Check the Makefile in each directory:
```bash
cat src/package/Makefile
# Look for MODULES+= lines to see what's built
```

Or use make's dry-run:
```bash
make -n all
# Shows commands that would run
```

---

## Complete Example: The nytid Repository

This section shows a real-world example from the nytid project.

### Overall Structure

```
nytid/
├── src/nytid/           # Literate source files
│   ├── Makefile
│   ├── schedules.nw → schedules.py + schedules.tex
│   ├── http_utils.nw → http_utils.py + http_utils.tex
│   ├── courses/
│   │   ├── Makefile
│   │   ├── init.nw → __init__.py + init.tex + tests
│   │   └── registry.nw → registry.py + registry.tex
│   ├── storage/
│   │   ├── Makefile
│   │   ├── init.nw → __init__.py + init.tex
│   │   └── afs.nw → afs.py + afs.tex
│   └── cli/
│       ├── Makefile
│       ├── init.nw → __init__.py + init.tex + shell scripts
│       ├── courses.nw → courses.py + courses.tex
│       └── utils/
│           ├── Makefile
│           └── rooms.nw → rooms.py + rooms.tex
├── doc/
│   ├── Makefile
│   ├── nytid.tex        # Master document
│   ├── nytid.pdf        # Generated documentation
│   └── preamble.tex
├── tests/
│   ├── Makefile
│   ├── test_courses.py (generated from courses/init.nw)
│   ├── test_sheets.py (generated from signup/sheets.nw)
│   └── test_storage.py (generated)
└── makefiles/           # Shared build infrastructure
    ├── Makefile
    ├── noweb.mk.nw → noweb.mk + noweb.tex
    ├── subdir.mk.nw → subdir.mk + subdir.tex
    └── tex.mk.nw → tex.mk + tex.tex
```

### Example: The courses Module

**File**: `src/nytid/courses/init.nw`

This single .nw file generates:
1. `__init__.py` - Module implementation
2. `init.tex` - Chapter for documentation
3. Test chunks extracted to `tests/test_courses.py`

**Makefile** (`src/nytid/courses/Makefile`):
```makefile
SUBDIR_GOALS=   all clean distclean
SUBDIR+=        # No subdirectories here

MODULES+=       registry.py

# Special handling for __init__.py
.INTERMEDIATE: init.py
__init__.py: init.py
    ${MV} $< $@

.PHONY: all
all: __init__.py ${MODULES}

# Include shared rules (two levels up from src/nytid/courses)
INCLUDE_MAKEFILES=../../../makefiles
include ${INCLUDE_MAKEFILES}/noweb.mk
include ${INCLUDE_MAKEFILES}/subdir.mk
```

### Example: Master Documentation

**File**: `doc/nytid.tex`

```latex
\documentclass{memoir}
\input{preamble}

\begin{document}

\part{The CLI}
\input{../src/nytid/cli/init.tex}
\input{../src/nytid/cli/courses.tex}
\input{../src/nytid/cli/schedule.tex}

\part{Storage}
\input{../src/nytid/storage/init.tex}
\input{../src/nytid/storage/afs.tex}

\part{Managing Courses}
\input{../src/nytid/courses/init.tex}
\input{../src/nytid/courses/registry.tex}

\end{document}
```

**Makefile** (`doc/Makefile`):
```makefile
all: nytid.pdf

# PDF depends on all .tex from src
nytid.pdf: ../src/nytid/cli/init.tex
nytid.pdf: ../src/nytid/cli/courses.tex
nytid.pdf: ../src/nytid/storage/init.tex
nytid.pdf: ../src/nytid/courses/init.tex
# ... more dependencies

# Pattern rule to build .tex in src directories
../src/nytid::
    ${MAKE} -C $@ all

../%::
    ${MAKE} -C $(dir $@) $(notdir $@)

# Compile PDF
INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
```

### Example: Multi-Output from Single .nw

**File**: `src/nytid/cli/init.nw` generates:

1. `__init__.py` (module code)
2. `init.tex` (documentation chapter)
3. `nytid.hourly.sh` (cron script)
4. `nytid.daily.sh` (cron script)
5. `nytid.weekly.sh` (cron script)

**Makefile** (`src/nytid/cli/Makefile`):
```makefile
# Regular module
MODULES+= courses.py
MODULES+= schedule.py

# Extra outputs from init.nw
EXTRAS+= nytid.hourly.sh
EXTRAS+= nytid.daily.sh
EXTRAS+= nytid.weekly.sh

# Special handling for __init__.py
.INTERMEDIATE: init.py
__init__.py: init.py
    ${MV} $< $@

# Extra files depend on init.nw
${EXTRAS}: init.nw
    ${NOTANGLE}
    chmod +x $@

.PHONY: all
all: __init__.py ${MODULES} ${EXTRAS}
```

### Workflow Example

**Adding a new feature:**

1. Edit `src/nytid/courses/init.nw` to add feature
2. Add test chunk `<<test courses.py>>=` with test cases
3. Run `make` in `src/nytid/courses` to generate code
4. Run `make` in `tests` to extract and run tests
5. Run `make` in `doc` to rebuild documentation
6. Commit only the .nw file (generated files are in .gitignore)

**Reading the documentation:**

```bash
cd doc
make all
xdg-open nytid.pdf
```

**Running tests:**

```bash
cd tests
make test
```

### Key Takeaways

1. **Single source of truth**: All content in .nw files
2. **Multiple outputs**: Code, docs, tests, scripts from one source
3. **Clean separation**: /src (sources), /doc (docs), /tests (tests)
4. **Hierarchical builds**: Recursive Makefiles with shared rules
5. **Self-documenting**: Even the build system is literate
6. **Version control**: Only .nw files committed, generated files ignored
