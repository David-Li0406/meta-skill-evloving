# Frameworks de Métricas de Produto

Um guia abrangente para escolher e implementar frameworks de métricas de produto para medir sucesso.

---

## Índice

1. [Visão Geral](#visão-geral)
2. [AARRR (Pirate Metrics)](#aarrr-pirate-metrics)
3. [HEART Framework](#heart-framework)
4. [North Star Metric](#north-star-metric)
5. [OKRs (Objectives & Key Results)](#okrs-objectives--key-results)
6. [Métricas de Product-Market Fit](#métricas-de-product-market-fit)
7. [Métricas de Engajamento](#métricas-de-engajamento)
8. [Escolhendo o Framework Certo](#escolhendo-o-framework-certo)

---

## Visão Geral

### Por Que Métricas Importam

**Métricas ajudam você a:**

- Medir sucesso de features objetivamente
- Tomar decisões baseadas em dados
- Alinhar times em torno de objetivos compartilhados
- Identificar o que está funcionando e o que não está
- Comunicar impacto para stakeholders

### Tipos de Métricas

**Leading Indicators:** Preveem resultados futuros

- Exemplo: Sign-ups de trial gratuito → Receita futura

**Lagging Indicators:** Medem resultados passados

- Exemplo: Receita mensal, churn rate

**Actionable vs. Vanity Metrics**

- **Actionable:** Podem ser influenciadas por mudanças no produto (ex: conversion rate)
- **Vanity:** Parecem boas mas não direcionam decisões (ex: total de usuários registrados)

---

## AARRR (Pirate Metrics)

Criado por Dave McClure, este framework foca no ciclo de vida do cliente.

### Os Cinco Estágios

```
Acquisition → Activation → Retention → Revenue → Referral
```

### 1. Acquisition

**O quê:** Como usuários encontram você?

**Métricas Principais:**

- Website traffic
- App store impressions
- Click-through rate (CTR) de ads
- Cost per acquisition (CPA)
- Traffic sources (orgânico, pago, referral)

**Metas de Exemplo:**

- 10.000 visitantes mensais no website
- CAC < $50
- 5% CTR em paid ads

**Perguntas a Responder:**

- Quais canais trazem mais usuários?
- Qual nosso custo por canal?
- Quais campanhas convertem melhor?

---

### 2. Activation

**O quê:** Usuários têm uma ótima primeira experiência?

**Métricas Principais:**

- Sign-up completion rate
- Time to "aha moment"
- Porcentagem atingindo milestone chave
- Onboarding completion rate
- Feature adoption na primeira sessão

**Metas de Exemplo:**

- 60% sign-up completion
- 40% atingem "aha moment" na primeira sessão
- 80% completam onboarding

**Perguntas a Responder:**

- Como é uma ótima primeira experiência?
- Onde usuários desistem no onboarding?
- Quão rápido usuários encontram valor?

**Exemplos de "Aha Moments":**

- **Slack:** Enviar sua primeira mensagem
- **Dropbox:** Fazer upload do primeiro arquivo
- **Airbnb:** Completar sua primeira reserva

---

### 3. Retention

**O quê:** Usuários voltam?

**Métricas Principais:**

- Daily/Weekly/Monthly Active Users (DAU/WAU/MAU)
- Curvas de retenção (Day 1, Day 7, Day 30)
- Churn rate
- Frequência de sessão
- Uso de features ao longo do tempo

**Metas de Exemplo:**

- 40% retenção Day 7
- 25% retenção Day 30
- < 5% churn mensal

**Cohort Analysis:**

```
| Cohort    | Week 1 | Week 2 | Week 3 | Week 4 |
|-----------|--------|--------|--------|--------|
| Jan 2024  | 100%   | 45%    | 30%    | 25%    |
| Fev 2024  | 100%   | 50%    | 35%    | 28%    |
```

**Perguntas a Responder:**

- O que faz usuários voltarem?
- Quando usuários fazem churn?
- Como podemos re-engajar usuários inativos?

---

### 4. Revenue

**O quê:** Como você monetiza?

**Métricas Principais:**

- Monthly Recurring Revenue (MRR)
- Average Revenue Per User (ARPU)
- Customer Lifetime Value (LTV)
- Conversion to paid rate
- Upsell/cross-sell rate

**Metas de Exemplo:**

- 5% conversão free-to-paid
- $50 ARPU
- LTV:CAC ratio > 3:1

**Fórmulas:**

```
LTV = ARPU × Average Customer Lifespan
LTV:CAC = Lifetime Value ÷ Customer Acquisition Cost
Churn Rate = Customers Lost ÷ Total Customers × 100
```

**Perguntas a Responder:**

- Quais features impulsionam conversões?
- Qual nosso payback period?
- Como podemos aumentar ARPU?

---

### 5. Referral

**O quê:** Usuários contam para outros?

**Métricas Principais:**

- Viral coefficient (K-factor)
- Net Promoter Score (NPS)
- Referral rate
- Social shares
- Word-of-mouth attribution

**Metas de Exemplo:**

- 15% dos usuários indicam outros
- NPS > 50
- K-factor > 1 (crescimento viral)

**Fórmulas:**

```
K-factor = (Número de Convites por Usuário) × (Taxa de Conversão de Convites)
NPS = % Promoters - % Detractors
```

**Perguntas a Responder:**

- Por que usuários indicam outros?
- Como podemos incentivar referrals?
- O que nos torna compartilháveis?

---

### Exemplo AARRR: Produto SaaS

| Estágio     | Métrica                | Atual  | Meta   | Ações                       |
| ----------- | ---------------------- | ------ | ------ | --------------------------- |
| Acquisition | Visitantes mensais     | 50.000 | 75.000 | SEO, content marketing      |
| Activation  | Sign-ups de trial      | 5%     | 8%     | Melhorar landing page       |
| Retention   | Retenção Day 30        | 20%    | 30%    | Melhorias no onboarding     |
| Revenue     | Conversão free-to-paid | 3%     | 5%     | Redesign da pricing page    |
| Referral    | Usuários que indicam   | 8%     | 15%    | Lançar programa de referral |

---

## HEART Framework

Criado pelo Google, foca na qualidade da experiência do usuário.

### As Cinco Dimensões

**HEART = Happiness + Engagement + Adoption + Retention + Task Success**

---

### 1. Happiness

**O quê:** Satisfação e percepção do usuário

**Métricas:**

- Net Promoter Score (NPS)
- Customer Satisfaction (CSAT)
- Avaliações/reviews de usuários
- Sentimento de tickets de suporte
- Scores de feedback de usuários

**Métodos de Medição:**

- Surveys (pós-interação, periódicos)
- Avaliações em app stores
- Formulários de feedback in-app
- Sentimento em redes sociais

**Exemplo:**

```
Feature: Novo fluxo de checkout
Happiness Metric: CSAT score
Meta: > 4.5/5 média de avaliação
Medição: Survey pós-compra
```

---

### 2. Engagement

**O quê:** Nível de envolvimento do usuário

**Métricas:**

- Duração da sessão
- Páginas/telas por sessão
- Frequência de uso de features
- Tempo gasto no app
- Ações por sessão

**Exemplo:**

```
Feature: News feed
Engagement Metric: Sessões diárias por usuário
Atual: 1.2 sessões/dia
Meta: 2.0 sessões/dia
```

---

### 3. Adoption

**O quê:** Novos usuários ou adoção de features

**Métricas:**

- Sign-ups de novos usuários
- Taxa de adoção de features
- Tempo até primeiro uso
- Porcentagem de usuários experimentando nova feature

**Exemplo:**

```
Feature: Dark mode
Adoption Metric: % de usuários habilitando dark mode
Meta: 40% em 30 dias do lançamento
```

---

### 4. Retention

**O quê:** Usuários retornando ao longo do tempo

**Métricas:**

- DAU/WAU/MAU
- Curvas de retenção
- Churn rate
- Taxa de uso repetido

**Exemplo:**

```
Feature: Ferramentas de colaboração
Retention Metric: Times ativos semana a semana
Meta: 70% dos times ativos semanalmente
```

---

### 5. Task Success

**O quê:** Usuários conseguem atingir seus objetivos?

**Métricas:**

- Taxa de conclusão de tarefa
- Taxa de erro
- Tempo para completar tarefa
- Taxa de sucesso de busca

**Exemplo:**

```
Feature: Upload de arquivo
Task Success Metric: Taxa de conclusão de upload
Atual: 85%
Meta: 95%
Análise de erro: Timeouts em arquivos grandes
```

---

### Template do HEART Framework

| Dimensão         | Objetivos                         | Sinais                  | Métricas            |
| ---------------- | --------------------------------- | ----------------------- | ------------------- |
| **Happiness**    | Usuários amam a feature           | Feedback positivo       | NPS > 40            |
| **Engagement**   | Usuários interagem frequentemente | Uso ativo diário        | 60% DAU/MAU         |
| **Adoption**     | Maioria dos usuários experimenta  | Ativação da feature     | 70% adoção          |
| **Retention**    | Usuários continuam voltando       | Taxa de retorno semanal | 50% retenção W1     |
| **Task Success** | Usuários completam objetivos      | Baixa taxa de erro      | 95% taxa de sucesso |

---

## North Star Metric

Uma única métrica que melhor captura o valor central que você entrega aos clientes.

### Características de uma Boa North Star Metric

1. **Reflete entrega de valor** aos clientes
2. **Mede progresso** em direção à sua visão
3. **Actionable** pelo time
4. **Leading indicator** de receita
5. **Compreensível** por todos

---

### Exemplos por Empresa

| Empresa      | North Star Metric            | Por quê                               |
| ------------ | ---------------------------- | ------------------------------------- |
| **Airbnb**   | Noites reservadas            | Valor central: estadias bem-sucedidas |
| **Spotify**  | Tempo ouvindo                | Valor central: prazer musical         |
| **Slack**    | Mensagens enviadas por times | Valor central: comunicação            |
| **Facebook** | Daily Active Users           | Valor central: conexão social         |
| **Netflix**  | Horas assistidas             | Valor central: entretenimento         |
| **Uber**     | Corridas completadas         | Valor central: transporte             |
| **Medium**   | Tempo total lendo            | Valor central: conteúdo de qualidade  |

---

### Encontrando Sua North Star Metric

**Passo 1: Defina sua proposta de valor**

- Qual valor central você entrega?
- Qual é o "aha moment" para usuários?

**Passo 2: Identifique a métrica**

- Qual medição melhor captura esse valor?
- É um leading indicator de sucesso do negócio?

**Passo 3: Valide a métrica**

- Correlaciona com receita?
- Times podem influenciá-la?
- É compreensível?

**Passo 4: Defina metas e acompanhe**

- Qual a baseline atual?
- Qual a taxa de crescimento alvo?
- Como você medirá progresso?

---

### Árvore da North Star Metric

Desmembre sua North Star em métricas contribuintes:

```
North Star: Weekly Active Users
    ├── New User Acquisition
    │   ├── Sign-ups
    │   └── Onboarding completion
    ├── Activation
    │   └── Usuários atingindo "aha moment"
    └── Retention
        ├── Retenção Week 1
        └── Retenção Week 4
```

---

## OKRs (Objectives & Key Results)

Framework de definição de metas popularizado pelo Google.

### Estrutura

**Objective:** Objetivo qualitativo, inspirador
**Key Results:** Resultados quantitativos, mensuráveis (3-5 por objetivo)

---

### Escrevendo Bons OKRs

**Características do Objective:**

- Inspirador e motivador
- Qualitativo
- Time-bound (trimestral ou anual)
- Alinhado com estratégia da empresa

**Características do Key Result:**

- Quantitativo e mensurável
- Específico com metas claras
- Ambicioso mas alcançável
- 3-5 por objective

---

### Exemplos

#### Exemplo 1: OKR de Crescimento

**Objective:** Tornar-se a plataforma referência para faturamento de pequenas empresas

**Key Results:**

1. Aumentar empresas ativas mensais de 10.000 para 25.000
2. Atingir 40% de retenção mês a mês
3. Alcançar NPS de 50+
4. Gerar $500K MRR

---

#### Exemplo 2: OKR de Qualidade de Produto

**Objective:** Entregar uma experiência mobile de classe mundial

**Key Results:**

1. Reduzir crash rate do app de 2.5% para <0.5%
2. Atingir avaliação 4.5+ estrelas em ambas app stores
3. Melhorar tempo de carregamento do app para <2 segundos (p95)
4. Aumentar ratio DAU/MAU mobile de 30% para 45%

---

#### Exemplo 3: OKR de Lançamento de Feature

**Objective:** Lançar com sucesso features de colaboração em time

**Key Results:**

1. 60% dos usuários ativos experimentam features de colaboração em 30 dias
2. 25% dos usuários se tornam colaboradores ativos semanais
3. Features de colaboração geram 15% de aumento em conversões pagas
4. Atingir CSAT score de 4.2/5 para features de colaboração

---

### Template de OKR para PRDs

```markdown
## OKRs

### Objective: [Objetivo inspirador]

**Key Results:**

1. [Métrica 1]: Aumentar/diminuir [atual] para [meta] até [data]
2. [Métrica 2]: Atingir [valor alvo] para [métrica]
3. [Métrica 3]: [Resultado mensurável específico]

**Acompanhamento:**

- Status atual: [Relatório de progresso]
- Dashboard: [Link para dashboard de métricas]
- Cadência de revisão: [Semanal/quinzenal]
```

---

## Métricas de Product-Market Fit

Medindo se você atingiu product-market fit.

### Teste Sean Ellis

Pergunta do survey: **"Como você se sentiria se não pudesse mais usar [produto]?"**

- Muito desapontado
- Um pouco desapontado
- Não desapontado

**Threshold de PMF:** 40%+ respondem "Muito desapontado"

---

### Outros Indicadores de PMF

**Sinais Qualitativos:**

- Usuários indicam voluntariamente outros
- Crescimento orgânico sem marketing
- Alto engajamento e retenção
- Usuários encontram casos de uso criativos
- Feedback positivo não solicitado

**Métricas Quantitativas:**

- **Retenção:** 40%+ retenção mês 1
- **NPS:** Score > 50
- **Crescimento:** 10%+ crescimento orgânico mês a mês
- **Engajamento:** Alto ratio DAU/MAU (>40%)
- **LTV:CAC:** Ratio > 3:1

---

## Métricas de Engajamento

Aprofundamento na medição de engajamento do usuário.

### DAU/WAU/MAU

**Definições:**

- **DAU:** Daily Active Users (usuários únicos em um dia)
- **WAU:** Weekly Active Users (usuários únicos em uma semana)
- **MAU:** Monthly Active Users (usuários únicos em um mês)

**Ratios:**

- **DAU/MAU:** Stickiness (quantos usuários mensais vêm diariamente)
- **DAU/WAU:** Intensidade de engajamento diário

**Benchmarks:**

- **Excelente:** DAU/MAU > 50% (ex: apps de mensagem)
- **Bom:** DAU/MAU = 20-50% (ex: redes sociais)
- **Médio:** DAU/MAU = 10-20% (ex: utilitários)

---

### Métricas de Sessão

**Medições Principais:**

- **Duração da sessão:** Tempo gasto por sessão
- **Frequência de sessão:** Sessões por usuário por dia/semana
- **Profundidade da sessão:** Ações/páginas por sessão

**Metas de Exemplo:**

- Duração da sessão: > 5 minutos
- Frequência de sessão: 2+ sessões/dia
- Profundidade da sessão: > 8 page views

---

### Engajamento de Features

**Métricas:**

- **Taxa de adoção:** % de usuários que experimentam a feature
- **Uso ativo:** % de usuários usando regularmente
- **Profundidade de uso:** Ações por usuário dentro da feature

**Exemplo:**

```
Feature: Colaboração em documentos
- Adoção: 50% dos usuários colaboraram pelo menos uma vez
- Uso ativo: 30% colaboram semanalmente
- Profundidade: Média de 12 edições colaborativas por semana
```

---

## Escolhendo o Framework Certo

### Matriz de Decisão

| Framework      | Melhor Para                               | Horizonte de Tempo | Complexidade |
| -------------- | ----------------------------------------- | ------------------ | ------------ |
| **AARRR**      | Produtos focados em crescimento, startups | Contínuo           | Média        |
| **HEART**      | Qualidade de UX, lançamentos de features  | Por feature        | Baixa-Média  |
| **North Star** | Alinhamento da empresa, foco              | Contínuo           | Baixa        |
| **OKRs**       | Definição de metas, alinhamento de times  | Trimestral         | Média-Alta   |

---

### Por Estágio do Produto

**Estágio Inicial (Pré-PMF):**

- Foco: Métricas de Product-Market Fit
- Framework: AARRR (foco em Activation & Retention)
- North Star: Métrica de engajamento inicial

**Estágio de Crescimento (Pós-PMF):**

- Foco: Escalar aquisição de usuários
- Framework: Funil AARRR completo
- North Star: Métrica orientada a crescimento

**Estágio Maduro:**

- Foco: Otimização e expansão
- Framework: HEART para features, OKRs para metas
- North Star: Métrica de receita ou engajamento

---

### Por Tipo de Produto

**Apps Consumer:**

- AARRR para funil de crescimento
- DAU/MAU para engajamento
- Coeficiente viral para referral

**SaaS B2B:**

- ARR/MRR para receita
- Churn rate para retenção
- Receita de expansão para crescimento

**Marketplace:**

- GMV (Gross Merchandise Value)
- Take rate (% da transação)
- Liquidez (balanço oferta/demanda)

**Plataformas de Conteúdo:**

- Tempo gasto na plataforma
- Taxa de criação de conteúdo
- Taxa de consumo de conteúdo

---

## Anti-Padrões de Métricas

### Erros Comuns

**1. Muitas Métricas**

- **Problema:** Acompanhar tudo = focar em nada
- **Solução:** Escolha 3-5 métricas chave por iniciativa

**2. Vanity Metrics**

- **Problema:** Total de usuários parece bom mas não informa decisões
- **Solução:** Foque em usuários ativos, engajamento, retenção

**3. Apenas Lagging**

- **Problema:** Acompanhar só receita = olhar pelo retrovisor
- **Solução:** Balance com leading indicators (activation, engajamento)

**4. Sem Metas**

- **Problema:** Acompanhar sem objetivos
- **Solução:** Defina metas específicas com prazos

**5. Não Segmentar**

- **Problema:** Métricas médias escondem padrões importantes
- **Solução:** Segmente por tipo de usuário, cohort, uso de features

---

## Template de Métricas para PRDs

```markdown
## Métricas de Sucesso

### North Star Metric

**Métrica:** [Sua métrica mais importante]
**Atual:** [Valor baseline]
**Meta:** [Valor objetivo em lançamento + X meses]
**Por quê:** [Por que esta métrica importa]

### Métricas de Suporte

#### Acquisition

- **Métrica 1:** [Nome] - Atual: [X], Meta: [Y]
- **Métrica 2:** [Nome] - Atual: [X], Meta: [Y]

#### Activation

- **Métrica 1:** [Nome] - Atual: [X], Meta: [Y]
- **Métrica 2:** [Nome] - Atual: [X], Meta: [Y]

#### Retention

- **Métrica 1:** [Nome] - Atual: [X], Meta: [Y]
- **Métrica 2:** [Nome] - Atual: [X], Meta: [Y]

#### Revenue (se aplicável)

- **Métrica 1:** [Nome] - Atual: [X], Meta: [Y]

### Counter-Metrics

[Métricas para garantir que você não está sacrificando outras áreas]

- Exemplo: Garantir que tickets de suporte não aumentem > 10%

### Plano de Medição

- **Dashboard:** [Link]
- **Cadência de Revisão:** [Semanal/quinzenal]
- **Responsável:** [Nome]
```

---

## Recursos & Ferramentas

### Plataformas de Analytics

- **Amplitude:** Product analytics, análise de retenção
- **Mixpanel:** Event tracking, análise de funil
- **Google Analytics:** Web analytics
- **Heap:** Auto-capture analytics

### Ferramentas de Survey

- **Delighted:** Surveys de NPS
- **SurveyMonkey:** Surveys customizados
- **Typeform:** Formulários de survey engajantes

### Ferramentas de Dashboard

- **Tableau:** Visualização de dados
- **Looker:** Business intelligence
- **Datadog:** Métricas de infraestrutura
- **Metabase:** BI open-source

---

## Resumo

**Principais Conclusões:**

1. **Escolha frameworks** que combinam com seu estágio de produto e objetivos
2. **Balance leading e lagging** indicators
3. **Defina metas específicas** com prazos
4. **Acompanhe counter-metrics** para evitar consequências não intencionadas
5. **Revise regularmente** e itere no que você mede
6. **Mantenha simples** - 3-5 métricas chave por iniciativa
7. **Alinhe métricas** com objetivos de negócio
8. **Torne métricas actionable** - o time pode influenciá-las?

**Lembre-se:** A melhor métrica é aquela que impulsiona o comportamento certo e alinha seu time em torno do que mais importa para usuários e negócio.
