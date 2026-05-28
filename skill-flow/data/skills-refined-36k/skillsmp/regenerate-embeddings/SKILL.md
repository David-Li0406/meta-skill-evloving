---
name: Regenerate Embeddings
description: Gerencia embeddings vetoriais do CarInsight para busca semântica
---

# Skill: Regenerar Embeddings Vetoriais

## Description

Use quando o usuário pedir para:
- "Gera os embeddings"
- "Atualiza os vetores"
- "Novos veículos foram adicionados, atualiza"
- "Mostra estatísticas de embeddings"
- "Regenera os embeddings"

## Commands

### Gerar Embeddings (Incremental)
Gera embeddings apenas para veículos que ainda não possuem:
```bash
npm run embeddings:generate
```

### Forçar Regeneração (Todos)
Regenera TODOS os embeddings, mesmo os existentes:
```bash
npm run embeddings:force
```

### Ver Estatísticas
Mostra quantidade de embeddings gerados e pendentes:
```bash
npm run embeddings:stats
```

## Smart Selection

| Usuário menciona | Comando |
|------------------|---------|
| "forçar", "todos", "regenerar tudo" | `npm run embeddings:force` |
| "estatísticas", "quantos", "stats" | `npm run embeddings:stats` |
| Nenhum específico | `npm run embeddings:generate` |

## Informações Técnicas

- **Provedor Primário**: OpenAI `text-embedding-3-small` (1536 dimensões)
- **Fallback**: Cohere `embed-multilingual-v3.0` (1024→1536 dimensões)
- **Custo**: ~$0.02 por 1M tokens (OpenAI)
- **Armazenamento**: PostgreSQL (campo JSON)

## Quando Usar

1. **Após adicionar novos veículos**: Use `embeddings:generate`
2. **Após mudar modelo de embedding**: Use `embeddings:force`
3. **Para debug/verificação**: Use `embeddings:stats`

## Warning

> ⚠️ `embeddings:force` consome API tokens e pode demorar.
> 
> Use apenas quando necessário (ex: mudança de modelo).
