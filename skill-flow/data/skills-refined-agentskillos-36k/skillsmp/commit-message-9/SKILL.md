---
type: skill
name: Commit Message
description: Generate commit messages following conventional commits with scope detection
skillSlug: commit-message
phases: [E, C]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Commit Message Skill

## When to Use

Use this skill when:
- Creating commit messages for code changes
- Following project commit conventions
- Ensuring clear commit history
- Grouping related changes logically

## Commit Message Format

Follow **Conventional Commits** format with scope detection:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Commit Types

Based on project patterns, use these types:

- `feat`: Nova funcionalidade
- `fix`: Correção de bugs
- `docs`: Mudanças na documentação
- `refactor`: Refatoração de código
- `perf`: Melhorias de performance
- `test`: Adição ou correção de testes
- `chore`: Tarefas de manutenção

## Scopes for This Project

Detect scope from files changed:

- `indexer`: Changes to `indexer.py`
- `search`: Changes to `search.py`
- `organize`: Changes to `organize.py`
- `metrics`: Changes to `metrics.py`
- `database`: Database schema changes
- `ocr`: OCR-related changes
- `docs`: Documentation updates
- `deps`: Dependency changes

## Examples from Project Context

### Feature Addition

```
feat(indexer): adiciona suporte a OCR para PDFs escaneados

- Implementa extração com pytesseract como fallback
- Adiciona métricas de extração ao banco de dados
- Garante extração completa mesmo de PDFs escaneados
```

### Bug Fix

```
fix(search): corrige tratamento de caracteres especiais em busca

Corrige problema onde termos com acentos não eram encontrados
corretamente em buscas FTS5.
```

### Documentation

```
docs(readme): atualiza instruções de instalação com OCR

Adiciona seção sobre instalação do Tesseract OCR para garantir
extração completa de todos os documentos.
```

### Refactoring

```
refactor(indexer): melhora organização das funções de extração

Separa lógica de extração direta e OCR em funções distintas
para melhor manutenibilidade.
```

### Performance

```
perf(database): adiciona índices para melhorar performance de busca

Cria índices em category e contract_number para acelerar
queries filtradas.
```

### Testing

```
test(indexer): adiciona testes para classificação de documentos

Testa classificação de contratos, aditivos e anexos com
diferentes padrões de nomes de arquivo.
```

### Chore

```
chore(deps): atualiza pdfplumber para versão 0.10.0

Atualiza dependência para versão mais recente com melhorias
de performance.
```

## Commit Message Best Practices

1. **Portuguese**: Use português para descrições (project standard)
2. **Clear Scope**: Always include scope when applicable
3. **Concise**: Keep first line under 72 characters
4. **Body**: Use body for detailed explanations when needed
5. **Breaking Changes**: Use `BREAKING CHANGE:` in footer if applicable

## Scope Detection Rules

Based on file paths:
- `contrato/indexer.py` → `(indexer)`
- `contrato/search.py` → `(search)`
- `contrato/organize.py` → `(organize)`
- `contrato/metrics.py` → `(metrics)`
- `contrato/requirements.txt` → `(deps)`
- `contrato/README.md` → `(docs)`
- Database files → `(database)`

## Examples from Codebase Context

### Adding OCR Feature

```
feat(indexer): adiciona OCR para extração de PDFs escaneados

Implementa extração completa de texto usando Tesseract OCR
como fallback quando pdfplumber não extrai texto suficiente.
Adiciona tabela extraction_metrics para rastrear métodos
de extração utilizados.
```

### Fixing Classification

```
fix(indexer): corrige classificação de anexos com partes

Ajusta regex para identificar corretamente anexos divididos
em partes (ex: Anexo III - Parte I).
```

### Database Changes

```
feat(database): adiciona tabela de métricas de extração

Cria tabela extraction_metrics para armazenar estatísticas
detalhadas de cada extração, incluindo método utilizado e
tempo de processamento.
```

## Checklist

When creating commit message:
- [ ] Type correctly identified (feat, fix, docs, etc.)
- [ ] Scope detected from changed files
- [ ] Description clear and in Portuguese
- [ ] Body explains "why" not just "what" (if needed)
- [ ] Breaking changes documented in footer
- [ ] Message follows conventional commits format
