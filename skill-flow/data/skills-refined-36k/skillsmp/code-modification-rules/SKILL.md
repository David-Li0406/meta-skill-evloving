---
name: code-modification-rules
description: Regras críticas sobre quando e como modificar código existente
triggers: [modify, change, alter, refactor, update code, edit]
---

# Code Modification Rules

**Regras fundamentais sobre quando e como modificar código existente.**

---

## Quando Usar

Aplicar esta skill quando:
- O usuário solicita modificações em código existente
- Há dúvida sobre o escopo de uma alteração
- Precisando decidir se deve fazer "melhorias" não solicitadas

---

## Regra Fundamental

**SÓ ALTERAR O QUE FOI EXPLICITAMENTE SOLICITADO:**

- ✅ Alterar apenas o que foi explicitamente solicitado pelo usuário
- ❌ NÃO fazer alterações "melhorias" não solicitadas
- ❌ NÃO remover código que não foi pedido para remover
- ❌ NÃO adicionar funcionalidades que não foram solicitadas
- ❌ NÃO refatorar código que não foi pedido para refatorar

---

## Proibições Absolutas

**NUNCA fazer sem solicitação explícita:**

1. Remover código existente
2. Adicionar novas funcionalidades
3. Refatorar código
4. Alterar estrutura de arquivos
5. Modificar configurações existentes
6. Alterar nomes de variáveis/funções/classes
7. Mudar estilo de código
8. Adicionar ou remover dependências
9. Modificar migrations Django/Alembic (já aplicadas)
10. Alterar arquivos de configuração (nginx, docker, etc.)

---

## Quando o Usuário Pede uma Alteração

**Fazer apenas:**
1. A alteração específica solicitada
2. Alterações mínimas necessárias para a alteração funcionar
3. Manter tudo o resto exatamente como estava

---

## Exemplos

### Exemplo 1: Adicionar Endpoint

**Solicitação:** "adicionar endpoint GET /users"

**✅ Correto:**
- Criar apenas o endpoint solicitado
- Seguir estrutura existente
- Não alterar outros endpoints
- Não refatorar código existente

**❌ Incorreto:**
- Refatorar todos os endpoints
- Alterar estrutura de pastas
- Adicionar funcionalidades extras
- Modificar outros arquivos não relacionados

### Exemplo 2: Corrigir Bug

**Solicitação:** "corrigir bug no cálculo de desconto"

**✅ Correto:**
- Corrigir apenas o bug específico
- Manter resto do código igual
- Não "melhorar" outras partes

**❌ Incorreto:**
- Refatorar toda a função
- Alterar outras funções relacionadas
- Adicionar validações extras não solicitadas

---

## Quando Há Dúvida

**Se não tiver certeza se deve alterar algo:**
1. Fazer apenas o que foi explicitamente pedido
2. Se necessário, perguntar ao usuário antes de alterar
3. NUNCA assumir que "melhorias" são desejadas

---

## Exceções Permitidas

**Alterações permitidas sem solicitação explícita:**
1. Correção de erros de sintaxe que impedem execução
2. Correção de imports quebrados necessários para a alteração
3. Ajustes mínimos de formatação para manter consistência (apenas se não alterar lógica)

---

## Checklist

Antes de fazer qualquer alteração:
- [ ] A alteração foi explicitamente solicitada?
- [ ] Estou alterando apenas o necessário?
- [ ] Não estou fazendo "melhorias" não solicitadas?
- [ ] Não estou removendo código não relacionado?
- [ ] Não estou adicionando funcionalidades extras?

---

## Referências

- **Migrations:** `skills/backend/fastapi/SKILL.md` e `skills/backend/django/SKILL.md`
- **Templates:** `core/templates/`

---

**Esta regra é crítica e deve ser seguida rigorosamente por todos os agentes.**

