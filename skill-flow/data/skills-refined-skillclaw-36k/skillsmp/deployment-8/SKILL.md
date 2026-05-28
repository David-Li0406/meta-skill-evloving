---
name: deployment
description: Processos gerais de deploy, validação, backup e boas práticas para deploy em produção
triggers: [deploy, deployment, production, server, ssh, hostinger, render, vercel, backup, rollback]
---

# Deployment - Processos e Boas Práticas

**Processos gerais de deploy, validação, backup e boas práticas para deploy em produção.**

**Última Atualização:** 2026-01-23

---

## Quando Usar

Aplicar esta skill quando:
- Fazer deploy em servidores de produção
- Configurar CI/CD
- Validar antes de deploy
- Fazer backup antes de mudanças críticas
- Documentar processos de deploy
- Configurar SSH, Docker, Nginx em servidores

---

## Princípios Core

### 1. Validação Obrigatória Antes de Deploy

**SEMPRE validar antes de fazer deploy:**

1. ✅ Testar em ambiente de desenvolvimento primeiro
2. ✅ Verificar migrations/alterações de banco
3. ✅ Verificar variáveis de ambiente
4. ✅ Verificar dependências e serviços
5. ✅ Verificar health checks configurados
6. ✅ Verificar logs de desenvolvimento

### 2. Backup Antes de Mudanças Críticas

**SEMPRE fazer backup antes de:**
- Aplicar migrations
- Atualizar versões de dependências críticas
- Modificar configurações de banco de dados
- Deploy de features grandes
- Mudanças em infraestrutura

**Processo de Backup:**
```bash
# Banco de dados
docker exec <db-container> pg_dump -U <user> <database> > backup_$(date +%Y%m%d).sql

# Arquivos media/static
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### 3. Documentação de Mudanças

**SEMPRE documentar:**
- Mudanças importantes em deploy
- Problemas encontrados e soluções
- Configurações específicas do servidor
- Processos de rollback (se necessário)

### 4. Testar em Desenvolvimento Primeiro

**NUNCA fazer deploy direto em produção:**
- ✅ Testar localmente primeiro
- ✅ Testar em ambiente de staging (se disponível)
- ✅ Validar todos os serviços
- ✅ Verificar logs e health checks

---

## Processos de Deploy

### Deploy via Docker Compose

**Seguir skill:** `skills/infrastructure/docker-execution/SKILL.md`

**Processo:**
1. Verificar Makefile primeiro (seguir `skills/infrastructure/makefile/SKILL.md`)
2. Executar comandos via Makefile
3. Verificar logs após deploy
4. Validar health checks

**Comandos típicos:**
```bash
# Via Makefile (preferencial)
make up-prod
make migrate
make health

# Ou direto (se Makefile não tem)
docker compose -f docker-compose.prod.yml up -d --build
```

### Deploy via SSH

**Processo:**
1. Conectar via SSH
2. Navegar para diretório do projeto
3. Pull das mudanças (se necessário)
4. Executar deploy via Makefile ou Docker Compose
5. Verificar logs e status

**Exemplo:**
```bash
ssh root@<server-ip>
cd /apps/<project>
git pull origin main
make up-prod
make logs
```

### Deploy via CI/CD

**Processo:**
1. Push para branch de produção
2. CI/CD detecta mudanças
3. Build automático
4. Deploy automático
5. Health checks automáticos
6. Notificações (se configurado)

---

## Plataformas de Deploy

### Hostinger (VPS)

**Características:**
- Servidores VPS com Docker
- Deploy via SSH + Docker Compose
- Configuração manual de Nginx e SSL
- Credenciais: Carregar de `config/.env.passwords`

**Processo:**
1. SSH no servidor
2. Navegar para diretório do projeto
3. Executar deploy via Makefile
4. Configurar Nginx (se necessário)
5. Configurar SSL (se necessário)

### Render.com

**Características:**
- Blueprint-based deployment
- Ambiente gerenciado
- Deploy automático via Git push
- API Key: Carregar de `config/.env.passwords` como `RENDER_API_KEY`

**Processo:**
1. Push para branch configurada
2. Render detecta mudanças automaticamente
3. Build e deploy de todos os serviços
4. Health checks automáticos

### Vercel

**Características:**
- Deploy de frontends e serverless
- Configuração via CLI ou Dashboard
- Deploy automático via Git push

**Processo:**
1. Configurar projeto no Vercel
2. Conectar repositório
3. Push para branch configurada
4. Deploy automático

---

## Validação Pós-Deploy

**SEMPRE verificar após deploy:**

1. **Health Checks**
   ```bash
   curl http://<server>/health
   make health
   ```

2. **Logs Iniciais**
   ```bash
   make logs
   docker compose logs --tail=100
   ```

3. **Status dos Serviços**
   ```bash
   make ps
   docker compose ps
   ```

4. **Acesso à Aplicação**
   - Verificar se aplicação carrega
   - Verificar endpoints principais
   - Verificar admin/dashboard (se aplicável)

---

## Rollback

**Processo de rollback:**

1. **Identificar versão anterior**
   ```bash
   git log --oneline
   git checkout <commit-anterior>
   ```

2. **Restaurar backup (se necessário)**
   ```bash
   docker exec -i <db-container> psql -U <user> <database> < backup.sql
   ```

3. **Redeploy**
   ```bash
   make up-prod
   ```

4. **Validar**
   ```bash
   make health
   make logs
   ```

---

## Troubleshooting

### Serviço não inicia
1. Verificar logs: `make logs` ou `docker compose logs`
2. Verificar variáveis de ambiente
3. Verificar conexão com banco
4. Verificar dependências (Redis, etc)
5. Verificar portas disponíveis

### Migration falha
1. Verificar conexão com banco
2. Verificar permissões
3. Verificar estado atual das migrations
4. Fazer backup antes de corrigir
5. Verificar logs de migration

### Health check falha
1. Verificar se serviço está rodando
2. Verificar porta e endpoint
3. Verificar logs do serviço
4. Verificar dependências (Redis, DB)

---

## Checklist de Deploy

### Antes do Deploy
- [ ] Testado em desenvolvimento
- [ ] Migrations validadas
- [ ] Variáveis de ambiente configuradas
- [ ] Backup feito (se necessário)
- [ ] Health checks configurados
- [ ] Logs verificados em dev

### Durante o Deploy
- [ ] Deploy executado via Makefile (preferencial)
- [ ] Logs monitorados
- [ ] Erros identificados e tratados

### Após o Deploy
- [ ] Health checks passaram
- [ ] Logs verificados (sem erros críticos)
- [ ] Status dos serviços verificado
- [ ] Aplicação acessível
- [ ] Funcionalidades principais testadas
- [ ] Documentação atualizada (se necessário)

---

## Referências

- **Docker Execution:** `skills/infrastructure/docker-execution/SKILL.md`
- **Makefile:** `skills/infrastructure/makefile/SKILL.md`
- **Docker Compose:** `skills/infrastructure/docker-compose/SKILL.md`
- **Scripts Temporários:** `skills/workflow/scripts-logs/SKILL.md`
- **Git/Commits:** `skills/workflow/commit-workflow/SKILL.md`

---

**Última Atualização:** 2026-01-23

