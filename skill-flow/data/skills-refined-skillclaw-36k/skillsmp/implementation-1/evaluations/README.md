# Avaliações da Skill Implementation

Cenários de avaliação para testar a skill Implementation em diferentes modelos Claude.

## Propósito

Essas avaliações garantem que a skill Implementation:
- Encontre e analise arquivos de especificação com precisão
- Quebre specs em planos de implementação acionáveis
- Crie tarefas no TodoWrite com critérios claros
- Acompanhe progresso e atualize status
- Funcione de forma consistente entre Haiku, Sonnet e Opus

## Arquivos de Avaliação

### basic-spec-implementation.json
Testa o fluxo básico de transformar uma spec em um plano de implementação.

**Cenário**: Implementar funcionalidade de autenticação de usuário a partir da spec
**Comportamentos-chave**:
- Procura e encontra o arquivo de spec
- Lê a spec e extrai requisitos
- Analisa requisitos em fases (setup, funcionalidades centrais, polimento)
- Cria arquivo de plano de implementação
- Quebra em fases claras com entregáveis
- Cria tarefas no TodoWrite

### spec-to-tasks.json
Testa a criação de tarefas concretas a partir de uma especificação.

**Cenário**: Criar tarefas a partir da spec de redesign de API
**Comportamentos-chave**:
- Encontra o arquivo da spec no projeto
- Extrai requisitos específicos e critérios de aceitação
- Cria várias tarefas no TodoWrite
- Cada tarefa tem content e activeForm
- Tarefas têm sequência lógica
- Vincula tarefas ao plano/spec

## Executando Avaliações

1. Habilite a skill `implementation`
2. Envie a query do arquivo de avaliação
3. Verifique se a skill encontra o arquivo da spec via Glob
4. Verifique se os requisitos são analisados com precisão
5. Confirme que o plano de implementação é criado com fases
6. Verifique se as tarefas são criadas no TodoWrite
7. Teste com Haiku, Sonnet e Opus

## Comportamentos Esperados da Skill

As avaliações de Implementation devem verificar:

### Descoberta e Análise da Spec
- Usa Glob para encontrar arquivos de especificação
- Lê conteúdo completo da spec com Read
- Extrai todos os requisitos com precisão
- Identifica dependências técnicas
- Entende critérios de aceitação
- Anota ambiguidades ou detalhes ausentes

### Planejamento de Implementação
- Cria arquivo de plano de implementação com Write
- Quebra o trabalho em fases lógicas:
  - Fase 1: Base/Setup
  - Fase 2: Implementação Central
  - Fase 3: Testes e Polimento
- Identifica dependências entre fases
- Referencia o arquivo da spec original

### Criação de Tarefas
- Cria tarefas no TodoWrite
- Cada tarefa tem:
  - content: forma imperativa ("Implementar X")
  - activeForm: forma contínua ("Implementando X")
  - status: "pending" (inicial)
- Tarefas no tamanho adequado (concluíveis em uma sessão)
- Ordenação lógica por dependência

### Acompanhamento de Progresso
- Atualiza status das tarefas via TodoWrite
- pending → in_progress → completed
- Apenas uma tarefa in_progress por vez

## Criando Novas Avaliações

Ao adicionar avaliações de Implementation:

1. **Teste diferentes tipos de spec** - Funcionalidades, migrações, refactors, mudanças de API, componentes de UI
2. **Varie a complexidade** - Implementações simples de 1 fase vs. complexas com múltiplas fases
3. **Teste a granularidade das tarefas** - Cria tarefas com tamanho adequado?
4. **Inclua casos de borda** - Specs vagas, requisitos conflitantes, detalhes ausentes
5. **Acompanhamento de progresso** - Atualizar TodoWrite conforme tarefas são concluídas

## Exemplo de Critérios de Sucesso

**Bom** (específico, testável):
- "Usa Glob com padrão apropriado para encontrar a spec"
- "Cria plano de implementação com 3 fases: Setup → Core → Polimento"
- "Cria 5-8 tarefas no TodoWrite com content e activeForm"
- "Cada tarefa tem status inicial 'pending'"
- "Tarefas ordenadas por dependência no array"

**Ruim** (vago, não testável):
- "Cria bom plano de implementação"
- "Tarefas são bem estruturadas"
- "Quebra a spec apropriadamente"
