# Templates de Referência

Este arquivo contém templates prontos para copiar e adaptar ao criar novos skills e comandos.

---

## Template: Skill Simples

Use para skills focados com uma única responsabilidade.

```yaml
---
name: meu-skill
description: [O que faz]. Use quando [cenário de uso específico].
---

# [Nome do Skill]

## Propósito

[Descrição do objetivo principal em 1-2 parágrafos]

## Quando Usar

Use este skill quando:
- [Cenário 1]
- [Cenário 2]
- [Cenário 3]

## Instruções

### [Funcionalidade Principal]

1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Exemplos

### Exemplo 1: [Título]

**Entrada**: "[Descrição da solicitação]"

**Saída**: [Descrição do resultado esperado]
```

---

## Template: Skill com Restrição de Ferramentas

Use quando o skill deve ter acesso limitado às ferramentas.

```yaml
---
name: meu-skill-restrito
description: [O que faz]. Use quando [cenário]. Somente leitura/análise.
allowed-tools: Read, Glob, Grep
---

# [Nome do Skill]

## Propósito

Este skill realiza análise/leitura de [domínio] sem modificar arquivos.

## Restrições

- Somente leitura de arquivos
- Não executa comandos externos
- Não modifica código

## Instruções

[Instruções detalhadas]
```

---

## Template: Skill Multi-arquivo

Use para skills complexos que precisam de documentação adicional.

### SKILL.md (principal)
```yaml
---
name: meu-skill-complexo
description: [O que faz]. Use quando [cenário]. Suporta [funcionalidades].
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# [Nome do Skill]

## Propósito

[Descrição detalhada]

## Arquivos de Referência

- `FORMATS.md` - Formatos suportados e especificações
- `EXAMPLES.md` - Exemplos detalhados de uso
- `scripts/` - Scripts auxiliares

## Instruções

[Instruções principais]

## Ver Também

Consulte os arquivos de referência para informações detalhadas.
```

### FORMATS.md (referência)
```markdown
# Formatos Suportados

## Formato 1: [Nome]

### Estrutura
[Descrição da estrutura]

### Exemplo
[Exemplo do formato]

## Formato 2: [Nome]

[...]
```

### EXAMPLES.md (referência)
```markdown
# Exemplos de Uso

## Caso de Uso 1: [Título]

### Contexto
[Descrição do cenário]

### Solicitação
"[Exemplo de prompt do usuário]"

### Resultado
[Descrição do resultado]

### Arquivos Gerados
[Lista de arquivos criados/modificados]

## Caso de Uso 2: [Título]

[...]
```

---

## Template: Slash Command Simples

Use para comandos invocados pelo usuário com `/nome`.

```yaml
---
description: [O que o comando faz em uma linha]
---

# [Nome do Comando]

[Instruções detalhadas para Claude executar quando o comando for invocado]

## Passos

1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

## Formato de Saída

[Descrição do formato esperado da saída]
```

---

## Template: Slash Command com Argumentos

Use quando o comando aceita parâmetros.

```yaml
---
description: [O que faz] com [tipo de argumento]
argument-hint: <argumento-obrigatório> [argumento-opcional]
---

# [Nome do Comando]

Recebe os seguintes argumentos:
- `$1` - [Descrição do primeiro argumento]
- `$2` - [Descrição do segundo argumento] (opcional)
- `$ARGUMENTS` - Todos os argumentos como string

## Instruções

Quando invocado com `$1`:

1. [Ação baseada no argumento]
2. [Próxima ação]

Se `$2` for fornecido:
- [Comportamento adicional]
```

---

## Template: Slash Command com Restrição

Use quando o comando deve ter escopo limitado.

```yaml
---
description: Analisa [algo] sem modificar arquivos
allowed-tools: Read, Glob, Grep
argument-hint: [caminho]
---

# [Nome do Comando]

## Restrições

Este comando é somente leitura. Não modifica arquivos.

## Instruções

Analise $ARGUMENTS e forneça:

1. [Tipo de análise 1]
2. [Tipo de análise 2]
3. [Resumo]
```

---

## Mapeamento de Ferramentas

Referência rápida de ferramentas disponíveis para `allowed-tools`:

| Ferramenta | Descrição |
|------------|-----------|
| `Read` | Leitura de arquivos |
| `Write` | Criação de arquivos |
| `Edit` | Edição de arquivos existentes |
| `Glob` | Busca por padrões de nome |
| `Grep` | Busca por conteúdo |
| `Bash` | Execução de comandos shell |
| `WebFetch` | Busca de conteúdo web |
| `WebSearch` | Pesquisa na web |
| `Task` | Execução de subagentes |
| `LSP` | Operações de Language Server |

### Combinações Comuns

```yaml
# Somente leitura/análise
allowed-tools: Read, Glob, Grep

# Leitura com web
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch

# Escrita completa
allowed-tools: Read, Write, Edit, Glob, Grep, Bash

# Pesquisa e exploração
allowed-tools: Read, Glob, Grep, Task
```
