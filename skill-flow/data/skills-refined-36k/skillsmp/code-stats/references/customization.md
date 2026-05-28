# Customization Guide

Extend the code-stats skill by adding new languages, custom comment patterns, and file type mappings.

## Adding New Languages

To add support for a new programming language, modify `scripts/utils/language.py`.

### Step 1: Add Extension Mapping

Add the file extension to the `EXTENSION_TO_LANG` dictionary:

```python
EXTENSION_TO_LANG: Dict[str, str] = {
    # ... existing mappings ...

    # Your new language
    ".scala": "Scala",
    ".elm": "Elm",
    ".ex": "Elixir",
}
```

### Step 2: Add Comment Patterns

Define the comment syntax for your language in `COMMENT_PATTERNS`:

```python
COMMENT_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    # ... existing patterns ...

    "Scala": {
        "line": ["//"],
        "block_start": ["/*"],
        "block_end": ["*/"],
    },

    "Elixir": {
        "line": ["#"],
        "block_start": [],
        "block_end": [],
    },
}
```

### Pattern Format

Each language has three pattern types:

- **`line`**: Single-line comment markers (e.g., `//`, `#`, `--`)
- **`block_start`**: Multi-line comment start markers (e.g., `/*`, `"""`, `<!--`)
- **`block_end`**: Multi-line comment end markers (e.g., `*/`, `"""`, `-->`)

### Examples

#### C-style Languages (C, C++, Java, C#, Go, Rust, etc.)

```python
"MyLang": {
    "line": ["//"],
    "block_start": ["/*"],
    "block_end": ["*/"],
}
```

#### Shell-style Languages (Shell, Python, Ruby, Make, etc.)

```python
"MyLang": {
    "line": ["#"],
    "block_start": [],
    "block_end": [],
}
```

#### Block Comments Only (CSS)

```python
"MyLang": {
    "line": [],
    "block_start": ["/*"],
    "block_end": ["*/"],
}
```

#### Multiple Line Comment Styles (PHP)

```python
"PHP": {
    "line": ["//", "#"],
    "block_start": ["/*"],
    "block_end": ["*/"],
}
```

#### Multi-line String Comments (Python)

```python
"Python": {
    "line": ["#"],
    "block_start": ['"""', "'''"],
    "block_end": ['"""', "'''"],
}
```

## Custom Comment Patterns

Some languages have unusual comment syntax. Here's how to handle them:

### Nested Comments

For languages that support nested comments (rare), the current implementation may not handle them correctly. The script tracks block comments but not nesting depth.

**Workaround**: Treat nested blocks as regular comments:

```python
"MyLang": {
    "line": ["//"],
    "block_start": ["(*"],
    "block_end": ["*)"],
}
```

### Conditional Compilation Comments

Some languages use comments for conditional compilation (e.g., Rust's `#[cfg(test)]`). These are currently counted as code, not comments.

**To treat them as comments**: Add them to the line comment patterns:

```python
"Rust": {
    "line": ["//", "#["],  # Add #[ for attributes
    "block_start": ["/*"],
    "block_end": ["*/"],
}
```

## Extension Aliases

Support multiple extensions for the same language:

```python
EXTENSION_TO_LANG: Dict[str, str] = {
    # C++ variants
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".hxx": "C++",

    # Script variants
    ".bash": "Bash",
    ".sh": "Shell",
}
```

## Configuration Files

You can also create configuration files for custom mappings without modifying the source code.

### Custom Language Mapping File

Create a JSON file (e.g., `custom-languages.json`):

```json
{
  ".myext": "MyLanguage",
  ".other": "OtherLang"
}
```

Then modify `count.py` to load it (future enhancement).

## Testing Custom Languages

After adding a new language:

1. Create a test file with your extension:

```bash
echo "// Comment
fn main() {
    println!(\"Hello\");
}" > test.myext
```

2. Run the counter:

```bash
python scripts/count.py --path . --extensions myext
```

3. Verify the output:
   - File is counted
   - Language name is correct
   - Comments are identified correctly

## File Type Detection

The script uses multiple methods to detect file types:

### 1. Extension Lookup (Primary)

First method is file extension mapping in `EXTENSION_TO_LANG`.

### 2. Binary Detection

Files with certain extensions are always treated as binary:

```python
binary_extensions = {
    '.pyc', '.pyo', '.so', '.dll', '.exe',
    '.png', '.jpg', '.pdf', '.zip',
    # ... more
}
```

Add new binary extensions in `count.py` if needed.

### 3. Content Detection

As a fallback, the script reads the first 1KB of each file and:

- Checks for null bytes (indicates binary)
- Attempts UTF-8 decode
- Skips files that fail these checks

To modify this behavior, edit the `is_binary_file()` function in `count.py`.

## Custom Directories to Skip

To skip additional directories, modify `SKIP_DIRECTORIES` in `count.py`:

```python
SKIP_DIRECTORIES = {
    ".git",
    "target",
    # Add your custom directories
    "vendor",
    "third_party",
    "external",
}
```

## Custom Output Formats

The current implementation outputs Markdown tables. To add new formats:

### Step 1: Add Formatter Function

Create a new formatter in `scripts/utils/markdown.py`:

```python
def format_json_table(stats: Dict[str, Dict[str, int]]) -> str:
    """Format statistics as JSON."""
    import json
    return json.dumps(stats, indent=2)

def format_csv_table(stats: Dict[str, Dict[str, int]]) -> str:
    """Format statistics as CSV."""
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Language", "Files", "Code", "Blank", "Comment", "Total"])

    for lang, lang_stats in stats.items():
        writer.writerow([
            lang,
            lang_stats.get('files', 0),
            lang_stats.get('code', 0),
            lang_stats.get('blank', 0),
            lang_stats.get('comment', 0),
            lang_stats.get('total', 0)
        ])

    return output.getvalue()
```

### Step 2: Add CLI Option

Modify `count.py` to accept `--output` option:

```python
parser.add_argument(
    '--output',
    type=str,
    choices=['markdown', 'json', 'csv'],
    default='markdown',
    help='Output format (default: markdown)'
)
```

### Step 3: Use Formatter

In the main function, select the formatter based on the argument:

```python
if args.output == 'json':
    table = format_json_table(stats)
elif args.output == 'csv':
    table = format_csv_table(stats)
else:  # markdown
    table = format_language_table(stats)
```

## Advanced: Custom Comment Parsing

For languages with complex comment syntax, you may need to extend the comment detection logic.

### Example: String Literal Handling

Current implementation has basic string detection. To improve it:

```python
def count_lines_advanced(filepath: Path) -> Dict[str, int]:
    """Count lines with proper string literal handling."""
    lang = detect_language(filepath.suffix)
    patterns = get_comment_patterns(lang)

    code_lines = 0
    blank_lines = 0
    comment_lines = 0

    in_block_comment = False
    in_string = False
    string_char = None

    for line in open(filepath).readlines():
        stripped = line.strip()

        # TODO: Track string literals properly
        # This requires character-by-character parsing
        # ...

    return {
        'code': code_lines,
        'blank': blank_lines,
        'comment': comment_lines,
    }
```

## Contributing

If you add support for a new language, consider:

1. Testing with real code examples
2. Handling edge cases (empty files, mixed syntax)
3. Adding to the 10 core languages in MVP
4. Documenting any special cases

## Examples

### Adding Swift Support

```python
# In EXTENSION_TO_LANG
".swift": "Swift",

# In COMMENT_PATTERNS
"Swift": {
    "line": ["//"],
    "block_start": ["/*"],
    "block_end": ["*/"],
}
```

### Adding Kotlin Support

```python
# In EXTENSION_TO_LANG
".kt": "Kotlin",
".kts": "Kotlin",

# In COMMENT_PATTERNS
"Kotlin": {
    "line": ["//"],
    "block_start": ["/*"],
    "block_end": ["*/"],
}
```

### Adding Lua Support

```python
# In EXTENSION_TO_LANG
".lua": "Lua",

# In COMMENT_PATTERNS
"Lua": {
    "line": ["--"],
    "block_start": ["--[[", "--[["],
    "block_end": ["]]", "]]"],
}
```

## Troubleshooting

### Language Not Detected

- Check the extension includes the dot (e.g., `.py`, not `py`)
- Verify the extension is in `EXTENSION_TO_LANG`
- Ensure the extension is lowercase (comparison is case-insensitive)

### Comments Not Counted

- Verify comment patterns are defined for the language
- Check that block start/end markers match
- Ensure line comment markers are correct
- Test with a simple file to confirm

### File Skipped as Binary

- Check if the extension is in `binary_extensions`
- Verify the file is actually text (open in a text editor)
- Check for null bytes or non-UTF-8 characters

## Best Practices

1. **Test with real code**: Use actual project files, not synthetic examples
2. **Handle edge cases**: Empty files, files with only comments, mixed syntax
3. **Document special cases**: Add comments for unusual comment syntax
4. **Keep it simple**: Don't overcomplicate for edge cases
5. **Share improvements**: Consider contributing new languages back