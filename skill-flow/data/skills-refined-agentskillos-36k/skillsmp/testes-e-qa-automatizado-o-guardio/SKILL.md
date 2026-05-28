---
name: Testes e QA Automatizado (O Guardião)
description: Padronização de testes unitários, integração e mocks para o ecossistema Biodiagnóstico.
---

# Skill: Testes e QA Automatizado ("O Guardião")

Esta skill fornece a infraestrutura e as diretrizes para garantir a estabilidade do Biodiagnóstico App através de testes automatizados. O objetivo é reduzir regressões e garantir que fluxos críticos (Login, Cadastro, Dashboard) funcionem conforme o esperado.

## 🎯 Objetivos
- Padronizar o uso do `pytest`.
- Fornecer mocks para serviços externos (Supabase, Cloudinary, Gemini AI) para testes rápidos e sem custos.
- Garantir que cada nova feature tenha pelo menos um teste de "Caminho Feliz" (Happy Path).

## 📂 Estrutura Recomendada
- `tests/`: Raiz dos testes (no diretório do app).
    - `unit/`: Testes de funções isoladas (utils, helpers).
    - `integration/`: Testes de fluxo (ex: Login -> Redirecionamento).
    - `conftest.py`: Fixtures globais e configuração de mocks.
- `e2e/`: Testes de ponta a ponta com Playwright.

## 🛠️ Ferramentas e Configuração
Certifique-se de que o `pytest` e `pytest-mock` estejam instalados.

### 1. Configuração do `conftest.py` (Template)
Use este template para "mockar" o Supabase e evitar chamadas reais durante os testes:

```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock
import sys

# Mock de módulos externos que podem não estar instalados no ambiente de teste CI/CD
sys.modules["reflex"] = MagicMock()

@pytest.fixture
def mock_supabase():
    """Retorna um client Supabase falso."""
    client = MagicMock()
    # Configurar retornos padrão aqui
    client.table.return_value.select.return_value.execute.return_value.data = []
    return client
```

### 2. Padrão de Nomenclatura
- Arquivos: `test_nome_do_arquivo.py`
- Funções: `test_o_que_esta_sendo_testado__resultado_esperado()`
    - Ex: `test_login__usuario_valido_deve_redirecionar()`

## 🧪 Receitas de Teste

### Testando Utils (Funções Puras)
```python
from biodiagnostico_app.utils.calculos import calcular_cv

def test_calcular_cv__input_valido():
    resultado = calcular_cv(100, 5) # valor, media
    assert resultado == 20.0 # (5/100) * 100? Revisar fórmula
```

### Mockando Gemini AI
```python
def test_analise_ia(mocker):
    mock_genai = mocker.patch("biodiagnostico_app.utils.ai.genai")
    mock_genai.GenerativeModel.return_value.generate_content.return_value.text = "Resultado Mockado"
    
    from biodiagnostico_app.services.ai_service import analisar_exame
    resultado = analisar_exame("texto do pdf")
    
    assert resultado == "Resultado Mockado"
    
### Testes E2E (Playwright)
```python
# tests/e2e/test_auth.py
from playwright.sync_api import Page, expect

def test_login_flow(page: Page):
    page.goto("http://localhost:3000/login")
    page.fill("input[name='username']", "admin")
    page.click("button[type='submit']")
    expect(page).to_have_url("http://localhost:3000/dashboard")
```
```

## 🚨 Checklist de QA ("Guardrails do Guardião")
Antes de considerar uma tarefa como "Pronta":
1. [ ] Criei um teste unitário para novas funções lógicas?
2. [ ] Se alterei o Supabase, os testes mocks ainda refletem a realidade?
3. [ ] Rodei `pytest` e todos os testes passaram (Verde)?

## 🛠️ Ferramentas de Monitoramento (Scripts)

Para garantir que o sistema não saia dos trilhos, use esses scripts de vigilância:

1.  **`testador_cliques.py`**: (O Testador) Simula um usuário clicando em tudo para ver se algo explode.
2.  **`vigia_performance.py`**: (O Vigia) Mede o tempo de carregamento e avisa se o site ficar "cansado".
3.  **`verificador_links.py`**: (O Carteiro) Checa se todos os links do sistema levam a algum lugar real.
4.  **`detetive_bugs.py`**: (O Sherlock) Analisa os registros de erro para descobrir o que quebrado.
5.  **`simulador_celular.py`**: (O Provador) Testa se o visual continua elegante em telas pequenas.

## 🏃 Como Rodar
Simplesmente execute na raiz do projeto:
```bash
pytest
```
Para ver logs detalhados (print):
```bash
pytest -s
```
