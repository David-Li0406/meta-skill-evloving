# Creating a new React hook

```bash
# Hook with directory (default)
pnpm file-factory hook useDebounce --package squareone

# Hook as a flat file (no directory)
pnpm file-factory hook useLocalStorage --flat-file --package squared
```

## Command reference

| Option                 | Description                                           |
| ---------------------- | ----------------------------------------------------- |
| `--flat-file`          | Create hook as a flat file instead of a directory     |
| `--with-test`          | Include test file (default from config)               |
| `--no-test`            | Exclude test file                                     |
| `-p, --package <name>` | Target package (e.g., `squared`, `squareone`)         |
| `--dry-run`            | Show what would be created without writing files      |
| `-v, --verbose`        | Verbose output                                        |

## File structures

**Directory structure (default):**

```
src/hooks/useDebounce/
├── useDebounce.ts
├── useDebounce.test.ts
└── index.ts
```

**Flat structure (`--flat-file`):**

```
src/hooks/
├── useLocalStorage.ts
└── useLocalStorage.test.ts
```
