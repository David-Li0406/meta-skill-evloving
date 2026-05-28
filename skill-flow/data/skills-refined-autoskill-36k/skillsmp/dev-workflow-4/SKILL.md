---
name: dev-workflow
description: Executa workflow completo de desenvolvimento (plan → implement → test → review). Use para implementar features ou corrigir bugs de forma estruturada e sequencial.
argument-hint: [descrição da feature ou bug]
---

# Dev Workflow

Workflow completo de desenvolvimento que executa sequencialmente as etapas de planejamento, implementação, testes e revisão.

## Uso

```
/dev-workflow Implementar sistema de autenticação com JWT
```

## Instruções

Execute o workflow completo de desenvolvimento para: $ARGUMENTS

### Validação Inicial

1. Se `$ARGUMENTS` estiver vazio, pergunte ao usuário o que deseja implementar
2. Inicie o workflow automaticamente sem confirmação

### Workflow Sequencial

Execute as seguintes etapas **em ordem**, aguardando a conclusão de cada uma antes de prosseguir:

---

## Etapa 1: Planejamento (/plan)

**Objetivo:** Criar um plano detalhado de implementação

1. Execute o comando `/plan` com a descrição fornecida
2. O plano será salvo em `specs/<nome_descritivo>.md`
3. Apresente o resumo do plano ao usuário
4. Prossiga automaticamente para a implementação

---

## Etapa 2: Implementação (/implement)

**Objetivo:** Implementar o código conforme o plano

1. Execute o comando `/implement` com o arquivo de spec gerado na etapa anterior
2. Implemente todos os itens listados no plano
3. Marque os checkboxes conforme cada item é concluído
4. Apresente um resumo das implementações realizadas
5. Prossiga automaticamente para os testes

---

## Etapa 3: Testes (/test-implementation)

**Objetivo:** Implementar e executar testes

1. Execute o comando `/test-implementation` referenciando o arquivo de spec
2. Implemente os testes unitários e de integração definidos no plano
3. Execute os testes e corrija falhas se necessário
4. Apresente o resultado dos testes
5. Prossiga automaticamente para a revisão

---

## Etapa 4: Revisão (/review)

**Objetivo:** Revisar o código implementado

1. Execute o comando `/review` para analisar as mudanças
2. Identifique possíveis melhorias, problemas de segurança ou inconsistências
3. Apresente o relatório de revisão ao usuário
4. Se houver problemas críticos, sugira correções

---

## Finalização

Ao concluir todas as etapas, apresente um resumo completo:

```
## Workflow Concluído

### Resumo
- **Feature/Bug:** [descrição]
- **Plano:** specs/[nome].md
- **Arquivos modificados:** [lista]
- **Testes:** [passed/failed]
- **Revisão:** [status]

```

## Regras do Workflow

1. **Sequencial:** Cada etapa deve ser completada antes de iniciar a próxima
2. **Automático:** Execute todas as etapas sem interrupção ou confirmação
3. **Transparência:** Mantenha o usuário informado do progresso em cada etapa

## Variáveis Importantes

- `$SPEC_FILE`: Caminho do arquivo de spec gerado (ex: `specs/feature-auth.md`)
- `$ARGUMENTS`: Descrição original da feature/bug

## Tratamento de Erros

- Se qualquer etapa falhar, tente corrigir automaticamente
- Se não for possível corrigir, continue para a próxima etapa e registre o problema no relatório final
- Mantenha log do que foi completado
