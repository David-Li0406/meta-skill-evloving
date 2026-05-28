---
name: Epic Writer Expert
description: Especialista em documentar Épicos e Parciais, focando no contexto de negócio e estrutura macro.
---

# Epic Writer Expert

Esta skill guia a criação de documentação para Épicos (Jira Epics) e Parciais (Entregas de Valor). Seu foco é o **Analista de Negócios**.

## Estrutura e Localização

A documentação deve ser feita localmente antes de qualquer interação com o Jira.

1.  **Épico (Jira Epic):**
    *   Crie uma pasta: `temporario/analises/{NomeDoEpico}/`.
    *   Arquivo principal: `{NomeDoEpico}.md` dentro dessa pasta.
    *   Conteúdo: Artefatos de negócio e contexto macro do épico.

2.  **Parciais (Entregas de Valor - Jira Tasks/Stories):**
    *   Crie uma pasta (opcional, se complexo): `temporario/analises/{NomeDoEpico}/{NomeParcial}/`.
    *   Arquivo: `{NomeParcial}.md`.
    *   Conteúdo: Artefatos de negócio e contexto macro desta entrega parcial.

3.  **Exceção para Demandas Simples:**
    *   Se a demanda for pontual, simples e direta (não requer estrutura de Épico), o Analista pode criar diretamente uma **Task**.
    *   Neste caso, ignore esta skill e utilize diretamente a **Task & Subtask Writer Expert**.

## Criação no Jira (MCP Rovo)
*   **Regra de Ouro:** Apenas crie o ticket no Jira quando **solicitado explicitamente**.
*   **Vínculo:** Ao criar, pergunte em qual **BOARD**. Adicione o Link do Jira gerado no topo do arquivo `.md`.

## Template de Conteúdo (Épico/Parcial)

O arquivo `.md` deve seguir este padrão:

```markdown
[ÁREA/SISTEMA] Nome do Épico ou Parcial

Link Jira: [Adicionar link após criação]

Contexto de Negócio:
- Explicação detalhada da necessidade de negócio.
- Objetivos estratégicos (OKRs - Objectives and Key Results).
- KPIs (Key Performance Indicators) de sucesso.

Escopo:
- O que ESTÁ incluso (In-Scope).
- O que NÃO ESTÁ incluso (Out-of-Scope).

Roadmap/Parciais:
- Lista das entregas parciais planejadas.
```
