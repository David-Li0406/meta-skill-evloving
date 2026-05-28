---
name: postman-development
description: Skill completa para desenvolvimento e documentação de APIs usando Postman, incluindo automação, CI/CD, e geração a partir de OpenAPI.
triggers: [postman, api documentation, newman, collection, openapi, jwt, session auth, api testing]
---

# Postman Development - Skill Completa

**Skill completa para desenvolvimento, documentação e automação de APIs usando Postman, seguindo padrões de produção e melhores práticas de mercado.**

---

## Quando Usar

Aplicar esta skill quando:
- Documentando APIs REST (Express, Django DRF, FastAPI)
- Criando collections Postman para testes
- Configurando automação com Newman
- Integrando testes Postman em CI/CD
- Gerando collections a partir de OpenAPI
- Implementando autenticação JWT ou Session

---

## Estrutura de Collection

### Informações Básicas (info)

```json
{
  "info": {
    "_postman_id": "unique-id",
    "name": "Nome da API - Documentação",
    "description": "# Descrição Completa\n\n## Visão Geral\n...",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  }
}
```

**Requisitos:**
- Nome descritivo e claro
- Description em Markdown com visão geral completa
- Listar todos os serviços/módulos incluídos
- URLs base de cada serviço
- Informações sobre autenticação
- Status dos serviços (se aplicável)

### Organização Hierárquica

```
Collection/
├── Authentication/
│   ├── Login
│   ├── Refresh Token
│   └── Validate Token
├── [Módulo Principal]/
│   ├── [Submódulo]/
│   │   ├── List [Resource]
│   │   ├── Create [Resource]
│   │   ├── Get [Resource]
│   │   ├── Update [Resource]
│   │   └── Delete [Resource]
│   └── [Outro Submódulo]/
└── Dashboard/
    ├── Filters
    ├── Stats
    └── Charts/
```

**Padrões de Nomenclatura:**
- **Pastas:** PascalCase (ex: `Authentication`, `Financial KPIs`)
- **Endpoints:** Verb + Resource (ex: `List Contracts`, `Create Contract`)
- **Subpastas:** Descritivas e hierárquicas

---

## Variáveis de Ambiente

### Variáveis Obrigatórias

```json
{
  "id": "postman-env-default",
  "name": "Local Env",
  "values": [
    { "key": "base_url", "value": "http://localhost:8000", "enabled": true },
    { "key": "auth_token", "value": "", "enabled": true },
    { "key": "refresh_token", "value": "", "enabled": true },
    { "key": "auth_expires_at", "value": "", "enabled": true },
    { "key": "user_email", "value": "test@example.com", "enabled": true },
    { "key": "user_password", "value": "changeme", "enabled": true }
  ]
}
```

**Variáveis padrão:**
- `base_url`: URL base da aplicação
- `auth_token`: Token JWT (preenchido automaticamente)
- `refresh_token`: Refresh token (preenchido automaticamente)
- `auth_expires_at`: Timestamp de expiração do token
- `user_email`: Email do usuário de teste
- `user_password`: Senha do usuário de teste

**Para Django DRF:**
- `admin_username`: Username do admin
- `admin_password`: Password do admin
- `encoded_token`: Token codificado (alternativa)

---

## Pre-request Scripts

### Collection-Level: Autenticação JWT Automática

**Snippet obrigatório para todas as collections com JWT:**

```javascript
// Collection-level pre-request: attach Bearer token and auto-refresh

// 1. Attach Authorization header if token exists
if (pm.environment.get('auth_token')) {
    pm.request.headers.upsert({ 
        key: 'Authorization', 
        value: 'Bearer ' + pm.environment.get('auth_token') 
    });
}

// 2. Auto-refresh token if expired
let expiresAt = pm.environment.get('auth_expires_at');
if (expiresAt && Date.now() >= parseInt(expiresAt)) {
    console.log('Access token expired — attempting refresh...');
    let refreshReq = {
        url: pm.environment.get('base_url') + '/auth/refresh',
        method: 'POST',
        header: { 'Content-Type': 'application/json' },
        body: { 
            mode: 'raw', 
            raw: JSON.stringify({ 
                refresh_token: pm.environment.get('refresh_token') 
            }) 
        }
    };
    pm.sendRequest(refreshReq, function (err, res) {
        if (!err && res.code === 200) {
            let json = res.json();
            if (json.access_token) {
                pm.environment.set('auth_token', json.access_token);
            }
            if (json.refresh_token) {
                pm.environment.set('refresh_token', json.refresh_token);
            }
            if (json.expires_in) {
                pm.environment.set('auth_expires_at', Date.now() + (json.expires_in * 1000));
            }
        } else {
            console.error('Refresh failed', err || res);
        }
    });
}
```

### Folder-Level: Autenticação Automática (Fallback)

**Para endpoints que requerem autenticação mas não têm token:**

```javascript
// Verificar se token existe, se não, fazer login
if (!pm.environment.get("auth_token")) {
    pm.sendRequest({
        url: pm.environment.get("base_url") + "/auth/login",
        method: "POST",
        header: {
            "Content-Type": "application/json"
        },
        body: {
            mode: "raw",
            raw: JSON.stringify({
                email: pm.environment.get("user_email"),
                password: pm.environment.get("user_password")
            })
        }
    }, function (err, res) {
        if (res.code === 200) {
            const jsonData = res.json();
            if (jsonData.access_token) {
                pm.environment.set("auth_token", jsonData.access_token);
            }
            if (jsonData.refresh_token) {
                pm.environment.set("refresh_token", jsonData.refresh_token);
            }
            if (jsonData.expires_in) {
                pm.environment.set("auth_expires_at", Date.now() + (jsonData.expires_in * 1000));
            }
        }
    });
}
```

### Variáveis Dinâmicas

```javascript
// Gerar timestamp atual
pm.environment.set("current_timestamp", new Date().toISOString());

// Gerar data futura
const futureDate = new Date();
futureDate.setDate(futureDate.getDate() + 30);
pm.environment.set("future_date", futureDate.toISOString().split('T')[0]);
```

---

## Test Scripts

### Login: Salvar Tokens Automaticamente

**Snippet obrigatório para endpoint `/auth/login`:**

```javascript
// Test: Save tokens from login response
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
});

let res = pm.response.json();

if (res.access_token) {
    pm.environment.set('auth_token', res.access_token);
}

if (res.refresh_token) {
    pm.environment.set('refresh_token', res.refresh_token);
}

if (res.expires_in) {
    let expiresAt = Date.now() + (res.expires_in * 1000);
    pm.environment.set('auth_expires_at', expiresAt);
}
```

### Validação de Status Code

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

### Validação de Schema

```javascript
pm.test("Response has required fields", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property("id");
    pm.expect(jsonData).to.have.property("name");
});
```

### Validação de Tipos

```javascript
pm.test("Response data types are correct", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.id).to.be.a("string");
    pm.expect(jsonData.count).to.be.a("number");
});
```

### Salvar Variáveis da Resposta

```javascript
if (pm.response.code === 200) {
    const jsonData = pm.response.json();
    pm.environment.set("resource_id", jsonData.id);
    pm.environment.set("logged_user", jsonData.user.id);
}
```

---

## Descrições de Endpoints

### Estrutura Obrigatória

Cada endpoint **DEVE** ter descrição completa em Markdown:

```markdown
## [Nome do Endpoint]

### Validações
- campo (tipo): Descrição → status_code: "mensagem de erro"
- campo (tipo): Descrição → status_code: "mensagem de erro"

### Regras de Negócio
- Regra 1
- Regra 2
- Regra 3

### Erros
- status_code: Descrição do erro
- status_code: Descrição do erro
```

**Exemplo:**

```markdown
## Login

### Validações
- email (string): Obrigatório → 422: "Email is required"
- password (string): Obrigatório → 422: "Password is required"

### Regras de Negócio
- Credenciais devem estar corretas
- Usuário deve estar ativo
- Token válido por 24h (access_token)
- Refresh token válido por 7 dias

### Erros
- 422: Email/Password ausente
- 401: Credenciais inválidas
- 403: Usuário inativo
```

---

## Exemplos de Resposta

### Estrutura Obrigatória

Cada endpoint **DEVE** ter:

1. **Exemplo de Sucesso** (status 200/201)
   - Nome: "✅ Sucesso" ou "✅ Sucesso - [Descrição]"
   - Body completo e real
   - Headers relevantes

2. **Exemplos de Erro de Validação** (status 400/422)
   - Um exemplo para cada campo obrigatório ausente
   - Um exemplo para cada validação específica
   - Mensagens de erro exatas

3. **Exemplos de Erro de Negócio** (status 404/403/401)
   - Recurso não encontrado
   - Permissão negada
   - Token inválido/expirado

### Formato de Exemplos

```json
{
  "name": "✅ Sucesso - Contrato criado",
  "code": 201,
  "body": "{\n  \"id\": 1,\n  \"term_number\": \"123/2024\",\n  \"status\": \"active\"\n}"
}
```

```json
{
  "name": "❌ 422 - term_number ausente",
  "code": 422,
  "body": "{\n  \"detail\": [\n    {\n      \"type\": \"value_error.missing\",\n      \"loc\": [\"body\", \"term_number\"],\n      \"msg\": \"This field is required.\"\n    }\n  ]\n}"
}
```

---

## Documentação de Parâmetros

### Query Parameters

```json
{
  "key": "year",
  "value": "2024",
  "description": "Ano para filtrar os dados (formato: YYYY).",
  "disabled": true
}
```

**Requisitos:**
- Descrição clara do parâmetro
- Tipo de dado esperado
- Formato (se aplicável)
- Exemplo de valor
- Se é obrigatório ou opcional

### Path Parameters

```json
{
  "variable": [
    {
      "key": "id",
      "value": "1",
      "description": "ID do contrato (número inteiro)."
    }
  ]
}
```

### Body Parameters

**Para JSON:**
- Usar variáveis quando possível: `{{variable_name}}`
- Incluir comentários quando necessário
- Exemplos com dados realistas

**Para multipart/form-data:**
- Documentar cada campo
- Tipo de arquivo aceito (se aplicável)
- Tamanho máximo (se aplicável)

### Choices para Campos Enum

```markdown
### Campo: status

**Tipo:** ChoiceField  
**Valores aceitos:**
- `PENDING`: Pendente
- `PROCESSING`: Processando
- `COMPLETED`: Concluído
- `FAILED`: Falha
```

---

## Autenticação

### JWT (JSON Web Tokens)

**Endpoints típicos:**

- `POST /auth/login` → retorna `{ access_token, refresh_token, expires_in }`
- `POST /auth/refresh` → retorna novo `access_token` (rotacionar refresh token)
- `POST /auth/logout` → invalidar refresh token (DB ou blacklist)

**Configuração recomendada:**
- `access_token`: expiração curta (ex: 15 minutos)
- `refresh_token`: long-lived (ex: 7 dias)
- Auto-refresh implementado no pre-request script

### Session / Cookie (Django DRF)

**Para APIs que usam sessão:**
- Configure Pre-request para enviar cookies
- Postman gerencia cookies automaticamente
- Tests: captura e salva `Set-Cookie` se necessário

```javascript
// Para Django DRF com Session
pm.request.headers.upsert({
    key: 'X-CSRFToken',
    value: pm.cookies.get('csrftoken')
});
```

---

## Automação com Newman

### O que é o Newman?

**Newman** é o CLI (Command Line Interface) do Postman. Ele **NÃO converte** documentação em collection. Ele **executa** uma collection Postman já existente.

**Diferença importante:**
- ❌ **NÃO faz:** Converter Swagger/OpenAPI/ReDoc → Postman Collection
- ✅ **FAZ:** Executar testes de uma collection Postman já criada

### Script de Execução Local

**Arquivo: `scripts/run_newman.sh`**

Este script **executa** uma collection Postman usando o Newman:

```bash
#!/usr/bin/env bash
# Runs Newman against the collection and environment.
# Usage: ./run_newman.sh [collection.json] [environment.json]

COLLECTION=${1:-postman/collection.json}
ENV=${2:-postman/environment.json}
REPORT_DIR=${REPORT_DIR:-reports/postman}

mkdir -p "$REPORT_DIR"

# EXECUTA a collection (não converte!)
npx newman run "$COLLECTION" -e "$ENV" \
  --reporters cli,junit,html \
  --reporter-junit-export "$REPORT_DIR/junit-results.xml" \
  --reporter-html-export "$REPORT_DIR/report.html"

EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
  echo "Newman tests failed (exit $EXIT_CODE)"
  exit $EXIT_CODE
fi

echo "Newman finished."
```

### Uso

```bash
# Executar com defaults (usa postman/collection.json)
./scripts/run_newman.sh

# Especificar collection e environment
./scripts/run_newman.sh postman/collection.json postman/environment.json
```

**O que acontece:**
1. Newman lê a collection Postman (`collection.json`)
2. Executa todos os requests da collection
3. Roda os test scripts de cada request
4. Gera relatórios (CLI, JUnit XML, HTML)
5. Retorna código de saída (0 = sucesso, != 0 = falha)

---

## CI/CD - GitHub Actions

### Workflow Completo

**Arquivo: `.github/workflows/postman-ci.yml`**

```yaml
name: Postman Collection Tests

on:
  push:
    branches: [ main, master ]
  pull_request:

jobs:
  postman-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci || npm i

      - name: Install jq (for environment manipulation)
        run: sudo apt-get update && sudo apt-get install -y jq

      - name: Run Newman (Postman tests)
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
          USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
        run: |
          # Write environment with secrets
          jq '.values[] |= (if .key=="base_url" then .value="'$BASE_URL'" elif .key=="user_email" then .value="'$USER_EMAIL'" elif .key=="user_password" then .value="'$USER_PASSWORD'" else . end)' postman/environment.json > tmp_env.json
          
          npx newman run postman/collection.json -e tmp_env.json \
            --reporters cli,junit \
            --reporter-junit-export postman/junit-results.xml
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: postman-results
          path: postman/junit-results.xml
```

### Secrets Necessários

Configurar no GitHub Repository Settings → Secrets:
- `BASE_URL`: URL base da API (ex: `https://api.example.com`)
- `TEST_USER_EMAIL`: Email do usuário de teste
- `TEST_USER_PASSWORD`: Senha do usuário de teste

---

## Geração a partir de OpenAPI/Swagger

### ⚠️ IMPORTANTE: Diferença entre Conversão e Execução

**Conversão (OpenAPI → Postman):**
- **Ferramenta:** `openapi-to-postmanv2` ou `postman-collection-transformer`
- **O que faz:** Converte arquivo OpenAPI/Swagger em uma collection Postman
- **Quando usar:** Quando você tem OpenAPI e quer gerar collection automaticamente

**Execução (Newman):**
- **Ferramenta:** `newman` (via `run_newman.sh`)
- **O que faz:** Executa testes de uma collection Postman já existente
- **Quando usar:** Para rodar testes automatizados da collection

### Fluxo Completo Recomendado

#### 1. Gerar/Atualizar OpenAPI

**Express.js:**
```bash
npm install swagger-jsdoc
# Gera openapi.json automaticamente
```

**Django DRF:**
```bash
pip install drf-spectacular
# Gera openapi.json via /api/schema/
```

**FastAPI:**
```python
# OpenAPI gerado automaticamente em /openapi.json
```

#### 2. Converter OpenAPI → Postman Collection

**Script: `generate-from-openapi.sh`**

```bash
#!/usr/bin/env bash
# Gera collection Postman a partir de OpenAPI/Swagger
# Usage: ./generate-from-openapi.sh [openapi.json] [output-dir]

OPENAPI_FILE=${1:-openapi.json}
OUTPUT_DIR=${2:-postman}

# Instalar ferramenta se necessário
if ! command -v openapi-to-postmanv2 &> /dev/null; then
    npm install -g openapi-to-postmanv2
fi

# Converter OpenAPI para Postman
openapi-to-postmanv2 -s "$OPENAPI_FILE" -o "$OUTPUT_DIR/collection.json"

echo "✅ Collection gerada em $OUTPUT_DIR/collection.json"
```

**Uso:**
```bash
# Converter openapi.json para postman/collection.json
./generate-from-openapi.sh openapi.json postman

# Ou especificar arquivo diferente
./generate-from-openapi.sh docs/swagger.json postman
```

#### 3. Injetar Scripts Automáticos

Após a conversão, você precisa **adicionar manualmente** (ou via script):
- Pre-request scripts de autenticação (collection-level)
- Test scripts para salvar tokens
- Configurar variáveis de ambiente

**Exemplo de script Python para injetar scripts:**

```python
import json

# Ler collection gerada
with open('postman/collection.json', 'r') as f:
    collection = json.load(f)

# Adicionar pre-request script (collection-level)
collection['event'] = [{
    "listen": "prerequest",
    "script": {
        "exec": [
            "// Auto-attach Bearer token",
            "if (pm.environment.get('auth_token')) {",
            "  pm.request.headers.upsert({ key: 'Authorization', value: 'Bearer ' + pm.environment.get('auth_token') });",
            "}"
        ],
        "type": "text/javascript"
    }
}]

# Salvar collection atualizada
with open('postman/collection.json', 'w') as f:
    json.dump(collection, f, indent=2)
```

#### 4. Executar Testes com Newman

**Agora sim, usar o `run_newman.sh`:**

```bash
# Executar testes da collection gerada
./run_newman.sh postman/collection.json postman/environment.json
```

#### 5. Commit e CI

- Commitar collection no diretório `postman/`
- CI executa Newman automaticamente (via GitHub Actions)
- Opcional: Publicar no Postman API via `collections.publish`

### Resumo do Fluxo

```
1. OpenAPI/Swagger (gerado pelo framework)
   ↓
2. openapi-to-postmanv2 (CONVERTE)
   ↓
3. postman/collection.json (collection gerada)
   ↓
4. Adicionar scripts manualmente (autenticação, testes)
   ↓
5. run_newman.sh (EXECUTA testes)
   ↓
6. Relatórios (junit-results.xml, report.html)
```

---

## Templates de Collection

### Template Base (JWT)

**Estrutura mínima:**

```json
{
  "info": {
    "name": "API - Boilerplate (Auth + CRUD)",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "description": "Coleção padrão: Auth (JWT), exemplos CRUD."
  },
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "POST /auth/login",
          "request": {
            "method": "POST",
            "header": [
              { "key": "Content-Type", "value": "application/json" }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"{{user_email}}\",\n  \"password\": \"{{user_password}}\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth","login"]
            }
          },
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "pm.test('status 200', function () { pm.response.to.have.status(200); });",
                  "let res = pm.response.json();",
                  "if(res.access_token){ pm.environment.set('auth_token', res.access_token); }",
                  "if(res.refresh_token){ pm.environment.set('refresh_token', res.refresh_token); }",
                  "if(res.expires_in){ let expiresAt = Date.now() + (res.expires_in * 1000); pm.environment.set('auth_expires_at', expiresAt); }"
                ],
                "type": "text/javascript"
              }
            }
          ]
        }
      ]
    }
  ],
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "exec": [
          "// Collection-level pre-request: attach Authorization header if auth_token present",
          "if (pm.environment.get('auth_token')) {",
          "  pm.request.headers.upsert({ key: 'Authorization', value: 'Bearer ' + pm.environment.get('auth_token') });",
          "}",
          "",
          "// Auto-refresh if token expired",
          "let expiresAt = pm.environment.get('auth_expires_at');",
          "if (expiresAt && Date.now() >= parseInt(expiresAt)) {",
          "  console.log('Access token expired — attempting refresh...');",
          "  let refreshReq = {",
          "    url: pm.environment.get('base_url') + '/auth/refresh',",
          "    method: 'POST',",
          "    header: { 'Content-Type': 'application/json' },",
          "    body: { mode: 'raw', raw: JSON.stringify({ refresh_token: pm.environment.get('refresh_token') }) }",
          "  };",
          "  pm.sendRequest(refreshReq, function (err, res) {",
          "    if (!err && res.code === 200) {",
          "      let json = res.json();",
          "      if (json.access_token) { pm.environment.set('auth_token', json.access_token); }",
          "      if (json.refresh_token) { pm.environment.set('refresh_token', json.refresh_token); }",
          "      if (json.expires_in) { pm.environment.set('auth_expires_at', Date.now() + (json.expires_in * 1000)); }",
          "    } else { console.error('Refresh failed', err || res); }",
          "  });",
          "}"
        ],
        "type": "text/javascript"
      }
    }
  ]
}
```

---

## Framework-Specific

### Express.js

**Endpoints típicos:**
- `POST /auth/login` → `{ access_token, refresh_token, expires_in }`
- `POST /auth/refresh` → novo `access_token` (rotacionar refresh token)
- `POST /auth/logout` → invalidar refresh token

**Pacotes recomendados:**
- `jsonwebtoken` para gerar tokens
- `express-jwt` ou middleware customizado para validação

**Configuração de desenvolvimento:**
- `expires_in` curto (ex: 15 minutos) para access_token
- Refresh token long-lived para facilitar testes

### Django DRF

**Configuração:**
- Use `djangorestframework-simplejwt` ou `dj-rest-auth`
- Configure token lifetimes no `settings.py`
- Endpoints: `/api/token/` e `/api/token/refresh/`

**Para sessões (cookies):**
- Ative CSRF
- Teste com Postman usando cookie jar
- Envie CSRF token nos headers

**Variáveis de ambiente:**
- `admin_username`: Username do admin
- `admin_password`: Password do admin
- `encoded_token`: Token codificado (alternativa)

### FastAPI

**OpenAPI automático:**
- FastAPI gera OpenAPI automaticamente
- Use `openapi-to-postmanv2` para converter
- Injete scripts de autenticação após conversão

---

## Checklist de Qualidade

### Estrutura
- [ ] Collection tem descrição completa em Markdown
- [ ] Variáveis de ambiente configuradas corretamente
- [ ] Organização hierárquica clara e lógica
- [ ] Nomenclatura consistente

### Endpoints
- [ ] Todos os endpoints documentados
- [ ] Cada endpoint tem descrição completa (Validações, Regras, Erros)
- [ ] Validações documentadas
- [ ] Regras de negócio documentadas
- [ ] Todos os erros possíveis documentados

### Exemplos
- [ ] Exemplo de sucesso para cada endpoint
- [ ] Exemplos de todos os erros de validação
- [ ] Exemplos de erros de negócio (404, 403, 401)
- [ ] Exemplos usam dados realistas
- [ ] Exemplos incluem headers relevantes

### Scripts
- [ ] Pre-request scripts para autenticação automática (collection-level)
- [ ] Auto-refresh de token implementado
- [ ] Test scripts validando status codes
- [ ] Test scripts validando schemas
- [ ] Test scripts salvando variáveis quando necessário

### Parâmetros
- [ ] Query parameters documentados com descrições
- [ ] Path parameters documentados
- [ ] Body parameters documentados
- [ ] Choices para campos enum documentados

### Automação
- [ ] Token é salvo automaticamente após login
- [ ] Variáveis dinâmicas configuradas quando necessário
- [ ] Scripts de teste validam respostas corretamente
- [ ] Newman configurado para execução local
- [ ] CI/CD configurado (GitHub Actions)

### Casos Especiais
- [ ] Fluxos assíncronos documentados completamente
- [ ] Uploads de arquivo documentados (multipart/form-data)
- [ ] KPIs com kpi_id documentados (strings como "4.1", "4.2", etc.)
- [ ] Status de processamento documentados

---

## Boas Práticas

### 1. Máxima Automação
- Sempre usar pre-request scripts para autenticação
- Salvar variáveis automaticamente após operações
- Validar respostas com test scripts
- Auto-refresh de tokens quando expirados

### 2. Exemplos Reais
- Fazer requisições reais para capturar respostas
- Usar dados da especificação técnica quando disponível
- Criar dados sintéticos realistas quando necessário

### 3. Cobertura Completa
- Documentar TODOS os casos de erro possíveis
- Incluir exemplos para cada validação
- Documentar regras de negócio importantes

### 4. Manutenibilidade
- Usar variáveis para valores repetidos
- Organizar hierarquicamente
- Nomenclatura clara e consistente
- Gerar collections a partir de OpenAPI quando possível

### 5. Reduzir Repetição
- Padronizar endpoints e variáveis
- Criar snippets de pre-request/test reutilizáveis
- Gerar collections a partir de OpenAPI
- Manter templates de request com placeholders

### 6. Tratamento de Erros

Quando encontrar erros durante a documentação:

1. **Documentar o erro:**
   - Request completo (método, URL, headers, body)
   - Response completo (status, headers, body)
   - Descrição clara do problema

2. **Informar necessidade de correção:**
   - Identificar se é bug na API ou na documentação
   - Sugerir correção quando possível

3. **Reteste completo:**
   - Após correção, refazer TODOS os testes do início ao fim
   - Validar que nada quebrou
   - Confirmar que o erro foi corrigido

---

## Estrutura de Diretórios

```
projeto/
├── postman/
│   ├── collection.json          # Collection principal
│   ├── environment.json        # Environment padrão
│   └── environment.prod.json   # Environment de produção (gitignored)
├── scripts/
│   └── run_newman.sh           # Script de execução Newman
├── .github/
│   └── workflows/
│       └── postman-ci.yml       # CI/CD workflow
└── reports/
    └── postman/                # Relatórios Newman (gitignored)
        ├── junit-results.xml
        └── report.html
```

---

## Referências

- **Documentação interna:** `core/docs/programming/postman-documentation-standards.md`
- **Postman Collection Format:** https://schema.getpostman.com/json/collection/v2.1.0/docs/index.html
- **Postman Scripting:** https://learning.postman.com/docs/writing-scripts/intro-to-scripts/
- **Newman CLI:** https://github.com/postmanlabs/newman
- **OpenAPI to Postman:** https://github.com/postmanlabs/openapi-to-postman

---

## Templates e Snippets

### Pre-request Snippet (JWT Auto-refresh)

```javascript
// Pre-request snippet: attach Bearer and refresh if expired

if (pm.environment.get('auth_token')) {
  pm.request.headers.upsert({ 
    key: 'Authorization', 
    value: 'Bearer ' + pm.environment.get('auth_token') 
  });
}

let expiresAt = pm.environment.get('auth_expires_at');
if (expiresAt && Date.now() >= parseInt(expiresAt)) {
  pm.sendRequest({
    url: pm.environment.get('base_url') + '/auth/refresh',
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    body: { 
      mode: 'raw', 
      raw: JSON.stringify({ 
        refresh_token: pm.environment.get('refresh_token') 
      }) 
    }
  }, function (err, res) {
    if (!err && res.code === 200) {
      let j = res.json();
      if (j.access_token) pm.environment.set('auth_token', j.access_token);
      if (j.refresh_token) pm.environment.set('refresh_token', j.refresh_token);
      if (j.expires_in) pm.environment.set('auth_expires_at', Date.now() + (j.expires_in * 1000));
    }
  });
}
```

### Test Snippet (Salvar Tokens)

```javascript
pm.test("Login works", function () { 
  pm.response.to.have.status(200); 
});

let r = pm.response.json();

if (r.access_token) pm.environment.set('auth_token', r.access_token);
if (r.refresh_token) pm.environment.set('refresh_token', r.refresh_token);
if (r.expires_in) pm.environment.set('auth_expires_at', Date.now() + (r.expires_in * 1000));
```

---

## Automação Avançada

### Geração de Collection a partir de OpenAPI

**Fluxo recomendado:**

1. Gerar/atualizar OpenAPI (Express: `swagger-jsdoc`, Django: `drf-spectacular`, FastAPI: automático)
2. Converter OpenAPI → Postman (`openapi-to-postmanv2`)
3. Injetar snippets de pre-request/tests que gerenciam JWT automaticamente
4. Gerar ambiente com variáveis e placeholders
5. Commitar collection/ambientes em `postman/` no repo
6. CI executa Newman automaticamente
7. Opcional: Publicar no Postman API via `collections.publish`

---

## Observações Finais

- **Mantenha collections pequenas e bem nomeadas** — prefira gerar via OpenAPI quando possível
- **Testes determinísticos** — evite dados dependentes de estado sem reset jobs
- **Concentre repetição em:**
  - Collection-level scripts (pre-request/tests)
  - Environment variables
  - Templates gerados pela skill

---

**Templates e Exemplos:** Ver `core/templates/postman-collection/` para templates completos de collection, environment e scripts de automação

