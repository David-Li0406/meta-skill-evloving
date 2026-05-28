---
name: postman-execution
description: Comandos e automação para executar operações Postman (conversão OpenAPI, execução de testes, geração de relatórios).
triggers: [postman, newman, openapi, swagger, convert, test, collection, generate]
---

# Postman Execution - Comandos e Automação

**Skill para executar operações Postman: converter OpenAPI, executar testes, gerar relatórios.**

---

## Quando Usar

Aplicar esta skill quando o agente for instruído a:
- Converter OpenAPI/Swagger em collection Postman
- Executar testes de uma collection Postman
- Gerar relatórios de testes
- Validar collection Postman
- Atualizar collection a partir de OpenAPI

---

## Comandos Disponíveis

### 1. Converter OpenAPI → Postman Collection

**Comando:** `make postman-generate` ou `make postman-generate OPENAPI=openapi.json OUTPUT=postman`

**O que faz:**
- Converte arquivo OpenAPI/Swagger em collection Postman
- Instala `openapi-to-postmanv2` se necessário
- Gera `postman/collection.json`

**Quando usar:**
- Quando OpenAPI foi atualizado
- Quando precisa gerar collection automaticamente
- Antes de executar testes pela primeira vez

**Exemplo:**
```bash
# Usar defaults (openapi.json → postman/collection.json)
make postman-generate

# Especificar arquivo e diretório
make postman-generate OPENAPI=docs/swagger.json OUTPUT=postman
```

---

### 2. Executar Testes Postman (Newman)

**Comando:** `make postman-test` ou `make postman-test COLLECTION=postman/collection.json ENV=postman/environment.json`

**O que faz:**
- Executa todos os requests da collection Postman
- Roda test scripts de cada request
- Gera relatórios (CLI, JUnit XML, HTML)
- Retorna código de saída (0 = sucesso, != 0 = falha)

**Quando usar:**
- Para validar que a API está funcionando
- Após fazer mudanças na API
- No CI/CD pipeline
- Para gerar relatórios de testes

**Exemplo:**
```bash
# Usar defaults (postman/collection.json, postman/environment.json)
make postman-test

# Especificar collection e environment
make postman-test COLLECTION=postman/api.json ENV=postman/prod.json
```

**Relatórios gerados:**
- `reports/postman/junit-results.xml` - Para integração com CI/CD
- `reports/postman/report.html` - Relatório visual HTML

---

### 3. Validar Collection Postman

**Comando:** `make postman-validate` ou `make postman-validate COLLECTION=postman/collection.json`

**O que faz:**
- Valida se a collection Postman está bem formada
- Verifica estrutura JSON
- Verifica se tem requests válidos
- Não executa testes, apenas valida estrutura

**Quando usar:**
- Antes de commitar collection
- Após gerar collection a partir de OpenAPI
- Para verificar se collection está correta

**Exemplo:**
```bash
# Validar collection padrão
make postman-validate

# Validar collection específica
make postman-validate COLLECTION=postman/api.json
```

---

### 4. Atualizar Collection a partir de OpenAPI

**Comando:** `make postman-update` ou `make postman-update OPENAPI=openapi.json`

**O que faz:**
- Converte OpenAPI → Postman Collection
- Preserva scripts customizados (se possível)
- Atualiza endpoints e schemas

**Quando usar:**
- Quando OpenAPI foi atualizado e collection precisa ser atualizada
- Para manter collection sincronizada com código

**Exemplo:**
```bash
# Atualizar collection padrão
make postman-update

# Especificar arquivo OpenAPI
make postman-update OPENAPI=docs/swagger.json
```

---

## Regras de Execução para Agentes

### 1. SEMPRE executar comandos diretamente

- ❌ **NUNCA** apenas mostrar o comando para o usuário
- ✅ **SEMPRE** executar via `make` ou diretamente
- ✅ **SEMPRE** analisar a saída e reportar resultados

### 2. Verificar pré-requisitos

Antes de executar qualquer comando:

```bash
# Verificar se Node.js está instalado
node --version

# Verificar se collection existe (para testes)
test -f postman/collection.json

# Verificar se OpenAPI existe (para conversão)
test -f openapi.json
```

### 3. Analisar resultados

Após executar:

- **Sucesso:** Reportar quantos testes passaram
- **Falha:** Analisar erros e sugerir correções
- **Conversão:** Verificar se collection foi gerada corretamente

### 4. Workflow recomendado

```
1. Verificar se OpenAPI existe → Se não, informar usuário
2. Executar make postman-generate → Gerar collection
3. Validar collection → make postman-validate
4. Executar testes → make postman-test
5. Analisar relatórios → Reportar resultados
```

---

## Estrutura de Diretórios Esperada

```
projeto/
├── openapi.json              # Ou swagger.json, docs/openapi.yaml
├── postman/
│   ├── collection.json       # Collection gerada/atualizada
│   └── environment.json      # Variáveis de ambiente
├── reports/
│   └── postman/              # Relatórios gerados (gitignored)
│       ├── junit-results.xml
│       └── report.html
└── Makefile                  # Comandos disponíveis
```

---

## Tratamento de Erros

### Erro: OpenAPI não encontrado

**Ação:**
1. Informar que arquivo OpenAPI não foi encontrado
2. Sugerir locais comuns: `openapi.json`, `swagger.json`, `docs/openapi.yaml`
3. Perguntar se usuário quer gerar OpenAPI primeiro

### Erro: Collection não encontrada

**Ação:**
1. Informar que collection não existe
2. Sugerir executar `make postman-generate` primeiro
3. Ou perguntar se usuário quer criar collection manualmente

### Erro: Testes falharam

**Ação:**
1. Analisar relatório HTML ou JUnit XML
2. Identificar quais requests falharam
3. Verificar se é problema na API ou na collection
4. Sugerir correções

### Erro: openapi-to-postmanv2 não instalado

**Ação:**
1. Instalar automaticamente: `npm install -g openapi-to-postmanv2`
2. Se falhar, informar usuário para instalar manualmente
3. Continuar com conversão após instalação

---

## Checklist de Execução

Antes de executar qualquer comando:

- [ ] Verificar se pré-requisitos estão instalados (Node.js, npm)
- [ ] Verificar se arquivos necessários existem (OpenAPI ou Collection)
- [ ] Executar comando via `make` quando disponível
- [ ] Analisar saída do comando
- [ ] Reportar resultados ao usuário
- [ ] Em caso de erro, analisar e sugerir correções

---

## Exemplos de Uso pelos Agentes

### Cenário 1: Gerar Collection pela primeira vez

```bash
# Agente executa:
make postman-generate

# Analisa saída:
# ✅ Collection gerada em postman/collection.json
# ⚠️  PRÓXIMOS PASSOS: Adicionar scripts de autenticação

# Agente reporta:
"Collection Postman gerada com sucesso. Próximo passo: adicionar scripts de autenticação."
```

### Cenário 2: Executar testes

```bash
# Agente executa:
make postman-test

# Analisa saída:
# ✅ 15/15 testes passaram
# Relatórios: reports/postman/report.html

# Agente reporta:
"Todos os testes passaram (15/15). Relatório disponível em reports/postman/report.html"
```

### Cenário 3: Atualizar collection

```bash
# Agente executa:
make postman-update

# Analisa saída:
# ✅ Collection atualizada
# ⚠️  Verificar scripts customizados

# Agente reporta:
"Collection atualizada. Verifique se scripts de autenticação foram preservados."
```

---

## Referências

- **Skill principal:** `skills/documentation/postman/SKILL.md`
- **Templates:** `core/templates/postman-collection/`
- **Newman CLI:** https://github.com/postmanlabs/newman
- **OpenAPI to Postman:** https://github.com/postmanlabs/openapi-to-postmanv2

