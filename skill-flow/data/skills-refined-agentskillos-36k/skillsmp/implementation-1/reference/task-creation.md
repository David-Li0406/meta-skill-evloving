# Criação de Tarefas a partir de Specs

## Usando TodoWrite

O Claude Code usa a ferramenta `TodoWrite` para gerenciar tarefas de implementação.

```
TodoWrite aceita um array de tarefas:
[
  {
    "content": "Descrição da tarefa (imperativo)",
    "activeForm": "Descrição da tarefa (gerúndio)",
    "status": "pending" | "in_progress" | "completed"
  }
]
```

## Estratégia de Quebra de Tarefas

### Diretrizes de Tamanho

**Bom tamanho de tarefa**:
- Concluível em uma sessão
- Entregável único e claro
- Testável de forma independente
- Dependências mínimas

**Muito grande**:
- Múltiplos entregáveis
- Muitas dependências
- Quebre em partes menores

**Muito pequena**:
- Granular demais
- Agrupe com trabalho relacionado

### Granularidade por Fase

**Fases iniciais**: Tarefas maiores são aceitáveis
- "Desenhar esquema do banco de dados"
- "Configurar estrutura da API"

**Fases intermediárias**: Tarefas de tamanho médio
- "Implementar autenticação de usuários"
- "Construir UI do dashboard"

**Fases finais**: Tarefas menores e precisas
- "Corrigir bug de validação no formulário"
- "Adicionar estado de carregamento no botão"

## Padrão de Criação de Tarefas

Para cada requisito ou item de trabalho:

```
1. Identificar o trabalho
2. Determinar o tamanho da tarefa
3. Definir content (forma imperativa)
4. Definir activeForm (forma contínua)
5. Adicionar ao TodoWrite com status "pending"
```

### Exemplo de TodoWrite

```json
[
  {
    "content": "Criar schema do banco para User Profile API",
    "activeForm": "Criando schema do banco para User Profile API",
    "status": "pending"
  },
  {
    "content": "Configurar bucket S3 para avatares",
    "activeForm": "Configurando bucket S3 para avatares",
    "status": "pending"
  },
  {
    "content": "Implementar endpoint GET de perfil",
    "activeForm": "Implementando endpoint GET de perfil",
    "status": "pending"
  }
]
```

## Tipos de Tarefa

### Tarefas de Infraestrutura/Setup

```
Content: "Setup: [O que está sendo configurado]"
Exemplos:
- "Setup: Configurar pool de conexões do banco"
- "Setup: Inicializar middleware de autenticação"
- "Setup: Criar pipeline de CI/CD"

Foco: Preparar ambiente/ferramentas
```

### Tarefas de Implementação de Funcionalidade

```
Content: "Implementar: [Nome da funcionalidade]"
Exemplos:
- "Implementar: Fluxo de login do usuário"
- "Implementar: Funcionalidade de upload de arquivos"
- "Implementar: Widget de dashboard"

Foco: Construir funcionalidade específica
```

### Tarefas de Integração

```
Content: "Integrar: [O que está sendo integrado]"
Exemplos:
- "Integrar: Conectar frontend à API"
- "Integrar: Adicionar provedor de pagamento"
- "Integrar: Vincular perfil do usuário ao dashboard"

Foco: Conectar componentes
```

### Tarefas de Testes

```
Content: "Testar: [O que está sendo testado]"
Exemplos:
- "Testar: Escrever testes unitários para o serviço de autenticação"
- "Testar: Testes E2E para o fluxo de checkout"
- "Testar: Testes de performance para a API"

Foco: Validação e garantia de qualidade
```

### Tarefas de Documentação

```
Content: "Documentar: [O que está sendo documentado]"
Exemplos:
- "Documentar: Endpoints da API"
- "Documentar: Instruções de setup"
- "Documentar: Decisões de arquitetura"

Foco: Criar documentação
```

### Tarefas de Correção de Bug

```
Content: "Corrigir: [Descrição do bug]"
Exemplos:
- "Corrigir: Erro de login no Safari"
- "Corrigir: Vazamento de memória no processamento de imagens"
- "Corrigir: Race condition no fluxo de pagamentos"

Foco: Resolver problemas
```

### Tarefas de Refatoração

```
Content: "Refatorar: [O que está sendo refatorado]"
Exemplos:
- "Refatorar: Extrair lógica de autenticação para serviço"
- "Refatorar: Otimizar queries do banco"
- "Refatorar: Simplificar hierarquia de componentes"

Foco: Melhorar qualidade do código
```

## Sequenciamento de Tarefas

### Caminho Crítico

Identifique tarefas que precisam acontecer primeiro:

```
1. Esquema do banco de dados
2. Base da API
3. Lógica de negócio central
4. Integração com frontend
5. Testes
6. Deploy
```

### Trilhas Paralelas

Tarefas que podem acontecer simultaneamente:

```
Trilha A: Desenvolvimento backend
- Endpoints da API
- Lógica de negócio
- Operações de banco

Trilha B: Desenvolvimento frontend
- Componentes de UI
- Gerenciamento de estado
- Roteamento

Trilha C: Infraestrutura
- Setup de CI/CD
- Monitoramento
- Documentação
```

### Sequenciamento por Fase

Agrupe por fase de implementação:

```
Fase 1 (Base):
- Tarefas de setup
- Tarefas de infraestrutura

Fase 2 (Core):
- Tarefas de implementação de funcionalidade
- Tarefas de integração

Fase 3 (Polimento):
- Tarefas de testes
- Tarefas de documentação
- Tarefas de otimização
```

## Atribuição de Prioridade

### P0/Crítico
- Bloqueia todo o restante
- Funcionalidade central
- Requisitos de segurança
- Integridade dos dados

### P1/Alta
- Funcionalidades importantes
- Funcionalidades voltadas ao usuário
- Requisitos de performance

### P2/Média
- Funcionalidades "nice-to-have"
- Otimizações
- Melhorias menores

### P3/Baixa
- Melhorias futuras
- Tratamento de edge cases
- Melhorias cosméticas

## Relações entre Tarefas

### Padrão de Tarefa Pai

Para funcionalidades grandes, quebre em subtarefas no TodoWrite:

```
Pai: "Funcionalidade: Autenticação de Usuário"
Filhas:
- "Setup: Configurar biblioteca de autenticação"
- "Implementar: Fluxo de login"
- "Implementar: Redefinição de senha"
- "Testar: Funcionalidade de autenticação"
```

### Padrão de Cadeia de Dependências

Para trabalho sequencial, ordene as tarefas no array:

```
[
  { "content": "Desenhar esquema do banco de dados", ... },
  { "content": "Implementar modelos de dados", ... },
  { "content": "Criar endpoints da API", ... },
  { "content": "Integrar com frontend", ... }
]
```

## Convenções de Nomenclatura de Tarefas

**Seja específico**:
✓ "Implementar login do usuário com email/senha"
✗ "Adicionar login"

**Inclua contexto**:
✓ "Dashboard: Adicionar widget de gráfico de receita"
✗ "Adicionar gráfico"

**Use verbos de ação**:
- Implementar, Construir, Criar
- Integrar, Conectar, Vincular
- Corrigir, Resolver, Depurar
- Testar, Validar, Verificar
- Documentar, Escrever, Atualizar
- Refatorar, Otimizar, Melhorar

## Checklist de Validação

Antes de finalizar as tarefas:

☐ Cada tarefa tem objetivo claro
☐ Tamanho adequado (concluível em uma sessão)
☐ Ordenadas por prioridade/dependência
☐ Forma imperativa (content) definida
☐ Forma contínua (activeForm) definida
☐ Status inicial é "pending"
