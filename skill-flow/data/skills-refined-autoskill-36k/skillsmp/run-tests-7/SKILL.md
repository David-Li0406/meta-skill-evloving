---
name: Run Tests
description: Executa testes unitários, integração e E2E do CarInsight
---

# Skill: Executar Testes

## Description

Use quando o usuário pedir para:
- "Roda os testes"
- "Testa se quebrou alguma coisa"
- "Roda os testes de integração"
- "Verifica o coverage"
- "Testa a funcionalidade X"

## Commands

### Todos os Testes
```bash
npm run test:run
```

### Testes Unitários
```bash
npm run test:unit
```

### Testes de Integração
```bash
npm run test:integration
```

### Testes E2E (End-to-End)
```bash
npm run test:e2e
```

### Com Relatório de Coverage
```bash
npm run test:coverage
```

### Watch Mode (Desenvolvimento)
```bash
npm run test:watch
```

### Interface Visual (Vitest UI)
```bash
npm run test:ui
```

## Smart Selection

Use estas regras para escolher o comando correto:

| Usuário menciona | Comando |
|------------------|---------|
| "unitário", "unit" | `npm run test:unit` |
| "integração", "integration", "API" | `npm run test:integration` |
| "e2e", "end-to-end", "ponta a ponta" | `npm run test:e2e` |
| "coverage", "cobertura" | `npm run test:coverage` |
| "watch", "assistir" | `npm run test:watch` |
| Nenhum específico | `npm run test:run` |

## Interpretando Resultados

- ✅ **PASS**: Teste passou
- ❌ **FAIL**: Teste falhou (verifique o log de erro)
- ⏭️ **SKIP**: Teste pulado (provavelmente marcado com `.skip`)

## Troubleshooting

Se os testes falharem:
1. Verifique se as dependências estão instaladas (`npm install`)
2. Verifique se o arquivo `.env.test` existe
3. Para testes de integração, o banco de dados pode precisar estar configurado
