# Acompanhamento de Progresso

## Frequência de Atualização

### Atualizações Diárias

Para trabalho de implementação ativo:

**O que atualizar**:
- Status da tarefa se mudou
- Adicionar nota de progresso na tarefa
- Atualizar bloqueios

**Quando**:
- Fim do dia de trabalho
- Após concluir trabalho significativo
- Ao encontrar bloqueios

### Atualizações de Marco

Para conclusão de fase/marco:

**O que atualizar**:
- Marcar fase como concluída no plano
- Adicionar resumo do marco
- Atualizar cronograma se necessário
- Reportar aos stakeholders

**Quando**:
- Conclusão de fase
- Entregável principal pronto
- Fim de sprint
- Release

### Atualizações de Mudança de Status

Para transições de estado da tarefa:

**O que atualizar**:
- Propriedade de status da tarefa
- Adicionar nota de transição
- Notificar pessoas relevantes

**Quando**:
- Iniciar trabalho (A Fazer → Em Progresso)
- Pronto para revisão (Em Progresso → Em Revisão)
- Concluir (Em Revisão → Concluído)
- Bloquear (Qualquer → Bloqueado)

## Formato de Nota de Progresso

### Nota de Progresso Diária

```markdown
## Progresso: [Data]

### Concluído
- [Conquista específica com detalhes]
- [Conquista específica com detalhes]

### Em Progresso
- [Item de trabalho atual]
- Status atual: [Percentual ou descrição]

### Próximos Passos
1. [Próxima ação planejada]
2. [Próxima ação planejada]

### Bloqueios
- [Descrição do bloqueio e quem/o que é necessário para destravar]
- Ou: Nenhum

### Decisões Tomadas
- [Decisões técnicas/produto]

### Observações
[Contexto adicional, aprendizados, problemas encontrados]
```

Exemplo:

```markdown
## Progresso: 14 out 2025

### Concluído
- Implementados endpoints da API de autenticação de usuários (login, logout, refresh)
- Adicionada geração e validação de tokens JWT
- Escritos testes unitários para o serviço de autenticação (95% de cobertura)

### Em Progresso
- Integração do formulário de login no frontend
- Atualmente: o formulário envia, mas precisa tratar estados de erro

### Próximos Passos
1. Concluir tratamento de erros no formulário de login
2. Adicionar estados de carregamento
3. Implementar funcionalidade "lembrar de mim"

### Bloqueios
Nenhum

### Decisões Tomadas
- Usar cookies HttpOnly para refresh tokens (mais seguro que localStorage)
- Timeout da sessão definido para 24 horas com base em revisão de segurança

### Observações
- Encontrado edge case com tentativas de login concorrentes, adicionado ao backlog
- Performance da checagem de autenticação está boa (<10ms)
```

### Resumo de Marco

```markdown
## Fase [N] Concluída: [Data]

### Visão Geral
[Descrição breve do que foi realizado nesta fase]

### Tarefas Concluídas
- <mention-page url="...">Tarefa 1</mention-page> ✅
- <mention-page url="...">Tarefa 2</mention-page> ✅
- <mention-page url="...">Tarefa 3</mention-page> ✅

### Entregáveis
- [Entregável 1]: [Link/descrição]
- [Entregável 2]: [Link/descrição]

### Principais Conquistas
- [Grande realização]
- [Grande realização]

### Métricas
- [Métrica relevante]: [Valor]
- [Métrica relevante]: [Valor]

### Desafios Superados
- [Desafio e como foi resolvido]

### Aprendizados
**O que funcionou bem**:
- [Fator de sucesso]

**O que melhorar**:
- [Área de melhoria]

### Impacto no Cronograma
- No prazo / [X dias adiantado/atrasado]
- Motivo: [Se houver desvio, explique]

### Próxima Fase
- **Início**: [Nome da próxima fase]
- **Data alvo de início**: [Data]
- **Foco**: [Objetivos principais]
```

## Atualizando o Plano de Implementação

### Indicadores de Progresso

Atualize a página do plano regularmente:

```markdown
## Visão Geral do Status

**Progresso Geral**: 45% concluído

### Status das Fases
- ✅ Fase 1: Base - Concluída
- 🔄 Fase 2: Funcionalidades Centrais - Em Progresso (60%)
- ⏳ Fase 3: Integração - Não Iniciada

### Resumo de Tarefas
- ✅ Concluídas: 12 tarefas
- 🔄 Em Progresso: 5 tarefas
- 🚧 Bloqueadas: 1 tarefa
- ⏳ Não Iniciadas: 8 tarefas

**Última atualização**: [Data]
```

### Atualizações de Checklist de Tarefas

Marque tarefas concluídas:

```markdown
## Fases de Implementação

### Fase 1: Base
- [x] <mention-page url="...">Esquema do banco de dados</mention-page>
- [x] <mention-page url="...">Estrutura inicial da API</mention-page>
- [x] <mention-page url="...">Configuração de autenticação</mention-page>

### Fase 2: Funcionalidades Centrais
- [x] <mention-page url="...">Gestão de usuários</mention-page>
- [ ] <mention-page url="...">Dashboard</mention-page>
- [ ] <mention-page url="...">Relatórios</mention-page>
```

### Atualizações de Cronograma

Atualize as datas de marcos:

```markdown
## Cronograma

| Marco | Original | Atual | Status |
|-----------|----------|---------|--------|
| Fase 1 | 15 out | 14 out | ✅ Concluída (1 dia adiantado) |
| Fase 2 | 30 out | 2 nov | 🔄 Em Progresso (atraso de 3 dias) |
| Fase 3 | 15 nov | 18 nov | ⏳ Planejada (ajustada) |
| Lançamento | 20 nov | 22 nov | ⏳ Planejado (ajustado) |

**Status do cronograma**: Levemente atrasado devido a [motivo]
```

## Acompanhamento de Status das Tarefas

### Definições de Status

**A Fazer**: Não iniciada
- Tarefa pronta para começar
- Dependências atendidas
- Atribuída (ou disponível)

**Em Progresso**: Em execução
- Trabalho iniciado
- Atribuída a alguém
- Atualizações regulares esperadas

**Bloqueada**: Não pode prosseguir
- Dependência não atendida
- Bloqueio externo
- Aguardando decisão/recurso

**Em Revisão**: Aguardando revisão
- Trabalho completo do ponto de vista de quem implementou
- Precisa de code review, QA ou aprovação
- Revisores identificados

**Concluída**: Finalizada
- Todos os critérios de aceitação atendidos
- Revisado e aprovado
- Deploy/entrega realizados

### Atualizando o Status da Tarefa

Ao atualizar:

```
1. Atualize a propriedade Status
2. Adicione nota de progresso explicando a mudança
3. Atualize tarefas relacionadas se necessário
4. Notifique pessoas relevantes via comentário

Exemplo:
properties: { "Status": "Em Progresso" }

Atualização de conteúdo:
## Progresso: 14 out 2025
Iniciada a implementação. Estrutura básica configurada e testes iniciais escritos.
```

## Acompanhamento de Bloqueios

### Registrando Bloqueios

Ao encontrar um bloqueio:

```markdown
## Bloqueios

### [Data]: [Descrição do bloqueio]
**Status**: 🚧 Ativo
**Impacto**: [O que está bloqueado]
**Necessário para destravar**: [Ação/pessoa/decisão necessária]
**Responsável**: [Quem é responsável por destravar]
**Resolução alvo**: [Data ou prazo]
```

### Resolvendo Bloqueios

Quando desbloqueado:

```markdown
## Bloqueios

### [Data]: [Descrição do bloqueio]
**Status**: ✅ Resolvido em [Data]
**Resolução**: [Como foi resolvido]
**Impacto**: [Qualquer impacto em cronograma/escopo]
```

### Escalonando Bloqueios

Se o bloqueio precisar de escalonamento:

```
1. Atualize o status do bloqueio na tarefa
2. Adicione comentário mencionando o stakeholder
3. Atualize o plano com o impacto do bloqueio
4. Proponha mitigação, se possível
```

## Acompanhamento de Métricas

### Acompanhamento de Velocidade

Monitore a taxa de conclusão:

```markdown
## Velocidade

### Semana 1
- Tarefas concluídas: 8
- Story points: 21
- Velocidade: Forte

### Semana 2
- Tarefas concluídas: 6
- Story points: 18
- Velocidade: Moderada (1 bloqueio)

### Semana 3
- Tarefas concluídas: 9
- Story points: 24
- Velocidade: Forte (bloqueio resolvido)
```

### Métricas de Qualidade

Monitore indicadores de qualidade:

```markdown
## Métricas de Qualidade

- Cobertura de testes: 87%
- Taxa de aprovação em code review: 95%
- Contagem de bugs: 3 (2 menores, 1 cosmético)
- Performance: Todas as metas atendidas
- Segurança: Nenhum problema encontrado
```

### Métricas de Progresso

Progresso quantitativo:

```markdown
## Métricas de Progresso

- Requisitos implementados: 15/20 (75%)
- Critérios de aceitação atendidos: 42/56 (75%)
- Casos de teste passando: 128/135 (95%)
- Código completo: 80%
- Documentação: 60%
```

## Comunicação com Stakeholders

### Relatório de Status Semanal

```markdown
## Status Semanal: [Semana da Data]

### Resumo
[Um parágrafo sobre progresso e status]

### Conquistas da Semana
- [Conquista chave]
- [Conquista chave]
- [Conquista chave]

### Plano da Próxima Semana
- [Trabalho planejado]
- [Trabalho planejado]

### Status
- No prazo / Em risco / Atrasado
- [Se em risco ou atrasado, explique e forneça plano de mitigação]

### Bloqueios e Necessidades
- [Bloqueio ativo ou necessidade de ajuda]
- Ou: Nenhum

### Riscos
- [Risco novo ou em evolução]
- Ou: Nenhum identificado no momento
```

### Resumo Executivo

Para atualizações de liderança:

```markdown
## Status da Implementação: [Nome da Funcionalidade]

**Status Geral**: 🟢 No Prazo / 🟡 Em Risco / 🔴 Atrasado

**Progresso**: [X]% concluído

**Principais Atualizações**:
- [Atualização mais importante]
- [Atualização mais importante]

**Cronograma**: [Status vs plano original]

**Riscos**: [Principais 1-2 riscos]

**Próximo Marco**: [Próximo marco e data]
```

## Acompanhamento Automático de Progresso

### Status Baseado em Consulta

Gere status a partir do banco de dados de tarefas:

```
Consultar banco de dados de tarefas:
SELECT 
  "Status",
  COUNT(*) as count
FROM "collection://tasks-uuid"
WHERE "Related Tasks" CONTAINS 'plan-page-id'
GROUP BY "Status"

Gerar resumo:
- A Fazer: 8
- Em Progresso: 5
- Bloqueado: 1
- Em Revisão: 2
- Concluído: 12

Geral: 44% concluído (12/28 tarefas)
```

### Cálculo de Cronograma

Calcule a conclusão projetada:

```
Velocidade média: 6 tarefas/semana
Tarefas restantes: 14
Conclusão projetada: 2,3 semanas a partir de agora

Comparação com a meta: [No prazo/Atrasado/Adiantado]
```

## Boas Práticas

1. **Atualize regularmente**: Não deixe atualizações acumularem
2. **Seja específico**: "Concluiu login" vs "Fez progresso"
3. **Quantifique o progresso**: Use percentuais, contagens, métricas
4. **Anote bloqueios imediatamente**: Não espere para reportar bloqueios
5. **Vincule ao trabalho**: Referencie PRs, deploys, demos
6. **Registre decisões**: Documente o porquê, não só o quê
7. **Seja honesto**: Reporte status real, não otimista
8. **Atualize em um só lugar**: Mantenha o plano de implementação como fonte de verdade

