---
name: Deploy Railway
description: Deploy do CarInsight para Railway com verificações prévias
---

# Skill: Deploy para Railway

## Description

Use quando o usuário pedir para:
- "Faz deploy"
- "Sobe pra Railway"
- "Publica as alterações"
- "Manda pro ar"
- "Deploy para produção"

## Pre-Flight Checks

> ⚠️ **IMPORTANTE**: Antes de fazer deploy, SEMPRE execute estes checks:

### 1. Verificar Lint
```bash
npm run lint
```

### 2. Verificar Build
```bash
npm run build
```

### 3. Rodar Testes
```bash
npm run test:run
```

## Deploy (após checks passarem)

### Via Git Push (Railway Auto-Deploy)
```bash
git add -A
git commit -m "deploy: <descrição das mudanças>"
git push origin main
```

### Script de Deploy Otimizado
```bash
./scripts/deploy-railway-optimized.bat
```

## Warning

> 🚨 **NUNCA faça deploy se os testes falharem!**
> 
> Informe o usuário sobre os erros encontrados e ajude a corrigi-los antes.

## Post-Deploy

Após o deploy, verifique:
1. Status no dashboard Railway
2. Logs da aplicação: `railway logs`
3. Health check: `curl https://carinsight.up.railway.app/admin/health`

## Rollback

Se algo der errado:
```bash
git revert HEAD
git push origin main
```

Ou reverta pelo dashboard da Railway.
