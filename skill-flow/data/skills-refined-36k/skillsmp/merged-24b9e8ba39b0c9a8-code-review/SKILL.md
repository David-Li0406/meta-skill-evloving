---
name: code-review
description: Use this skill when you want to review code to ensure quality through a comprehensive checklist.
---

# Code Review Skill

Este skill é ativado quando o usuário quer revisar código para garantir qualidade.

## Checklist de Review

### 1. Qualidade de Código

- [ ] **Nomes claros**: Variáveis, funções e classes têm nomes descritivos?
- [ ] **Funções pequenas**: Funções fazem uma coisa só?
- [ ] **DRY**: Não há código duplicado?
- [ ] **Complexidade**: Lógica é simples de entender?
- [ ] **Tratamento de erros**: Erros são tratados adequadamente?

### 2. Padrões do Projeto

- [ ] **Estrutura**: Segue a arquitetura definida?
- [ ] **Nomenclatura**: Segue convenções do projeto?
- [ ] **Imports**: Organizados e sem dependências desnecessárias?
- [ ] **Estilo**: Consistente com o resto do código?

### 3. Segurança (OWASP Top 10)

- [ ] **Injection**: Input é sanitizado/validado?
- [ ] **XSS**: Output é escapado corretamente?
- [ ] **Auth**: Autenticação/autorização está correta?
- [ ] **Secrets**: Não há credenciais hardcoded?
- [ ] **Dados sensíveis**: Estão protegidos/criptografados?

### 4. Testes

- [ ] **Existem**: Testes foram escritos?
- [ ] **Coverage**: Coverage >= 80%?
- [ ] **Qualidade**: Testam comportamento, não implementação?
- [ ] **Edge cases**: Casos limites estão cobertos?

### 5. Performance

- [ ] **N+1**: Não há queries N+1?
- [ ] **Loops**: Não há loops desnecessários?
- [ ] **Memory**: Não há memory leaks óbvios?
- [ ] **Async**: Operações async são tratadas corretamente?

## Classificação de Issues

### CRITICAL (Bloqueador)
- Vulnerabilidades de segurança
- Bugs que quebram funcionalidade
- Violações graves de arquitetura

### HIGH (Importante)
- Falta de testes para código crítico
- Performance issues significativos
- Código muito difícil de manter

### MEDIUM (Recomendado)
- Melhorias de legibilidade
- Refatorações menores
- Documentação faltando

### LOW (Sugestão)
- Nitpicks de estilo
- Otimizações opcionais

## Formato de Feedback

```markdown
### [SEVERITY] Título da Issue

**Arquivo:** `path/to/file.ts:42`

**Problema:**
Descrição clara do problema encontrado.

**Sugestão:**
Como resolver ou melhorar.

**Exemplo:**
\`\`\`typescript
// Antes (problema)
// Depois (solução)
\`\`\`
```

## Pontos Positivos

Sempre mencione também o que está bom:
- Boas práticas seguidas
- Código bem estruturado
- Testes bem escritos
- Documentação clara