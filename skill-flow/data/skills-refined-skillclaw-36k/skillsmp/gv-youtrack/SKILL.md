---
name: gv-youtrack
description: Guia de utilização do YouTrack no Grupo Voalle. Use sempre que precisar interagir com cards do YouTrack para seguir o workflow correto.
autoContext: true
---

# YouTrack - Grupo Voalle

Guia completo para utilização do YouTrack nos projetos do Grupo Voalle.

## Quando Usar

- Mover status de cards
- Registrar tempo de trabalho
- Criar ou atualizar issues
- Vincular issues do GitLab

## Estrutura de Issues

### Hierarquia

```
Epic
└── User Story (US)
    └── Task (onde ficam as issues do GitLab)
```

- **Epic**: Grandes iniciativas ou funcionalidades
- **User Story**: Entregáveis de valor para o usuário
- **Task**: Trabalho técnico específico (código, testes, etc.)

### Issues do GitLab

As issues do GitLab são vinculadas às **Tasks** no YouTrack, não às User Stories diretamente.

Exemplo:
- US: `ORN-1148 - Renderização especiais de mensagem`
- Task: `ORN-1155 - [Task Frontend] Renderização especiais de mensagem`
- GitLab Issue: `#50` (vinculada à Task)

## Etapas (State)

| Etapa | Descrição |
|-------|-----------|
| Upstream | Ideação, descoberta, refinamento |
| Downstream | Desenvolvimento ativo |
| Landing | Aguardando deploy |

**IMPORTANTE**: Novas Tasks devem ser criadas na etapa **Downstream**.

## Workflow de Status

O YouTrack possui workflows que **restringem transições de status**. Não é possível pular etapas.

### Fluxo típico de Review

```
Backlog-Review → In Progress-Review → Waiting for Validation → Backlog-QA
```

### Transições permitidas

| Status Atual | Próximos Status Permitidos |
|--------------|---------------------------|
| Backlog-Review | In Progress-Review |
| In Progress-Review | Waiting for Validation, Backlog-Fixing-DEV |
| Waiting for Validation | Backlog-QA, Backlog-Fixing-DEV |

### Exemplo de movimentação correta

```python
# ERRADO - Pular etapas
Backlog-Review → Waiting for Validation  # ❌ Bloqueado pelo workflow

# CORRETO - Seguir o fluxo
Backlog-Review → In Progress-Review      # ✅ Primeiro
In Progress-Review → Waiting for Validation  # ✅ Depois
```

## Registro de Tempo de Trabalho

Ao atualizar status ou concluir trabalho, **sempre registre o tempo gasto**.

### Registro obrigatório antes de sair

O workflow **bloqueia** a saída dos seguintes status se não houver tempo registrado:

| Status | Requer tempo para sair |
|--------|------------------------|
| In Progress DEV | ✅ Sim |
| In Progress-Review | ✅ Sim |
| Waiting for Validation | ✅ Sim |

**Mensagem de erro típica:**
```
❌ É necessário registrar tempo antes de mover para "Waiting for Validation".
```

**Solução:** Registre o tempo de trabalho com `log_work` antes de atualizar o status.

### Tipos de trabalho disponíveis

- Testing
- Fixing
- Study
- Implementation
- Code Review
- Test Case
- Deploy
- Analysis
- Validation
- Code Review Test Case
- Automation E2E
- Script

### Exemplo

```
issueId: ORN-1148
durationMinutes: 15
description: "Code review e correções no MR !104"
workType: "Code Review"
```

## Verificação Pós-Atualização

**SEMPRE** verifique se a atualização foi aplicada após qualquer mudança:

1. Após `update_issue`, faça `get_issue` para confirmar
2. Se o status não mudou, verifique os comentários do card (o workflow pode ter rejeitado)
3. Mensagens de erro aparecem como comentários do "Job Automation"

### Padrão de mensagem de erro

```
❌ De 'Backlog-Review' não é permitido ir para 'Waiting for Validation'.
Opções permitidas a partir de 'Backlog-Review': In Progress-Review
```

## Boas Práticas

1. **Antes de mover status**: Verifique qual é o status atual e as transições permitidas
2. **Após mover status**: Sempre confirme com `get_issue`
3. **Registre tempo**: Toda movimentação deve ter tempo de trabalho registrado
4. **Vincule corretamente**: Issues do GitLab vão nas Tasks, não nas US
5. **Use a etapa correta**: Tasks novas sempre em Downstream

## Campos Customizados Importantes

| Campo | Descrição |
|-------|-----------|
| Status | Estado atual no workflow |
| State | Etapa (Upstream/Downstream/Production) |
| Atendente | Responsáveis pela issue |
| Data repactuada | Prazo acordado |
| Tempo gasto | Horas trabalhadas (calculado automaticamente) |
| Peso | Complexidade (1-10) |

## Queries Úteis

```
# Issues em revisão
project: {EV Orion} Status: {Backlog-Review}, {In Progress-Review}

# Minhas issues
for: me State: Downstream

# Issues sem atendente
project: {EV Orion} Atendente: -?
```
