---
name: tdd-development
description: Use this skill when you want to implement code following Test-Driven Development (TDD) principles.
---

# TDD Development Skill

Este skill é ativado quando o usuário quer implementar código. Garante que todo código seja escrito seguindo TDD.

## Ciclo Obrigatório

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
- Escreva o teste ANTES do código.
- O teste DEVE falhar inicialmente.
- O teste define o comportamento esperado.
- Commit: `test: add test for <funcionalidade>`

### 2. GREEN - Implementar Mínimo

```typescript
function minhaFuncao(input: Input): Output {
  // Implementação MÍNIMA para passar o teste
  return expected;
}
```

**Regras:**
- Implemente APENAS o necessário para passar.
- Não adicione funcionalidades extras.
- Não otimize prematuramente.
- Commit: `feat: implement <funcionalidade>`

### 3. REFACTOR - Melhorar

```typescript
function minhaFuncao(input: Input): Output {
  // Código melhorado, mais limpo
  const processed = processInput(input);
  return formatOutput(processed);
}
```

**Regras:**
- Melhore sem mudar o comportamento.
- Testes DEVEM continuar passando.
- Remova duplicações.
- Melhore nomes.
- Commit: `refactor: improve <o que melhorou>`

## Padrões de Teste

Ver `patterns/test-patterns.md` para exemplos.

## Anti-Padrões

### NÃO FAÇA:

```typescript
// Implementar primeiro, testar depois
function feature() { ... }

// Teste que testa implementação, não comportamento
it('should call methodX', () => {
  expect(spy).toHaveBeenCalled();
});

// Teste que depende de outros testes
it('should do B after A', () => {
  // Depende do estado de teste anterior
});
```

### FAÇA:

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

- Testes em `*.test.ts` ou `*.spec.ts`.
- Código em arquivos correspondentes.
- Commits incrementais seguindo padrão.