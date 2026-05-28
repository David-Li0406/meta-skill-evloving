---
name: task-planner
description: Decomposição de tarefas complexas de desenvolvimento em steps executáveis, estimativas de esforço, identificação de dependências, e criação de planos de trabalho. Usar para planejar refatorações, migrações de sistemas, implementação de features complexas, e organizar sprints de desenvolvimento.
---

# Task Planner

Skill para planejamento e decomposição de tarefas de desenvolvimento.

## Framework de Decomposição

### Estrutura de Tarefa

```markdown
## [NOME DA TAREFA]

### Contexto
- O que existe atualmente
- Por que a mudança é necessária
- Resultado esperado

### Dependências
- [ ] Pré-requisitos técnicos
- [ ] Acessos necessários
- [ ] Decisões pendentes

### Subtarefas
1. [Subtarefa 1] - [Estimativa]
2. [Subtarefa 2] - [Estimativa]
...

### Riscos
- Risco 1: [Mitigação]
- Risco 2: [Mitigação]

### Critérios de Aceite
- [ ] Critério 1
- [ ] Critério 2

### Estimativa Total: [X horas/dias]
```

## Exemplo: Migração de Sistema Legado

```markdown
# Migração SKYNET-COPAC para Laravel

## Contexto
Sistema PHP procedural de 15 anos com código espaguete, sem testes, 
estrutura de arquivos desorganizada. Objetivo: estruturar em MVC 
antes de migrar para Laravel.

## Fase 1: Análise e Preparação (1 semana)

### 1.1 Mapeamento do Sistema Atual
- [ ] Listar todos os arquivos PHP (2h)
- [ ] Identificar entry points (páginas principais) (4h)
- [ ] Mapear includes/requires (2h)
- [ ] Documentar fluxos críticos (8h)
**Entregável**: Documento de arquitetura atual

### 1.2 Análise de Banco de Dados
- [ ] Gerar ERD do schema atual (2h)
- [ ] Identificar tabelas órfãs (2h)
- [ ] Documentar relacionamentos implícitos (4h)
- [ ] Listar queries mais frequentes (4h)
**Entregável**: Documentação de schema + ERD

### 1.3 Setup do Ambiente
- [ ] Criar ambiente Docker (4h)
- [ ] Configurar Git se não existir (2h)
- [ ] Setup de CI básico (4h)
**Entregável**: Ambiente replicável

---

## Fase 2: Refatoração Estrutural (3 semanas)

### 2.1 Organização de Diretórios (Semana 1)
- [ ] Criar estrutura MVC de pastas (1h)
- [ ] Mover arquivos de view para /views (4h)
- [ ] Separar configs em /config (2h)
- [ ] Isolar includes em /includes (4h)
- [ ] Atualizar paths nos arquivos (8h)
- [ ] Testar cada página após mudança (8h)
**Checkpoint**: Sistema funciona com nova estrutura

### 2.2 Extração de Modelos (Semana 2)
- [ ] Criar classe base Model (4h)
- [ ] Extrair User model (8h)
- [ ] Extrair Contract model (8h)
- [ ] Extrair Client model (8h)
- [ ] Extrair Payment model (8h)
- [ ] Criar relationships básicos (4h)
**Checkpoint**: CRUD via Models funcionando

### 2.3 Extração de Controllers (Semana 3)
- [ ] Criar classe base Controller (2h)
- [ ] Migrar lógica de usuários (8h)
- [ ] Migrar lógica de contratos (8h)
- [ ] Migrar lógica de clientes (8h)
- [ ] Migrar lógica de pagamentos (8h)
- [ ] Implementar routing básico (4h)
**Checkpoint**: Rotas funcionando via Controllers

---

## Fase 3: Infraestrutura Laravel (2 semanas)

### 3.1 Setup Laravel (Semana 4)
- [ ] Criar projeto Laravel novo (1h)
- [ ] Configurar database connection (2h)
- [ ] Gerar migrations do schema existente (8h)
- [ ] Criar Models Eloquent (8h)
- [ ] Configurar factories e seeders (8h)
**Checkpoint**: Laravel conectado ao DB existente

### 3.2 Migração de Features (Semana 5)
- [ ] Auth/Login (8h)
- [ ] CRUD de Clientes (8h)
- [ ] CRUD de Contratos (8h)
- [ ] CRUD de Pagamentos (8h)
- [ ] Dashboard básico (4h)
**Checkpoint**: Features principais no Laravel

---

## Fase 4: Testes e Deploy (1 semana)

### 4.1 Testes
- [ ] Testes de integração críticos (16h)
- [ ] Testes de API (8h)
- [ ] Teste de carga básico (4h)

### 4.2 Deploy
- [ ] Configurar servidor produção (4h)
- [ ] Script de deploy automatizado (4h)
- [ ] Rollback plan (2h)
- [ ] Monitoramento básico (2h)

---

## Resumo de Estimativas

| Fase | Duração | Horas |
|------|---------|-------|
| Análise | 1 semana | 34h |
| Refatoração | 3 semanas | 82h |
| Laravel | 2 semanas | 43h |
| Testes/Deploy | 1 semana | 40h |
| **TOTAL** | **7 semanas** | **~200h** |

## Riscos Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Código com dependências ocultas | Alta | Alto | Testes manuais após cada mudança |
| Dados inconsistentes no DB | Média | Alto | Auditoria prévia + scripts de correção |
| Resistência da equipe | Baixa | Médio | Documentação + treinamento |
| Downtime em produção | Baixa | Alto | Deploy em horário de baixo uso + rollback |

## Checkpoints de Go/No-Go

- [ ] **Semana 1**: Documentação completa → GO para refatoração
- [ ] **Semana 4**: MVC funcionando → GO para Laravel
- [ ] **Semana 6**: Features migradas → GO para testes
- [ ] **Semana 7**: Testes OK → GO para deploy
```

## Template: Feature Nova

```markdown
# Implementar [FEATURE]

## User Story
Como [PERSONA]
Quero [AÇÃO]
Para [BENEFÍCIO]

## Tasks

### Backend
- [ ] Migration: criar tabela X (1h)
- [ ] Model: criar com relationships (2h)
- [ ] FormRequest: validações (1h)
- [ ] Controller: CRUD completo (4h)
- [ ] Service: lógica de negócio (4h)
- [ ] Tests: unitários + feature (4h)

### Frontend
- [ ] Componentes de listagem (4h)
- [ ] Formulário de criação/edição (4h)
- [ ] Integração com API (2h)

### Docs
- [ ] Documentar endpoints (1h)
- [ ] Atualizar README (0.5h)

**Total estimado**: 27.5h (~4 dias)

## Critérios de Aceite
- [ ] CRUD completo funcionando
- [ ] Validações aplicadas
- [ ] Testes com >80% coverage
- [ ] Code review aprovado
```

## Técnicas de Estimativa

```markdown
## Fibonacci para Complexidade
1 - Trivial (< 2h)
2 - Simples (2-4h)
3 - Médio (4-8h)
5 - Complexo (1-2 dias)
8 - Muito complexo (3-5 dias)
13 - Épico (deve ser quebrado)

## Multiplicadores
- Código legado sem testes: x1.5
- Tecnologia nova: x1.3
- Integração externa: x1.4
- Primeira vez fazendo: x1.5

## Buffer de Segurança
- Tarefas conhecidas: +20%
- Tarefas com incerteza: +40%
- Tarefas com dependências externas: +50%
```
