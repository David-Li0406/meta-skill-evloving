# Pattern 6: Code Organization

**Problem**: Code is scattered without clear structure. New features have no obvious home. Files grow to thousands of lines.

**Solution**: Follow language conventions for project layout. One module = one responsibility. Keep files focused and small.

---

## Concept

Code Organization answers: **"Where does this code go?"**

Good organization provides:
1. **Predictability** — New developers find code where they expect
2. **Separation** — Changes are isolated to relevant files
3. **Testability** — Small, focused modules are easy to test
4. **Maintainability** — Less cognitive load

---

## Python CLI Layout

```
my-tool/
├── pyproject.toml           # Project metadata, dependencies, entry points
├── README.md                # User documentation
├── CLAUDE.md                # AI collaboration guide
├── src/
│   └── my_tool/             # Package directory
│       ├── __init__.py      # Public API exports
│       ├── __main__.py      # python -m my_tool entry point
│       ├── cli.py           # Argument parsing (no business logic)
│       ├── config.py        # Configuration dataclasses
│       ├── models.py        # Domain models (dataclasses)
│       ├── <domain>.py      # Core business logic
│       ├── formatters.py    # Output formatting
│       └── utils.py         # Pure utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_cli.py
│   ├── test_<domain>.py
│   └── fixtures/            # Test data files
└── .gitignore
```

### Module Responsibilities

```python
# __init__.py - Public API only
"""My Tool - A tool for doing things."""
from .models import Config, Result
from .pipeline import Pipeline

__version__ = "1.0.0"
__all__ = ["Config", "Result", "Pipeline", "__version__"]

# __main__.py - Entry point
"""Allow running with python -m my_tool."""
from .cli import main

if __name__ == "__main__":
    main()

# cli.py - Argument parsing ONLY
"""Command-line interface. No business logic here."""
import argparse
from .config import Config
from .pipeline import Pipeline

def main():
    parser = argparse.ArgumentParser(description="My Tool")
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    config = Config(
        input_path=args.input,
        output_path=args.output,
        verbose=args.verbose
    )
    pipeline = Pipeline(config)
    pipeline.run()

# config.py - Configuration models
"""Configuration dataclasses."""
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    input_path: str
    output_path: str | None = None
    verbose: bool = False

# models.py - Domain models
"""Domain models. No business logic, just data structures."""
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

@dataclass
class Task:
    id: str
    name: str
    status: Status = Status.PENDING

# pipeline.py - Core business logic
"""Main processing logic."""
from .config import Config
from .models import Task

class Pipeline:
    def __init__(self, config: Config):
        self.config = config

    def run(self):
        # Core logic here
        pass

# utils.py - Pure utility functions
"""Utility functions. Pure, no side effects."""
def sanitize_filename(name: str) -> str:
    return name.replace("/", "_").replace("\\", "_")
```

---

## Node.js CLI Layout

```
my-tool/
├── package.json             # Project metadata, dependencies, bin
├── README.md
├── CLAUDE.md
├── src/
│   ├── cli.js              # Entry point with shebang
│   ├── config.js           # Configuration loading
│   ├── <domain>.js         # Core business logic
│   ├── state.js            # Persistence layer
│   └── utils.js            # Pure utilities
├── tests/
│   ├── setup.js            # Test configuration
│   ├── cli.test.js
│   └── <domain>.test.js
├── __mocks__/              # Manual mocks for external deps
│   └── googleapis.js
└── .gitignore
```

### Module Responsibilities

```javascript
// cli.js - Entry point
#!/usr/bin/env node
const { Command } = require('commander');
const { processItems } = require('./processor');
const { loadConfig } = require('./config');

const program = new Command();

program
  .name('my-tool')
  .description('A tool for doing things')
  .version('1.0.0');

program
  .command('process <input>')
  .option('-o, --output <path>', 'Output path')
  .option('-v, --verbose', 'Verbose output')
  .action(async (input, options) => {
    const config = loadConfig(options);
    await processItems(input, config);
  });

program.parse();

// config.js - Configuration
const path = require('path');
const os = require('os');

const CONFIG_DIR = path.join(os.homedir(), '.config', 'my-tool');

function loadConfig(options = {}) {
  return {
    verbose: options.verbose ?? false,
    outputPath: options.output ?? null,
    configDir: CONFIG_DIR
  };
}

module.exports = { loadConfig, CONFIG_DIR };

// processor.js - Core logic
async function processItems(input, config) {
  // Core business logic here
}

module.exports = { processItems };

// state.js - Persistence
const fs = require('fs');
const path = require('path');

function saveState(state, filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, JSON.stringify(state, null, 2));
}

function loadState(filePath) {
  if (!fs.existsSync(filePath)) return null;
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

module.exports = { saveState, loadState };

// utils.js - Pure utilities
function sanitizeFilename(name) {
  return name.replace(/[/\\]/g, '_');
}

module.exports = { sanitizeFilename };
```

---

## TypeScript Browser Extension Layout

```
my-extension/
├── manifest.json           # Extension configuration
├── package.json           # Build dependencies
├── tsconfig.json          # TypeScript configuration
├── src/
│   ├── ts/
│   │   ├── types.ts       # Type definitions
│   │   ├── background.ts  # Service worker
│   │   ├── popup.ts       # Popup controller
│   │   ├── dashboard.ts   # Dashboard page controller
│   │   ├── state.ts       # State management
│   │   └── utils.ts       # Pure utilities
│   ├── html/
│   │   ├── popup.html
│   │   └── dashboard.html
│   └── test/
│       └── setup.ts       # Test setup with mocks
├── icons/
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
├── dist/                  # Build output
└── .gitignore
```

---

## Principles

### 1. One Module = One Responsibility

```python
# BAD: cli.py does everything
def main():
    args = parse_args()
    data = load_data(args.input)
    processed = transform_data(data)
    formatted = format_output(processed)
    save_output(formatted, args.output)

# GOOD: cli.py only parses args, delegates to pipeline
def main():
    args = parse_args()
    config = Config.from_args(args)
    pipeline = Pipeline(config)
    pipeline.run()
```

### 2. Imports Flow One Direction

```
cli.py
  ├── imports config.py
  ├── imports pipeline.py
  │     ├── imports models.py
  │     ├── imports processor.py
  │     └── imports formatter.py
  └── imports utils.py (anyone can import utils)
```

Never create circular imports. If A imports B, B should never import A.

### 3. Keep Files Under 300 Lines

When a file exceeds ~300 lines, split it:

```python
# BAD: processor.py (800 lines)
class Processor:
    def preprocess(self): ...  # 200 lines
    def process(self): ...     # 400 lines
    def postprocess(self): ... # 200 lines

# GOOD: Split into focused modules
# preprocessor.py (200 lines)
# processor.py (400 lines)
# postprocessor.py (200 lines)
```

### 4. Group by Feature, Not Type

For larger projects:

```
# BAD: Group by type
src/
├── models/
│   ├── user.py
│   ├── post.py
│   └── comment.py
├── services/
│   ├── user_service.py
│   ├── post_service.py
│   └── comment_service.py
└── handlers/
    ├── user_handler.py
    ├── post_handler.py
    └── comment_handler.py

# GOOD: Group by feature
src/
├── users/
│   ├── models.py
│   ├── service.py
│   └── handler.py
├── posts/
│   ├── models.py
│   ├── service.py
│   └── handler.py
└── shared/
    └── utils.py
```

---

## Checklist

- [ ] Project follows language conventions (src/, tests/)
- [ ] Entry point (cli.py/cli.js) only parses args
- [ ] Models separate from business logic
- [ ] Utils are pure functions (no side effects)
- [ ] No circular imports
- [ ] Files under ~300 lines
- [ ] New features have obvious home

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| God file | One file does everything | Split by responsibility |
| Deep nesting | `src/a/b/c/d/e/f.py` | Flatten to 2-3 levels |
| Circular imports | A imports B imports A | Restructure dependencies |
| `helpers.py` | Grab bag of random functions | Name by what it does |
