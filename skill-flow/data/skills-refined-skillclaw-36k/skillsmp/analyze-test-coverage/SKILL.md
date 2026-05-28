---
name: analyze-test-coverage
description: Analisa commits e sugere testes necessários (unit, integration, contract, smoke, E2E). Roda em background após commits.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task]
---

# Analyze Test Coverage (Post-Commit)

## Objetivo

Garantir que todas as novas funcionalidades tenham cobertura de testes apropriada, sugerindo automaticamente quais testes criar baseado nas mudanças do último commit.

## Quando usar

- **Automático**: Após cada commit (via post-commit hook)
- **Manual**: Quando quiser validar cobertura de um commit específico

## Regras de Análise

### 1. Mudanças em Routers (`api/routers/*.py`)

**Testes necessários:**
- ✅ **Contract Test** (OBRIGATÓRIO): Valida schema da response
- ✅ **E2E Test** (se for endpoint público crítico)

**Template Contract:**
```python
# tests/contract/test_api_contracts.py
def test_{endpoint}_contract(client):
    """Valida schema da resposta de {endpoint}."""
    response = client.get("/{endpoint}")

    assert response.status_code == 200
    body = response.json()

    # Campos obrigatórios
    assert "id" in body
    assert "name" in body
    assert isinstance(body["status"], str)
```

### 2. Mudanças em Services (`services/*.py`)

**Testes necessários:**
- ✅ **Integration Test** (OBRIGATÓRIO): Testa fluxo completo
- ⚠️ **Unit Test** (se tiver lógica complexa)

**Template Integration:**
```python
# tests/integration/test_{service}_workflow.py
def test_{service}_flow(client, db_session):
    """Testa fluxo completo do serviço."""
    # 1. Chama API
    response = client.post("/{endpoint}", json={"data": "value"})
    resource_id = response.json()["id"]

    # 2. Valida no DB
    resource = db_session.query(Model).get(resource_id)
    assert resource is not None
    assert resource.status == "expected"
```

### 3. Mudanças em Models (`models/orm/*.py`)

**Testes necessários:**
- ✅ **Schema Test** (AUTOMÁTICO - já existe validação)
- ✅ **Migration** (OBRIGATÓRIO - criar com alembic)

**Checklist:**
```bash
# 1. Criar migration (use dev database)
DATABASE_URL="postgresql://synthlab:synthlab@localhost:5432/synthlab" \
  alembic -c src/synth_lab/alembic/alembic.ini revision --autogenerate -m "Add {Model}"

# 2. Aplicar ao dev
DATABASE_URL="postgresql://synthlab:synthlab@localhost:5432/synthlab" \
  alembic -c src/synth_lab/alembic/alembic.ini upgrade head

# 3. Validar (test container aplica migrations automaticamente)
make test-fast
```

### 4. Mudanças em Repositories (`repositories/*.py`)

**Testes necessários:**
- ✅ **Integration Test** (OBRIGATÓRIO): Valida queries SQL
- ⚠️ **Unit Test** (se tiver lógica de transformação)

### 5. Mudanças em Frontend (`frontend/src/`)

**Testes necessários:**
- ✅ **E2E Test** (se for fluxo principal do usuário)
- ⚠️ **Component Test** (se for componente reutilizável)

**Template E2E:**
```typescript
// frontend/tests/e2e/{feature}.spec.ts
test('{feature} flow', async ({ page }) => {
  // 1. Navega
  await page.goto('/');

  // 2. Interage
  await page.click('text=Button');
  await page.fill('input[name="field"]', 'value');
  await page.click('button[type="submit"]');

  // 3. Valida
  await expect(page).toHaveURL(/\/success/);
});
```

## Workflow

### 1. Análise Automática (Background)

```bash
# Post-commit hook executa automaticamente
git commit -m "Add new endpoint"

# Skill roda em background (não bloqueia)
🤖 Analisando mudanças...
   ├─ api/routers/experiments.py (modificado)
   └─ services/experiment_service.py (modificado)

📊 Cobertura de Testes Recomendada:
   ├─ ✅ Contract Test: test_experiment_endpoint_contract
   ├─ ✅ Integration Test: test_experiment_creation_flow
   └─ ⚠️  E2E Test: test_create_experiment_user_flow (se for fluxo crítico)

💡 Ações sugeridas:
   1. Criar contract test (OBRIGATÓRIO antes de push)
   2. Criar integration test (RECOMENDADO)
   3. Considerar E2E test se for fluxo de usuário principal

🎯 Próximos passos:
   - Aceitar sugestões e gerar testes automaticamente? (y/n)
   - Ou criar manualmente seguindo templates acima
```

### 2. Uso Manual

```bash
# Analisar último commit
claude analyze-test-coverage

# Analisar commit específico
claude analyze-test-coverage --commit abc123

# Apenas mostrar sugestões (sem gerar testes)
claude analyze-test-coverage --dry-run

# Gerar testes automaticamente
claude analyze-test-coverage --auto-generate
```

## Algoritmo de Decisão

```python
def analyze_changes(files_changed):
    """Determina quais testes são necessários."""
    suggestions = []

    for file_path in files_changed:
        # Routers → Contract + E2E
        if "api/routers" in file_path:
            suggestions.append({
                "type": "contract",
                "priority": "OBRIGATÓRIO",
                "file": f"tests/contract/test_api_contracts.py",
                "reason": "Endpoint público deve ter contract test"
            })
            suggestions.append({
                "type": "e2e",
                "priority": "RECOMENDADO",
                "file": f"frontend/tests/e2e/{feature}.spec.ts",
                "reason": "Endpoint pode ser usado por usuários"
            })

        # Services → Integration
        elif "services/" in file_path:
            suggestions.append({
                "type": "integration",
                "priority": "OBRIGATÓRIO",
                "file": f"tests/integration/test_{service}_workflow.py",
                "reason": "Serviço precisa de teste de fluxo completo"
            })

        # Models → Schema + Migration
        elif "models/orm" in file_path:
            suggestions.append({
                "type": "migration",
                "priority": "OBRIGATÓRIO",
                "reason": "Model mudou, precisa de migration"
            })

        # Frontend → E2E
        elif "frontend/src/pages" in file_path:
            suggestions.append({
                "type": "e2e",
                "priority": "RECOMENDADO",
                "file": f"frontend/tests/e2e/{page}.spec.ts",
                "reason": "Nova página precisa de teste E2E"
            })

    return prioritize(suggestions)
```

## Priorização

1. **OBRIGATÓRIO** (bloqueia push):
   - Contract tests para endpoints públicos
   - Migrations para models
   - Integration tests para services

2. **RECOMENDADO** (aviso, mas não bloqueia):
   - E2E tests para fluxos principais
   - Unit tests para lógica complexa

3. **OPCIONAL**:
   - Component tests para UI
   - Unit tests para funções simples

## Outputs

### JSON Report (para CI/CD)
```json
{
  "commit": "abc123",
  "files_changed": 3,
  "tests_missing": [
    {
      "type": "contract",
      "priority": "OBRIGATÓRIO",
      "file": "tests/contract/test_api_contracts.py",
      "function": "test_experiment_endpoint_contract"
    }
  ],
  "coverage_status": "INCOMPLETE"
}
```

### CLI Output (para desenvolvedor)
```
📊 Análise de Cobertura de Testes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commit: abc123
Arquivos modificados: 3

🔴 OBRIGATÓRIO (2)
   ├─ Contract Test: test_experiment_endpoint_contract
   │  Arquivo: tests/contract/test_api_contracts.py
   │  Razão: Endpoint público deve ter contract test
   │
   └─ Integration Test: test_experiment_creation_flow
      Arquivo: tests/integration/test_experiment_workflow.py
      Razão: Serviço precisa de teste de fluxo completo

🟡 RECOMENDADO (1)
   └─ E2E Test: test_create_experiment_user_flow
      Arquivo: frontend/tests/e2e/create-experiment.spec.ts
      Razão: Fluxo principal de usuário

💡 Próximos passos:
   1. Gerar testes automaticamente? (y/n)
   2. Ver templates para criar manualmente? (y/n)
```

## Integração com Git Hooks

### Post-Commit Hook (Background)

```bash
#!/bin/bash
# .git/hooks/post-commit

# Roda análise em background (não bloqueia commit)
{
  claude analyze-test-coverage --async
} &

# Commit já foi feito, apenas sugere testes
```

### Pre-Push Hook (Validação)

```bash
#!/bin/bash
# .git/hooks/pre-push

# Valida que testes OBRIGATÓRIOS foram criados
if ! claude analyze-test-coverage --validate; then
  echo "❌ Testes obrigatórios estão faltando!"
  echo "   Execute: claude analyze-test-coverage --auto-generate"
  exit 1
fi
```

## Checklist de Implementação

Antes de finalizar a skill, verificar:

- [ ] Analisa corretamente mudanças em routers
- [ ] Analisa corretamente mudanças em services
- [ ] Analisa corretamente mudanças em models
- [ ] Sugere contract tests para endpoints públicos
- [ ] Sugere integration tests para services
- [ ] Sugere E2E tests para fluxos principais
- [ ] Prioriza testes (OBRIGATÓRIO vs RECOMENDADO)
- [ ] Pode rodar em background (--async)
- [ ] Pode gerar testes automaticamente (--auto-generate)
- [ ] Gera relatório JSON para CI/CD
- [ ] Integra com git hooks

## Referências

- [docs/TESTING.md](../../../docs/TESTING.md): Guia completo de testes
- [.claude/skills/update-tests.md](../update-tests.md): Templates de testes
