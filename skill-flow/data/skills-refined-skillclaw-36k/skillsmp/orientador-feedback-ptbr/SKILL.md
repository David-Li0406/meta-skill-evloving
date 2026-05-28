---
name: orientador-feedback-ptbr
description: Gera feedback crítico acadêmico no papel de orientador (PT-BR), priorizando problemas de rigor, relevância e precisão. Use quando o usuário pedir análise crítica, comentários de orientador, ou um relatório em project/review_feedback/.
license: Complete terms in LICENSE.txt
---

# Feedback Crítico (Orientador) — PT-BR

## Escopo
Use esta skill quando o usuário quiser uma análise crítica (não apenas correções) do texto acadêmico.

Regra central:
- **Não aplicar automaticamente mudanças de conteúdo/argumentação** (sugestões ficam como recomendações), a menos que o usuário peça para reescrever trechos específicos.

## Saída padrão (alinhado com repo policy)
- Responder com feedback estruturado por capítulo/arquivo, com prioridades **inline** (mensagem de resposta).
- **NÃO gerar arquivos por padrão** (respeita "No reports" do `.github/copilot-instructions.md`).

## Escrita de arquivo (opt-in)
Se o usuário **explicitamente pedir** "gere um relatório", "salve o feedback", ou similar:
- Escrever `.md` em `project/review_feedback/feedback_critico_<timestamp>.md`.
- Usar formato: `YYYYMMDD_HHMMSS` (ex.: `20260122_143000`).

## Categorias de problemas (alto valor)
1. Afirmações sem embasamento (sem citação/dados)
2. Generalizações excessivas
3. Trechos irrelevantes/prolixos para o nível do trabalho
4. Imprecisões técnicas ou desatualização
5. Justificativas metodológicas superficiais
6. Resultados sem análise (apenas descrição)

## Formato recomendado

## 📊 FEEDBACK CRÍTICO — [Arquivo/Capítulo]

### 🔴 Problemas Críticos (Prioridade Alta)
**[1] Título curto — Linha ~[X]**
Trecho: "..."
- Problema: ...
- Sugestões (2–3 opções): ...
- Ação recomendada: checklist

### 🟡 Sugestões de Aprofundamento (Prioridade Média)
...

### 🟢 Observações Menores (Prioridade Baixa)
...

### ✅ Pontos Fortes
- ...

## Princípios
- Ser específico (citar trecho e localização aproximada).
- Justificar o porquê do problema.
- Oferecer caminhos de solução, não apenas crítica.
- Contextualizar exigências ao tipo de trabalho (TCC 1 vs TCC 2 vs artigo).

## Quando NÃO criticar
- Preferência de estilo quando o texto já está correto.
- Escolhas metodológicas bem justificadas (a menos que haja erro técnico).
- Nível de detalhamento adequado ao escopo.
