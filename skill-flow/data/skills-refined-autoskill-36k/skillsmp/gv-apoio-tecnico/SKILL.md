---
name: gv-apoio-tecnico
description: Resolve apoios técnicos do Grupo Voalle. Analisa o problema, investiga o código, documenta a análise e implementa correções quando necessário.
user-invocable: true
---

# Resolver Apoio Técnico - Grupo Voalle

Você está resolvendo um apoio técnico. O argumento passado é o caminho para o arquivo markdown do apoio técnico.

**Arquivo do apoio técnico:** $ARGUMENTS

## Fluxo de Resolução

### 1. Leitura e Entendimento

1. Leia o arquivo markdown do apoio técnico
2. Identifique:
   - Número do protocolo
   - Descrição do problema
   - Evidências fornecidas
   - Perguntas do solicitante

### 2. Investigação Técnica

1. Baseado na descrição do problema, identifique os módulos/sistemas envolvidos
2. Pesquise o código fonte para entender o comportamento atual:
   - Use `Grep` para encontrar arquivos relevantes
   - Use `Read` para analisar o código
   - Trace o fluxo de execução
3. Identifique a causa raiz do problema
4. Determine se é:
   - **Bug**: Requer correção de código
   - **Comportamento esperado**: Apenas esclarecimento
   - **Configuração**: Ajuste de configuração do cliente

### 3. Documentação da Análise

Atualize o arquivo markdown do apoio técnico com a seção "Análise Técnica" contendo:

```markdown
## Análise Técnica

### Validação do Código (DATA_ATUAL)

[Descreva o que foi encontrado]

### Componentes Envolvidos

| Sistema | Descrição |
|---------|-----------|
| ... | ... |

### Arquivos Relevantes

| Arquivo | Função |
|---------|--------|
| ... | ... |

### Causa Raiz

[Explique a causa do problema]

### Solução Proposta

[Se for bug, descreva a solução técnica]
```

### 4. Sugestão de Resposta

Adicione uma seção "Sugestão de Resposta" com texto pronto para enviar ao solicitante:

```markdown
## Sugestão de Resposta

\`\`\`
Olá [Nome],

[Resposta clara e objetiva sobre o problema]

Att.
\`\`\`
```

### 5. Classificação

Adicione a classificação:

```markdown
## Classificação

| Campo | Valor |
|-------|-------|
| **Criticidade** | [Baixo/Médio/Alto/Crítico] |
| **Módulos Envolvidos** | [Lista de módulos] |
| **Requer Alteração de Código?** | [SIM/NÃO] |
```

### 6. Ação Recomendada

Se for bug que requer correção:

```markdown
## Ação Recomendada

> **MIGRAR PARA INCIDENTE**
>
> [Descrição do bug]
>
> **Arquivos a corrigir:**
> - [lista de arquivos]
>
> **Correção:** [Descrição técnica da correção]
```

### 7. Implementação (se for bug)

Se identificado como bug e o usuário confirmar:

1. **GitLab**:
   - Crie uma issue no projeto apropriado via MCP GitLab
   - Crie um MR vinculado à issue (isso gera a branch automaticamente)

2. **Código**:
   - Faça checkout da branch criada
   - Implemente a correção seguindo os padrões do projeto (ver CLAUDE.md)
   - Faça commit (sem co-author)
   - Faça push

3. **YouTrack**:
   - Atualize o card para "Backlog-Review"

## Padrões de Código (lerna-repo)

- **Sem ponto-e-vírgula** (ESLint)
- **Chaves sempre obrigatórias** em statements de controle
- **Template literals:** `${ variable }` com espaços dentro das chaves
- **JSX curly spacing:** `{ value }` com espaços
- **Ordem de imports:** react → externos → @syntesis → relativos → estilos

## Convenção de Commit

```
<type>: <subject>

Types: feat, fix, refactor, style, docs, test
```

Exemplo: `fix: limpar roomId órfão das abas quando atendimento omni é concluído`

## Ferramentas MCP Disponíveis

- **GitLab**: `mcp__gitlab-syntesis__*` - criar issues, MRs, branches
- **YouTrack**: `mcp__youtrack__*` - buscar e atualizar cards

## Notas Importantes

- Sempre leia o código antes de propor alterações
- Valide se a solução segue os padrões existentes no projeto
- Use `reaction` do MobX para comunicação entre stores (evita dependência circular)
- Documente bem a análise para facilitar futuras consultas
