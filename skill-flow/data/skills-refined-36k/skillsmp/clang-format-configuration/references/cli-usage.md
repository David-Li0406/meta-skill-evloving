# clang-format CLI Usage

[← Back to Index](index.md) | [Quick Reference](quick-reference.md) | [Full CLI Reference](complete/clang-format-cli.md)

Command-line usage, tools, and integrations for clang-format.

**Documentation Version:** Updated for Clang v22.0.0

## Command-Line Options

### Basic Usage

```bash
# Format from stdin, output to stdout
cat file.cpp | clang-format

# Format file(s) and output to stdout
clang-format file.cpp

# Format file(s) in-place
clang-format -i file.cpp file.h

# Format multiple files
clang-format -i src/*.cpp include/*.h
```

### Common Flags

#### `-i` - In-Place Editing

Modify files directly instead of outputting to stdout:

```bash
clang-format -i file.cpp
```

#### `--style=<style>` - Set Coding Style

Specify the formatting style:

```bash
# Use a predefined style
clang-format --style=google file.cpp

# Use .clang-format file (default)
clang-format --style=file file.cpp

# Specify explicit config file path
clang-format --style=file:/path/to/.clang-format file.cpp

# Inline style configuration
clang-format --style="{BasedOnStyle: llvm, IndentWidth: 8}" file.cpp
```

**Available Predefined Styles:**

- `LLVM`, `GNU`, `Google`, `Chromium`, `Microsoft`, `Mozilla`, `WebKit`, `InheritParentConfig`

Note: `InheritParentConfig` is not a real style, but allows using the `.clang-format` file from the parent directory. If no parent file is found, it falls back to the `fallback` style.

#### `--dry-run` / `-n` - Check Without Modifying

Check what would change without making modifications:

```bash
clang-format --dry-run file.cpp
clang-format -n file.cpp
```

#### `--fallback-style=<style>` - Fallback Style

Style to use if `.clang-format` file cannot be found:

```bash
clang-format --style=file --fallback-style=google file.cpp

# Skip formatting if no config found
clang-format --style=file --fallback-style=none file.cpp
```

#### `--dump-config` - Show Effective Configuration

Display the configuration that will be used:

```bash
# Dump LLVM style
clang-format --style=llvm --dump-config

# Dump effective config for a file
clang-format --dump-config file.cpp

# Create .clang-format from a style
clang-format --style=google --dump-config > .clang-format
```

### Advanced Options

#### `--lines=<start>:<end>` - Format Specific Lines

Format only specified line ranges:

```bash
# Format lines 10-20
clang-format --lines=10:20 file.cpp

# Format multiple ranges
clang-format --lines=10:20 --lines=50:60 file.cpp
```

#### `--offset=<bytes>` and `--length=<bytes>` - Format by Byte Range

Format specific byte ranges:

```bash
clang-format --offset=100 --length=500 file.cpp

# Format from offset to end of file
clang-format --offset=100 file.cpp
```

#### `--assume-filename=<name>` - Set Language for stdin

Specify filename for language detection when reading from stdin:

```bash
cat source.txt | clang-format --assume-filename=file.cpp
```

**Supported Languages (as of Clang v22):**

- C
- C++ (Cpp)
- C# (CSharp): `.cs`
- Java: `.java`
- JavaScript: `.js`, `.mjs`, `.cjs`, `.ts`
- JSON (Json): `.json`, `.ipynb`
- Objective-C (ObjC): `.m`, `.mm`
- Protocol Buffers (Proto): `.proto`, `.protodevel`
- TableGen: `.td`
- Text Protocol Buffers (TextProto): `.txtpb`, `.textpb`, `.pb.txt`, `.textproto`, `.asciipb`
- Verilog: `.sv`, `.svh`, `.v`, `.vh`

For `.h` files, you can specify the language by adding `// clang-format Language: Cpp` (or `C`, `ObjC`) before the first non-comment line.

#### `--files=<filename>` - Process File List

Read list of files to process from a file:

```bash
# Create file list
find src -name '*.cpp' > files.txt

# Format all files in list
clang-format -i --files=files.txt
```

#### `--verbose` - Show Processed Files

Display the list of files being processed:

```bash
clang-format -i --verbose src/*.cpp
```

### Error Handling

#### `--Werror` - Treat Warnings as Errors

Convert formatting warnings to errors:

```bash
clang-format --Werror --dry-run file.cpp
```

#### `--Wno-error=<type>` - Ignore Specific Warnings

```bash
# Allow unknown format options
clang-format --Wno-error=unknown -i file.cpp
```

#### `--ferror-limit=<n>` - Limit Error Count

Set maximum number of errors before stopping:

```bash
clang-format --dry-run --ferror-limit=10 file.cpp
```

#### `--fail-on-incomplete-format` - Fail on Incomplete Formatting

Exit with code 1 if formatting is incomplete:

```bash
clang-format --fail-on-incomplete-format file.cpp
```

## .clang-format-ignore File

Create a `.clang-format-ignore` file to exclude files from formatting.

### Format

```gitignore
# Comments start with #
# Blank lines are ignored

# Ignore third-party code
third_party/**
external/**

# Ignore generated files
*.pb.cc
*.pb.h
*_generated.cpp

# Ignore specific directories
build/**
node_modules/**

# Negate patterns with !
# Format everything except test data
tests/**
!tests/data/**

# Ignore specific files
legacy/old_code.cpp
vendor/library.h
```

### Pattern Rules

- **Blank lines** are skipped
- **Leading/trailing spaces** are trimmed
- **`#` prefix** indicates a comment
- **`/` separator** for directories
- **Patterns are relative** to the `.clang-format-ignore` file location
- **Absolute patterns** start with `/`
- **Bash globstar `**`\*\* is supported
- **`!` prefix** negates the pattern

### Multiple .clang-format-ignore Files

Similar to `.clang-format` files, you can have multiple `.clang-format-ignore` files at different directory levels. Lower-level files override higher-level ones.

## Git Integration

### git clang-format Command

Format only the lines that have changed in git commits:

```bash
# Format staged changes
git clang-format

# Format everything since HEAD~1
git clang-format HEAD~1

# Format everything since main branch
git clang-format main

# Show diff instead of applying
git clang-format --diff

# Show diffstat
git clang-format --diffstat

# Format specific files only
git clang-format main -- src/*.cpp

# Interactive hunk selection
git clang-format -p
```

### Options

```bash
git clang-format [OPTIONS] [<commit>] [<commit>|--staged] [--] [<file>...]
```

**Common Options:**

- `--binary <path>` - Path to clang-format binary
- `--style <style>` - Formatting style to use
- `--diff` - Print diff instead of applying
- `--diffstat` - Print diffstat instead of applying
- `-f, --force` - Allow changes to unstaged files
- `-p, --patch` - Select hunks interactively
- `--staged, --cached` - Format lines in stage instead of working dir
- `-q, --quiet` - Print less information
- `-v, --verbose` - Print extra information

### Git Config

Configure default options in git config:

```bash
git config clangFormat.binary /usr/local/bin/clang-format
git config clangFormat.style file
git config clangFormat.extensions "h,cpp,cc,c"
```

### Pre-Commit Hook Example

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Format staged changes before commit
git clang-format --staged --quiet
```

## Script Tools

### clang-format-diff.py

Format only changed lines from a unified diff:

```bash
# Format git diff
git diff -U0 --no-color --relative HEAD^ | clang-format-diff.py -p1 -i

# Format svn diff
svn diff --diff-cmd=diff -x-U0 | clang-format-diff.py -i

# Format mercurial diff
hg diff -U0 --color=never | clang-format-diff.py -i -p1
```

**Options:**

- `-i` - Apply edits to files instead of displaying diff
- `-p <num>` - Strip N leading directories from paths
- `-regex <pattern>` - Custom pattern for file paths (case sensitive)
- `-iregex <pattern>` - Custom pattern for file paths (case insensitive)
- `-style <style>` - Formatting style
- `-fallback-style <style>` - Fallback style
- `-binary <path>` - Path to clang-format binary
- `-v, --verbose` - Be more verbose

**Example with filters:**

```bash
# Only format .cpp files
git diff -U0 | clang-format-diff.py -i -regex '.*\.cpp'

# Format C++ and header files
git diff -U0 | clang-format-diff.py -i -iregex '.*\.(cpp|h)'
```

## Editor Integration

### Visual Studio Code

Install the "Clang-Format" extension from the marketplace.

**Configuration (settings.json):**

```json
{
  "editor.defaultFormatter": "xaver.clang-format",
  "editor.formatOnSave": true,
  "[cpp]": {
    "editor.defaultFormatter": "xaver.clang-format"
  },
  "clang-format.executable": "/usr/bin/clang-format",
  "clang-format.style": "file"
}
```

**Default Keybinding:** `Alt+Shift+F`

### CLion

CLion has built-in clang-format support.

**Enable:**

1. Settings → Editor → Code Style
2. Enable "Enable ClangFormat support"
3. Place `.clang-format` in project root

**Features:**

- Automatic formatting on type
- Respects `.clang-format` file
- Can generate `.clang-format` from IDE settings

### Vim

Add to `.vimrc`:

```vim
" Python 3 support
if has('python3')
  map <C-K> :py3f /path/to/clang-format.py<cr>
  imap <C-K> <c-o>:py3f /path/to/clang-format.py<cr>
endif

" Python 2 support
if has('python')
  map <C-K> :pyf /path/to/clang-format.py<cr>
  imap <C-K> <c-o>:pyf /path/to/clang-format.py<cr>
endif
```

**Format on save:**

```vim
function! Formatonsave()
  let l:formatdiff = 1
  py3f /path/to/clang-format.py
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp call Formatonsave()
```

### Emacs

Add to `.emacs`:

```elisp
(load "/path/to/clang-format.el")
(global-set-key [C-M-tab] 'clang-format-region)
```

### BBEdit

1. Copy `clang-format-bbedit.applescript` to `~/Library/Application Support/BBEdit/Scripts/`
2. Edit the script to point to your clang-format binary
3. Access from Script menu or assign keyboard shortcut

### Visual Studio

Download the extension from the [LLVM builds site](https://llvm.org/builds/).

**Default Keybinding:** `Ctrl+R, Ctrl+F`

## Common Workflows

### Format Entire Project

```bash
# Find and format all C++ files
find . -name '*.cpp' -o -name '*.h' | xargs clang-format -i

# Using git to find tracked files
git ls-files '*.cpp' '*.h' | xargs clang-format -i
```

### Check Formatting in CI

```bash
# Check if any files need formatting (exit non-zero if changes needed)
clang-format --dry-run --Werror src/**/*.{cpp,h}

# Generate diff for review
clang-format --dry-run src/**/*.{cpp,h} > format-diff.txt
```

### Format Only Modified Files

```bash
# Format files modified in last commit
git diff --name-only HEAD~1 | grep -E '\.(cpp|h)$' | xargs clang-format -i

# Format uncommitted changes
git diff --name-only | grep -E '\.(cpp|h)$' | xargs clang-format -i
```

### Parallel Formatting

```bash
# Format files in parallel (requires GNU parallel)
find src -name '*.cpp' | parallel clang-format -i {}
```

## Troubleshooting

### Configuration File Not Found

clang-format searches for `.clang-format` or `_clang-format` starting from the source file's directory up to the filesystem root.

**Solutions:**

```bash
# Specify config file explicitly
clang-format -style=file:/path/to/.clang-format file.cpp

# Check which config file will be used
clang-format -dump-config file.cpp
```

### Unknown Format Options

Occurs when your config file has options not supported by your clang-format version.

**Solutions:**

```bash
# Warn instead of error
clang-format --Wno-error=unknown -i file.cpp

# Check your clang-format version
clang-format --version

# Regenerate config with your version
clang-format -style=llvm -dump-config > .clang-format
```

### Performance Issues

For large files or projects:

```bash
# Format specific line ranges only
clang-format --lines=100:200 large_file.cpp

# Use parallel processing
find src -name '*.cpp' | parallel -j8 clang-format -i {}

# Format only changed lines
git clang-format
```

## What's New in Clang v22

Clang-format v22 introduces several new style configuration options:

- **AllowBreakBeforeQtProperty**: Control line breaks before Qt `Q_Property` keywords
- **NumericLiteralCase**: Configure capitalization style for numeric literals
- **SpaceInEmptyBraces**: More granular control over spacing in empty braces

For a complete list of v22 style options, refer to the [ClangFormatStyleOptions_v22.md](../../knowledge/ClangFormatStyleOptions_v22.md) documentation.

## Reference

For complete command-line documentation, see [Full CLI Reference](complete/clang-format-cli.md).

---

[← Back to Index](index.md) | [Quick Reference](quick-reference.md) | [Full CLI Reference](complete/clang-format-cli.md)
