---
name: meta-agent-expert
description: Gera agents experts especializados em areas especificas da codebase. Use quando precisar criar um novo agent expert com knowledge base, sub-comandos e integracao com a codebase.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Meta Agent Expert: Gerador de Agents Especialistas

## Proposito

Este skill cria agents experts que tem dominio profundo sobre partes especificas da codebase. Cada agent gerado:

1. **Conhece sua area**: Tem um knowledge base com os arquivos que domina
2. **Tem sub-comandos**: Operacoes especializadas que pode executar
3. **Pode chamar outros agents**: Integra com outros experts quando necessario
4. **Usa /question**: Explora a codebase para responder perguntas da sua area

## Estrutura Gerada

```
.claude/commands/experts/
  <nome-do-agent>/
    <nome-do-agent>.md       # Comando principal do agent
    question.md              # [OBRIGATORIO] Question especializado para esta area
    sync.md                  # [OBRIGATORIO] Auto-atualizacao do knowledge base
    sub-comando-1.md         # Sub-comandos especializados
    sub-comando-2.md
    KNOWLEDGE.md             # Base de conhecimento do agent
```

### Arquivos Obrigatorios

Todo agent expert DEVE ter:

1. **`<nome>.md`**: Comando principal
2. **`question.md`**: Responde perguntas focando apenas nos arquivos do knowledge base
3. **`sync.md`**: Atualiza o knowledge base quando o codigo muda
4. **`KNOWLEDGE.md`**: Lista de arquivos que o agent domina

## Quando Usar

Use este skill quando:
- Precisar criar um novo agent expert para uma area da codebase
- Quiser automatizar operacoes especificas de um dominio
- Precisar de um "especialista" que conheca profundamente certos arquivos
- Quiser delegar tarefas complexas para agents focados

## Workflow de Criacao

### Passo 1: Coleta de Informacoes

Quando o usuario solicitar criar um agent, colete:

1. **Nome do agent**: kebab-case (ex: `kanban-workflow`, `git-operations`)
2. **Area de dominio**: Qual parte da codebase ele domina
3. **Responsabilidades**: O que esse agent deve saber fazer
4. **Sub-comandos desejados**: Operacoes especificas (opcional - pode sugerir)

### Passo 2: Discovery do Knowledge Base

Use o comando `/question` ou Task com subagent_type=Explore para descobrir:

1. **Arquivos principais**: Quais arquivos sao core para essa area
2. **Padroes de codigo**: Como o codigo esta organizado nessa area
3. **Dependencias**: Quais outros modulos essa area usa
4. **Tipos e interfaces**: Types relevantes para o dominio

**Exemplo de discovery:**
```
Prompt para Task/Explore: "Liste todos os arquivos relacionados a [AREA].
Inclua: models, routes, services, components, hooks, types.
Identifique os arquivos mais importantes e suas responsabilidades."
```

### Passo 3: Geracao dos Arquivos

Gere os arquivos na seguinte ordem:

1. **KNOWLEDGE.md**: Base de conhecimento com paths e descricoes
2. **<nome>.md**: Comando principal do agent
3. **question.md**: [OBRIGATORIO] Question especializado para a area do agent
4. **sync.md**: [OBRIGATORIO] Auto-atualizacao do knowledge base
5. **Sub-comandos**: Arquivos .md para cada operacao especializada

### Passo 4: Validacao

Apos gerar, valide:
- [ ] Frontmatter YAML valido em todos os arquivos
- [ ] Knowledge base com paths corretos
- [ ] **question.md criado** com foco nos arquivos do KNOWLEDGE.md
- [ ] **sync.md criado** com paths corretos para detectar mudancas
- [ ] Sub-comandos referenciados no comando principal
- [ ] Instrucoes claras de quando chamar cada sub-comando

## Instrucoes de Geracao

### Question Especializado (question.md) - OBRIGATORIO

Cada agent DEVE ter um question.md que:

1. **Foca apenas nos arquivos do KNOWLEDGE.md**
2. **Nao modifica arquivos** - apenas le e responde
3. **Referencia o codigo real** nas respostas
4. **Diferente do /question global** que consulta toda a codebase

Beneficio: Quando o usuario quer entender algo especifico da area do agent, o `/[agent]/question` da respostas mais precisas e focadas.

### Sync/Auto-Atualizacao (sync.md) - OBRIGATORIO

Cada agent DEVE ter um sync.md que:

1. **Detecta mudancas** nos arquivos do knowledge base
2. **Atualiza KNOWLEDGE.md** quando arquivos sao criados/removidos/renomeados
3. **Atualiza sub-comandos** se paths mudaram
4. **Mantem o agent sincronizado** com a codebase atual

Beneficio: Quando o codigo evolui, o agent nao fica desatualizado. O usuario pode rodar `/[agent]/sync` para atualizar o knowledge base.

### Comando Principal do Agent

O comando principal deve:

1. Ser o ponto de entrada para qualquer pergunta/tarefa da area
2. Ter acesso ao KNOWLEDGE.md para saber quais arquivos consultar
3. Decidir quando delegar para sub-comandos
4. Poder chamar /question para explorar a codebase
5. Poder chamar outros agents quando necessario

### Sub-comandos

Cada sub-comando deve:

1. Ser focado em UMA operacao especifica
2. Poder ser chamado diretamente pelo usuario OU pelo agent principal
3. Ter seu proprio knowledge base subset (opcional)
4. Retornar resultado claro para o agent principal

### Knowledge Base

O KNOWLEDGE.md deve conter:

1. **Arquivos Core**: Lista dos arquivos mais importantes
2. **Estrutura**: Como os arquivos se relacionam
3. **Padroes**: Convencoes de codigo da area
4. **Dependencias**: Outros modulos/agents relacionados

## Exemplo de Uso

**Solicitacao**: "Crie um agent expert para o sistema de Kanban workflow"

**Discovery**:
```
Task(Explore): "Liste todos os arquivos relacionados ao Kanban workflow.
Inclua: componentes de board, cards, colunas, drag-drop, hooks de automacao,
API routes, models, services. Identifique responsabilidades de cada arquivo."
```

**Arquivos Gerados**:
```
.claude/commands/experts/kanban-workflow/
  kanban-workflow.md        # Comando principal
  validate-transition.md    # Valida transicoes entre colunas
  card-lifecycle.md         # Gerencia ciclo de vida dos cards
  automation-triggers.md    # Triggers de automacao por coluna
  KNOWLEDGE.md              # Knowledge base
```

## Templates

Consulte o arquivo TEMPLATES.md para templates prontos de:
- Comando principal de agent
- Sub-comandos especializados
- Knowledge base
- Integracao entre agents

## Integracao com Outros Agents

Quando um agent precisar de funcionalidade de outra area:

```markdown
## Quando Chamar Outros Agents

- `/git-operations`: Quando precisar criar worktree ou fazer merge
- `/ai-execution`: Quando precisar executar comandos do Claude SDK
- `/metrics`: Quando precisar coletar ou consultar metricas
```

## Checklist de Validacao

Antes de finalizar o agent:

- [ ] Nome segue padrao kebab-case
- [ ] KNOWLEDGE.md tem paths validos
- [ ] Comando principal referencia KNOWLEDGE.md
- [ ] **question.md criado** com allowed-tools: Read, Glob, Grep
- [ ] **sync.md criado** com processo de deteccao de mudancas
- [ ] Sub-comandos estao listados no comando principal
- [ ] Instrucoes de "quando chamar" estao claras
- [ ] Integracao com outros agents esta documentada (se aplicavel)
