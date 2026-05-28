---
name: daily-standup
description: Análise completa de status e planejamento diário usando Notion MCP
triggers: [daily, standup, planning, status, review, análise]
---

# Daily Standup - Análise Completa

**Análise profunda de status usando Notion MCP e contexto completo.**

---

## Quando Usar

Quando usuário pedir:
- "fazer daily"
- "standup"
- "review de status"
- "planejamento do dia"

---

## Processo Obrigatório

### 1. Solicitar Contexto

**SEMPRE perguntar de qual frente:**
- Trabalho
- Estudos
- Geral (todas as frentes)

### 2. Coletar Informações

**Usar Notion MCP (PRIORIDADE):**
- Buscar tarefas atrasadas (data final < hoje e status != concluído)
- Buscar tarefas em andamento (pelo status)
- Buscar tarefas não iniciadas com atraso (data inicial < hoje e não está em andamento)
- Buscar tarefas pendentes

**Analisar contexto:**
- Logs recentes (`logs/`)
- Arquivos temporários (`@temp/`)
- Contexto da conversa atual

### 3. Análise Profunda

**Fornecer:**
- Resumo executivo da situação
- Tarefas críticas/urgentes
- Tarefas em andamento
- Tarefas atrasadas
- Tarefas não iniciadas com atraso
- Proposta de cronograma para o dia
- Prioridades sugeridas

### 4. Proposta de Cronograma

**Incluir:**
- Sequência sugerida de execução
- Tempo estimado por tarefa
- Blocos de tempo disponíveis
- Dependências entre tarefas

---

## Formato de Resposta

```markdown
# Daily Standup - [Frente] - [Data]

## Resumo Executivo
- Total de tarefas: X
- Atrasadas: Y
- Em andamento: Z
- Pendentes: W

## 🔴 Críticas/Urgentes
- [Tarefa] (deadline: hoje)
- [Tarefa] (atrasada há X dias)

## 🟠 Em Andamento
- [Tarefa] (X% completo)
- [Tarefa] (bloqueada por Y)

## 🟡 Pendentes com Atraso
- [Tarefa] (deveria ter iniciado há X dias)

## 📅 Proposta de Cronograma
1. [09:00-10:00] Tarefa crítica X
2. [10:00-11:30] Tarefa Y
3. [14:00-16:00] Tarefa Z

## 💡 Recomendações
- Focar em [área] hoje
- Considerar delegar [tarefa]
```

---

## Checklist

- [ ] Frente solicitada (trabalho/estudos/geral)
- [ ] Notion MCP usado para buscar tarefas
- [ ] Contexto analisado (logs, temp, conversa)
- [ ] Análise profunda realizada
- [ ] Cronograma proposto
- [ ] Prioridades definidas

