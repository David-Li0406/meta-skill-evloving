# Skill: Analyze Test Coverage

Analisa commits automaticamente e sugere testes necessários (unit, integration, contract, smoke, E2E).

## Uso

### Modo Automático (Post-Commit Hook)

A skill roda automaticamente em background após cada commit:

```bash
git commit -m "Add new endpoint"

# Hook executa automaticamente:
# 🤖 Analisando cobertura de testes para este commit...
#
# 📊 Análise de Cobertura de Testes (Commit)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Commit: HEAD
# Arquivos modificados: 3
#
# 🔴 OBRIGATÓRIO (2)
#    ├─ CONTRACT Test: test_experiments_contract
#    │  Arquivo: tests/contract/test_api_contracts.py
#    │  Razão: Endpoint público experiments deve ter contract test
#    ...
```

### Modo Manual

```bash
# Analisar último commit
python scripts/analyze_test_coverage.py --commit HEAD

# Analisar commit específico
python scripts/analyze_test_coverage.py --commit abc123

# Ver templates de testes
python scripts/analyze_test_coverage.py --commit HEAD --show-templates

# Output JSON (para CI/CD)
python scripts/analyze_test_coverage.py --commit HEAD --json
```

### Via Claude Code Skill

```bash
# Invoca a skill através do Claude Code
claude analyze-test-coverage
```

## O que analisa

### Mudanças em Routers (`api/routers/*.py`)

**Sugere:**
- ✅ Contract Test (OBRIGATÓRIO)
- ⚠️ E2E Test (RECOMENDADO)

### Mudanças em Services (`services/*.py`)

**Sugere:**
- ✅ Integration Test (OBRIGATÓRIO)

### Mudanças em Models (`models/orm/*.py`)

**Sugere:**
- ✅ Migration via Alembic (OBRIGATÓRIO)
- Schema Test (automático)

### Mudanças em Repositories (`repositories/*.py`)

**Sugere:**
- ✅ Integration Test (OBRIGATÓRIO)

### Mudanças em Frontend (`frontend/src/pages/*.tsx`)

**Sugere:**
- ⚠️ E2E Test (RECOMENDADO)

## Prioridades

### 🔴 OBRIGATÓRIO
Testes que **devem** ser criados antes do push:
- Contract tests para endpoints públicos
- Integration tests para services e repositories
- Migrations para models

### 🟡 RECOMENDADO
Testes fortemente sugeridos:
- E2E tests para fluxos principais
- Unit tests para lógica complexa

### ⚪ OPCIONAL
Testes nice-to-have:
- Component tests
- Unit tests para funções simples

## Integração com Git Hooks

### Post-Commit (Atual)

Roda **em background** após cada commit para não bloquear:

```bash
# .git/hooks/post-commit
# Analisa commit em background
{
    python scripts/analyze_test_coverage.py --commit HEAD
} &
```

### Pre-Push (Futuro)

Pode ser configurado para **bloquear** push se faltar testes obrigatórios:

```bash
# .git/hooks/pre-push
if ! python scripts/analyze_test_coverage.py --commit HEAD; then
    echo "❌ Testes OBRIGATÓRIOS faltando!"
    exit 1
fi
```

## Output Formats

### Console (Default)

```
📊 Análise de Cobertura de Testes (Commit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Commit: HEAD
Arquivos modificados: 3

🔴 OBRIGATÓRIO (1)
   ├─ CONTRACT Test: test_experiments_contract
   │  Arquivo: tests/contract/test_api_contracts.py
   │  Razão: Endpoint público experiments deve ter contract test

💡 Próximos passos:
   1. Criar testes OBRIGATÓRIOS antes do push
   2. Executar novamente com --show-templates para ver exemplos
```

### Console com Templates

```bash
python scripts/analyze_test_coverage.py --commit HEAD --show-templates
```

```
🔴 OBRIGATÓRIO (1)
   ├─ CONTRACT Test: test_experiments_contract
   │  Arquivo: tests/contract/test_api_contracts.py
   │  Razão: Endpoint público experiments deve ter contract test
   │  Template:
   │    def test_experiments_contract(client):
   │        """Valida schema da resposta de /experiments."""
   │        response = client.get("/experiments")
   │
   │        assert response.status_code == 200
   │        body = response.json()
   │
   │        # Campos obrigatórios (ajustar conforme schema real)
   │        assert "id" in body
   │        assert "name" in body
```

### JSON (para CI/CD)

```bash
python scripts/analyze_test_coverage.py --commit HEAD --json
```

```json
{
  "commit": "abc123",
  "files_changed": [
    "src/synth_lab/api/routers/experiments.py"
  ],
  "tests_missing": [
    {
      "type": "contract",
      "priority": "OBRIGATÓRIO",
      "file": "tests/contract/test_api_contracts.py",
      "function": "test_experiments_contract",
      "reason": "Endpoint público experiments deve ter contract test",
      "template": "def test_experiments_contract(client):..."
    }
  ],
  "coverage_status": "INCOMPLETE"
}
```

## Exit Codes

- `0`: Nenhum teste obrigatório faltando (ou commit OK)
- `1`: Testes obrigatórios faltando

Útil para CI/CD:

```bash
if python scripts/analyze_test_coverage.py --commit $CI_COMMIT_SHA; then
    echo "✅ Cobertura OK"
else
    echo "❌ Testes obrigatórios faltando"
    exit 1
fi
```

## Desabilitar

### Temporariamente
```bash
# Desabilita hook para um commit
git commit --no-verify -m "WIP: work in progress"
```

### Permanentemente
```bash
# Remove o hook
rm .git/hooks/post-commit
```

## Referências

- [SKILL.md](./SKILL.md): Documentação técnica completa
- [docs/TESTING.md](../../../docs/TESTING.md): Guia de testes do projeto
- [scripts/analyze_test_coverage.py](../../../scripts/analyze_test_coverage.py): Implementação
