# Exemplo: Implementação de Funcionalidade de API

## Solicitação do Usuário

> "Crie um plano de implementação para a spec da User Profile API"

## Execução do Fluxo

### Etapa 1: Buscar Especificação

```
Glob
pattern: "**/*user*profile*spec*.md"

Encontrado: "docs/specs/user-profile-api-spec.md"

Read
file_path: "docs/specs/user-profile-api-spec.md"
```

### Etapa 2: Analisar Especificação

**Conteúdo da Spec Extraído:**

```markdown
# Especificação da API de Perfil de Usuário

## Visão Geral
API RESTful para gerenciamento de perfil de usuário

## Requisitos

### Funcionais
- FR-1: Obter perfil do usuário por ID
- FR-2: Atualizar perfil do usuário (nome, bio, avatar)
- FR-3: Enviar avatar do perfil
- FR-4: Obter perfil público do usuário (campos limitados)
- FR-5: Buscar usuários por nome

### Não Funcionais
- NFR-1: Tempo de resposta < 200ms (p95)
- NFR-2: Suportar 1000 usuários concorrentes
- NFR-3: Upload de avatar < 5MB
- NFR-4: Compatível com GDPR (portabilidade de dados)

## Endpoints da API

GET /api/v1/users/:id
PUT /api/v1/users/:id
POST /api/v1/users/:id/avatar
GET /api/v1/users/:id/public
GET /api/v1/users/search

## Modelo de Dados
- id (UUID)
- email (string, único)
- name (string)
- bio (text, máx 500 caracteres)
- avatar_url (string)
- created_at (timestamp)
- updated_at (timestamp)

## Segurança
- Autenticação: JWT bearer token
- Autorização: Usuários só podem atualizar o próprio perfil
- Rate limiting: 100 req/min por usuário

## Critérios de Aceitação
- AC-1: Todos os endpoints retornam códigos HTTP adequados
- AC-2: Erros de validação retornam 400 com detalhes
- AC-3: Acesso não autorizado retorna 401
- AC-4: Limite de taxa excedido retorna 429
- AC-5: Imagens de avatar armazenadas no S3
```

### Etapa 3: Criar Plano de Implementação

```
Write
file_path: "docs/planos/user-profile-api.md"
content: "[Plano de implementação]"
```

**Plano de Implementação Criado:**

```markdown
# Plano de Implementação: User Profile API

## Visão Geral
Construir API RESTful para gerenciamento de perfil de usuário com operações CRUD, upload de avatar e busca.

## Especificação Vinculada
- docs/specs/user-profile-api-spec.md

## Resumo de Requisitos

### Requisitos Funcionais
- [ ] Obter perfil do usuário (autenticado)
- [ ] Atualizar campos do perfil (nome, bio)
- [ ] Enviar avatar com processamento de imagem
- [ ] Visualização de perfil público (campos limitados)
- [ ] Busca de usuários por nome

### Requisitos Não Funcionais
- **Performance**: tempo de resposta < 200ms (p95)
- **Escalabilidade**: 1000 usuários concorrentes
- **Armazenamento**: arquivos de avatar < 5MB no S3
- **Compliance**: portabilidade de dados (GDPR)

### Critérios de Aceitação
- Todos os endpoints com códigos de status corretos
- Validação de entrada com detalhes de erro
- Autenticação JWT obrigatória
- Rate limiting aplicado
- Avatares armazenados no S3

## Abordagem Técnica

### Arquitetura
- **Framework**: Express.js (Node.js)
- **Banco de dados**: PostgreSQL
- **Armazenamento**: AWS S3 para avatares
- **Cache**: Redis para dados de perfil
- **Busca**: Pesquisa full-text do PostgreSQL

### Decisões de Design Principais
1. **Autenticação JWT**: Auth stateless, escala horizontalmente
2. **S3 para Avatares**: Desacoplar armazenamento, pronto para CDN
3. **Cache Redis**: Reduz carga no DB para perfis acessados com frequência
4. **Rate Limiting**: Algoritmo token bucket, limites por usuário

## Fases de Implementação

### Fase 1: Base
**Objetivo**: Preparar infraestrutura central

**Tarefas**:
- [ ] Configurar esquema do banco
- [ ] Configurar bucket S3
- [ ] Configurar cache Redis
- [ ] Criar estrutura inicial da API

**Entregáveis**: Esqueleto funcional com DB, storage e cache prontos

### Fase 2: Endpoints Principais
**Objetivo**: Implementar operações CRUD principais

**Tarefas**:
- [ ] Implementar GET de perfil do usuário
- [ ] Implementar PUT de atualização de perfil
- [ ] Adicionar validação de entrada
- [ ] Adicionar middleware de autenticação JWT
- [ ] Implementar rate limiting

**Entregáveis**: CRUD funcional com autenticação

### Fase 3: Upload de Avatar
**Objetivo**: Gerenciar avatares com S3

**Tarefas**:
- [ ] Implementar endpoint de upload de avatar
- [ ] Adicionar validação de imagem (tamanho, formato)
- [ ] Processar e redimensionar imagens
- [ ] Upload para S3 com URLs assinadas

**Entregáveis**: Upload/atualização de avatar

### Fase 4: Busca e Perfil Público
**Objetivo**: Concluir funcionalidades restantes

**Tarefas**:
- [ ] Implementar busca de usuários
- [ ] Implementar endpoint de perfil público
- [ ] Adicionar indexação de busca
- [ ] Otimizar queries de busca

**Entregáveis**: Busca e perfis públicos funcionando

### Fase 5: Testes e Otimização
**Objetivo**: Qualidade pronta para produção

**Tarefas**:
- [ ] Escrever testes unitários
- [ ] Escrever testes de integração
- [ ] Testes de performance
- [ ] Auditoria de segurança
- [ ] Documentação da API

**Entregáveis**: API testada, documentada, pronta para produção

## Dependências

### Dependências Externas
- Bucket AWS S3 criado
- Instância Redis disponível
- Banco PostgreSQL provisionado

### Dependências Internas
- Serviço de autenticação JWT (existe)
- Tabela de usuários (existe)
- Infraestrutura de logs (existe)

## Riscos e Mitigação

| Risco | Mitigação |
|-------|-----------|
| Performance do processamento de imagens | Usar fila de jobs em background |
| Falhas de upload no S3 | Retry com backoff exponencial |
| Performance de busca | Adicionar índices, considerar Elasticsearch |

## Critérios de Sucesso

### Sucesso Técnico
- [ ] Todos os 5 endpoints implementados
- [ ] Tempo de resposta < 200ms (p95)
- [ ] Suporta 1000 usuários concorrentes
- [ ] Cobertura de testes > 80%

### Sucesso de Negócio
- [ ] Atualização de perfil funcional
- [ ] Uploads de avatar funcionando
- [ ] Busca retorna resultados relevantes
```

### Etapa 4: Criar Tarefas de Implementação

```
TodoWrite
todos: [
  {
    "content": "Configurar esquema do banco para User Profile API",
    "activeForm": "Configurando esquema do banco para User Profile API",
    "status": "pending"
  },
  {
    "content": "Configurar bucket S3 para avatares",
    "activeForm": "Configurando bucket S3 para avatares",
    "status": "pending"
  },
  {
    "content": "Configurar cache Redis",
    "activeForm": "Configurando cache Redis",
    "status": "pending"
  },
  {
    "content": "Criar estrutura inicial da API",
    "activeForm": "Criando estrutura inicial da API",
    "status": "pending"
  },
  {
    "content": "Implementar GET de perfil do usuário",
    "activeForm": "Implementando GET de perfil do usuário",
    "status": "pending"
  },
  {
    "content": "Implementar PUT de atualização de perfil",
    "activeForm": "Implementando PUT de atualização de perfil",
    "status": "pending"
  },
  {
    "content": "Adicionar validação de entrada",
    "activeForm": "Adicionando validação de entrada",
    "status": "pending"
  },
  {
    "content": "Adicionar middleware de autenticação JWT",
    "activeForm": "Adicionando middleware de autenticação JWT",
    "status": "pending"
  },
  {
    "content": "Implementar rate limiting",
    "activeForm": "Implementando rate limiting",
    "status": "pending"
  },
  {
    "content": "Implementar endpoint de upload de avatar",
    "activeForm": "Implementando endpoint de upload de avatar",
    "status": "pending"
  },
  {
    "content": "Adicionar validação de imagem",
    "activeForm": "Adicionando validação de imagem",
    "status": "pending"
  },
  {
    "content": "Processar e redimensionar imagens",
    "activeForm": "Processando e redimensionando imagens",
    "status": "pending"
  },
  {
    "content": "Upload para S3 com URLs assinadas",
    "activeForm": "Implementando upload para S3 com URLs assinadas",
    "status": "pending"
  },
  {
    "content": "Implementar busca de usuários",
    "activeForm": "Implementando busca de usuários",
    "status": "pending"
  },
  {
    "content": "Implementar endpoint de perfil público",
    "activeForm": "Implementando endpoint de perfil público",
    "status": "pending"
  },
  {
    "content": "Escrever testes unitários",
    "activeForm": "Escrevendo testes unitários",
    "status": "pending"
  },
  {
    "content": "Escrever testes de integração",
    "activeForm": "Escrevendo testes de integração",
    "status": "pending"
  },
  {
    "content": "Testes de performance",
    "activeForm": "Executando testes de performance",
    "status": "pending"
  },
  {
    "content": "Documentação da API",
    "activeForm": "Escrevendo documentação da API",
    "status": "pending"
  }
]
```

## Resumo Fornecido ao Usuário

```markdown
## Plano de Implementação Criado ✅

### Visão Geral do Plano
- **Funcionalidade**: User Profile API
- **Fases**: 5 (Base → Core → Avatar → Busca → Testes)
- **Tarefas**: 19 tarefas criadas no TodoWrite

### Fases de Implementação

**Fase 1: Base**
- Esquema do banco de dados
- Setup de S3 e Redis
- Estrutura inicial da API

**Fase 2: Endpoints Principais**
- GET/PUT de perfil do usuário
- Autenticação e validação
- Rate limiting

**Fase 3: Upload de Avatar**
- Upload de imagem e validação
- Integração com S3
- Processamento de imagem

**Fase 4: Busca e Perfil Público**
- Busca de usuários
- Endpoint de perfil público

**Fase 5: Testes e Otimização**
- Testes unitários e de integração
- Testes de performance
- Documentação

### Arquivos Criados
- docs/planos/user-profile-api.md (plano completo)
- 19 tarefas no TodoWrite

### Próximos Passos
1. Revisar o plano
2. Iniciar Fase 1 (Base)

**Pronto para iniciar a implementação!**
```

## Principais Funcionalidades Demonstradas

### Análise de Spec
- Requisitos extraídos (funcionais e não funcionais)
- Endpoints da API identificados
- Modelo de dados anotado
- Critérios de aceitação capturados
- Requisitos de segurança compreendidos

### Planejamento de Implementação
- Quebra em fases lógicas
- Sequenciamento adequado (base → funcionalidades → testes)
- Dependências identificadas

### Criação de Tarefas
- 19 tarefas específicas geradas no TodoWrite
- Cada tarefa com content e activeForm
- Tarefas ordenadas por fase

Perfeito para: implementação de funcionalidades, desenvolvimento de API, projetos técnicos
