---
name: notion-integration
description: Integração completa com Notion usando MCP customizado (notion-automation-suite)
triggers: [notion, card, task, project, course, episode, series, work, studies, personal, youtuber]
source: my-local-place/services/external/notion-automation-suite
---

# Notion Integration

**Integração completa com Notion usando MCP customizado `notion-automation-suite`.**

**Última Atualização:** 2026-01-21  
**MCP Server:** `notion-automation-suite`  
**Localização:** `my-local-place/services/external/notion-automation-suite`

---

## Quando Usar

Aplicar esta skill quando:
- Criar, atualizar ou consultar cards no Notion
- Trabalhar com projetos de trabalho, estudos, pessoal ou YouTube
- Usar o MCP customizado `notion-automation-suite`
- Precisar seguir regras específicas de organização do Notion

## ⚠️ REGRA CRÍTICA: Execução Completa

**QUANDO O USUÁRIO PEDIR PARA CRIAR/ATUALIZAR CARDS NO NOTION, EXECUTAR ATÉ O FINAL.**

### O que significa "até o final":
- ✅ Criar TODOS os cards solicitados (não apenas gerar instruções)
- ✅ Criar hierarquia completa (curso → fases → aulas, projeto → tarefas, etc.)
- ✅ Usar o MCP diretamente para criar os cards
- ✅ NÃO apenas gerar scripts ou instruções
- ✅ NÃO parar no meio - completar toda a estrutura solicitada

### Exemplos:

**❌ ERRADO:**
- Gerar apenas instruções de como criar
- Criar apenas o curso base e parar
- Deixar para o usuário executar

**✅ CORRETO:**
- Criar curso base → criar todas as fases → criar todas as aulas
- Criar projeto → criar todas as tarefas vinculadas
- Executar todos os comandos MCP necessários até completar

---

## MCP Customizado: notion-automation-suite

### Configuração

**Localização:** `my-local-place/services/external/notion-automation-suite`

**Configuração:**
- **Documentação:** `my-local-place/services/external/notion-automation-suite/config/README.md`
- **Template:** `my-local-place/services/external/notion-automation-suite/config/defaults/env.example`
- **Arquivo real:** `my-local-place/services/external/notion-automation-suite/config/.env` ou `config/notion-mcp.env` (gitignored)

**Variáveis de Ambiente Obrigatórias:**
- `NOTION_API_TOKEN` - Token da API do Notion
- `NOTION_WORK_DATABASE_ID` - ID da base de trabalho
- `NOTION_STUDIES_DATABASE_ID` - ID da base de estudos
- `NOTION_PERSONAL_DATABASE_ID` - ID da base pessoal
- `NOTION_YOUTUBER_DATABASE_ID` - ID da base YouTube

**⚠️ IMPORTANTE:** Os IDs das databases ficam no projeto do MCP via variáveis de ambiente. O cursor-multiagent-system não deve ter acesso direto a esses IDs, apenas usar o MCP construído.

**Execução:**
```bash
# Via stdio
notion-mcp-server

# Via Docker
docker run -i --rm \
  -e NOTION_API_TOKEN=secret_xxx \
  -e NOTION_WORK_DATABASE_ID=... \
  -e NOTION_STUDIES_DATABASE_ID=... \
  -e NOTION_PERSONAL_DATABASE_ID=... \
  -e NOTION_YOUTUBER_DATABASE_ID=... \
  notion-mcp-server
```

### Tools Disponíveis

O MCP expõe tools especializadas por domínio:

#### Work (Trabalho)
- `work_create_project` - Criar projeto de trabalho
- `work_create_sprint` - Criar sprint com subtarefas
- `work_create_task` - Criar tarefa/subitem vinculado
- `work_update_status` - Atualizar status
- `work_assign_project` - Alterar projeto vinculado
- `work_query_projects` - Consultar cards por filtros

#### Studies (Estudos)
- `study_create_course` - Criar curso (apenas data, sem horário)
- `study_create_course_complete` - Criar curso completo com fases/seções/aulas
- `study_create_phase` - Criar fase vinculada a curso
- `study_create_section` - Criar seção vinculada
- `study_create_class` - Criar aula (com horário, respeita regras 19h-21h)
- `study_reschedule_section` - Reagendar aulas de uma seção
- `study_query_schedule` - Consultar aulas por período/status

#### Personal (Pessoal)
- `personal_create_task` - Criar tarefa pessoal
- `personal_create_subtask` - Criar subtarefa vinculada
- `personal_use_template` - Usar template genérico (ex: weekly_planning)
- `personal_create_medical_appointment` - Criar consulta médica

#### Youtuber (YouTube)
- `youtuber_create_series` - Criar série completa com episódios automáticos
- `youtuber_create_episode` - Criar episódio vinculado a série
- `youtuber_schedule_recordings` - Gerar episódios sequenciais
- `youtuber_update_episode_status` - Atualizar status do episódio
- `youtuber_reschedule_episode` - Reagendar gravação/publicação
- `youtuber_query_schedule` - Consultar episódios por filtros

---

## Estrutura das 4 Bases

### 1. BASE TRABALHO (WORK)

**Campo de Título:** `Nome do projeto`  
**Campo de Relação:** `item principal`  
**Uso:** Projetos profissionais (ExpenseIQ, HubTravel, etc.)

#### Propriedades Principais
- `Nome do projeto` (title) - Título do card
- `Status` (status) - Estado atual
- `Cliente` (select) - Astracode, Pessoal, FIAP
- `Projeto` (select) - ExpenseIQ, HubTravel, Avulso
- `Prioridade` (select) - Baixa, Normal, Média, Alta, Urgente
- `Periodo` (date) - Data/hora de execução
- `item principal` (relation) - Vínculo com card pai

#### Status Disponíveis
- `Não iniciado` (padrão)
- `Em Andamento`
- `Em Revisão`
- `Concluído`
- `Pausado`
- `Cancelado`

#### Valores Padrão
- `cliente`: `"Astracode"` (padrão para trabalho profissional)
- `projeto`: `"Avulso"` (quando não especificado)
- `prioridade`: `"Normal"`
- `status`: `"Não iniciado"`

#### Exemplo de Uso (MCP)
```python
# Via MCP tool
work_create_project(
    title="Implementar Feature X",
    cliente="Astracode",
    projeto="ExpenseIQ",
    prioridade="Alta",
    icon="🚀"
)
```

---

### 2. BASE PESSOAL (PERSONAL)

**Campo de Título:** `Nome da tarefa`  
**Campo de Relação:** `tarefa principal`  
**Campo de Data:** `Data` (não `Periodo`)  
**Uso:** Tarefas pessoais, organização, hábitos

#### Propriedades Principais
- `Nome da tarefa` (title) - Título da tarefa
- `Status` (status) - Estado atual
- `Atividade` (select) - Tipo de atividade
- `Data` (date) - Data da tarefa (campo específico)
- `Descrição` (rich_text) - Descrição detalhada
- `tarefa principal` (relation) - Tarefa principal (pai)

#### Status Disponíveis
- `Não iniciado` (padrão)
- `Em Andamento`
- `Concluído`
- `Cancelado`

#### Atividades Comuns
- `Desenvolvimento`
- `Organização`
- `Estudo`
- `Teste`
- `Planejamento`
- `Financeiro`
- `Saúde`
- `Lazer`

#### Exemplo de Uso (MCP)
```python
# Via MCP tool
personal_create_task(
    title="Organizar Documentos",
    atividade="Organização",
    data={
        "start": "2025-10-15T19:00:00-03:00",
        "end": "2025-10-15T20:00:00-03:00"
    },
    icon="👤"
)
```

---

### 3. BASE CURSOS (STUDIES)

**Campo de Título:** `Project name`  
**Campo de Relação:** `Parent item`  
**Campo de Data:** `Período` (com acento)  
**Uso:** Cursos, formações, aulas, estudos

#### Propriedades Principais
- `Project name` (title) - Nome do curso/aula
- `Status` (status) - Estado atual
- `Categorias` (multi_select) - Tags do curso
- `Prioridade` (select) - Nível de prioridade
- `Período` (date) - Quando estudar
- `Tempo Total` (rich_text) - Duração estimada (HH:MM:SS)
- `Parent item` (relation) - Item pai (curso/seção)

#### Status Disponíveis
- `Não Adquirido`
- `Para Fazer` (padrão)
- `Em Revisão`
- `Em Pausa`
- `Em Andamento`
- `Descontinuado`
- `Concluido` (sem acento)

#### Estrutura Hierárquica
```
Formação/Curso (sem horário)
├── Fase/Bloco (sem horário)
│   ├── Seção/Módulo (sem horário)
│   │   ├── Aula 1 (COM horário 19:00-21:00)
│   │   ├── Aula 2 (COM horário 19:00-21:00)
│   │   └── Aula 3 (COM horário 19:00-21:00)
```

#### Regra de Horários
- **Aulas (nível mais baixo):** COM horário específico (19:00-21:00)
- **Seções/Módulos:** SEM horário (apenas data)
- **Cursos/Formações:** SEM horário (apenas data)

#### Horários de Estudo
- **Segunda, Quarta, Quinta, Sexta:** 19:00-21:00
- **Terça:** 19:30-21:00 (após tratamento médico)
- **LIMITE MÁXIMO:** 21:00 (NUNCA ultrapassar)
- **Se passar das 21:00:** Mover aula para próximo dia útil às 19:00

#### Exemplo de Uso (MCP)
```python
# Curso (sem horário)
study_create_course(
    title="FIAP IA para Devs",
    categorias=["FIAP", "Inteligência Artificial"],
    periodo={"start": "2025-10-16", "end": "2025-12-15"},
    tempo_total="40:00:00",
    icon="🎓"
)

# Aula (com horário)
study_create_class(
    parent_id=section_id,
    title="Aula 1: Introdução",
    start_time="2025-10-16T19:00:00-03:00",
    duration_minutes=120,  # 2 horas (19:00-21:00)
    icon="🎯"
)
```

---

### 4. BASE YOUTUBE (YOUTUBER)

**Campo de Título:** `Nome do projeto`  
**Campo de Relação:** `item principal`  
**Uso:** Séries de jogos e episódios do canal

#### Propriedades Principais
- `Nome do projeto` (title) - Nome da série/episódio
- `Status` (status) - Estado atual
- `Periodo` (date) - Data/hora de GRAVAÇÃO
- `Data de Lançamento` (date) - Data/hora de PUBLICAÇÃO
- `Resumo do Episodio` (rich_text) - Sinopse do episódio/série
- `Link do Video` (url) - URL do vídeo publicado
- `item principal` (relation) - Série (para episódios)

#### Status Disponíveis
- `Para Gravar`
- `Não iniciado` (padrão)
- `Gravando`
- `Para Edição`
- `Editando`
- `Editado`
- `Publicado`
- `Concluído`

#### Diferença Entre Campos de Data

**`Periodo` (Data de Gravação):**
- Quando o episódio será GRAVADO
- Data e hora reais de trabalho
- Exemplo: `2025-10-16T21:00:00-03:00` até `2025-10-16T23:30:00-03:00`

**`Data de Lançamento` (Publicação):**
- Quando o episódio será PUBLICADO
- Data e hora que ficará público no YouTube
- Exemplo: `2025-10-17T12:00:00-03:00`

#### Estrutura Hierárquica
```
Série Principal (sem Data de Lançamento)
  └─ Periodo: início da gravação do 1º ep → fim da gravação do último ep
├── Episódio 01 (com Periodo E Data de Lançamento)
├── Episódio 02 (com Periodo E Data de Lançamento)
└── Episódio 03 (com Periodo E Data de Lançamento)
```

#### Regras Especiais
- **Série:** Tem `Periodo` (gravação), NÃO tem `Data de Lançamento`
- **Episódios:** Tem AMBOS (`Periodo` e `Data de Lançamento`)
- **Primeiro episódio:** Deve ter sinopse da série em `Resumo do Episodio`

#### Exemplo de Uso (MCP)
```python
# Série
youtuber_create_series(
    title="The Legend of Heroes",
    sinopse="Série completa sobre...",
    total_episodes=10,
    first_recording="2025-10-16T21:00:00-03:00",
    recording_interval_days=1,
    publication_hour=12,
    icon="🎮"
)

# Episódio
youtuber_create_episode(
    parent_id=series_id,
    episode_number=1,
    title="Episódio 01",
    recording_date="2025-10-16T21:00:00-03:00",
    publication_date="2025-10-17T12:00:00-03:00",
    resumo_episodio="Sinopse da série completa...",  # Obrigatório no ep 1
    icon="📺"
)
```

---

## Regras Críticas

### 1. Timezone - OBRIGATÓRIO GMT-3

**SEMPRE usar GMT-3 (São Paulo)**  
**NUNCA usar UTC**

#### Formatos Corretos

**Com Horário:**
```python
'start': '2025-10-16T19:00:00-03:00'
'end': '2025-10-16T21:00:00-03:00'
```

**Sem Horário (apenas data):**
```python
'start': '2025-10-16'
'end': '2025-10-30'
```

#### Código Python
```python
from datetime import datetime, timezone, timedelta

SAO_PAULO_TZ = timezone(timedelta(hours=-3))
dt = datetime(2025, 10, 16, 19, 0, 0, tzinfo=SAO_PAULO_TZ)
data_notion = dt.isoformat()  # '2025-10-16T19:00:00-03:00'
```

---

### 2. Ícones e Emojis

**Emojis SEMPRE como ícone da página**  
**NUNCA no título do card**

#### Formato Correto
```python
# ✅ CORRETO
{
    "icon": {"emoji": "🎓"},  # Ícone aqui
    "properties": {
        "Project name": {
            "title": [{"text": {"content": "Meu Curso"}}]  # Sem emoji
        }
    }
}

# ❌ ERRADO
"title": [{"text": {"content": "🎓 Meu Curso"}}]
```

#### Emojis Recomendados por Base

**WORK:**
- Projetos: `🚀`, `💼`, `🏢`
- Sub-itens: `📋`, `✅`, `🔧`

**PERSONAL:**
- Tarefas: `👤`, `📝`, `🎯`
- Subtarefas: `✅`, `📌`, `⚡`

**STUDIES:**
- Cursos: `🎓`, `📚`, `🎯`
- Fases: `📖`, `📑`
- Seções: `📑`, `📂`
- Aulas: `🎯`, `📝`, `💡`

**YOUTUBER:**
- Séries: `🎬`, `🎮`, `📺`
- Episódios: `📺`, `🎥`, `▶️`

---

### 3. Hierarquias e Vínculos

**Sub-itens DEVEM ter campo de relação preenchido**

#### Campos de Relação por Base

| Base | Para Criar Sub-item | Campo a Usar | Valor |
|------|---------------------|--------------|-------|
| WORK | Sub-item de projeto | `item_principal` | ID do projeto pai |
| PERSONAL | Subtarefa | `tarefa_principal` | ID da tarefa pai |
| STUDIES | Aula de curso | `parent_item` | ID do curso/seção |
| YOUTUBER | Episódio de série | `item_principal` | ID da série |

#### Exemplo de Hierarquia (WORK)
```python
# 1. Criar projeto principal
project_id = work_create_project(
    title="Projeto Principal",
    cliente="Astracode",
    projeto="ExpenseIQ"
)

# 2. Criar sub-item LINKADO
task_id = work_create_task(
    parent_id=project_id,  # ← VÍNCULO
    title="Sub-item 1"
)
```

---

### 4. Campos de Data por Base

| Base | Campo de Data | Formato |
|------|---------------|---------|
| WORK | `Periodo` | Com horário (ex: `2025-10-16T09:00:00-03:00`) |
| PERSONAL | `Data` | Com horário (ex: `2025-10-16T19:00:00-03:00`) |
| STUDIES | `Período` (com acento) | Sem horário para cursos/seções, com horário para aulas |
| YOUTUBER | `Periodo` + `Data de Lançamento` | Ambos com horário |

---

### 5. Validações Obrigatórias

**Antes de criar qualquer card:**

1. ✅ Verificar título (sem emojis)
2. ✅ Verificar status válido para a base
3. ✅ Verificar timezone GMT-3 em todas as datas
4. ✅ Verificar campo de relação correto (se sub-item)
5. ✅ Verificar horários apenas onde necessário (aulas, episódios)
6. ✅ Verificar duplicatas (título + data + cliente/projeto)

---

## Mapeamento de Campos

### Como Passar Dados para MCP Tools

| Base | Você Passa | Vira no Notion |
|------|------------|----------------|
| **WORK** | `title` | `Nome do projeto` |
| | `cliente` | `Cliente` |
| | `projeto` | `Projeto` |
| | `prioridade` | `Prioridade` |
| | `periodo` | `Periodo` |
| | `item_principal` | `item principal` |
| **PERSONAL** | `title` | `Nome da tarefa` |
| | `atividade` | `Atividade` |
| | `data` | `Data` |
| | `tarefa_principal` | `tarefa principal` |
| **STUDIES** | `title` | `Project name` |
| | `categorias` | `Categorias` |
| | `prioridade` | `Prioridade` |
| | `tempo_total` | `Tempo Total` |
| | `periodo` | `Período` |
| | `parent_item` | `Parent item` |
| **YOUTUBER** | `title` | `Nome do projeto` |
| | `periodo` | `Periodo` |
| | `data_lancamento` | `Data de Lançamento` |
| | `resumo_episodio` | `Resumo do Episodio` |
| | `item_principal` | `item principal` |

---

## Exemplos Práticos

### Criar Projeto de Trabalho com Subtarefas

```python
# Via MCP tool
project = work_create_project(
    title="Implementar Feature X",
    cliente="Astracode",
    projeto="ExpenseIQ",
    prioridade="Alta",
    icon="🚀"
)

# Criar subtarefas
for task_title in ["Mapear requisitos", "Implementar", "Testar"]:
    work_create_task(
        parent_id=project["id"],
        title=task_title,
        icon="📋"
    )
```

### Criar Curso Completo com Aulas

```python
# Curso (sem horário)
course = study_create_course(
    title="FIAP IA para Devs - Fase 5",
    categorias=["FIAP", "Inteligência Artificial"],
    periodo={"start": "2025-01-15", "end": "2025-03-31"},
    tempo_total="80:00:00",
    icon="🎓"
)

# Seção (sem horário)
section = study_create_section(
    parent_id=course["id"],
    title="Seção 1: Fundamentos",
    periodo={"start": "2025-01-15", "end": "2025-01-31"},
    tempo_total="16:00:00",
    icon="📑"
)

# Aula (com horário, respeita 19h-21h)
class_card = study_create_class(
    parent_id=section["id"],
    title="Aula 1: Introdução",
    start_time="2025-01-15T19:00:00-03:00",
    duration_minutes=120,  # 2 horas (19:00-21:00)
    icon="🎯"
)
```

### Criar Série YouTube com Episódios

```python
# Série completa (gera episódios automaticamente)
series = youtuber_create_series(
    title="The Legend of Heroes",
    sinopse="Série completa sobre...",
    total_episodes=10,
    first_recording="2025-10-16T21:00:00-03:00",
    recording_interval_days=1,
    publication_hour=12,
    icon="🎮"
)

# Ou criar episódio individual
episode = youtuber_create_episode(
    parent_id=series["id"],
    episode_number=1,
    title="Episódio 01",
    recording_date="2025-10-16T21:00:00-03:00",
    publication_date="2025-10-17T12:00:00-03:00",
    resumo_episodio="Sinopse da série completa...",  # Obrigatório no ep 1
    icon="📺"
)
```

---

## Checklist de Validação

### Antes de Criar Card

- [ ] Base correta identificada (WORK, PERSONAL, STUDIES, YOUTUBER)
- [ ] Campo de título preenchido (sem emojis)
- [ ] Ícone definido (emoji separado)
- [ ] Status válido para a base
- [ ] Timezone GMT-3 em todas as datas
- [ ] Se for sub-item: ID do pai conhecido e campo de relação correto
- [ ] Se STUDIES: Horário apenas em aulas (nível mais baixo)
- [ ] Se YOUTUBER: Série SEM `data_lancamento`, Episódios COM `data_lancamento`
- [ ] Verificado duplicatas (título + data + cliente/projeto)

---

## Erros Comuns

### 1. Status Inválido
```python
# ❌ ERRADO - YOUTUBER
'status': 'Para Fazer'  # Não existe nesta base

# ✅ CORRETO - YOUTUBER
'status': 'Não iniciado'
```

### 2. Campo de Data Errado
```python
# ❌ ERRADO - PERSONAL
'periodo': {...}  # Campo não existe

# ✅ CORRETO - PERSONAL
'data': {...}  # Campo correto
```

### 3. Campo de Relação Errado
```python
# ❌ ERRADO - STUDIES
'item_principal': 'id'  # Campo errado

# ✅ CORRETO - STUDIES
'parent_item': 'id'  # Campo correto
```

### 4. Emoji no Título
```python
# ❌ ERRADO
'title': '🎓 Meu Curso'

# ✅ CORRETO
'title': 'Meu Curso', 'icon': '🎓'
```

### 5. Horário em Card Errado
```python
# ❌ ERRADO - Seção de curso
'periodo': {'start': '2025-10-16T19:00:00-03:00'}  # Não deve ter horário

# ✅ CORRETO - Seção de curso
'periodo': {'start': '2025-10-16'}  # Apenas data
```

---

## Referências

- **MCP Server:** `my-local-place/services/external/notion-automation-suite`
- **Configurações Privadas:** `config/notion/` (compromissos, projetos e informações pessoais por frente)
- **Contexto Geral:** `config/CONTEXTO_GERAL.md` (horários e rotina - NUNCA duplicar aqui)

---

**Sempre usar o MCP customizado `notion-automation-suite` para garantir que todas as regras sejam respeitadas automaticamente.**

