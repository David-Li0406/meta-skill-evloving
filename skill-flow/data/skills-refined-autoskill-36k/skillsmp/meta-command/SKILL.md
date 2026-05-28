---
name: meta-command
description: Gera skills e comandos personalizados para Claude Code. Use quando precisar criar novas capacidades, templates de comandos, ou estrutura de skills. Inclui templates para skills simples, multi-arquivo, e com restrições de ferramentas.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Meta-Command: Gerador de Skills e Comandos

## Propósito

Este skill ajuda a criar novos skills e comandos personalizados para Claude Code. Ele fornece:

1. **Scaffolding de skills**: Gera estruturas completas de diretórios para skills
2. **Templates de comandos**: Cria templates de slash commands personalizados
3. **Guia de boas práticas**: Garante que seus skills sigam as convenções do Claude Code
4. **Validação**: Verifica skills gerados quanto à sintaxe e estrutura

## Quando usar este skill

Use meta-command quando precisar:
- Criar um novo Agent Skill
- Gerar um template de slash command personalizado
- Estruturar skills multi-arquivo com documentação de suporte
- Validar skills existentes
- Compartilhar templates de skills com sua equipe

## Instruções

### Gerar um novo skill

Quando solicitado a criar um skill, colete:
1. **Nome do skill**: O que o skill faz (ex: "pdf-processor")
2. **Descrição**: O que faz e quando usar
3. **Escopo**: Pessoal (~/.claude/skills/) ou projeto (./.claude/skills/)
4. **Tipo**: Simples (arquivo único) ou complexo (multi-arquivo com scripts)
5. **Ferramentas necessárias**: Quais ferramentas o skill deve ter acesso (opcional)

### Workflow de criação de skill

1. Criar estrutura de diretórios
2. Gerar SKILL.md com frontmatter YAML correto
3. Adicionar arquivos de suporte se for skill multi-arquivo
4. Criar exemplos de uso
5. Validar sintaxe YAML
6. Fornecer instruções de uso

### Geração de slash command

Quando criar um slash command personalizado, colete:
1. **Nome do comando**: kebab-case (ex: /meu-comando)
2. **Propósito**: O que o comando faz
3. **Argumentos**: Quaisquer parâmetros que aceita
4. **Escopo**: Pessoal ou projeto

---

## Estrutura de Arquivos

### Skill Pessoal (disponível em todos os projetos)
```
~/.claude/skills/nome-do-skill/
├── SKILL.md                 (obrigatório)
├── TEMPLATES.md             (opcional)
├── EXAMPLES.md              (opcional)
└── scripts/
    └── helper.py            (opcional)
```

### Skill de Projeto (compartilhado com equipe)
```
.claude/skills/nome-do-skill/
├── SKILL.md
├── TEMPLATES.md
├── EXAMPLES.md
└── scripts/
    └── helper.py
```

### Slash Command
```
.claude/commands/nome-do-comando.md
```

---

## Templates

### Template de SKILL.md

```yaml
---
name: nome-do-skill
description: Descrição clara do que faz E quando usar. Seja específico!
allowed-tools: Read, Write, Glob, Grep  # opcional - restringe ferramentas
---

# Nome do Skill

## Propósito
Explique o objetivo principal do skill.

## Quando usar
Liste cenários específicos de uso.

## Instruções
Forneça passos claros de como o skill funciona.

## Exemplos
Mostre casos de uso concretos.
```

### Template de Slash Command

```yaml
---
description: Descrição breve do comando
allowed-tools: Read, Grep  # opcional
argument-hint: [arg1] [arg2]  # opcional
---

# Nome do Comando

Instruções detalhadas para Claude.
Use $1 e $2 para argumentos posicionais.
Use $ARGUMENTS para todos os argumentos.
```

---

## Boas Práticas

### Descrições Específicas

```yaml
# BOM - Específico e claro
description: Extrai texto, preenche formulários e mescla PDFs. Use quando trabalhar com arquivos PDF.

# RUIM - Muito vago
description: Para documentos
```

### Skills Focados

```yaml
# BOM - Uma capacidade
name: pdf-text-extractor

# RUIM - Muito amplo
name: document-processor
```

### Convenções de Nomenclatura

- **Nomes de skills**: minúsculas com hífens (máx 64 caracteres)
- **Slash commands**: começam com `/`, minúsculas com hífens
- **Arquivos**: SKILL.md, TEMPLATES.md, EXAMPLES.md (maiúsculas)

### Restrições de Ferramentas

Use `allowed-tools` quando:
- O skill deve ser somente leitura
- Precisa limitar escopo por segurança
- Quer garantir comportamento previsível

```yaml
# Skill somente leitura
allowed-tools: Read, Glob, Grep

# Skill com escrita
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
```

---

## Exemplos de Geração

### Exemplo 1: Skill Simples

**Solicitação**: "Crie um skill para analisar commits do git"

**Saída gerada**:
```
.claude/skills/git-commit-analyzer/
└── SKILL.md
```

### Exemplo 2: Skill Multi-arquivo

**Solicitação**: "Crie um skill complexo para processar arquivos Excel"

**Saída gerada**:
```
.claude/skills/excel-processor/
├── SKILL.md
├── FORMATS.md
├── EXAMPLES.md
└── scripts/
    └── validate.py
```

### Exemplo 3: Slash Command

**Solicitação**: "Crie um comando /security-audit"

**Saída gerada**:
```
.claude/commands/security-audit.md
```

---

## Checklist de Validação

Antes de finalizar um skill gerado, verifique:

- [ ] Frontmatter YAML válido (abertura e fechamento com `---`)
- [ ] Campo `name` usa apenas letras minúsculas, números, hífens (máx 64 chars)
- [ ] Campo `description` inclui O QUE faz E QUANDO usar (máx 1024 chars)
- [ ] Campo `allowed-tools` especificado se restringir acesso
- [ ] Arquivos no local correto
- [ ] Sem barras invertidas Windows nos caminhos
- [ ] Sintaxe Markdown válida

---

## Debugging

Se Claude não usar o skill automaticamente:

1. **Verifique especificidade da descrição** - deve ser clara sobre uso
2. **Confirme caminho do arquivo** - use `ls -la` para verificar
3. **Valide sintaxe YAML** - use `head -n 10 SKILL.md`
4. **Modo debug** - execute `claude --debug`
