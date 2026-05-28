---
name: prd-writing
description: Skill para escrever PRDs estruturados para features de software
triggers:
  - "criar prd"
  - "nova feature"
  - "definir requisitos"
  - "especificar feature"
  - "documentar feature"
---

# PRD Writing Skill

Este skill e ativado automaticamente quando o usuario quer definir uma nova feature ou criar documentacao de requisitos.

## Quando Usar

- Definir uma nova feature
- Documentar requisitos de negocio
- Especificar comportamento esperado
- Criar criterios de aceitacao

## Template

Use o template em `templates/prd-template.md` como base.

## Processo

1. **Entender o problema**
   - Qual problema esta sendo resolvido?
   - Quem sao os usuarios afetados?
   - Qual o impacto de nao resolver?

2. **Definir requisitos funcionais**
   - O que o sistema deve fazer?
   - Quais sao os inputs e outputs?
   - Quais validacoes sao necessarias?

3. **Definir requisitos nao-funcionais**
   - Performance esperada
   - Seguranca necessaria
   - Escalabilidade requerida

4. **Estabelecer criterios de aceitacao**
   - Como validar que esta pronto?
   - Quais testes sao necessarios?
   - Quem aprova a entrega?

## Outputs

- `.claude/plans/features/<nome>/prd.md`

## Arquivos Relacionados

- `templates/prd-template.md` - Template padrao
