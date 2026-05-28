---
name: cursor-handoff
description: Regras de transição entre Cursor e Claude Code
triggers: [handoff, transição, cursor, review]
---

# Cursor ↔ Claude Code Handoff

## Quando Usar

Ativar quando:
- Cursor terminou implementação
- Precisa de code review
- Precisa executar testes
- Precisa preparar commit

## Divisão de Responsabilidades

### CURSOR faz:
1. Escrita de código novo
2. Refatoração complexa
3. Debug interativo
4. Implementação de UI/UX

### CLAUDE CODE faz:
1. Code review (qualidade, padrões, segurança)
2. Execução de testes automatizados
3. Preparação de commits (COM PERMISSÃO)
4. Preparação de PRs (COM PERMISSÃO)

### HUMANO faz:
1. Definir requisitos
2. Aprovar commits/PRs
3. Revisar sugestões
4. Testes manuais exploratórios

## Fluxo de Handoff

### Cursor → Claude Code

```bash
# Após implementar
claude "review as alterações, rode os testes e reporte"

# Só review
claude "review as alterações"

# Preparar commit
claude "prepare o commit"
```

### Claude Code → Cursor

Quando encontrar issues:
```
Issues encontrados:
1. [CRÍTICO] [arquivo:linha] - descrição
2. [MÉDIO] [arquivo:linha] - descrição

Cursor: corrija os issues acima
```

Quando tudo OK:
```
Review aprovado. Sem issues.
Pronto para commit. Confirma?
```

## Regras Críticas

### Claude Code NUNCA faz sem permissão:
- `git commit`
- `git push`
- `git reset`
- Deletar arquivos
- Modificar código (só sugere)

### Claude Code SEMPRE faz:
- Mostrar diff antes de ações
- Pedir confirmação explícita
- Seguir conventional commits
- Reportar todos os issues encontrados

## Checklist de Handoff

### Cursor → Claude Code
- [ ] Código implementado e salvo
- [ ] Funcionalidade testada manualmente
- [ ] Sem erros de sintaxe óbvios

### Claude Code → Commit
- [ ] Review aprovado
- [ ] Testes passando
- [ ] Issues críticos corrigidos
- [ ] Mensagem de commit apropriada
- [ ] Confirmação do usuário obtida
