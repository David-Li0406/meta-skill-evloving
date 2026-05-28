---
name: prd-writing
description: Use this skill when you need to write structured PRDs for software features.
---

# PRD Writing Skill

Este skill é ativado automaticamente quando o usuário quer definir uma nova feature ou criar documentação de requisitos.

## Quando Usar

- Definir uma nova feature
- Documentar requisitos de negócio
- Especificar comportamento esperado
- Criar critérios de aceitação

## Template

Use o template em `templates/prd-template.md` como base.

## Processo

1. **Entender o problema**
   - Qual problema está sendo resolvido?
   - Quem são os usuários afetados?
   - Qual o impacto de não resolver?

2. **Definir requisitos funcionais**
   - O que o sistema deve fazer?
   - Quais são os inputs e outputs?
   - Quais validações são necessárias?

3. **Definir requisitos não-funcionais**
   - Performance esperada
   - Segurança necessária
   - Escalabilidade requerida

4. **Estabelecer critérios de aceitação**
   - Como validar que está pronto?
   - Quais testes são necessários?
   - Quem aprova a entrega?

## Outputs

- `.claude/plans/features/<nome>/prd.md`

## Arquivos Relacionados

- `templates/prd-template.md` - Template padrão