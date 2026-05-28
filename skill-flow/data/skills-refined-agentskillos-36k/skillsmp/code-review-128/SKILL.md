---
name: code-review
description: Skill para revisar codigo com checklist de qualidade
triggers:
  - "revisar codigo"
  - "code review"
  - "review"
  - "analisar codigo"
  - "verificar qualidade"
---

# Code Review Skill

Este skill e ativado quando o usuario quer revisar codigo para garantir qualidade.

## Checklist de Review

### 1. Qualidade de Codigo

- [ ] **Nomes claros**: Variaveis, funcoes e classes tem nomes descritivos?
- [ ] **Funcoes pequenas**: Funcoes fazem uma coisa so?
- [ ] **DRY**: Nao ha codigo duplicado?
- [ ] **Complexidade**: Logica e simples de entender?
- [ ] **Tratamento de erros**: Erros sao tratados adequadamente?

### 2. Padroes do Projeto

- [ ] **Estrutura**: Segue a arquitetura definida?
- [ ] **Nomenclatura**: Segue convencoes do projeto?
- [ ] **Imports**: Organizados e sem dependencias desnecessarias?
- [ ] **Estilo**: Consistente com o resto do codigo?

### 3. Seguranca (OWASP Top 10)

- [ ] **Injection**: Input e sanitizado/validado?
- [ ] **XSS**: Output e escapado corretamente?
- [ ] **Auth**: Autenticacao/autorizacao esta correta?
- [ ] **Secrets**: Nao ha credenciais hardcoded?
- [ ] **Dados sensiveis**: Estao protegidos/criptografados?

### 4. Testes

- [ ] **Existem**: Testes foram escritos?
- [ ] **Coverage**: Coverage >= 80%?
- [ ] **Qualidade**: Testam comportamento, nao implementacao?
- [ ] **Edge cases**: Casos limites estao cobertos?

### 5. Performance

- [ ] **N+1**: Nao ha queries N+1?
- [ ] **Loops**: Nao ha loops desnecessarios?
- [ ] **Memory**: Nao ha memory leaks obvios?
- [ ] **Async**: Operacoes async sao tratadas corretamente?

## Classificacao de Issues

### CRITICAL (Bloqueador)
- Vulnerabilidades de seguranca
- Bugs que quebram funcionalidade
- Violacoes graves de arquitetura

### HIGH (Importante)
- Falta de testes para codigo critico
- Performance issues significativos
- Codigo muito dificil de manter

### MEDIUM (Recomendado)
- Melhorias de legibilidade
- Refatoracoes menores
- Documentacao faltando

### LOW (Sugestao)
- Nitpicks de estilo
- Otimizacoes opcionais

## Formato de Feedback

```markdown
### [SEVERITY] Titulo da Issue

**Arquivo:** `path/to/file.ts:42`

**Problema:**
Descricao clara do problema encontrado.

**Sugestao:**
Como resolver ou melhorar.

**Exemplo:**
\`\`\`typescript
// Antes (problema)
// Depois (solucao)
\`\`\`
```

## Pontos Positivos

Sempre mencione tambem o que esta bom:
- Boas praticas seguidas
- Codigo bem estruturado
- Testes bem escritos
- Documentacao clara
