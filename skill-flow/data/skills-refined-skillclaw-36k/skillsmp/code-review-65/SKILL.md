---
name: code-review
description: Padrões e checklist para code review
triggers: [review, qualidade, código, análise]
---

# Code Review Patterns

## Quando Usar

Ativar quando:
- Código novo foi implementado
- Pull request precisa de review
- Refatoração foi feita

## Checklist de Review

### 1. Funcionalidade
- [ ] Código faz o que deveria fazer
- [ ] Edge cases tratados
- [ ] Comportamento consistente

### 2. Qualidade
- [ ] Código legível e bem organizado
- [ ] Nomes descritivos (variáveis, funções, classes)
- [ ] Funções pequenas e focadas (< 50 linhas ideal)
- [ ] Sem código duplicado (DRY)
- [ ] Sem código morto/comentado

### 3. Segurança
- [ ] Sem credenciais hardcoded
- [ ] Input validation presente
- [ ] Sem SQL injection
- [ ] Sem XSS vulnerabilities
- [ ] Dados sensíveis protegidos
- [ ] Logs não expõem dados sensíveis

### 4. Performance
- [ ] Sem N+1 queries
- [ ] Algoritmos eficientes
- [ ] Recursos liberados corretamente
- [ ] Caching onde apropriado

### 5. Tratamento de Erros
- [ ] Erros capturados adequadamente
- [ ] Mensagens de erro úteis
- [ ] Fallbacks implementados
- [ ] Logging de erros

### 6. Testes
- [ ] Testes existem para nova funcionalidade
- [ ] Testes passando
- [ ] Cobertura adequada (> 80% ideal)
- [ ] Testes são legíveis

### 7. Documentação
- [ ] Funções públicas documentadas
- [ ] Complexidade explicada
- [ ] README atualizado se necessário

## Formato de Report

```markdown
## Code Review: [descrição]

### Sumário
- **Arquivos:** X modificados
- **Linhas:** +Y / -Z
- **Issues:** A críticos, B médios, C baixos

### Issues Encontrados

#### Críticos (bloqueia merge)
1. **[arquivo:linha]** Descrição
   - Problema: ...
   - Solução: ...

#### Médios (deveria corrigir)
2. **[arquivo:linha]** Descrição

#### Baixos (nice to have)
3. **[arquivo:linha]** Descrição

### Pontos Positivos
- Boa separação de responsabilidades
- Testes bem escritos

### Recomendações
1. ...
2. ...

### Veredicto
- [ ] Aprovado
- [ ] Aprovado com ressalvas
- [ ] Precisa de correções
```

## Severidade de Issues

### Crítico
- Bugs que quebram funcionalidade
- Vulnerabilidades de segurança
- Perda de dados possível
- **Ação:** Bloqueia merge

### Médio
- Code smells
- Performance issues
- Falta de testes
- **Ação:** Deveria corrigir

### Baixo
- Estilo/formatação
- Melhorias opcionais
- Documentação
- **Ação:** Nice to have

## Boas Práticas de Review

### DO
- Seja específico e construtivo
- Sugira soluções, não só problemas
- Reconheça código bem escrito
- Foque no código, não na pessoa

### DON'T
- Críticas pessoais
- Nitpicking excessivo
- Bloquear por preferência pessoal
- Ignorar contexto/deadline
