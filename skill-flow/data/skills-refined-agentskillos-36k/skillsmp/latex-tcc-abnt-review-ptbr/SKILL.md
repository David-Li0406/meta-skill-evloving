---
name: latex-tcc-abnt-review-ptbr
description: Revisão sistemática de TCC/dissertação em LaTeX com foco em ABNT (PT-BR). Use quando solicitado para revisar capítulos, corrigir gramática/formatação, padronizar termos técnicos e validar estrutura/figuras/tabelas.
license: Complete terms in LICENSE.txt
---

# Revisão de TCC (ABNT) em LaTeX — PT-BR

## Escopo
Use esta skill para revisar projetos LaTeX de TCC (ABNT), aplicando correções diretamente nos arquivos permitidos.

Restrições obrigatórias (sempre respeitar):
- Nunca editar `template/` nem `sample*`.
- Priorizar correções objetivas; preservar a voz do autor.

## Modo padrão (default)
**Revisão com melhoria moderada de fluidez**:
- Corrigir ortografia, concordância, pontuação e clareza.
- Melhorar conectivos e coesão *sem* alterar sentido técnico.
- Evitar reescritas extensas; mudanças devem ser incrementais.

Se o autor pedir “mínima intervenção”, fazer apenas correções objetivas (ortografia/formatação), sem reestruturar períodos.

## Workflow recomendado (three-phase model)
1. **Discovery Phase**
   - Ler `prompt.md` (se existir) — contém checklist detalhado de 397 linhas.
   - Mapear todos os `.tex` com `file_search: "project/**/*.tex"`.
   - Identificar arquivo principal (ex.: `project/tcc.tex`) e o grafo de `\input`/`\include`.
   - **CRITICAL**: Use `manage_todo_list` para criar ~10 tarefas (pré-textuais → capítulos → apêndices → validação).

2. **Systematic Revision Phase**
   - Para cada tarefa:
     - Marcar como "in-progress".
     - Ler arquivo completo (50-100 linhas por vez).
     - Aplicar correções (use `multi_replace_string_in_file` quando múltiplas edições independentes).
     - Marcar como "completed" IMEDIATAMENTE.

3. **Validation Phase**
   - Rodar `grep_search` para verificar consistência (termos, itálico, aspas, espaços duplos).
   - Executar `get_errors` no arquivo principal quando disponível.
   - Confirmar 100% da todo-list completa.

## Checklist ABNT/LaTeX (itens comuns)
### Figuras
- Possuem `\\caption{}`, `\\label{}` e indicação de fonte (ex.: `\\centerline{{Fonte: ...}}`).
- São referenciadas no texto com `\\ref{fig:...}`.

### Tabelas
- `\\caption{}` acima, `\\label{}` e fonte (ex.: `\\footnotesize{Fonte: ...}`).
- Referenciadas no texto com `\\ref{tab:...}`.

### Termos técnicos estrangeiros
- Padronizar com itálico: `\\textit{back-end}`, `\\textit{front-end}`, `\\textit{offline}`, `\\textit{framework}`, `\\textit{middleware}`, etc.

### Aspas
- Evitar aspas retas: usar ``assim'' em LaTeX.

### Concordância e vírgulas com citação
- “Segundo `\\cite{...}`, ...” (vírgula após a citação quando apropriado).

## Padrões linguísticos (PT-BR acadêmico)
- Preferir impessoalidade: “Foi implementado…” em vez de “Nós implementamos…”.
- Evitar “através de” quando significar meio: usar “por meio de”.
- Evitar intensificadores vagos (“muito”, “bastante”) sem qualificação.

## Buscas de validação (sugestões)
- `através de|atraves`
- `back-end|front-end|offline|framework|middleware` (verificar itálico)
- `  +` (espaços duplos)

## Resultado esperado
- Texto corrigido e padronizado.
- Estrutura/elementos obrigatórios conferidos.
- Sem alterações em `template/` e `sample*`.
