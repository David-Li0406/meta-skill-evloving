# Análise de Especificação

## Encontrando a Especificação

Antes de analisar, localize o arquivo de especificação:

```
1. Pesquise a especificação:
   Use Glob para encontrar arquivos de spec:
   - "**/*spec*.md"
   - "**/docs/**/*.md"
   - "**/requirements/**/*.md"

2. Ou use Grep para buscar por conteúdo:
   - "requisitos"
   - "funcionalidade"
   - "critérios de aceitação"

3. Trate os resultados:
   - Se encontrado → usar Read para ler
   - Se múltiplos → perguntar ao usuário qual é
   - Se não encontrado → pedir caminho ao usuário
```

## Lendo Especificações

Depois de encontrar a spec, leia com `Read`:

1. Ler o conteúdo completo
2. Identificar seções-chave
3. Extrair informações estruturadas
4. Anotar ambiguidades ou lacunas

```
Read
file_path: "docs/specs/user-profile-api.md"
```

## Estruturas Comuns de Especificação

### Especificação Baseada em Requisitos

```
# Especificação da Funcionalidade
## Visão Geral
[Descrição da funcionalidade]

## Requisitos
### Funcionais
- REQ-1: [Requisito]
- REQ-2: [Requisito]

### Não Funcionais
- PERF-1: [Requisito de performance]
- SEC-1: [Requisito de segurança]

## Critérios de Aceitação
- AC-1: [Critério]
- AC-2: [Critério]
```

Extraia:
- Lista de requisitos funcionais
- Lista de requisitos não funcionais
- Lista de critérios de aceitação

### Especificação Baseada em User Story

```
# Especificação da Funcionalidade
## User Stories
### Como [tipo de usuário]
Quero [objetivo]
Para [benefício]

**Critérios de Aceitação**:
- [Critério]
- [Critério]
```

Extraia:
- Personas de usuário
- Metas/capacidades necessárias
- Critérios de aceitação por story

### Documento de Design Técnico

```
# Design Técnico
## Definição do Problema
[Descrição do problema]

## Solução Proposta
[Abordagem da solução]

## Arquitetura
[Detalhes de arquitetura]

## Plano de Implementação
[Abordagem de implementação]
```

Extraia:
- Problema sendo resolvido
- Abordagem da solução proposta
- Decisões de arquitetura
- Orientação de implementação

### Documento de Requisitos do Produto (PRD)

```
# PRD: [Funcionalidade]
## Objetivos
[Metas de negócio]

## Necessidades do Usuário
[Problemas do usuário que serão resolvidos]

## Funcionalidades
[Lista de funcionalidades]

## Métricas de Sucesso
[Como medir o sucesso]
```

Extraia:
- Metas de negócio
- Necessidades do usuário
- Lista de funcionalidades
- Métricas de sucesso

## Estratégias de Extração

### Identificação de Requisitos

Procure por:
- Frases com "deve", "deveria", "vai"
- Requisitos numerados (REQ-1, etc.)
- User stories (Como... Quero...)
- Seções de critérios de aceitação
- Listas de funcionalidades

### Categorização

Agrupe requisitos por:

**Funcionais**: O que o sistema faz
- Capacidades do usuário
- Comportamentos do sistema
- Operações de dados

**Não Funcionais**: Como o sistema se comporta
- Metas de performance
- Requisitos de segurança
- Necessidades de escalabilidade
- Requisitos de disponibilidade
- Requisitos de compliance

**Restrições**: Limitações
- Restrições técnicas
- Restrições de negócio
- Restrições de cronograma

### Extração de Prioridade

Identifique indicadores de prioridade:
- "Crítico", "Obrigatório", "P0"
- "Importante", "Deveria ter", "P1"
- "Seria bom ter", "Poderia ter", "P2"
- "Futuro", "Não terá", "P3"

Mapeie para fases de implementação com base na prioridade.

## Lidando com Ambiguidade

### Requisitos Pouco Claros

Quando um requisito é ambíguo:

```markdown
## Esclarecimentos Necessários

### [ID/Descrição do Requisito]
**Texto atual**: "[Requisito ambíguo]"
**Pergunta**: [O que precisa de esclarecimento]
**Impacto**: [Por que isso importa para a implementação]
**Assumido por ora**: [Suposição de trabalho, se houver]
```

Use AskUserQuestion para esclarecer.

### Informações Ausentes

Quando falta informação crítica:

```markdown
## Informações Ausentes

- **[Tema]**: A spec não especifica [o que está faltando]
- **Impacto**: Bloqueia [tarefas afetadas]
- **Ação**: Precisa [como resolver]
```

### Requisitos Conflitantes

Quando requisitos conflitam:

```markdown
## Requisitos Conflitantes

**Conflito**: REQ-1 diz [X], mas REQ-5 diz [Y]
**Impacto**: [Impacto na implementação]
**Resolução necessária**: [Decisão necessária]
```

## Análise de Critérios de Aceitação

### Critérios Explícitos

Critérios de aceitação diretos:

```
## Critérios de Aceitação
- Usuário consegue fazer login com email e senha
- Sistema envia email de confirmação
- Sessão expira após 24 horas
```

Converta para checklist:
- [ ] Usuário consegue fazer login com email e senha
- [ ] Sistema envia email de confirmação
- [ ] Sessão expira após 24 horas

### Critérios Implícitos

Derive a partir dos requisitos:

```
Requisito: "Usuários podem enviar arquivos até 100MB"

Critérios de aceitação implícitos:
- [ ] Arquivos até 100MB enviam com sucesso
- [ ] Arquivos acima de 100MB são rejeitados com mensagem de erro
- [ ] Indicador de progresso aparece durante o upload
- [ ] Upload pode ser cancelado
```

### Critérios Testáveis

Garanta que os critérios são testáveis:

❌ **Não testável**: "O sistema é rápido"
✓ **Testável**: "A página carrega em < 2 segundos"

❌ **Não testável**: "Usuários gostam da interface"
✓ **Testável**: "90% dos usuários de teste completam a tarefa com sucesso"

## Extração de Detalhes Técnicos

### Informações de Arquitetura

Extraia:
- Componentes do sistema
- Modelos de dados
- APIs/interfaces
- Pontos de integração
- Escolhas de tecnologia

### Decisões de Design

Registre:
- Seleções de tecnologia
- Padrões de arquitetura
- Trade-offs realizados
- Racional informado

### Orientação de Implementação

Procure por:
- Abordagem sugerida
- Exemplos de código
- Recomendações de bibliotecas
- Boas práticas mencionadas

## Identificação de Dependências

### Dependências Externas

A partir da spec, identifique:
- Serviços de terceiros necessários
- APIs externas necessárias
- Requisitos de infraestrutura
- Dependências de ferramentas/bibliotecas

### Dependências Internas

Identifique:
- Outras funcionalidades necessárias primeiro
- Componentes compartilhados necessários
- Dependências entre equipes
- Dependências de dados

## Extração de Escopo

### Dentro do Escopo

O que está explicitamente incluído:
- Funcionalidades a construir
- Casos de uso a suportar
- Usuários/personas a atender

### Fora do Escopo

O que está explicitamente excluído:
- Funcionalidades adiadas
- Casos de uso não suportados
- Edge cases não tratados

### Suposições

O que está assumido:
- Suposições de ambiente
- Suposições sobre usuários
- Suposições do estado do sistema

## Identificação de Riscos

Extraia informações de risco:

### Riscos Técnicos
- Tecnologia não comprovada
- Integração complexa
- Preocupações de performance
- Incógnitas de escalabilidade

### Riscos de Negócio
- Momento de mercado
- Disponibilidade de recursos
- Dependência de terceiros

### Estratégias de Mitigação

Anote quaisquer abordagens de mitigação mencionadas na spec.

## Avaliação de Qualidade da Spec

Avalie a completude da spec:

✓ **Boa spec**:
- Requisitos claros
- Critérios de aceitação explícitos
- Prioridades definidas
- Riscos identificados
- Abordagem técnica delineada

⚠️ **Spec incompleta**:
- Requisitos vagos
- Critérios de aceitação ausentes
- Prioridades pouco claras
- Sem análise de riscos
- Detalhes técnicos ausentes

Documente lacunas e use AskUserQuestion para esclarecer.

## Checklist de Análise

Antes de criar o plano de implementação:

☐ Todos os requisitos funcionais identificados
☐ Requisitos não funcionais anotados
☐ Critérios de aceitação extraídos
☐ Dependências identificadas
☐ Riscos anotados
☐ Ambiguidades documentadas
☐ Abordagem técnica compreendida
☐ Escopo está claro
☐ Prioridades estão definidas
