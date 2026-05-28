# Noweb Commands Reference

This reference provides detailed documentation for noweb commands used in literate programming.

## Table of Contents

1. [Tangling (Extracting Code)](#tangling-extracting-code)
2. [Weaving (Creating Documentation)](#weaving-creating-documentation)
3. [Common Patterns](#common-patterns)
4. [Language-Specific Notes](#language-specific-notes)
5. [Troubleshooting](#troubleshooting)

---

## Tangling (Extracting Code)

Tangling extracts executable code from a literate program.

### Basic Usage

```bash
# Extract a specific root chunk
notangle -Rchunkname file.nw > output.ext

# With line number directives for debugging
notangle -L -Rchunkname file.nw > output.ext

# Default root is <<*>>
notangle file.nw > output.ext

# List all root chunks (not used in other chunks)
noroots file.nw
```

### Common Flags

| Flag | Description |
|------|-------------|
| `-R<name>` | Specify root chunk to extract (can be repeated) |
| `-L` | Emit line number directives (`#line` for C, etc.) |
| `-L'format'` | Custom line number format |
| `-t<n>` | Preserve tabs, with stops every n columns |
| `-filter cmd` | Filter through command before tangling |

### [[...]] Notation for LaTeX-Safe Chunk Names

When chunk names contain underscores (common in Python), LaTeX interprets them as math subscripts, causing compilation errors. Use noweb's `[[...]]` notation:

```noweb
<<[[module_name.py]]>>=
def my_function():
    pass
@
```

Extract with:

```bash
notangle -R"[[module_name.py]]" file.nw > module_name.py
```

**Why this works:**
- `[[...]]` tells noweb to escape all LaTeX special characters
- Works for underscores, hashes, ampersands, and other special characters
- Chunk name matches filename exactly (no renaming needed)

---

## Weaving (Creating Documentation)

Weaving produces documentation from a literate program.

### Basic Usage

```bash
# Generate LaTeX
noweave -latex file.nw > output.tex

# Generate with cross-references
noweave -latex -x file.nw > output.tex

# Generate with index and autodefs for language
noweave -latex -index -autodefs lang file.nw > output.html

# Generate HTML
noweave -html -index -autodefs lang file.nw > output.html

# No wrapper (for inclusion in larger document)
noweave -n -latex file.nw > output.tex

# Delay preamble (for custom \documentclass)
noweave -delay -latex file.nw > output.tex
```

### Common Flags

| Flag | Description |
|------|-------------|
| `-latex` | Emit LaTeX (default) |
| `-html` | Emit HTML |
| `-tex` | Emit plain TeX |
| `-n` | No wrapper (no document structure) |
| `-delay` | Delay file info until after first doc chunk |
| `-x` | Add cross-references and chunk definitions |
| `-index` | Build identifier index |
| `-autodefs lang` | Auto-detect definitions in language |
| `-t<n>` | Expand tabs to n columns |

### Weaving for Inclusion

When weaving for inclusion in a master document, use `-n -delay`:

```bash
noweave -n -delay -x -t2 file.nw > file.tex
```

This produces .tex without `\documentclass`, suitable for `\input{...}`.

---

## Common Patterns

### Multiple Outputs from One File

```bash
notangle -Rprogram.c file.nw > program.c
notangle -Rprogram.h file.nw > program.h
notangle -RMakefile file.nw > Makefile
```

### Building with Make

```makefile
%.py: %.nw
    notangle -R$@ $< > $@

%.tex: %.nw
    noweave -n -latex $< > $@

%.pdf: %.tex
    pdflatex $<
```

### Documentation with Tests

Interleave test code with implementation:

```noweb
Here's our sort function:
<<sort function>>=
def sort(lst):
    <<sorting implementation>>
@

Let's verify it works:
<<test code>>=
assert sort([3,1,2]) == [1,2,3]
@
```

---

## Language-Specific Notes

### C/C++

- Use `-L` flag for `#line` directives
- Put headers and implementation in same .nw file
- Extract with: `notangle -L -Rfile.cpp file.nw > file.cpp`

### Python

- No special flags needed
- Keep lines under 80 characters in .nw files
- Consider using formatters on output: `notangle -Rfile.py file.nw | black - > file.py`
- Note: Black may reformat to different line lengths

**Docstring Anti-Pattern**: Never include LaTeX commands in Python docstrings.

**Bad** - LaTeX in docstring causes warnings:
```python
def func(x):
    """See \cref{Section} for details."""  # WARNING: invalid escape
    ...
```

**Good** - Plain docstring, LaTeX in literate source:
```noweb
This function implements the algorithm from \cref{Algorithm}.

<<functions>>=
def func(x):
    """Process the input using the algorithm."""
    ...
@
```

### Haskell

- Use `-L` flag (GHC understands line pragmas)
- Note: Haskell also has native `.lhs` literate format

### Make

- Use `-t2` to convert spaces to tabs: `notangle -t2 -RMakefile file.nw > Makefile`

### Shell Scripts

- No special flags needed
- Remember to `chmod +x` the output

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "chunk not defined" error | Check chunk name spelling with `noroots` |
| Line numbers wrong in debugger | Use `-L` flag with notangle |
| Formatting broken | Check that `<<` starts in column 1 |
| Chunks in wrong order | Remember, notangle assembles them correctly |
| Documentation not rendering | Verify `@` markers for documentation chunks |
| LaTeX errors with underscores | Use `[[...]]` notation for chunk names |

### Using noroots

The `noroots` command lists all root chunks (chunks not referenced by other chunks). Use it to:

1. Find typos in chunk names (orphaned chunks appear in output)
2. Discover all extractable targets in a file
3. Verify your main chunk is not accidentally referenced elsewhere

```bash
noroots file.nw
# Output: <<main.py>> <<test.py>> <<Makefile>>
```

If you see a chunk you expect to be used, check for spelling errors in references.
