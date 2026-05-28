---
name: scripts-logs-organization
description: Regras obrigatórias para organização de scripts temporários, logs, feedbacks e planejamentos
triggers: [script, log, feedback, relatorio, planejamento, temporario, @temp, analise, resumo, daily]
---

# Organização de Scripts e Logs

**Regras obrigatórias para scripts temporários, logs, feedbacks e planejamentos.**

**Última Atualização:** 2026-01-23

---

## ⚠️ REGRA CRÍTICA

**NUNCA criar pastas `@temp/` em `config/` ou na raiz do projeto.**

Todos os arquivos temporários devem ir para `logs/` conforme as regras abaixo.

---

## 📋 Scripts Temporários

### Definição

Scripts de verificação, validação, execução avulsa, uso de MCP que **não fazem parte do código do projeto**.

### Localização

**Obrigatória:** `logs/[frente]/[projeto]/scripts-temporarios/` ou `logs/system/scripts-temporarios/`

**NUNCA criar em:**
- ❌ `config/` ou qualquer subpasta de `config/`
- ❌ `@temp/` (não existe mais)
- ❌ Raiz de projetos com git (exceto em `logs/`)

### Formato de Nome

`YYYY-MM-DD_[assunto].py` ou `YYYY-MM-DD_[assunto].sh`

**Exemplos:**
- `2025-12-08_verificar_notion.py`
- `2025-12-08_testar_mcp.py`
- `2025-12-08_limpar_dados.sh`

### Regras

- ✅ Devem ser apagados periodicamente (após uso ou mensalmente)
- ✅ Nunca devem ir para projetos com git
- ✅ Devem ter data e assunto no nome
- ✅ São descartáveis após uso

### Exemplos de Uso

- Scripts de verificação de Notion
- Scripts de validação de configuração
- Scripts de teste de MCP
- Scripts de deploy específico
- Scripts de atualização pontual

---

## 📝 Scripts Permanentes/Genéricos

### Definição

Scripts muito utilizados e requisitados que devem ser reutilizáveis.

### Localização

**Obrigatória:** `scripts/` (raiz do cursor-multiagent-system)

### Características

- ✅ Bem estruturados (classes, funções modulares)
- ✅ Muito bem documentados (exemplos, uso, explicação)
- ✅ Executáveis por linha de comando
- ✅ Aceitam parâmetros de entrada diferentes
- ✅ Genéricos e reutilizáveis
- ✅ Sem dados sigilosos (tokens, usuários, IPs)
- ✅ Dados sigilosos em arquivos `.env` em `config/`

### Exemplos

- Scripts de validação genérica
- Scripts de deploy genérico
- Scripts de sincronização
- Utilitários comuns

---

## 📄 Scripts Específicos de Projetos

### Definição

Scripts que fazem parte do código do projeto.

### Localização

Dentro da estrutura do projeto específico (não em `logs/`)

### Regras

- ✅ Fazem parte do projeto
- ✅ Podem ser versionados no git do projeto
- ✅ Específicos para aquele projeto

---

## 📝 Feedback, Relatórios, Planejamentos e Documentos Gerados por IA

### Localização

**Obrigatória:** `logs/[frente]/[projeto]/interacao-diaria/` ou `logs/[frente]/[projeto]/historico-contexto/` ou `logs/system/interacao-diaria/`

**NUNCA criar em:**
- ❌ `config/` ou qualquer subpasta de `config/`
- ❌ `@temp/` (não existe mais)
- ❌ Raiz de projetos com git (exceto em `logs/`)

### Formato de Nome

`YYYY-MM-DD_[assunto].md` ou `PLANO_[ASSUNTO].md`

**Exemplos:**
- `2025-12-08_validacao_notion.md`
- `2025-12-08_analise_deploy.md`
- `2025-12-08_feedback_sessao.md`
- `2025-12-08_daily.md`
- `2025-12-08_planejamento-sprint.md`
- `PLANO_MIGRACAO_FRONTEND.md`
- `ESTRATEGIA_REFATORACAO.md`
- `ANALISE_TECNICA.md`

### Conteúdo

**Interação Diária** (`logs/[frente]/[projeto]/interacao-diaria/`):
- Dailys do projeto
- Logs de interação com chat
- Planejamentos diários
- Decisões tomadas em sessões
- Resumos de conversas
- Dúvidas e respostas
- Análises temporárias

**Histórico de Contexto** (`logs/[frente]/[projeto]/historico-contexto/`):
- Histórico de decisões importantes
- Mudanças de contexto
- Evolução do projeto
- Relatórios de análise
- Feedbacks de conversas com IA
- Relatórios de status
- Análises geradas por agentes
- **Arquivos de planejamento** (planos de migração, estratégias, análises de projeto)
- Documentos gerados por IA

### Regras

- ✅ Data e assunto no nome
- ✅ Logs mínimos possíveis
- ✅ Apenas quando necessário
- ✅ Nunca devem ir para projetos com git (exceto pastas de logs)
- ✅ Planejamentos são logs do projeto, não documentação do código

---

## 🗂️ Estrutura de Logs

```
logs/
├── personal/
│   └── [projeto]/
│       ├── historico-contexto/
│       ├── interacao-diaria/
│       └── scripts-temporarios/
├── studies/
│   └── [projeto]/
│       ├── historico-contexto/
│       ├── interacao-diaria/
│       └── scripts-temporarios/
├── work/
│   └── [projeto]/
│       ├── historico-contexto/
│       ├── interacao-diaria/
│       └── scripts-temporarios/
├── youtube/
│   └── [projeto]/
│       ├── historico-contexto/
│       ├── interacao-diaria/
│       └── scripts-temporarios/
└── system/
    ├── historico-contexto/
    ├── interacao-diaria/
    └── scripts-temporarios/
```

---

## 🚫 Proibições

1. ❌ **NUNCA criar scripts temporários em projetos com git** (exceto em `logs/`)
2. ❌ **NUNCA criar feedbacks/relatórios em projetos com git** (exceto em `logs/`)
3. ❌ **NUNCA criar arquivos de planejamento em projetos com git** (exceto em `logs/`)
4. ❌ **NUNCA commitar scripts temporários** em repositórios de projetos
5. ❌ **NUNCA commitar feedbacks/relatórios/planejamentos** em repositórios de projetos
6. ❌ **NUNCA commitar dados sigilosos** em scripts permanentes
7. ❌ **NUNCA criar scripts sem data e assunto** quando temporários
8. ❌ **NUNCA criar pastas `@temp/` em `config/` ou na raiz do projeto**

---

## ✅ Boas Práticas

1. **Scripts temporários:** criar em `logs/`, usar data e assunto, apagar após uso
2. **Scripts genéricos:** criar em `scripts/`, bem documentados, genéricos
3. **Scripts de projeto:** criar na estrutura do projeto
4. **Logs:** mínimos, com data e assunto, em `logs/`
5. **Planejamentos:** criar em `logs/[frente]/[projeto]/`, nunca no repositório do projeto
6. **Interação diária:** criar em `logs/[frente]/[projeto]/interacao-diaria/`

---

## 📚 Referências

- Scripts permanentes: `scripts/`
- Logs: `logs/[frente]/[projeto]/`
- Configs: `config/[frente]/[projeto]/`
- Skill relacionada: `skills/workflow/project-organization/SKILL.md`

---

**Última Atualização:** 2026-01-23

