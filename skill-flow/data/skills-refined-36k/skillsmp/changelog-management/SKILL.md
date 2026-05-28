---
name: changelog-management
description: Gerenciamento obrigatório de CHANGELOG e versionamento seguindo Keep a Changelog e Semantic Versioning em todos os projetos.
triggers: [changelog, versioning, release, changes, updates, semantic versioning, tags]
source: https://keepachangelog.com/
---

# CHANGELOG Management

**Regras obrigatórias para manter CHANGELOG em todos os projetos seguindo o padrão Keep a Changelog.**

---

## Quando Usar

Aplicar esta skill em **TODOS os projetos** quando:
- Criando ou modificando qualquer arquivo
- Fazendo commits
- Preparando releases
- Documentando mudanças

---

## Regras CRÍTICAS (NÃO NEGOCIÁVEIS)

1. **CHANGELOG obrigatório em todos os projetos:**
   - Todo projeto **DEVE** ter um arquivo `CHANGELOG.md` na raiz
   - Seguir rigorosamente o formato [Keep a Changelog](https://keepachangelog.com/)
   - Usar [Semantic Versioning](https://semver.org/)

2. **Agentes só podem modificar versão não lançada:**
   - **NUNCA** modificar versões já lançadas (com tags como `[1.2.0]`)
   - **SEMPRE** adicionar mudanças em `[Unreleased]`
   - Versões antigas só podem ser modificadas com permissão explícita do usuário

3. **Todas as mudanças devem estar no CHANGELOG:**
   - **SEMPRE** documentar mudanças no CHANGELOG antes de commitar
   - Incluir resumos concisos mas completos
   - Categorizar corretamente: Added, Changed, Deprecated, Removed, Fixed, Security

4. **Formato obrigatório:**
   ```markdown
   # Changelog
   
   All notable changes to this project will be documented in this file.
   
   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
   and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
   
   ## [Unreleased]
   
   ### Added
   - Nova funcionalidade X
   
   ### Changed
   - Melhoria Y
   
   ### Fixed
   - Correção Z
   
   ## [1.2.0] - 2025-12-08
   
   ### Added
   - Versão anterior...
   ```

---

## Categorias do CHANGELOG

### Added
- Novas funcionalidades
- Novos arquivos, módulos, scripts
- Novas dependências
- Novas configurações

### Changed
- Mudanças em funcionalidades existentes
- Refatorações
- Atualizações de dependências
- Mudanças de comportamento

### Deprecated
- Funcionalidades que serão removidas em versões futuras
- APIs obsoletas

### Removed
- Funcionalidades removidas
- Arquivos deletados
- Dependências removidas

### Fixed
- Correções de bugs
- Correções de segurança
- Correções de performance

### Security
- Vulnerabilidades corrigidas
- Melhorias de segurança
- Remoção de dados sensíveis

---

## Workflow Obrigatório

1. **Antes de fazer mudanças:**
   - Verificar se `CHANGELOG.md` existe
   - Se não existir, criar seguindo o template

2. **Durante as mudanças:**
   - Documentar cada mudança relevante
   - Categorizar corretamente
   - Adicionar em `[Unreleased]`

3. **Antes de commitar:**
   - Verificar se todas as mudanças estão no CHANGELOG
   - Garantir que está em `[Unreleased]`
   - Não modificar versões já lançadas

4. **Ao criar release:**
   - Mover `[Unreleased]` para nova versão com data
   - Criar tag Git correspondente
   - Manter link de comparação no final
   - Atualizar número de versão em documentação
   - Criar release no GitHub (se aplicável)

---

## Exemplo de Entrada

```markdown
## [Unreleased]

### Added
- Nova skill `changelog-management` para gerenciamento obrigatório de CHANGELOG
- Script `utils/database.py` genérico para queries SQL puro (Django)

### Changed
- `.gitignore` simplificado usando pastas ao invés de listar arquivos
- `skills/README.md` atualizado para referenciar scripts genéricos

### Security
- Removidas referências a projetos de trabalho confidenciais
```

---

## Checklist

- [ ] `CHANGELOG.md` existe na raiz do projeto
- [ ] Todas as mudanças documentadas em `[Unreleased]`
- [ ] Categorias corretas usadas (Added/Changed/Fixed/etc)
- [ ] Versões antigas não foram modificadas
- [ ] Formato segue Keep a Changelog
- [ ] Links de comparação atualizados (se aplicável)

---

## Template Inicial

Se o projeto não tem CHANGELOG, criar com este template:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup

---

[Unreleased]: https://github.com/USER/REPO/compare/v1.0.0...HEAD
```

---

## Semantic Versioning

Este projeto segue [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html):

- **MAJOR** (X.0.0): Mudanças incompatíveis na API
- **MINOR** (x.Y.0): Novas funcionalidades compatíveis
- **PATCH** (x.y.Z): Correções de bugs compatíveis

### Exemplos

- `1.0.0` → `1.1.0`: Nova funcionalidade adicionada
- `1.1.0` → `1.1.1`: Bug corrigido
- `1.1.1` → `2.0.0`: Mudança que quebra compatibilidade

---

## Releases

### Criando uma Release

1. **Atualizar versão nos arquivos**
   - Atualizar `CHANGELOG.md` (mover `[Unreleased]` para nova versão)
   - Atualizar número de versão em documentação (se aplicável)

2. **Commit e Tag**
   ```bash
   git commit -m "chore: release v1.2.0"
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin main --tags
   ```

3. **Criar Release no GitHub** (se aplicável)
   - Ir para releases do repositório
   - Clicar em "Create a new release"
   - Selecionar a tag criada
   - Adicionar título: "v1.2.0 - Nome da Release"
   - Copiar conteúdo relevante do CHANGELOG
   - Publicar release

---

## Segurança

### Proteção de Tokens

Antes de commitar, sempre verificar:

```bash
# Verificar diff antes de commitar
git diff

# Procurar por tokens
grep -r "ntn_" .
grep -r "secret_" .
grep -r "password" .
```

### Placeholders Seguros

Use sempre placeholders em documentação:

```python
# ✗ ERRADO - Nunca commite tokens reais
TOKEN = 'ntn_ABC123XYZ456REAL_TOKEN_HERE'

# ✓ CORRETO - Use placeholders
TOKEN = 'ntn_YOUR_NOTION_TOKEN_HERE'
```

---

## Recursos

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

