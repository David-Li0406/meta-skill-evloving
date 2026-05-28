---
name: docker-execution
description: Agentes DEVEM executar containers e scripts, não apenas mostrar comandos
triggers: [docker, container, compose, build, run, execute, script, make]
---

# Docker e Scripts - Execução Obrigatória

**REGRAS RÍGIDAS: Agentes DEVEM executar, não apenas mostrar comandos.**

---

## Regra de Ouro: EXECUTAR, NÃO MOSTRAR

### ❌ PROIBIDO

```
Para subir o container, execute:
docker compose up -d

Para ver os logs:
docker compose logs -f
```

**NUNCA fazer isso!** O agente deve EXECUTAR, não pedir para o usuário executar.

### ✅ CORRETO

O agente deve:
1. **Executar o comando diretamente**
2. **Mostrar a saída**
3. **Analisar logs se necessário**
4. **Verificar se está funcionando**
5. **Reportar o resultado**

---

## Quando Executar Containers

**SEMPRE executar quando:**
- Usuário pede para "subir container"
- Usuário pede para "fazer build"
- Usuário pede para "ver logs"
- Usuário pede para "testar"
- Criar novo docker-compose.yml
- Modificar Dockerfile ou docker-compose.yml

**Processo obrigatório:**
1. Executar `docker compose up -d --build` (ou comando apropriado)
2. Aguardar conclusão
3. Verificar status com `docker compose ps`
4. Verificar logs iniciais com `docker compose logs --tail=50`
5. Reportar se está funcionando ou se há erros

---

## Prioridade: Makefile

**SEMPRE verificar se existe Makefile antes de executar comandos diretos:**

### Processo Obrigatório

1. **Verificar se existe Makefile**
2. **Se existe:** Usar comandos do Makefile
3. **Se não existe:** Criar comandos no Makefile primeiro
4. **Depois:** Executar via Makefile

### Exemplo

```bash
# ❌ ERRADO: Executar direto
docker compose up -d

# ✅ CORRETO: Verificar Makefile primeiro
# Se Makefile tem "make up" → usar "make up"
# Se não tem → criar no Makefile, depois executar
```

---

## Execução de Scripts

**SEMPRE executar scripts quando solicitado:**

### ❌ PROIBIDO

```
Para executar o script:
python scripts/setup.py
```

### ✅ CORRETO

1. Executar o script diretamente
2. Capturar saída
3. Verificar erros
4. Reportar resultado

---

## Análise de Logs

**Após executar container, SEMPRE:**
1. Verificar logs iniciais
2. Procurar por erros
3. Verificar se serviços estão saudáveis
4. Reportar status

**Comandos obrigatórios após subir container:**
```bash
# Status
docker compose ps

# Logs recentes
docker compose logs --tail=100

# Logs de serviço específico
docker compose logs service-name --tail=50

# Health check (se configurado)
docker compose ps --format json | jq '.[] | {name: .Name, status: .State, health: .Health}'
```

---

## Checklist

- [ ] Comando foi EXECUTADO (não apenas mostrado)
- [ ] Makefile verificado antes de executar
- [ ] Container subiu com sucesso
- [ ] Logs verificados
- [ ] Status reportado ao usuário
- [ ] Erros identificados e reportados (se houver)

