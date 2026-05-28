---
name: Task & Subtask Writer Expert
description: Especialista em documentar Tasks/Bugs e Subtasks, focando em detalhamento técnico e critérios de aceite.
---

# Task & Subtask Writer Expert

Esta skill guia a criação de documentação para Tasks isoladas, Bugs e Subtasks técnicas. Seu foco é o **Engenheiro** e **Líder Técnico**.

## Estrutura e Localização

A documentação deve ser feita localmente antes de qualquer interação com o Jira.

1.  **Localização:**
    *   Se pertence a um Épico/Parcial: Salve dentro da pasta correspondente (`temporario/analises/{NomeEpico}/...`).
    *   Se for avulsa: Salve diretamente em `temporario/analises/`.
    *   Nome do arquivo: `{NomeDaTask}.md`.

2.  **Hierarquia:**
    *   **Task/Story/Bug:** Entregas funcionais ou correções. (Se tem épico, é filha do épico).
    *   **Subtask:** Tickets estritamente técnicos de desenvolvimento para um sistema específico (Filha de uma Task/Story).
        *   Exemplos: `[Widget API] Criação e Edição de View Mode`, `[Atom] Criação de componente`.

## Criação no Jira (MCP Rovo)
*   **Regra de Ouro:** Apenas crie o ticket no Jira quando **solicitado explicitamente**.
*   **Vínculo:** Ao criar, pergunte em qual **BOARD**. Adicione o Link do Jira gerado no topo do arquivo `.md`.

## Template Obrigatório

O arquivo `.md` deve seguir ESTRITAMENTE este padrão:

```markdown
[SISTEMA] Descrição do ticket

Link Jira: [se existir]

Razão do ticket:
- Descrever o motivo do ticket
- Por que ele é importante
- Qual o impacto de não resolvê-lo

Definition of Done:
- O que precisa ser feito para considerar o ticket concluído
- Quais são as entregas esperadas (resumo)
- Qual processo de qualidade deve ser feito

História:
COMO [quem]
QUERO [o que]
PARA [por que]

Cenários:
Número do cenário - Descrição do cenário
COMO [quem]
DADO QUE [condição]
QUANDO [ação]
ENTÃO [resultado esperado]

Regras para Cenários:
- Escritos em primeira pessoa (usuário final).
- Contexto de TESTE FUNCIONAL.
- Fáceis de testar, claros e objetivos.
- Cobrir sucesso e falha.
- Atenção ao contexto de uso (API vs Tela).
  - Ex: "COMO usuário do ViewMode...", "COMO consumidor da Widget API...".

Observações técnicas: (se existirem)
```
