---
name: Health Check
description: Verifica o status da API e serviços do CarInsight
---

# Skill: Verificar Status da API

## Description

Use este skill quando o usuário perguntar:
- "O servidor está rodando?"
- "A API está online?"
- "Está tudo funcionando?"
- "Verifica o status pra mim"
- "Health check"

## Usage

Execute o script `check_health.ts` para verificar o status de todos os serviços.

```bash
npx tsx .antigravity/skills/health-check/check_health.ts
```

Alternativamente, faça uma requisição GET para o endpoint de health:

```bash
curl http://localhost:3000/admin/health
```

## Expected Output

O script retorna um JSON com status de:
- **Server**: Se o Express está rodando
- **Database**: Conexão com PostgreSQL via Prisma
- **LLM Router**: Status do OpenAI/Groq
- **Embedding Service**: Status do serviço de embeddings

## Troubleshooting

Se o health check falhar:
1. Verifique se o servidor está rodando (`npm run dev`)
2. Verifique as variáveis de ambiente no `.env`
3. Verifique a conexão com o banco de dados
