# Troubleshooting

## LSP Returns No Results

**Symptoms:** `findReferences` or `documentSymbol` returns empty

**Checks:**
1. Verify file type has LSP support (Python, TypeScript, Go, etc.)
2. Ensure language server is running
3. Check that symbol exists at specified line/character position

**Resolution:** Fall back to Grep-based workflow

## Rename Breaks Imports

**Symptoms:** After rename, imports fail to resolve

**Checks:**
1. Verify all import statements were updated
2. Check for dynamic imports or string-based references
3. Look for re-exports that may have been missed

**Resolution:**
1. Use `Grep(pattern="OldName")` to find remaining references
2. Manually update any missed locations

## Extract Creates Invalid Code

**Symptoms:** Extracted function has wrong signature or missing variables

**Checks:**
1. Verify all input variables identified
2. Check for closures or captured variables
3. Ensure return values properly handled

**Resolution:** Manually adjust function signature and call site

## Dead Code Detection False Positives

**Symptoms:** LSP says zero references, but code is used

**Causes:**
- Dynamic references (`getattr`, reflection)
- String-based lookups
- External entry points (CLI, API endpoints)
- Test-only code

**Resolution:** Check for dynamic usage patterns before removal
