---
type: skill
name: Documentation
description: Generate and update technical documentation
skillSlug: documentation
phases: [P, C]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Documentation Skill

## When to Use

Use this skill when:
- Creating or updating project documentation (README.md, API docs)
- Documenting functions and modules in the codebase
- Updating documentation in `.context/docs/` directory
- Creating user guides and technical specifications

## Documentation Standards

### README Structure

The project uses a clear README structure following this pattern:

1. **Title & Description** - Clear project purpose
2. **Funcionalidades** - Feature list with checkmarks
3. **Instalação** - Installation steps including dependencies
4. **Uso** - Usage examples with code blocks
5. **Estrutura do Banco de Dados** - Database schema documentation
6. **Exemplos** - Practical examples
7. **Notas** - Important notes and limitations

### Code Documentation

- **Function Docstrings**: Use triple-quoted strings with Portuguese descriptions
  ```python
  def extract_text_from_pdf(filepath):
      """Extrai texto de um arquivo PDF."""
  ```

- **Inline Comments**: Portuguese comments for complex logic
- **Module Docstrings**: Document purpose at module level

### File Organization

- Main documentation: `contrato/README.md`
- Context documentation: `.context/docs/`
- Agent playbooks: `.context/agents/`
- Skills: `.context/skills/`

## Documentation Guidelines

### README.md

Structure:
- **Funcionalidades**: List key features with ✅ checkmarks
- **Instalação**: Step-by-step installation with code blocks
- **Uso**: CLI examples with proper formatting
- **Estrutura do Banco de Dados**: Document database schema
- **Notas**: Important limitations and notes

Example format from project:
```markdown
## Funcionalidades

- ✅ Indexação automática de PDFs
- ✅ Extração completa de texto
- ✅ Indicadores de sucesso
```

### API Documentation

For CLI scripts, document:
- Command syntax
- Options and flags
- Example usage
- Output format

### Database Documentation

Document:
- Table schemas
- Indexes and triggers
- Relationships
- Query patterns

## Examples from Codebase

### Good Documentation Example

From `contrato/README.md`:
```markdown
### 1. Indexar Documentos

Primeiro, indexe todos os documentos PDF da pasta:

```bash
python indexer.py
```

O script irá:
- Percorrer todos os subdiretórios procurando arquivos PDF
- Extrair o texto de cada PDF (método direto primeiro)
- Se necessário, usar OCR para PDFs escaneados (imagens)
```

### Function Documentation Pattern

```python
def extract_text_from_pdf(filepath):
    """Extrai texto de um arquivo PDF usando pdfplumber e OCR como fallback."""
    # Implementation...
```

## Best Practices

1. **Always in Portuguese** - Project documentation is in Portuguese
2. **Code Examples** - Include practical CLI examples
3. **Clear Structure** - Use headers and lists for readability
4. **Keep Updated** - Update docs when adding features
5. **Cross-Reference** - Link related documentation files

## Checklist

When creating/updating documentation:
- [ ] Portuguese language used
- [ ] Code examples included and tested
- [ ] Installation steps verified
- [ ] Usage examples match actual CLI
- [ ] Database schema documented
- [ ] Cross-references to related docs added
- [ ] README.md updated if adding new features
