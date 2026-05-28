# Changelog - Analyze Test Coverage Skill

## [1.0.0] - 2026-01-14

### ✨ Implementação Inicial

Skill completa para análise automática de cobertura de testes após commits.

### 📦 Arquivos Criados

- `.claude/skills/analyze-test-coverage/SKILL.md`: Documentação técnica completa
- `.claude/skills/analyze-test-coverage/README.md`: Guia de uso
- `.claude/skills/analyze-test-coverage/CHANGELOG.md`: Este arquivo
- `.git/hooks/post-commit`: Hook Git para execução automática

### 🔧 Arquivos Modificados

- `scripts/analyze_test_coverage.py`:
  - Adicionado análise de commits específicos (`--commit`)
  - Adicionado templates de código (`--show-templates`)
  - Adicionado output JSON (`--json`)
  - Mantida compatibilidade com análise global existente

### ✅ Funcionalidades

#### Análise Automática
- Roda em background após cada commit (não bloqueia workflow)
- Identifica arquivos modificados por tipo
- Sugere testes apropriados baseado no tipo de arquivo

#### Tipos de Análise por Arquivo

**Routers** (`api/routers/*.py`):
- Contract Test (OBRIGATÓRIO)
- E2E Test (RECOMENDADO)

**Services** (`services/*.py`):
- Integration Test (OBRIGATÓRIO)

**Models** (`models/orm/*.py`):
- Migration via Alembic (OBRIGATÓRIO)
- Schema Test (automático)

**Repositories** (`repositories/*.py`):
- Integration Test (OBRIGATÓRIO)

**Frontend Pages** (`frontend/src/pages/*.tsx`):
- E2E Test (RECOMENDADO)

#### Priorização

**🔴 OBRIGATÓRIO**: Bloqueiam push (se configurado no pre-push)
- Contract tests para endpoints públicos
- Integration tests para services/repositories
- Migrations para models

**🟡 RECOMENDADO**: Fortemente sugeridos
- E2E tests para fluxos principais
- Unit tests para lógica complexa

**⚪ OPCIONAL**: Nice-to-have
- Component tests
- Unit tests para funções simples

#### Templates de Código

Cada sugestão inclui template pronto para copiar:
- Contract Test template
- Integration Test template
- E2E Test template
- Migration commands

#### Outputs

**Console padrão**:
```
📊 Análise de Cobertura de Testes (Commit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Commit: HEAD
Arquivos modificados: 3

🔴 OBRIGATÓRIO (2)
   ├─ CONTRACT Test: test_experiments_contract
   │  Arquivo: tests/contract/test_api_contracts.py
   │  Razão: Endpoint público experiments deve ter contract test
   ...
```

**JSON** (para CI/CD):
```json
{
  "commit": "abc123",
  "files_changed": ["src/synth_lab/api/routers/experiments.py"],
  "tests_missing": [...],
  "coverage_status": "INCOMPLETE"
}
```

#### Exit Codes
- `0`: Nenhum teste obrigatório faltando
- `1`: Testes obrigatórios faltando (útil para CI/CD)

### 🚀 Uso

#### Automático
```bash
git commit -m "Add new feature"
# Hook roda automaticamente em background
```

#### Manual
```bash
# Analisar último commit
python scripts/analyze_test_coverage.py --commit HEAD

# Com templates
python scripts/analyze_test_coverage.py --commit HEAD --show-templates

# Output JSON
python scripts/analyze_test_coverage.py --commit HEAD --json

# Commit específico
python scripts/analyze_test_coverage.py --commit abc123
```

#### Via Skill
```bash
claude analyze-test-coverage
```

### ⚙️ Configuração

#### Desabilitar Temporariamente
```bash
git commit --no-verify
```

#### Desabilitar Permanentemente
```bash
rm .git/hooks/post-commit
```

#### Adicionar Validação no Pre-Push
```bash
# .git/hooks/pre-push
if ! python scripts/analyze_test_coverage.py --commit HEAD; then
    echo "❌ Testes OBRIGATÓRIOS faltando!"
    exit 1
fi
chmod +x .git/hooks/pre-push
```

### 🎯 Benefícios

1. **Não bloqueia desenvolvimento**: Execução em background
2. **Zero configuração**: Funciona imediatamente após instalação
3. **Sugestões contextuais**: Inteligência baseada no tipo de arquivo
4. **Templates prontos**: Código pronto para copiar e ajustar
5. **Integração CI/CD**: Output JSON + exit codes
6. **Priorização clara**: Sabe o que é crítico vs nice-to-have
7. **Mantém compatibilidade**: Análise global existente continua funcionando

### 📚 Referências

- [SKILL.md](./SKILL.md): Documentação técnica detalhada
- [README.md](./README.md): Guia de uso completo
- [docs/TESTING.md](../../../docs/TESTING.md): Guia geral de testes
- [scripts/analyze_test_coverage.py](../../../scripts/analyze_test_coverage.py): Implementação

### 🔮 Futuras Melhorias

- [ ] Geração automática de testes (não apenas sugestão)
- [ ] Análise de múltiplos commits (range)
- [ ] Integração com GitHub Actions
- [ ] Detecção de testes existentes que precisam atualização
- [ ] Análise de cobertura real (pytest-cov integration)
- [ ] Sugestões para testes de regressão
- [ ] Dashboard de cobertura histórica
