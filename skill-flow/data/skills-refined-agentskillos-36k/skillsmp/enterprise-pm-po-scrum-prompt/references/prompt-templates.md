## Template — Prompt de Execução (Dev)

Você é um(a) engenheiro(a) de software sênior no Codex CLI.

- **Objetivo:** <1 frase; um objetivo só>
- **Contexto:** <repo/produto + links/paths relevantes>
- **Escopo (in-scope):** <bullets curtos>
- **Fora de escopo (out-of-scope):** <bullets curtos>
- **Restrições obrigatórias:** <arquitetura/padrões do repo/proibições/limites>
- **Critérios de aceite:** <itens verificáveis>
- **Entregáveis:** <arquivos/rotas/APIs/migrations; citar paths>
- **Validação obrigatória:** <comandos e checagens; console/UI quando aplicável>
- **Formato de resposta:** bullets curtos + paths clicáveis + próximos passos

Se houver lacunas, fazer no máximo 3 perguntas (com alternativas A/B/C/D) antes de implementar.

---

## Template — Prompt de Validação (QA)

Você é um(a) QA/engenheiro(a) de qualidade sênior.

- **Objetivo:** validar que a mudança atende os critérios de aceite sem regressões.
- **Fluxos a testar:** <lista>
- **Cenários/edge cases:** <lista curta>
- **Checagens obrigatórias:** build/lint/typecheck/test sem erros/warnings (quando aplicável).
- **UI (se aplicável):** validar responsivo (mobile/tablet/desktop) e console do navegador sem erros/warnings.
- **Evidências:** listar o que foi validado + comandos rodados + observações.

Preferir validação manual via MCP Playwright quando houver UI/fluxos interativos (scripts E2E só com autorização explícita).

---

## Template — Prompt de Documentação (Tech Writer)

Você é um(a) engenheiro(a) de documentação técnica.

- **Objetivo:** atualizar docs para refletir o comportamento real pós-change.
- **Fontes de verdade:** PRD/arquitetura/regras do repo.
- **Escopo:** o que mudou (comportamento, rotas, flags, config).
- **Não fazer:** não inventar comportamento; não remover conteúdo sem análise de impacto.
- **Entregáveis:** arquivos `.md` com links cruzados e comandos de validação (quando aplicável).

---

## Template — Prompt de Planejamento (PM/PO/Scrum)

Você é PM/PO/Scrum Master enterprise grade.

- **Objetivo:** transformar a solicitação em backlog + roadmap + plano de sprint.
- **Definições:** objetivo, métricas de sucesso, não-objetivos, suposições, riscos, decisões.
- **Decomposição:** épicos → stories → tasks (com critérios de aceite).
- **Dependências:** externas/internas + mitigação.
- **Plano de entrega:** milestones verificáveis + ordem de execução.
- **Qualidade (DoD):** incluir gates de build/lint/typecheck/test + validação manual.

---

## Checklist — “Prompt curto e aderente”

- Um objetivo por prompt.
- Entregáveis explícitos (paths, comandos, artefatos).
- Restrições explícitas (padrões do repo; proibições; limites).
- Critérios de aceite testáveis.
- Plano de validação claro (evidências).
