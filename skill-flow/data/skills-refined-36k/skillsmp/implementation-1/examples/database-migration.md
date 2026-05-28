# Exemplo: Implementação de Migração de Banco de Dados

**Solicitação do Usuário**: "Planeje e implemente a migração do banco para o schema de preferências do usuário"

## Fluxo

### 1. Encontrar e Ler Spec
```
Glob
pattern: "**/*migration*spec*.md"

Read
file_path: "docs/specs/user-preferences-migration.md"
```

**Resumo da Spec**: Migrar de blob JSON para schema estruturado para melhor performance e integridade de dados.

### 2. Analisar Requisitos
- **Atual**: Coluna de preferências JSONB
- **Alvo**: Tabelas separadas `user_preferences` e `notification_preferences`
- **Deve manter**: Compatibilidade retroativa durante a migração
- **Performance**: Suportar 1M+ usuários com zero downtime

### 3. Criar Plano de Implementação
```
Write
file_path: "docs/planos/user-preferences-migration.md"
content: "[Plano completo de implementação com fases]"
```

**Plano incluiu**:
- **Fase 1**: Criar novas tabelas com índices
- **Fase 2**: Backfill de dados a partir do JSONB
- **Fase 3**: Modo dual-write (tanto antigo quanto novo)
- **Fase 4**: Trocar leituras para o novo schema
- **Fase 5**: Remover coluna JSONB antiga

### 4. Criar Tarefas no TodoWrite

```
TodoWrite
todos: [
  {
    "content": "Escrever scripts SQL de migração",
    "activeForm": "Escrevendo scripts SQL de migração",
    "status": "pending"
  },
  {
    "content": "Implementar job de backfill",
    "activeForm": "Implementando job de backfill",
    "status": "pending"
  },
  {
    "content": "Adicionar lógica de dual-write na API",
    "activeForm": "Adicionando lógica de dual-write na API",
    "status": "pending"
  },
  {
    "content": "Atualizar queries de leitura",
    "activeForm": "Atualizando queries de leitura",
    "status": "pending"
  },
  {
    "content": "Criar plano de rollback e monitoramento",
    "activeForm": "Criando plano de rollback e monitoramento",
    "status": "pending"
  }
]
```

### 5. Acompanhar Progresso

Conforme o trabalho avança, atualizar o TodoWrite:

```
TodoWrite
todos: [
  {
    "content": "Escrever scripts SQL de migração",
    "activeForm": "Escrevendo scripts SQL de migração",
    "status": "completed"
  },
  {
    "content": "Implementar job de backfill",
    "activeForm": "Implementando job de backfill",
    "status": "in_progress"
  },
  ...
]
```

## Principais Entregas

**Arquivo do Plano de Implementação** (docs/planos/user-preferences-migration.md)
**5 Tarefas no TodoWrite** (com dependências implícitas pela ordem)
**Acompanhamento de Progresso** (atualizado conforme o trabalho avança)

## Fatores de Sucesso
- Quebra de migração complexa em fases claras
- Tarefas criadas com escopo bem definido
- Dependências estabelecidas (Fase 1 → 2 → 3 → 4 → 5)
- Abordagem de zero downtime com plano de rollback
- Todo o trabalho vinculado à spec original
