# Templates para Agents Experts

Templates prontos para copiar e adaptar ao criar novos agents experts.

---

## Template: KNOWLEDGE.md (Knowledge Base)

```markdown
# Knowledge Base: [Nome do Agent]

## Arquivos Core

Arquivos principais que este agent domina:

### Models/Tipos
| Arquivo | Responsabilidade |
|---------|------------------|
| `backend/src/models/exemplo.py` | Model SQLAlchemy para X |
| `frontend/src/types/exemplo.ts` | Tipos TypeScript para X |

### Services/Logica de Negocio
| Arquivo | Responsabilidade |
|---------|------------------|
| `backend/src/services/exemplo.py` | Servico que faz Y |
| `backend/src/agent.py:100-200` | Funcao Z relevante |

### Routes/API
| Arquivo | Responsabilidade |
|---------|------------------|
| `backend/src/routes/exemplo.py` | Endpoints de X |

### Components/UI
| Arquivo | Responsabilidade |
|---------|------------------|
| `frontend/src/components/Exemplo.tsx` | Componente visual de X |

### Hooks
| Arquivo | Responsabilidade |
|---------|------------------|
| `frontend/src/hooks/useExemplo.ts` | Hook para gerenciar X |

## Estrutura e Relacionamentos

```
[Diagrama ASCII ou descricao de como os arquivos se relacionam]

Model -> Repository -> Service -> Route
                                    |
                                    v
                     Hook -> Component -> Page
```

## Padroes de Codigo

### Convencoes desta area:
- [Padrao 1]: Descricao
- [Padrao 2]: Descricao

### Tipos importantes:
- `TipoX`: Usado para Y
- `InterfaceZ`: Define estrutura de W

## Dependencias

### Dependencias Internas (outros agents):
- `git-operations`: Para criar worktrees
- `ai-execution`: Para executar comandos

### Dependencias Externas:
- SQLAlchemy para ORM
- React para UI
- dnd-kit para drag-and-drop

## Comandos Uteis

Para explorar esta area:
- `/question Como funciona X nesta codebase?`
- `Grep: pattern="ClasseX" path="backend/src/"`
```

---

## Template: Comando Principal do Agent

```yaml
---
description: Agent expert em [AREA]. Responde perguntas, executa tarefas e gerencia [DOMINIO].
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Agent Expert: [Nome]

## Proposito

Sou o agent especialista em [AREA] desta codebase. Tenho conhecimento profundo sobre:

- [Responsabilidade 1]
- [Responsabilidade 2]
- [Responsabilidade 3]

## Knowledge Base

Consulte `KNOWLEDGE.md` nesta pasta para a lista completa de arquivos que domino.

### Arquivos Principais:
- `path/to/main/file.py` - Descricao
- `path/to/component.tsx` - Descricao
- `path/to/service.py` - Descricao

## Sub-comandos Disponiveis

Posso delegar para sub-comandos especializados:

| Sub-comando | Quando Usar |
|-------------|-------------|
| `/[agent]/sub-comando-1` | Quando precisar fazer X |
| `/[agent]/sub-comando-2` | Quando precisar fazer Y |
| `/[agent]/sub-comando-3` | Quando precisar fazer Z |

## Instrucoes

### Para Perguntas sobre [AREA]:

1. Consulte o KNOWLEDGE.md para identificar arquivos relevantes
2. Use `/question` se precisar explorar mais a codebase
3. Leia os arquivos identificados
4. Responda com base no codigo real

### Para Tarefas de [AREA]:

1. Entenda o que o usuario precisa
2. Verifique se um sub-comando pode resolver
3. Se sim, delegue para o sub-comando apropriado
4. Se nao, execute diretamente usando o knowledge base

### Quando Chamar Outros Agents:

- `/[outro-agent]`: Quando [situacao]
- `/[outro-agent]`: Quando [situacao]

## Fluxo de Decisao

```
Usuario faz pergunta/tarefa
         |
         v
   E sobre [AREA]?
    /          \
  Sim          Nao
   |             |
   v             v
Consultar    Indicar agent
KNOWLEDGE    apropriado
   |
   v
Sub-comando resolve?
   /          \
 Sim          Nao
  |            |
  v            v
Delegar    Executar
           diretamente
```

## Exemplos de Uso

### Exemplo 1: Pergunta
**Usuario**: "Como funciona X?"
**Acao**: Consulto KNOWLEDGE.md, leio arquivos relevantes, explico

### Exemplo 2: Tarefa
**Usuario**: "Faca Y no sistema"
**Acao**: Verifico se sub-comando resolve, delego ou executo

### Exemplo 3: Integracao
**Usuario**: "Preciso fazer Z que envolve outra area"
**Acao**: Chamo agent apropriado para parte que nao domino

## Argumentos

$ARGUMENTS - A pergunta ou tarefa do usuario sobre [AREA]
```

---

## Template: Sub-comando Especializado

```yaml
---
description: [Operacao especifica] do agent [NOME]. Use para [QUANDO USAR].
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Sub-comando: [Nome da Operacao]

## Proposito

Este sub-comando e especializado em [OPERACAO ESPECIFICA].

## Quando Sou Chamado

- Pelo agent principal quando [SITUACAO 1]
- Diretamente pelo usuario quando [SITUACAO 2]

## Arquivos que Manipulo

Subset do knowledge base do agent principal:

- `path/to/file1.py` - Para fazer X
- `path/to/file2.tsx` - Para fazer Y

## Instrucoes

### Passo 1: [Acao]
[Descricao detalhada]

### Passo 2: [Acao]
[Descricao detalhada]

### Passo 3: [Acao]
[Descricao detalhada]

## Validacoes

Antes de executar, verifico:
- [ ] [Validacao 1]
- [ ] [Validacao 2]

Apos executar, confirmo:
- [ ] [Confirmacao 1]
- [ ] [Confirmacao 2]

## Retorno

Quando chamado pelo agent principal, retorno:
- Status: sucesso/falha
- Resultado: [descricao do output]
- Proximos passos: [se houver]

## Argumentos

$ARGUMENTS - [Descricao do que espera receber]
```

---

## Template: Question Especializado

Este comando permite consultar a codebase focando apenas nos arquivos do knowledge base do agent:

```yaml
---
description: Responde perguntas sobre [AREA] consultando o knowledge base do agent
allowed-tools: Read, Glob, Grep
---

# Question: [Nome do Agent]

## Proposito

Responder perguntas sobre [AREA] de forma focada, consultando apenas os arquivos relevantes do knowledge base deste agent.

## Diferenca do /question Global

- **/question global**: Consulta toda a codebase
- **/[agent]/question**: Consulta apenas arquivos do KNOWLEDGE.md deste agent

## Knowledge Base

Arquivos que este agent domina (ver KNOWLEDGE.md):

### Core
- `path/to/file1.py`
- `path/to/file2.ts`

### Related
- `path/to/related1.py`
- `path/to/related2.ts`

## Instrucoes

1. **Leia o KNOWLEDGE.md** para entender o escopo
2. **Identifique arquivos relevantes** para a pergunta
3. **Consulte apenas esses arquivos** usando Read, Glob, Grep
4. **Responda com base no codigo real** encontrado
5. **Referencie os arquivos** que fundamentam a resposta

## Restricoes

- **NAO MODIFICAR** nenhum arquivo
- **NAO CRIAR** novos arquivos
- **APENAS LER** e responder
- **FOCAR** nos arquivos do knowledge base

## Formato de Resposta

1. Resposta direta a pergunta
2. Referencias aos arquivos consultados (path:line)
3. Trechos de codigo relevantes (se aplicavel)
4. Conexoes com outros arquivos da area

## Pergunta

$ARGUMENTS
```

---

## Template: Sync/Auto-Atualizacao

Este comando sincroniza o knowledge base quando o codigo muda:

```yaml
---
description: Sincroniza o knowledge base do agent [NOME] quando houver mudancas no codigo
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Sync: [Nome do Agent]

## Proposito

Manter o knowledge base e os comandos do agent atualizados quando houver mudancas no codigo que afetam esta area.

## Quando Executar

Este comando deve ser executado quando:
- Novos arquivos foram criados na area do agent
- Arquivos existentes foram renomeados ou movidos
- Campos/funcoes importantes foram adicionados ou removidos
- Estrutura do codigo mudou significativamente

## Processo de Sync

### Passo 1: Detectar Mudancas

Use git para identificar arquivos modificados na area:

```bash
git diff --name-only HEAD~10 -- <paths-do-knowledge-base>
```

Ou use Glob/Grep para varrer os paths do knowledge base:

```
Glob: pattern que cobre os arquivos do KNOWLEDGE.md
```

### Passo 2: Analisar Impacto

Para cada arquivo modificado:
1. Verifique se ainda existe
2. Verifique se a responsabilidade mudou
3. Identifique novos arquivos que deveriam ser incluidos
4. Identifique arquivos obsoletos que deveriam ser removidos

### Passo 3: Atualizar KNOWLEDGE.md

Atualize as tabelas de arquivos:
- Adicionar novos arquivos relevantes
- Remover arquivos que nao existem mais
- Atualizar descricoes de responsabilidade
- Atualizar secao de padroes se necessario

### Passo 4: Atualizar Comandos

Verifique se os sub-comandos ainda fazem sentido:
- Paths nos comandos ainda existem?
- Novos sub-comandos sao necessarios?
- Algum sub-comando ficou obsoleto?

### Passo 5: Validar

Apos atualizar:
- [ ] KNOWLEDGE.md tem paths validos
- [ ] Todos os arquivos listados existem
- [ ] Descricoes estao atualizadas
- [ ] Sub-comandos referenciam arquivos corretos

## Output

Ao finalizar, reporte:
- Arquivos adicionados ao knowledge base
- Arquivos removidos do knowledge base
- Mudancas em descricoes
- Sub-comandos afetados

## Argumentos

$ARGUMENTS - Opcional: especificar o que verificar (ex: "models", "routes")
```

---

## Template: Integracao Entre Agents

Adicione esta secao ao comando principal quando ele precisar chamar outros agents:

```markdown
## Integracao com Outros Agents

### Agents que Posso Chamar

| Agent | Quando Chamar | Exemplo |
|-------|---------------|---------|
| `/git-operations` | Preciso criar branch ou worktree | "Criar worktree para card X" |
| `/ai-execution` | Preciso executar comando do SDK | "Rodar /plan no worktree" |
| `/metrics` | Preciso consultar metricas | "Quanto custou a ultima execucao?" |

### Como Chamar

Para chamar outro agent, use:

1. Identifique qual agent tem dominio sobre a tarefa
2. Formule a solicitacao de forma clara
3. Aguarde o resultado
4. Continue com base no retorno

### Agents que Podem Me Chamar

Este agent pode ser chamado por:
- `/[agent-x]`: Quando [situacao]
- `/[agent-y]`: Quando [situacao]
```

---

## Template: Discovery Prompt

Use este prompt com Task(Explore) ou /question para descobrir o knowledge base:

```markdown
Explore a codebase para identificar todos os arquivos relacionados a [AREA].

Busque por:
1. **Models/Schemas**: Definicoes de dados (SQLAlchemy, Pydantic, TypeScript types)
2. **Services**: Logica de negocio e processamento
3. **Routes/API**: Endpoints e handlers
4. **Components**: Componentes React/UI relacionados
5. **Hooks**: Custom hooks que gerenciam estado/logica
6. **Utils**: Funcoes utilitarias da area
7. **Tests**: Arquivos de teste relacionados

Para cada arquivo encontrado, informe:
- Path completo
- Responsabilidade principal
- Funcoes/classes mais importantes
- Relacao com outros arquivos da area

Organize por categoria e indique quais sao os arquivos "core" vs "auxiliares".
```

---

## Exemplo Completo: Agent de Kanban Workflow

### question.md (Sub-comando de Question)
```yaml
---
description: Responde perguntas sobre Kanban workflow consultando o knowledge base
allowed-tools: Read, Glob, Grep
---

# Question: Kanban Workflow

## Proposito

Responder perguntas sobre o Kanban workflow focando nos arquivos do knowledge base.

## Knowledge Base

Ver KNOWLEDGE.md. Arquivos principais:
- `backend/src/models/card.py`
- `backend/src/services/workflow_service.py`
- `frontend/src/components/Kanban*.tsx`
- `frontend/src/hooks/useWorkflow*.ts`

## Instrucoes

1. Leia KNOWLEDGE.md para contexto
2. Identifique arquivos relevantes para a pergunta
3. Consulte usando Read, Glob, Grep
4. Responda com referencias ao codigo

## Restricoes

- NAO MODIFICAR arquivos
- APENAS LER e responder
- FOCAR nos arquivos do knowledge base

$ARGUMENTS
```

### sync.md (Sub-comando de Sync)
```yaml
---
description: Sincroniza o knowledge base do Kanban workflow
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Sync: Kanban Workflow

## Processo

1. Verificar mudancas em `backend/src/models/card.py`
2. Verificar mudancas em `backend/src/services/workflow*`
3. Verificar mudancas em `frontend/src/components/Kanban*`
4. Verificar mudancas em `frontend/src/hooks/useWorkflow*`
5. Atualizar KNOWLEDGE.md se necessario
6. Atualizar comandos afetados

$ARGUMENTS
```

### KNOWLEDGE.md
```markdown
# Knowledge Base: Kanban Workflow

## Arquivos Core

### Models
| Arquivo | Responsabilidade |
|---------|------------------|
| `backend/src/models/card.py` | Model Card com estados e transicoes |
| `frontend/src/types/card.ts` | Tipos TypeScript para Card |

### Services
| Arquivo | Responsabilidade |
|---------|------------------|
| `backend/src/services/workflow_service.py` | Logica de transicao |
| `backend/src/agent.py:200-400` | Automacao de workflow |

### Components
| Arquivo | Responsabilidade |
|---------|------------------|
| `frontend/src/components/KanbanBoard.tsx` | Board principal |
| `frontend/src/components/KanbanColumn.tsx` | Colunas do board |
| `frontend/src/components/KanbanCard.tsx` | Cards arrastáveis |

### Hooks
| Arquivo | Responsabilidade |
|---------|------------------|
| `frontend/src/hooks/useWorkflowAutomation.ts` | Automacao de transicoes |
| `frontend/src/hooks/useDragAndDrop.ts` | Logica de drag-drop |

## Padroes

### State Machine de Colunas:
backlog -> plan -> implement -> test -> review -> done -> completed

### Regras de Transicao:
- Nao pode pular colunas
- Cada coluna pode ter trigger automatico
- Transicao dispara eventos
```

### kanban-workflow.md (comando principal)
```yaml
---
description: Agent expert em Kanban workflow. Gerencia transicoes, cards, colunas e automacao do board.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Agent Expert: Kanban Workflow

## Proposito

Sou o especialista em tudo relacionado ao Kanban board:
- Transicoes entre colunas
- Lifecycle dos cards
- Automacao de triggers
- Drag-and-drop
- Validacoes de workflow

## Knowledge Base

Ver KNOWLEDGE.md para lista completa.

## Sub-comandos

| Sub-comando | Uso |
|-------------|-----|
| `/kanban-workflow/validate-transition` | Validar se transicao e permitida |
| `/kanban-workflow/card-lifecycle` | Gerenciar ciclo de vida do card |
| `/kanban-workflow/automation-triggers` | Configurar triggers automaticos |

## Quando Chamar Outros Agents

- `/git-operations`: Quando transicao precisa criar worktree
- `/ai-execution`: Quando coluna dispara execucao de comando

## Argumentos

$ARGUMENTS
```
