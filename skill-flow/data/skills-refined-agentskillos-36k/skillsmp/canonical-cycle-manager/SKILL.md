---
name: Canonical Cycle Manager
description: Especialista em gerenciar o fluxo do Canonical Cycle (Raw -> Filtered -> Canonical -> Artifacts).
---

# Canonical Cycle Manager

Esta skill fornece ferramentas e diretrizes para gerenciar o Canonical Cycle.

## Estrutura do Ciclo
O ciclo segue o fluxo:
`Raw Material` -> `Filtered Material` -> `Canonical Material` -> `Artifacts` -> `Delivery`

Toda estrutura reside em `archives/NUMERO_NOME/ROLE/`.

## Funcionalidades

### Diretrizes Gerais de Escrita
*   **Siglas:** Sempre que utilizar siglas (ex: OKRs, KPIs, ADRs, BDD), coloque o nome completo em parênteses na primeira citação. Exemplo: `OKRs (Objectives and Key Results)`.

### 1. Iniciar Novo Ciclo
Para iniciar um novo ciclo, utilize o script `init_cycle.py`.
**Uso:**
```bash
python3 .agent/skills/canonical-cycle/scripts/init_cycle.py <role> <cycle_name>
```
*Roles válidas:* analista, designer, arquiteto, engenheiro, desenvolvedor.

### 2. Guia de Processamento

Ao guiar o usuário pelo ciclo, siga estas etapas para cada estágio:

#### A. Raw Material
1.  Instrua o usuário a colocar todo o material bruto na pasta `raw/`.
2.  Isso pode incluir: anotações, transcripts, imagens, documentos desestruturados.

#### B. Filtered Material
1.  Após o Raw estar pronto, atue como a Role definida para processar o material.
2.  Leia o conteúdo de `raw/`.
3.  Organize, sintetize e esclareça dúvidas.
4.  **Validação de Ambiguidades:**
    *   Se houver pontos confusos, faltantes ou ambíguos no material bruto, crie uma seção explícita "Pontos para Definição" no arquivo filtrado.
    *   PERGUNTE ao usuário sobre esses pontos. O usuário pode responder via chat ou editando o próprio arquivo filtrado.
    *   Se necessário, atualize o `Filtered Material` com as respostas antes de prosseguir.
5.  Salve o resultado em `filter/`.
    *   Use templates se disponíveis em `canonicalCycleDoc/templates`.

#### C. Canonical Material
1.  Apresente o Filtered Material para o usuário revisar.
2.  **CRÍTICO:** O usuário (Humano) deve validar e aprovar.
3.  Faça os ajustes solicitados.
4.  Quando aprovado, salve a versão final em `canonical/`.
5.  Este é o ponto de verdade ("Source of Truth").

#### D. Artifacts
1.  Gere os artefatos de saída baseados EXCLUSIVAMENTE no `canonical/`.
2.  Salve em `artifacts/` ou aplique diretamente no projeto.

## Skills Específicas (Context Loading)

Para maximizar a eficácia de cada Role, o Agente **DEVE** carregar a skill específica da Role ativa no início do processo de filtragem.

*   **Analista:** Utilize `.agent/skills/analista/SKILL.md`
*   **Designer:** Utilize `.agent/skills/designer/SKILL.md`
*   **Arquiteto:** Utilize `.agent/skills/arquiteto/SKILL.md`
*   **Engenheiro:** Utilize `.agent/skills/engenheiro/SKILL.md`
*   **Desenvolvedor:** Utilize `.agent/skills/desenvolvedor/SKILL.md`

## Integração com Jira (Epic & Task Writers)

Se o ciclo envolver a criação de documentação para Jira (Épicos, Tasks, Subtasks), utilize as skills apropriadas:

*   **Para Épicos e Parciais (Contexto de Negócio):** Carregue `.agent/skills/epic-writer/SKILL.md`
*   **Para Tasks e Subtasks (Contexto Técnico):** Carregue `.agent/skills/task-writer/SKILL.md`

**IMPORTANTE:** Só utilize as ferramentas MCP Rovo para criar tickets após a documentação `.md` estar aprovada pelo usuário.
