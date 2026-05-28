# ⚡ Quick Start: Skills e Agents - Plataforma B2B de treinamento técnico corporativo

**Objetivo:** Começar a usar Skills e Agents em 5 minutos

---

## ✅ Checklist de Configuração

- [x] Skills criadas em `.claude/skills/` (5 skills)
- [x] Agent criado em `.claude/agents/` (1 agent)
- [x] `CLAUDE.md` atualizado com documentação
- [x] `README-SKILLS-AGENTS.md` com guia completo

**Status:** ✅ Tudo pronto! Pode começar a usar.

---

## 🚀 Teste Rápido (2 Minutos)

### Teste 1: Skill de Nomenclatura

```
1. Abra: src/components/BashLearningSystem.jsx
2. Procure por: "Ver Notas" ou "Sistema de Aprendizado"
3. Claude automaticamente sugerirá substituição conforme glossário ÉPICO 12
```

**Resultado Esperado:** Claude alerta sobre termo proibido e sugere correção.

---

### Teste 2: Skill de Arquitetura

```
1. Pergunte: "Quantos componentes React tem o projeto?"
2. Claude responde: "17 componentes" (usando platform-architecture skill)
3. Pergunte: "Qual a estrutura de navegação?"
4. Claude explica: 4 níveis (Hub → Curso → Aula → Prática)
```

**Resultado Esperado:** Respostas instantâneas sem precisar ler arquivos.

---

### Teste 3: Agent de UX

```
User: "Implementar breadcrumb seguindo US-061"

→ ux-refactor-agent ativa
→ Usa breadcrumb-impl skill como referência
→ Entrega código completo + acessibilidade
```

**Resultado Esperado:** Implementação completa com WCAG AA.

---

## 📖 3 Casos de Uso Comuns

### Caso 1: Refatorar Nomenclatura

**Tarefa:** Substituir todos os "Ver Notas" por "📖 Estudar"

**Como fazer:**
```
User: "Substituir 'Ver Notas' por '📖 Estudar' em todos os Learning Systems"

→ ux-nomenclature skill ativa automaticamente
→ Claude lista todos os arquivos afetados
→ Aplica substituições seguindo glossário
→ Valida consistência
```

---

### Caso 2: Criar Componente Genérico

**Tarefa:** Extrair BaseLearningSystem dos 5 sistemas duplicados

**Como fazer:**
```
User: "Refatorar Learning Systems para reduzir duplicação conforme US-043"

→ component-refactor skill ativa
→ Analisa código duplicado (~800 linhas)
→ Propõe estrutura de BaseLearningSystem
→ Extrai hooks customizados
→ Migra primeiro sistema (pilot)
```

---

### Caso 3: Integrar Nova Tecnologia

**Tarefa:** Adicionar Radix UI ao projeto

**Como fazer:**
```
User: "Usar meta-skill para integrar Radix UI ao Plataforma B2B de treinamento técnico corporativo"

→ meta-configuracao-evolucao skill ativa
→ WebSearch("Radix UI React documentation 2025")
→ WebFetch para extrair padrões
→ Cria .claude/skills/radix-ui/SKILL.md
→ Documenta em docs/integrations/
```

---

## 🎯 Comandos Úteis

### Verificar Skills Ativas

```bash
# Listar todas as skills
ls .claude/skills/

# Output esperado:
# breadcrumb-impl/
# component-refactor/
# meta-configuracao-evolucao/
# platform-architecture/
# ux-nomenclature/
```

### Ver Conteúdo de uma Skill

```bash
# Ver skill de nomenclatura
cat .claude/skills/ux-nomenclature/SKILL.md | head -50
```

### Validar Estrutura

```bash
# Validar que todas as skills têm frontmatter correto
for skill in .claude/skills/*/SKILL.md; do
  head -5 "$skill" | grep "name:"
done

# Output esperado: 5 linhas com "name: [skill-name]"
```

---

## 💡 Dicas Pro

1. **Skills ativam automaticamente** - Não precisa invocar
2. **Agents precisam ser solicitados** - Use comandos explícitos
3. **Meta-skill economiza tempo** - Use para novas integrações
4. **CLAUDE.md é referência** - Consulte para detalhes
5. **README completo** - `.claude/README-SKILLS-AGENTS.md`

---

## 🐛 Troubleshooting

### Skill não está ativando

**Problema:** Editei arquivo mas skill não sugeriu nada

**Solução:**
1. Verificar se arquivo corresponde ao contexto da skill
2. Checar frontmatter do SKILL.md (name, description, allowed-tools)
3. Reiniciar sessão Claude Code

### Agent não reconhece comando

**Problema:** Pedi para usar agent mas nada aconteceu

**Solução:**
1. Usar comando explícito: "Usar ux-refactor-agent para..."
2. Mencionar User Story: "Implementar US-061"
3. Verificar que agent está em `.claude/agents/`

### Erro ao criar nova skill

**Problema:** Criei SKILL.md mas não funciona

**Solução:**
1. Validar frontmatter YAML (---\nname: ...\n---)
2. Verificar que pasta tem nome correto
3. Testar em contexto relevante
4. Checar logs do Claude Code

---

## 📚 Próximos Passos

1. ✅ Testar skills existentes (5 minutos)
2. ✅ Experimentar ux-refactor-agent (10 minutos)
3. ✅ Criar primeira skill customizada (30 minutos)
4. ✅ Refatorar código usando component-refactor skill (1 hora)
5. ✅ Integrar nova tecnologia com meta-skill (2 horas)

---

## 🎓 Aprendizado

**Skills** = Conhecimento sempre disponível (automático)
**Agents** = Trabalhadores especializados (manual)
**Meta-Skill** = Fábrica de skills (auto-evolução)

**Resultado:** Sistema que aprende e evolui continuamente! 🚀

---

**📅 Criado:** 2025-11-13
**⏱️ Tempo de Setup:** 5 minutos
**🎯 Dificuldade:** Fácil
**✅ Status:** Pronto para usar!
