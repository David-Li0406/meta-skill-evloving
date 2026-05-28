---
name: tdd-development
description: Skill para desenvolvimento guiado por testes (Test-Driven Development)
triggers:
  - "implementar"
  - "desenvolver"
  - "codar"
  - "programar"
  - "criar codigo"
---

# TDD Development Skill

Este skill e ativado quando o usuario quer implementar codigo. Garante que todo codigo seja escrito seguindo TDD.

## Ciclo Obrigatorio

### 1. RED - Escrever Teste que Falha

```typescript
describe('MinhaFuncao', () => {
  it('should fazer X quando Y', () => {
    const result = minhaFuncao(input);
    expect(result).toBe(expected);
  });
});
```

**Regras:**
- Escreva o teste ANTES do codigo
- O teste DEVE falhar inicialmente
- Teste define o comportamento esperado
- Commit: `test: add test for <funcionalidade>`

### 2. GREEN - Implementar Minimo

```typescript
function minhaFuncao(input: Input): Output {
  // Implementacao MINIMA para passar o teste
  return expected;
}
```

**Regras:**
- Implemente APENAS o necessario para passar
- Nao adicione funcionalidades extras
- Nao otimize prematuramente
- Commit: `feat: implement <funcionalidade>`

### 3. REFACTOR - Melhorar

```typescript
function minhaFuncao(input: Input): Output {
  // Codigo melhorado, mais limpo
  const processed = processInput(input);
  return formatOutput(processed);
}
```

**Regras:**
- Melhore sem mudar comportamento
- Testes DEVEM continuar passando
- Remova duplicacoes
- Melhore nomes
- Commit: `refactor: improve <o que melhorou>`

## Padroes de Teste

Ver `patterns/test-patterns.md` para exemplos.

## Anti-Padroes

### NAO FACA:

```typescript
// Implementar primeiro, testar depois
function feature() { ... }

// Teste que testa implementacao, nao comportamento
it('should call methodX', () => {
  expect(spy).toHaveBeenCalled();
});

// Teste que depende de outros testes
it('should do B after A', () => {
  // Depende do estado de teste anterior
});
```

### FACA:

```typescript
// Teste primeiro, implementar depois
it('should return X when Y', () => { ... });
function feature() { ... }

// Teste que testa comportamento
it('should return valid user', () => {
  expect(result.email).toBe('test@example.com');
});

// Teste independente
beforeEach(() => { /* setup limpo */ });
it('should do B', () => { ... });
```

## Outputs

- Testes em `*.test.ts` ou `*.spec.ts`
- Codigo em arquivos correspondentes
- Commits incrementais seguindo padrao
