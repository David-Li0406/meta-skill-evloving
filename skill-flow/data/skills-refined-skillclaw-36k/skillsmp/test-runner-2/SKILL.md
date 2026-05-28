---
name: test-runner
description: Execução e análise de testes automatizados
triggers: [test, pytest, jest, testes, coverage]
---

# Test Runner

## Quando Usar

Ativar quando:
- Precisa executar testes
- Verificar cobertura
- Analisar testes falhando

## Detecção de Framework

### Python
```bash
# pytest (preferido)
pytest -v --tb=short

# unittest
python -m unittest discover

# Com cobertura
pytest --cov=src --cov-report=term-missing
```

### JavaScript/TypeScript
```bash
# Jest
npm test

# Vitest
npx vitest run

# Com cobertura
npm test -- --coverage
```

### Go
```bash
go test ./... -v
go test ./... -cover
```

## Flags Úteis

### pytest
| Flag | Uso |
|------|-----|
| `-v` | Verbose |
| `-x` | Para no primeiro erro |
| `--lf` | Roda últimos falhando |
| `-k "nome"` | Filtra por nome |
| `--cov=src` | Cobertura |
| `--tb=short` | Traceback curto |
| `-n auto` | Paralelo (pytest-xdist) |

### Jest
| Flag | Uso |
|------|-----|
| `--verbose` | Detalhado |
| `--coverage` | Cobertura |
| `--watch` | Watch mode |
| `-t "nome"` | Filtra por nome |
| `--bail` | Para no primeiro erro |

## Formato de Report

```markdown
## Test Report

### Sumário
| Métrica | Valor |
|---------|-------|
| Total | 42 |
| Passou | 40 ✅ |
| Falhou | 2 ❌ |
| Skipped | 0 ⏭️ |
| Cobertura | 78% |

### Testes Falhando

#### `test_user_creation`
**Arquivo:** `tests/test_user.py:45`
```
AssertionError: Expected 201, got 400
```
**Causa provável:** Validação de email falhando

---

### Cobertura por Arquivo
| Arquivo | Cobertura |
|---------|-----------|
| `src/auth.py` | 95% |
| `src/user.py` | 82% |
| `src/utils.py` | 45% ⚠️ |

### Arquivos Sem Cobertura
- `src/legacy.py`
- `src/migrations/`

### Recomendações
1. Adicionar testes para `src/utils.py`
2. Investigar `test_user_creation`
```

## Análise de Falhas

### Tipos Comuns

#### Assertion Error
```python
# Esperado vs Obtido
assert result == expected
# Verificar: lógica, dados de teste, estado
```

#### Import Error
```python
# Módulo não encontrado
# Verificar: PYTHONPATH, venv, dependências
```

#### Timeout
```python
# Teste demorou demais
# Verificar: mocks, I/O, loops infinitos
```

#### Fixture Error
```python
# Setup/teardown falhou
# Verificar: database, arquivos, conexões
```

## Cobertura de Testes

### Regras Obrigatórias

1. **Cobertura mínima por arquivo: 90%** - OBRIGATÓRIO
2. **Meta de cobertura: 100%** - Sempre tentar alcançar
3. **Análise por arquivo** - Verificar cobertura individual, não apenas geral
4. **Arquivos sem cobertura** - Identificar e justificar (ex: migrations, configs)

### Comandos de Cobertura

```bash
# pytest com cobertura detalhada por arquivo
pytest --cov=src --cov-report=term-missing --cov-report=html

# Verificar arquivos abaixo de 90%
pytest --cov=src --cov-report=term-missing | grep -E "TOTAL|^\w+.*\s+\d+%" | awk '$NF < 90'
```

---

## Boas Práticas

### Estrutura de Teste
```python
def test_should_do_something():
    # Arrange
    data = setup_data()

    # Act
    result = function_under_test(data)

    # Assert
    assert result == expected
```

### Naming
```python
# Bom
test_user_creation_with_valid_email_returns_201
test_login_with_wrong_password_returns_401

# Ruim
test_1
test_user
```

### Isolamento
- Cada teste independente
- Limpar estado entre testes
- Usar fixtures para setup comum
- Mockar dependências externas

## Framework Obrigatório (Python)

**Usar pytest para todos os testes:**
- pytest em funções (não classes)
- pytest-django para projetos Django
- pytest-asyncio para código assíncrono

## Estrutura de Testes

**A estrutura dos testes deve espelhar a estrutura da aplicação:**

```
app/
├── users/
│   ├── controllers/
│   │   └── user_controller.py
│   └── models/
│       └── user.py

tests/
├── users/
│   ├── controllers/
│   │   └── test_user_controller.py
│   └── models/
│       └── test_user.py
```

**Regra:** Quando procurar um teste de um arquivo, ele deve estar na mesma estrutura relativa.

## Mocks Obrigatórios

**Todos os acessos externos devem ser mockados:**

1. **Banco de dados:**
   - Usar fixtures do pytest-django
   - Mockar queries complexas quando necessário
   - Não usar banco real em testes

2. **Sistema de fila (Redis, RabbitMQ, etc.):**
   - Mockar todas as operações de fila
   - Não enviar mensagens reais

3. **Cache (Redis, Memcached, etc.):**
   - Mockar operações de cache
   - Não usar cache real

4. **APIs externas:**
   - Usar `responses` ou `httpx` para mockar requisições HTTP
   - Não fazer chamadas reais a APIs externas

5. **Sistema de arquivos:**
   - Usar `tempfile` ou mockar operações de arquivo
   - Não criar arquivos reais no sistema

## Nomenclatura

**Arquivos de teste:**
- `test_*.py` ou `*_test.py`
- Exemplo: `test_user_controller.py`

**Funções de teste:**
- `test_*`
- Exemplo: `test_create_user_success()`

**Descritivo:**
- `test_create_user_with_valid_data_success()`
- `test_create_user_with_invalid_email_fails()`

## Estrutura de Teste (AAA Pattern)

**Cada teste deve ter:**
1. Arrange (setup)
2. Act (execução)
3. Assert (verificação)

**Exemplo:**
```python
def test_create_user_success():
    # arrange
    user_data = {"email": "test@example.com", "name": "Test User"}
    
    # act
    result = create_user(user_data)
    
    # assert
    assert result.email == "test@example.com"
    assert result.id is not None
```

## Fixtures e conftest.py

**Usar fixtures para setup comum:**
- Criar fixtures em `conftest.py`
- Reutilizar fixtures entre testes
- Fixtures devem ser específicas e isoladas

**Exemplo:**
```python
@pytest.fixture
def user_data():
    return {"email": "test@example.com", "name": "Test User"}

@pytest.fixture
def mock_redis(monkeypatch):
    mock_redis = Mock()
    monkeypatch.setattr("app.utils.cache_system.CacheSystem", mock_redis)
    return mock_redis
```

## pytest.ini e conftest.py

**Templates obrigatórios:**
- `core/templates/django/pytest.ini`
- `core/templates/django/conftest.py`

**Usar sempre os templates como base.**

## Testes Unitários vs Integração

**Testes unitários:**
- Testam uma função/método isoladamente
- Todas as dependências mockadas
- Rápidos e determinísticos

**Testes de integração:**
- Testam múltiplos componentes juntos
- Podem usar banco de teste (isolado)
- Mais lentos, mas validam integração

**Priorizar testes unitários (maioria).**

## Checklist

- [ ] Todos os testes executados
- [ ] Testes falhando investigados
- [ ] Cobertura mínima por arquivo: **90%** (obrigatório)
- [ ] Meta de cobertura: **100%** (sempre tentar alcançar)
- [ ] Novos testes para novo código
- [ ] Testes são determinísticos
- [ ] Estrutura de testes espelha estrutura da aplicação
- [ ] Todos os acessos externos mockados (DB, APIs, cache, filas)
- [ ] Fixtures criadas em `conftest.py` para setup comum
- [ ] Testes seguem padrão AAA (Arrange, Act, Assert)
- [ ] pytest.ini configurado com cobertura mínima 90%
