---
type: skill
name: Api Design
description: Design RESTful APIs following best practices
skillSlug: api-design
phases: [P, R]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# API Design Skill

## When to Use

Use this skill when:
- Designing CLI interfaces
- Planning function signatures
- Creating export formats
- Designing data structures

## CLI API Design

### Command Structure

**Pattern from project:**
```
script.py [command] [options] [arguments]
```

**Examples:**
```bash
# Simple command
python indexer.py

# Command with arguments
python search.py "termo de busca"

# Command with options
python search.py "termo" --category anexo --export results.csv

# Command with flags
python search.py --list-categories
```

### Function API Design

**Pattern: Function Signatures**

```python
# Good: Clear parameters with defaults
def search(query, category=None, contract_number=None, export_csv=None):
    """Busca documentos no banco de dados."""
```

### Argument Parsing Pattern

Use `argparse` for CLI:
```python
parser = argparse.ArgumentParser(description='Busca documentos indexados')
parser.add_argument('query', nargs='?', help='Termo de busca')
parser.add_argument('--category', '-c', help='Filtrar por categoria')
```

## Data Structure Design

### Return Values

**Pattern: Dictionary for complex data**
```python
return {
    "category": category,
    "contract_number": contract_number,
    "document_type": document_type,
    "document_number": document_number
}
```

### Metadata Format

**Pattern: JSON metadata**
```python
metadata = {
    "size": stat.st_size,
    "size_mb": round(stat.st_size / (1024 * 1024), 2),
    "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
}
metadata_json = json.dumps(metadata, ensure_ascii=False)
```

## Export Format Design

### CSV Export

**Pattern: Consistent column names**
```python
data.append({
    "Arquivo": filename,
    "Categoria": category,
    "Tipo": doc_type,
    "Contrato": contract_number or "",
    "Trecho": fragment,
    "Caminho": filepath
})
```

## API Versioning

Current approach: CLI-based (no versioning needed)
- Functions can evolve
- CLI commands stable
- Export formats consistent

## Design Principles

1. **Consistency**: Similar functions have similar signatures
2. **Clarity**: Parameter names are self-documenting
3. **Flexibility**: Optional parameters for common use cases
4. **Error Handling**: Clear error messages in Portuguese

## Examples from Codebase

### Good API Design

```python
def search(query, category=None, contract_number=None, export_csv=None):
    """Busca documentos no banco de dados."""
    # Clear parameters
    # Optional filters
    # Export option
```

### Good CLI Design

```bash
python search.py "termo" --category anexo --contract TNE_JU_COM_0002-13 --export results.csv
```

## Checklist

- [ ] Clear function signatures
- [ ] Consistent naming
- [ ] Optional parameters have defaults
- [ ] Error handling documented
- [ ] Examples provided
- [ ] Export formats consistent
