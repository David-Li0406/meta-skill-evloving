# Python Coding Rules

## Table of Contents

1. [Rule Index](#rule-index)
2. [Definitions](#definitions)
3. [Formatting Rules (FT)](#formatting-rules-ft)
4. [Import Rules (IM)](#import-rules-im)
5. [Code Generation Rules (CG)](#code-generation-rules-cg)
6. [Naming Rules (NM)](#naming-rules-nm)
7. [Comment Rules (CM)](#comment-rules-cm)
8. [Logging Rules (LG)](#logging-rules-lg)

## Rule Index

**Formatting (FT)**
- **PYTHON-FT-01**: Indentation with TAB (2 spaces)
- **PYTHON-FT-02**: Single line for statements ≤ MAX_LINE_CHARS
- **PYTHON-FT-03**: Function signature on single line
- **PYTHON-FT-04**: One empty line between functions/classes
- **PYTHON-FT-05**: Function grouping with topic markers

**Imports (IM)**
- **PYTHON-IM-01**: All imports at top of file
- **PYTHON-IM-02**: Core imports on single line
- **PYTHON-IM-03**: No local imports inside functions
- **PYTHON-IM-04**: Group imports by origin
- **PYTHON-IM-05**: Prefer single-line multi-name imports

**Code Generation (CG)**
- **PYTHON-CG-01**: Do not rename existing symbols
- **PYTHON-CG-02**: Re-use existing patterns
- **PYTHON-CG-03**: Check for existing helpers before creating new
- **PYTHON-CG-04**: Principle of Least Surprise
- **PYTHON-CG-05**: Prefer explicit for loops over functional helpers
- **PYTHON-CG-06**: Prefer standard library
- **PYTHON-CG-07**: No emojis in code/logging
- **PYTHON-CG-08**: Use timezone-aware datetime
- **PYTHON-CG-09**: Handle singular/plural correctly

**Naming (NM)**
- **PYTHON-NM-01**: Use clear, fully written names
- **PYTHON-NM-02**: Follow existing naming patterns
- **PYTHON-NM-03**: Avoid ambiguous abbreviations

**Comments (CM)**
- **PYTHON-CM-01**: Comment intent, not obvious code
- **PYTHON-CM-02**: No docstrings for small functions
- **PYTHON-CM-03**: Docstrings for complex functions with examples
- **PYTHON-CM-04**: Use ASCII quotes in documentation
- **PYTHON-CM-05**: Use tree characters for hierarchies

**Logging (LG)**
- **PYTHON-LG-01**: Indent sub-actions with 2 spaces
- **PYTHON-LG-02**: Log action before executing
- **PYTHON-LG-03**: Status keywords on separate indented line
- **PYTHON-LG-04**: Surround paths/names/IDs with single quotes
- **PYTHON-LG-05**: Iteration format `[ x / n ]`
- **PYTHON-LG-06**: Retry format `( x / n )` inline
- **PYTHON-LG-07**: Numbers first in results (exception: activity verbs)
- **PYTHON-LG-08**: Property format `property_name='value'`
- **PYTHON-LG-09**: Use UNKNOWN constant for missing values
- **PYTHON-LG-10**: Nested function indentation (+2 spaces per level)
- **PYTHON-LG-11**: Error concatenation with ` -> `
- **PYTHON-LG-12**: Additional identifiers in parentheses `(ID=xxx)`

## Definitions

```
MAX_LINE_CHARS = 220
TAB = "  " (2 spaces)
UNKNOWN = '[UNKNOWN]'
```

## Formatting Rules (FT)

### PYTHON-FT-01: Indentation
Indent code with TAB (2 spaces).

### PYTHON-FT-02: Single Line Statements
If a statement is ≤ MAX_LINE_CHARS characters (including spaces), keep it on a single line.
Ignore MAX_LINE_CHARS restrictions in Markdown; especially for tables and UI prototypes.

*BAD*:
```python
content_page = client.vector_stores.files.content(
  vector_store_id=vector_store_id,
  file_id=file_id
)
```
*GOOD*:
```python
content_page = client.vector_stores.files.content(vector_store_id=vector_store_id, file_id=file_id)
```

*BAD*:
```python
if not vector_store_id:
  raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```
*GOOD*:
```python
if not vector_store_id: raise ValueError(f"Expected a non-empty value for 'vector_store_id' but received {vector_store_id!r}")
```

### PYTHON-FT-03: Function Signatures
Put the full signature on a single line; function body starts on the next line.

### PYTHON-FT-04: Empty Lines
One empty line as delimiter between imports, functions and class definitions.

### PYTHON-FT-05: Function Grouping
Group functions under common topic with start/end markers (127 chars long). Single line space after each function.

*BAD*:
```python
def function01():
  ...


def function02():
  ...
def function03():
  ...
```
*GOOD*:
```python
# ----------------------------------------- START: Topic A --------------------------------------------------------------------

def function01():
  ...

def function02():
  ...

# ----------------------------------------- END: Topic A ----------------------------------------------------------------------


# ----------------------------------------- START: Topic B --------------------------------------------------------------------

def function03():
  ...

def function04():
  ...

# ----------------------------------------- END: Topic B ----------------------------------------------------------------------
```

*BAD*:
```python
# ============================================
# MONITOR ENDPOINT
# ============================================
[ ... CODE ... ]
```
*GOOD*:
```python
# ----------------------------------------- START: /monitor endpoint ----------------------------------------------------------

[ ... CODE ... ]

# ----------------------------------------- END: /monitor endpoint -------------------------------------------------------------
```

## Import Rules (IM)

### PYTHON-IM-01: Import Location
All imports at the top of the file.

### PYTHON-IM-02: Core Imports
All core imports on a single line (even if longer than MAX_LINE_CHARS).

*BAD*:
```python
import asyncio
import datetime
import json
import random
```
*GOOD*:
```python
import asyncio, datetime, json, random
```

### PYTHON-IM-03: No Local Imports
No local imports inside functions.

*BAD*:
```python
def function_abc():
  from utils import convert_to_nested_html_table
  # ...
```
*GOOD*:
```python
from utils import convert_to_flat_html_table, convert_to_nested_html_table

def function_abc():
  # ...
```

### PYTHON-IM-04: Import Grouping
Group imports: standard library first, then third-party libraries, then internal modules.

### PYTHON-IM-05: Multi-Name Imports
Prefer importing all needed names from a module in a single line.

## Code Generation Rules (CG)

### PYTHON-CG-01: No Symbol Renaming
Do not rename existing symbols unless explicitly asked.

### PYTHON-CG-02: Re-use Patterns
Analyze the existing codebase before creating new code. Re-use existing implementation patterns, naming patterns, code formatting, design philosophy, logging style and functions.

### PYTHON-CG-03: Check Existing Helpers
Before implementing new helper functions, make sure no alternatives exist in the codebase.

### PYTHON-CG-04: Principle of Least Surprise
Prefer simple, idiomatic Python over clever or magical code. Optimize for readability and maintainability, not micro-optimizations. Concise is good, but not at the expense of clarity.

### PYTHON-CG-05: Explicit Loops
Avoid `lambda`, `map`, `filter`, `reduce` and similar helpers for control flow; use explicit `for` loops.
**Exception**: string / list joins.

### PYTHON-CG-06: Standard Library First
Prefer standard library over third-party packages; add dependencies only if a helper function would be unreasonably complex.

### PYTHON-CG-07: No Emojis
No emojis in the code or logging.
**Exception**: UI may occasionally use ✅=yes/pass, ❌=no/fail, ⚠️=warning/partial, ★=filled star, ☆=outlined star, ⯪=half star

### PYTHON-CG-08: Timezone-Aware Datetime
Use `datetime.datetime.now(datetime.timezone.utc)` instead of deprecated `datetime.datetime.utcnow()`.

### PYTHON-CG-09: Singular/Plural
Handle singular and plural correctly: `0 files found.`, `1 file`, `2 files`. Avoid `1 file(s)`.

*BAD*:
```python
print(f"{count} file(s) found.")
```
*GOOD*:
```python
print(f"{count} file(s)".replace("(s)", "s" if count != 1 else "") + " found.")
```

## Naming Rules (NM)

### PYTHON-NM-01: Clear Names
Use clear, fully written names.

### PYTHON-NM-02: Follow Patterns
Follow existing naming patterns in the codebase.

### PYTHON-NM-03: No Abbreviations
Avoid ambiguous abbreviations.

*BAD* -> *GOOD*:
```
body_attrs -> body_attributes
content -> html_content
dynamic_count -> use_dynamic_count_for_updating
```

## Comment Rules (CM)

### PYTHON-CM-01: Comment Intent
Avoid comments that restate obvious code; comment intent, edge cases, and non-obvious behavior.

### PYTHON-CM-02: No Docstrings for Small Functions
No docstrings for small, single-purpose functions with self-explanatory names and arguments. Use a single comment above such functions if intent or types need clarification.

*BAD*:
```python
def generate_error_response(error_message: str, format: str, status_code: int = 400):
  """
  Generate error response in requested format.
  Args: ...
  Returns: ...
  """
  if format == 'json':
    return JSONResponse({"error": error_message}, status_code=status_code)
  else:
    return HTMLResponse(generate_error_div(error_message), status_code=status_code)
```
*GOOD*:
```python
# Generate HTTP error response in requested format ('json' | 'html')
def generate_error_response(error_message: str, format: str, status_code: int = 400):
  if format == 'json': return JSONResponse({"error": error_message}, status_code=status_code)
  else: return HTMLResponse(generate_error_div(error_message), status_code=status_code)
```

*BAD*:
```python
def set_config(app_config):
  """Set the configuration for Crawler management."""
  global config
  config = app_config
```
*GOOD*:
```python
# Set the configuration for Crawler management. app_config: Config dataclass with openai_client, persistent_storage_path, etc.
def set_config(app_config):
  global config
  config = app_config
```

### PYTHON-CM-03: Docstrings for Complex Functions
Use docstrings for FastAPI endpoints and complex functions (more than 5 arguments, multiple responsibilities, or complex/structured return types), and include example outputs.

*GOOD*:
```python
def generate_simple_page(title: str, html_content: str, body_attributes: str = "") -> str:
  """
  Generate simple HTML page with title and html content.
  
  Example output:
    <!DOCTYPE html><html><head>[GENERATE_HTML_HEAD_OUTPUT]</head>
    <body [BODY_ATTRIBUTES_IF_ANY]>
      [HTML_CONTENT]
    </body>
    </html>
  """
  head = generate_html_head(title)
  body_tag = f"<body {body_attributes}>" if body_attributes else "<body>"
  return f"""{head}
{body_tag}
  {html_content}
</body>
</html>"""
```

### PYTHON-CM-04: ASCII Quotes
For documentation or UI output, avoid "typographic quotes" and use typewriter / ASCII "double quotes" or 'single quotes'.

### PYTHON-CM-05: Hierarchy Characters
When creating hierarchies and maps, use "└──" for indenting.

## Logging Rules (LG)

### PYTHON-LG-01: Sub-Action Indentation
Indent sub-actions with 2 spaces.

### PYTHON-LG-02: Log Before Action
Log the action description before executing it.

### PYTHON-LG-03: Status Keywords
Put status keywords on a separate, indented line: `OK`, `ERROR`, `FAIL`, `WARNING`.
- `OK` = action succeeded
- `ERROR` = intermediate or final error occurred
- `FAIL` = action failed even after error mitigation
- `WARNING` = intermediate error that will be mitigated

### PYTHON-LG-04: Quote Paths and IDs
Surround file paths, names and IDs with single quotes `'...'`.

### PYTHON-LG-05: Iteration Format
For iterations, prefix lines with `[ x / n ]` at the beginning of a line where x = current item number, n = total items.

### PYTHON-LG-06: Retry Format
For retries, use `( x / n )` inline where x = current retry, n = max retries.

### PYTHON-LG-07: Numbers First
When logging results, always state numbers first. Honor the singular / plural rule.
**Exception**: When starting activities, the activity verb should go first.

*BAD*:
```
Retrieved 1 items so far...
Total files retrieved: 2
Successfully converted 2 of 10 files to SharePointFile objects
```
*GOOD*:
```
Retrieving 1 item from 'https://xxx'...
  1 item retrieved so far...
2 total files retrieved.
2 of 10 files successfully converted to SharePointFile objects.
```

### PYTHON-LG-08: Property Format
When logging IDs, paths, names, or properties that may contain spaces, use `property_name='value'` format. This disambiguates values and makes logs parseable. Do not use colons after prepositions like "from".

*BAD*:
```
Loading domain AiSearchTest01 from: E:\dev\domains\domain.json
Using file source: SharedDocuments
Site URL: https://example.com/sites/Test
Library: /Shared Documents
```
*GOOD*:
```
Loading domain 'AiSearchTest01' from 'E:\dev\domains\domain.json'...
Using file source: source_id='SharedDocuments'
Site: site_url='https://example.com/sites/Test'
Library: sharepoint_url_part='/Shared Documents'
```

### PYTHON-LG-09: UNKNOWN Constant
Missing values returned by APIs **should NOT be converted to arbitrary default values**. Define a global `UNKNOWN` constant in `common_logging_functions_v2.py`. Use `or UNKNOWN` pattern for values that go to logs. **NEVER risk breaking logging**.

*BAD*:
```python
# Inconsistent placeholders
lib_title = props.get('Title', '?')
lib_id = props.get('Id', 'Unknown')
file_path = props.get('Path', '')

# None shown directly in logs
lib_title = props.get('Title')  # Returns None
logger.log(f"Library: '{lib_title}'")  # Output: "Library: 'None'"

# Magic strings scattered everywhere
lib_title = props.get('Title', '[UNKNOWN]')
```

*GOOD*:
```python
# In self-containing files use
UNKNOWN = '[UNKNOWN]'

# In other files - import and use
from routers_v2.common_logging_functions_v2 import MiddlewareLogger, UNKNOWN

lib_title = props.get('Title') or UNKNOWN
lib_id = props.get('Id') or UNKNOWN
logger.log(f"Library: '{lib_title}' (ID={lib_id})")
```

Output examples:
- With value: `Library: 'Documents' (ID=045229b3-57de-49ce-b36a-00c3ec0f4fd4)`
- Without value: `Library: '[UNKNOWN]' (ID=[UNKNOWN])`

### PYTHON-LG-10: Nested Function Indentation
When functions call other functions that also log, each nesting level adds 2 spaces:
- Depth 1 (top-level function): 2 spaces from section header
- Depth 2 (nested function): 4 spaces
- Depth 3 (doubly nested): 6 spaces

*BAD*:
```
[ 9 / 12 ] export_list_to_csv()
START: export_list_to_csv()...
START: get_list_items()...
6 list items retrieved.
END: get_list_items()
6 items exported.
END: export_list_to_csv()
```
*GOOD*:
```
[ 9 / 12 ] export_list_to_csv()
  START: export_list_to_csv()...
    START: get_list_items()...
    6 list items retrieved.
    END: get_list_items()
  6 items exported.
  END: export_list_to_csv()
```

### PYTHON-LG-11: Error Concatenation
When logging errors, concatenate the description with the exception using ` -> ` without dot before. Always include paths and identifiers of the current activity to track down individual items in logs.

*BAD*:
```
Uploading file...
Success.
Download complete
failed to process file
Warning: retrying...
ERROR: Connection refused
```
*GOOD*:
```
Uploading file 'C:\abc\def.pdf' to library 'https://...'...
  OK.
Downloading file 'https://...' (ID=xxx)...
  ERROR: Connection timeout -> ConnectionRefusedError: [Errno 111] Connection refused
Processing file 'C:\abc\def.pdf'...
  FAIL: Skipped processing after 3 retries.
Opening file 'C:\abc\def.pdf'...
  WARNING: File locked, waiting for release -> BlockingIOError: [Errno 11] Resource temporarily unavailable
```

Code examples:
```python
# Simple error logging
try:
  download_file()
except Exception as e:
  logger.log(f"  ERROR: Could not download file -> {e}")

# With context
try:
  ctx.execute_query()
except Exception as e:
  logger.log(f"  ERROR: Failed to retrieve files for library '{lib_title}' (ID={lib_id}) -> {e}")

# Warning with recovery
try:
  open_file(path)
except BlockingIOError as e:
  logger.log(f"  WARNING: File could not be opened -> {e}")
  wait_and_retry()
```

### PYTHON-LG-12: Additional Info in Parentheses
Use parentheses for **additional/secondary information** that supplements the main log message. Primary identifiers can be inline.

**Primary identifier inline** (no parentheses needed):
- `Deleted file ID=file_xyz789`
- `File file_xyz789 removed from vector store vs_abc123`
- `Download source 'source01' (type=file_sources, mode=full, dry_run=false)`

**Additional info in parentheses**:
- `Library: 'Documents' (ID=045229b3...)`
- `Downloading file 'report.pdf' (ID=xxx)...`

*BAD*: `Deleted file (ID='file_xyz789').` (over-parenthesizing primary attribute or identifyer)
*GOOD*: `Deleted file ID=file_xyz789`

## Complete Logging Example

*BAD*:
```
Uploading item 1/2 Example.docx to vs_62573645276345
SUCCESS: Verified uploaded file.
Uploading item 1/2 Test.docx to vs_62573645276345
ERROR: BlockingIOError: [Errno 11] Resource temporarily unavailable
```

*GOOD*:
```
[ 1 / 2 ] Uploading file 'C:\Example.docx' to vector store ID='vs_62573645276345'...
  Verifying uploaded file ID='file_923748237' (file_path='C:\Example.docx')...
  OK.
[ 2 / 2 ] Uploading file 'C:\Test.docx' to vector store ID='vs_62573645276345'...
  WARNING: File could not be opened. Maybe it's locked -> BlockingIOError: [Errno 11] Resource temporarily unavailable
  Waiting 5 seconds ( 1 / 2 ) for retry...
  Uploading file...
  Verifying uploaded file ID='file_238756235'...
  OK.
```
