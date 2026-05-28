# Documentation Guidelines

## Language and Format

### Primary Language: English

- All documentation should be written in English as the primary language
- English content comes first in all documents

### Secondary Language: Korean (\_KO)

- Create separate files with `_KO` suffix for Korean translations
- Example: `README.md` (English) and `README_KO.md` (Korean)
- Use clear file naming convention: `FILENAME_KO.md`

## Format Structure

### Recommended: Separate Files

- **English**: `README.md` (or `FILENAME.md`)
- **Korean**: `README_KO.md` (or `FILENAME_KO.md`)

Each file should be complete and standalone.

### Alternative: Single File with Sections

```markdown
# English Title

English content here...

---

## 한국어 (Korean) \_KO

한국어 내용 여기...
```

**Note**: Separate files are preferred for better maintainability.

## Examples

### README Files

- **Recommended**: Separate files
  - `README.md` - English version
  - `README_KO.md` - Korean version with `_KO` suffix
- **Alternative**: Single file with sections
  - Main content in English
  - Korean translation section at the bottom with `_KO` marker

### Code Comments

- Use English for code comments
- Add Korean explanation in separate `_KO` section if needed

### API Documentation

- English as primary
- Korean translation in separate `_KO` file or section

## Guidelines

1. **Consistency**: Always use English first, Korean second
2. **Clarity**: Keep translations accurate and contextually appropriate
3. **Separation**: Use separate files (`_KO` suffix) for better organization
4. **Completeness**: Ensure both languages cover the same content
5. **File Naming**: Use `_KO` suffix for Korean files (e.g., `README_KO.md`)
