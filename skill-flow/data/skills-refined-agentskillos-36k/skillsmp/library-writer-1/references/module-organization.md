# Module Organization

How to structure library source code for clarity and maintainability.

## Directory Layouts

### Minimal Library

```
my-library/
├── lib/
│   └── my_library.ext       # Single file for small libraries
├── tests/
│   └── test_my_library.ext
├── README.md
├── LICENSE
└── [package manifest]
```

### Standard Library

```
my-library/
├── lib/                     # Or src/
│   ├── my_library.ext       # Entry point
│   └── my_library/          # Internal modules
│       ├── client.ext
│       ├── config.ext
│       ├── errors.ext
│       └── utils.ext
├── tests/
│   ├── test_client.ext
│   ├── test_config.ext
│   └── fixtures/
├── README.md
├── LICENSE
└── [package manifest]
```

### Library with Framework Integration

```
my-library/
├── lib/
│   ├── my_library.ext       # Entry point
│   └── my_library/
│       ├── core/            # Core functionality
│       │   ├── client.ext
│       │   └── config.ext
│       └── integrations/    # Framework integrations
│           ├── rails.ext
│           ├── django.ext
│           └── express.ext
├── tests/
│   ├── core/
│   └── integrations/
└── ...
```

## Entry Point Design

### Single Entry Point

Users should only need one import:

```
# User imports
import my_library

# Everything accessible from there
my_library.Client()
my_library.configure(...)
my_library.Error
```

### Entry Point File Structure

```
# my_library.ext (entry point)

# 1. Standard library imports
import os
import json

# 2. Internal imports
from .client import Client
from .config import Config
from .errors import Error, ConfigError

# 3. Conditional framework loading
if framework_loaded():
    from .integrations.framework import setup

# 4. Module-level configuration
api_key = os.environ.get("MYLIB_API_KEY")
timeout = 30

# 5. Public API exports
__all__ = ["Client", "Config", "Error", "api_key", "timeout"]
```

## File Naming Conventions

### Use Clear, Descriptive Names

```
Good:
  client.ext      # HTTP client
  config.ext      # Configuration
  errors.ext      # Error classes
  utils.ext       # Utility functions
  types.ext       # Type definitions

Bad:
  c.ext           # Unclear
  helpers.ext     # Vague
  misc.ext        # Catch-all
  stuff.ext       # Meaningless
```

### Match Class Names to Files

```
# client.ext contains class Client
# config.ext contains class Config
# Easy to find where things are defined
```

## Internal vs Public

### Mark Internal Modules

```
Conventions by language:

Python:
  _internal.py           # Leading underscore
  my_lib/_internal/      # Internal package

JavaScript:
  internal/              # Internal folder
  _helpers.js            # Leading underscore

Go:
  internal/              # Special internal package

Ruby:
  # No convention, use documentation
```

### Public API Surface

Keep the public API minimal:

```
Public (exported):
  - Client class
  - Configuration accessors
  - Error classes
  - Main functions

Private (internal):
  - Helper functions
  - Internal classes
  - Implementation details
```

## Require/Import Organization

### Order of Imports

```
1. Standard library
2. Third-party dependencies (if any)
3. Internal modules (relative imports)
```

### Relative vs Absolute Imports

```
Inside the library, use relative imports:

Good:
  from .client import Client
  from ..utils import helper

Bad:
  from my_library.client import Client
  # Breaks if package is renamed
```

## Module Dependencies

### Avoid Circular Imports

```
Bad:
  # client.ext imports config
  # config.ext imports client
  # Circular dependency!

Good:
  # Both import from shared module
  # Or restructure to eliminate cycle
```

### Dependency Direction

```
Entry point
    ↓
High-level modules (Client, API)
    ↓
Low-level modules (Utils, Errors)
    ↓
No dependencies (Types, Constants)

# Dependencies flow downward only
```

## Splitting Large Modules

### When to Split

Split a module when:
- File exceeds 500 lines
- Contains multiple unrelated classes
- Hard to navigate
- Tests are becoming unwieldy

### How to Split

```
Before:
  client.ext (800 lines)
    - Client class
    - Request class
    - Response class
    - HTTP utilities

After:
  client/
    __init__.ext    # Exports Client
    client.ext      # Client class
    request.ext     # Request class
    response.ext    # Response class
    http.ext        # HTTP utilities
```

## Version File

### Single Source of Truth

```
# version.ext
VERSION = "1.2.3"

# Or in package manifest
# package.json: "version": "1.2.3"
# setup.py: version="1.2.3"
```

### Accessing Version

```
import my_library
print(my_library.__version__)  # "1.2.3"
```

## Configuration Files

### What Goes Where

```
Library code:
  lib/               # Source code only

Configuration:
  package.json       # Package manifest
  setup.py           # Python packaging
  Cargo.toml         # Rust packaging

Development:
  .gitignore         # Git ignore
  .editorconfig      # Editor settings
  [linter config]    # Linting rules

Documentation:
  README.md          # Main docs
  CHANGELOG.md       # Version history
  LICENSE            # License text
```

## Testing Structure

### Mirror Source Structure

```
lib/
  my_library/
    client.ext
    config.ext

tests/
  test_client.ext    # Tests client.ext
  test_config.ext    # Tests config.ext
```

### Test Fixtures

```
tests/
  fixtures/
    sample_data.json
    mock_responses/
      success.json
      error.json
```

## Documentation Structure

### Inline Documentation

```
Every public class/function should have:
- Brief description
- Parameters (with types)
- Return value
- Example usage
- Exceptions raised
```

### External Documentation

```
docs/                # For larger libraries
  getting-started.md
  api-reference.md
  examples/
    basic.md
    advanced.md
```
