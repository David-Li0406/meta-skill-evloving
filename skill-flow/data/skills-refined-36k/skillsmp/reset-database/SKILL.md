---
name: Reset Database
description: Reset e seed do banco de dados do CarInsight
---

# Skill: Reset e Seed do Banco de Dados

## Description

Use quando o usuário pedir para:
- "Reseta o banco pra mim"
- "Popula o banco com dados de teste"
- "Limpa o banco e popula de novo"
- "Roda o seed"
- "Faz push do schema"

## Commands

### Aplicar Schema (sem perda de dados)
```bash
npm run db:push
```

### Seed com Dados Reais (Recomendado)
```bash
npm run db:seed:real
```

### Seed Básico
```bash
npm run db:seed
```

### Abrir Prisma Studio (UI para visualizar dados)
```bash
npm run db:studio
```

## Warning

> ⚠️ **ATENÇÃO**: Este skill MODIFICA dados do banco.
> 
> - Sempre confirme com o usuário antes de executar em **produção**
> - O seed sobrescreve dados existentes
> - Faça backup antes se houver dados importantes

## Workflow Recomendado

1. Aplicar schema: `npm run db:push`
2. Popular dados: `npm run db:seed:real`
3. Gerar embeddings: `npm run embeddings:generate`
