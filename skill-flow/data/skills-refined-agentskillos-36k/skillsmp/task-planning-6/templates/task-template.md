# Tasks: [NOME DA FEATURE]

**PRD:** ./prd.md
**Data:** YYYY-MM-DD
**Total de Tasks:** N

---

## Resumo

| Tipo | Quantidade |
|------|------------|
| Setup | X |
| Implementacao | Y |
| Teste | Z |
| Documentacao | W |
| **Total** | **N** |

---

## Dependencias entre Tasks

```
Task 1 (Setup)
  └─> Task 2 (Implementacao)
        └─> Task 3 (Teste)
              └─> Task 4 (Documentacao)
```

---

## Tasks

### Task 1: [Setup Inicial]

**Tipo:** setup
**Prioridade:** P0
**Dependencias:** nenhuma
**Status:** [ ] Pendente | [ ] Em Progresso | [ ] Completo

**Descricao:**
[O que precisa ser feito]

**Arquivos:**
- Criar: `path/to/new/file.ts`
- Modificar: `path/to/existing/file.ts`

**Criterios de Aceitacao:**
- [ ] Criterio 1
- [ ] Criterio 2

**Comandos de Validacao:**
```bash
npm run type-check
npm test
```

---

### Task 2: [Implementar RF1]

**Tipo:** implementacao
**Prioridade:** P0
**Dependencias:** Task 1
**Status:** [ ] Pendente

**Descricao:**
Implementar [requisito funcional 1] conforme PRD.

**Arquivos:**
- Criar: `src/feature/handler.ts`
- Criar: `src/feature/handler.test.ts`
- Modificar: `src/routes/index.ts`

**Criterios de Aceitacao:**
- [ ] Endpoint responde corretamente
- [ ] Validacoes funcionam
- [ ] Erros retornam codigo correto

**Testes Necessarios:**
- [ ] Teste unitario: handler processa input valido
- [ ] Teste unitario: handler rejeita input invalido
- [ ] Teste integracao: endpoint completo

**TDD Steps:**
1. RED: Escrever `handler.test.ts` com testes que falham
2. GREEN: Implementar `handler.ts` minimo
3. REFACTOR: Melhorar codigo

---

### Task 3: [Implementar RF2]

**Tipo:** implementacao
**Prioridade:** P1
**Dependencias:** Task 2
**Status:** [ ] Pendente

[Mesma estrutura]

---

### Task 4: [Testes de Integracao]

**Tipo:** teste
**Prioridade:** P1
**Dependencias:** Task 2, Task 3
**Status:** [ ] Pendente

**Descricao:**
Criar testes de integracao para o fluxo completo.

**Arquivos:**
- Criar: `tests/integration/feature.test.ts`

**Criterios de Aceitacao:**
- [ ] Teste cobre fluxo completo
- [ ] Teste cobre casos de erro
- [ ] Coverage >= 80%

---

### Task 5: [Documentacao]

**Tipo:** documentacao
**Prioridade:** P2
**Dependencias:** Task 4
**Status:** [ ] Pendente

**Descricao:**
Documentar a feature implementada.

**Arquivos:**
- Modificar: `README.md`
- Modificar: `.claude/memory/architecture.md`
- Criar: `docs/feature-name.md`

**Criterios de Aceitacao:**
- [ ] README atualizado
- [ ] API documentada
- [ ] Exemplos incluidos

---

## Checklist Final

Antes de considerar feature completa:

- [ ] Todas as tasks completas
- [ ] Todos os testes passando
- [ ] Coverage >= 80%
- [ ] Documentacao atualizada
- [ ] Code review aprovado
- [ ] PRD criterios atendidos

---

## Notas

[Observacoes importantes durante implementacao]

---

## Historico

| Data | Task | Status | Notas |
|------|------|--------|-------|
| YYYY-MM-DD | Task 1 | Completo | Setup finalizado |
