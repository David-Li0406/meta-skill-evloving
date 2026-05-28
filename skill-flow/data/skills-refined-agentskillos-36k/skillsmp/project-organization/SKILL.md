---
name: project-organization
description: Regras para organização de projetos em config/ vs logs/ - quando usar cada pasta
triggers: [config, logs, projeto, freelancer, proposta, organizar, mover, estrutura]
---

# Organização de Projetos - Config vs Logs

**Regras críticas para organização de projetos e propostas.**

---

## ⚠️ REGRA CRÍTICA - Projetos Freelancer

### `config/work/freelancer/` - Apenas Projetos Reais

**Esta pasta contém APENAS projetos que viraram projetos reais** (em desenvolvimento ou concluídos).

**Critérios para ficar em `config/work/freelancer/`:**
- ✅ Projeto aprovado e em desenvolvimento
- ✅ Projeto concluído
- ✅ Projeto com estrutura técnica definida (arquitetura, specs, etc.)
- ✅ Projeto com código em desenvolvimento

**Estrutura obrigatória:**
```
config/work/freelancer/[projeto]/
├── README.md                    # Visão geral
├── requisitos-tecnicos/        # Requisitos técnicos
├── requisitos-processos/       # Regras de negócio
├── arquitetura-diagramas/      # Decisões de arquitetura
└── consulta/                   # Arquivos de referência
```

---

### `logs/work/freelancer/` - Propostas e Temporários

**Esta pasta contém propostas e projetos temporários que não viraram projetos reais.**

**Critérios para ir para `logs/work/freelancer/`:**
- ❌ Apenas propostas enviadas (sem aprovação ainda)
- ❌ Projetos temporários que não viraram projetos
- ❌ Análises e estudos de viabilidade que não resultaram em projeto
- ❌ Contexto de negociação que não evoluiu para projeto

**Objetivo:** Evitar acumular contexto permanente com coisas que não vingaram, mantendo o `config/` limpo e focado apenas em projetos reais.

---

## 🔄 Quando Mover de Logs para Config

**Quando um projeto temporário for aprovado e iniciado:**

1. **Mover** a pasta de `logs/work/freelancer/` para `config/work/freelancer/`
2. **Aplicar** estrutura padrão (requisitos-tecnicos, requisitos-processos, etc.)
3. **Criar** `README.md` com visão geral do projeto
4. **Manter** histórico relevante em `logs/work/[projeto]/historico-contexto/`

---

## 📋 Checklist de Decisão

### Perguntar antes de criar em `config/work/freelancer/`:

- [ ] O projeto foi aprovado pelo cliente?
- [ ] O projeto está em desenvolvimento ativo?
- [ ] Existe estrutura técnica definida (arquitetura, specs)?
- [ ] O projeto tem código sendo desenvolvido?

**Se TODAS as respostas forem SIM** → `config/work/freelancer/`  
**Se ALGUMA resposta for NÃO** → `logs/work/freelancer/`

---

## 🎯 Regra Geral para Todos os Projetos

### `config/work/[projeto]/` ou `config/studies/[projeto]/`
- **Conteúdo**: Requisitos técnicos, regras de negócio, decisões de arquitetura
- **Propósito**: Documentação permanente do projeto
- **Estrutura**: Padronizada (requisitos-tecnicos, requisitos-processos, arquitetura-diagramas, consulta)

### `logs/work/[projeto]/` ou `logs/studies/[projeto]/`
- **Conteúdo**: Interação diária, dailys, histórico de contexto
- **Propósito**: Rastreamento de evolução e decisões do dia a dia
- **Estrutura**: historico-contexto/ e interacao-diaria/

**Regra:** Logs de interação sempre ficam em `logs/`, nunca em `config/`.

---

## 📝 Exemplos

### Exemplo 1: Proposta não aprovada
- **Localização**: `logs/work/freelancer/[nome-proposta]/`
- **Conteúdo**: Proposta enviada, contexto do cliente, análise técnica
- **Status**: Não aprovado, não virou projeto
- **Ação**: Manter em `logs/`

### Exemplo 2: Projeto aprovado e iniciado
- **Localização**: `config/work/freelancer/[nome-projeto]/`
- **Conteúdo**: Arquitetura, specs, requisitos, código
- **Status**: Em desenvolvimento
- **Ação**: Estrutura padrão aplicada

### Exemplo 3: Análise de viabilidade
- **Localização**: `logs/work/freelancer/[nome-analise]/`
- **Conteúdo**: Análise técnica, estimativas, decisão de não prosseguir
- **Status**: Não virou projeto
- **Ação**: Manter em `logs/`

---

## ⚠️ Importante

**NUNCA acumular contexto permanente** com coisas que não vingaram ou ficaram apenas na fase de proposta. Isso mantém o `config/` limpo, organizado e focado apenas em projetos reais.

---

**Última Atualização:** 2026-01-23

