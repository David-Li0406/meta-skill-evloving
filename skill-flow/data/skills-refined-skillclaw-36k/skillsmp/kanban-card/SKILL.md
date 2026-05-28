---
name: kanban-card
description: Cria cards no Kanban board. Use quando usuário pedir para criar tarefa, card, ticket, issue, ou adicionar algo ao backlog.
allowed-tools: Bash
---

# Kanban Card Creator

## Propósito

Criar cards no Kanban board através do chat. Quando o usuário pedir para criar uma tarefa, issue, ticket ou card, extraia as informações e crie via API.

## Quando usar

- Usuário pede para "criar um card"
- Usuário pede para "adicionar uma tarefa"
- Usuário pede para "criar um ticket/issue"
- Usuário menciona algo que precisa ser feito no backlog

## Instruções

### 1. Extrair informações da mensagem

Do pedido do usuário, extraia:
- **Título**: O que será feito (obrigatório)
- **Descrição**: Detalhes adicionais se houver (opcional)

### 2. Criar o card via API

Execute o seguinte comando, substituindo os valores:

```bash
curl -s -X POST http://localhost:3001/api/cards \
  -H "Content-Type: application/json" \
  -d '{"title": "TITULO_AQUI", "description": "DESCRICAO_AQUI"}'
```

Se não houver descrição, omita o campo:

```bash
curl -s -X POST http://localhost:3001/api/cards \
  -H "Content-Type: application/json" \
  -d '{"title": "TITULO_AQUI"}'
```

### 3. Confirmar ao usuário

Após executar, informe:
- Que o card foi criado
- O título do card
- Que está no backlog

## Exemplos

### Exemplo 1: Pedido simples
**Usuário**: "Cria um card para implementar login"
**Ação**: Extrair título "Implementar login"
**Comando**:
```bash
curl -s -X POST http://localhost:3001/api/cards \
  -H "Content-Type: application/json" \
  -d '{"title": "Implementar login"}'
```

### Exemplo 2: Com descrição
**Usuário**: "Adiciona uma tarefa para corrigir o bug de timeout na API. O problema acontece quando a conexão demora mais de 30s"
**Ação**: Extrair título e descrição
**Comando**:
```bash
curl -s -X POST http://localhost:3001/api/cards \
  -H "Content-Type: application/json" \
  -d '{"title": "Corrigir bug de timeout na API", "description": "O problema acontece quando a conexão demora mais de 30s"}'
```

### Exemplo 3: Múltiplos cards
**Usuário**: "Cria 3 cards: autenticação, dashboard e relatórios"
**Ação**: Executar 3 comandos curl separados

## Notas

- O card sempre é criado na coluna "backlog"
- Os modelos padrão (opus-4.5) são usados automaticamente
- A API retorna o ID do card criado na resposta
