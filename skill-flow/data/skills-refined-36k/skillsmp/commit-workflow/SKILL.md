---
name: commit-workflow
description: Fluxo completo de Git: branches, commits, pull requests e code review
triggers: [commit, git, push, conventional, branch, pr, pull request, code review]
---

# Commit Workflow

## Quando Usar

Ativar quando:
- Código está pronto para commit
- Review foi aprovado
- Testes passaram

## Conventional Commits

### Formato
```
<type>(<scope>): <description>

[body opcional]

[footer opcional]
```

### Types
| Type | Uso |
|------|-----|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (não afeta código) |
| `refactor` | Refatoração |
| `test` | Testes |
| `chore` | Manutenção |
| `perf` | Performance |
| `ci` | CI/CD |

### Scope
Área afetada: `auth`, `api`, `ui`, `db`, etc.

### Exemplos
```
feat(auth): add JWT refresh token endpoint
fix(api): handle null response in user service
docs(readme): update installation instructions
refactor(utils): extract date formatting to helper
test(auth): add unit tests for login flow
chore(deps): update dependencies to latest
```

## Workflow Obrigatório

### 1. Verificar Status
```bash
git status
git diff --stat
```

### 2. Mostrar Alterações
```bash
git diff
```

### 3. Sugerir Mensagem
Baseado nas alterações, sugerir mensagem seguindo conventional commits.

### 4. PEDIR CONFIRMAÇÃO
```
Commit sugerido:
feat(auth): implement password reset

Arquivos: 3 modificados, 45+, 12-

**Posso fazer o commit?** [AGUARDAR RESPOSTA]
```

### 5. Executar (só com permissão)
```bash
git add -A
git commit -m "mensagem"
```

### 6. Perguntar sobre Push
```
Commit feito. **Quer fazer push?** [AGUARDAR RESPOSTA]
```

## Regras CRÍTICAS

### NUNCA sem permissão:
- `git commit`
- `git push`
- `git reset --hard`
- `git rebase`
- `git merge`

### SEMPRE fazer:
- Mostrar diff antes
- Pedir confirmação explícita
- Usar conventional commits
- **NUNCA adicionar co-author de IA**

## CHANGELOG Obrigatório

**ANTES de commitar, SEMPRE atualizar o CHANGELOG:**

1. Verificar se `CHANGELOG.md` existe na raiz do projeto
2. Se não existir, criar seguindo o template em `skills/workflow/changelog/SKILL.md`
3. Adicionar todas as mudanças em `[Unreleased]`
4. Categorizar corretamente: Added, Changed, Deprecated, Removed, Fixed, Security
5. **NUNCA** modificar versões já lançadas

Ver `skills/workflow/changelog/SKILL.md` para detalhes completos.

---

---

## Workflow de Branches

### Feature Branches Obrigatório

```bash
# Sempre usar feature branches
git checkout -b feature/nome-da-feature
git checkout -b fix/nome-do-bug
git checkout -b refactor/nome-do-refactor
```

### Estrutura de Branches

```
main                    # produção (protegida)
├── develop            # desenvolvimento (opcional)
├── feature/xxx        # novas features
├── fix/xxx            # correções de bugs
├── refactor/xxx       # refatorações
└── hotfix/xxx         # correções urgentes em produção
```

### Git Flow Simplificado

**Princípios:**
- `main` sempre estável e deployável
- Features desenvolvidas em branches separadas
- Merge apenas via pull request
- Code review obrigatório antes de merge
- **Hotfixes**: podem ser commitados direto em `main` (correções urgentes em produção)

**Fluxo:**
1. Criar branch a partir de `main`
2. Desenvolver feature
3. Commitar frequentemente com mensagens descritivas
4. Criar pull request
5. Code review
6. Merge após aprovação
7. Deletar branch após merge

**Hotfixes (exceção):**
- Correções urgentes em produção
- Podem ser commitados direto em `main`
- Usar tipo `fix:` ou `hotfix:` no commit
- Exemplo: `fix: corrigir erro crítico em produção`

---

## Pull Requests

### Antes de Criar PR

- [ ] Código testado localmente
- [ ] Todos os testes passando
- [ ] Sem conflitos com main
- [ ] Código revisado (self-review)
- [ ] Documentação atualizada se necessário
- [ ] **CHANGELOG.md atualizado**

### Descrição do PR

```markdown
## Descrição
Breve descrição do que foi feito.

## Tipo de mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Refatoração
- [ ] Documentação

## Checklist
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Código segue padrões do projeto
- [ ] Sem breaking changes (ou documentados)
- [ ] CHANGELOG.md atualizado
```

---

## Code Review

### Antes de Aprovar

- [ ] Código segue padrões do projeto
- [ ] Testes adequados
- [ ] Sem código comentado desnecessário
- [ ] Sem secrets hardcoded
- [ ] Performance considerada
- [ ] Segurança considerada
- [ ] CHANGELOG.md atualizado

### Feedback

- Ser construtivo e educacional
- Explicar o porquê das sugestões
- Sugerir alternativas quando possível
- Reconhecer boas práticas

---

## Tags e Releases

### Semantic Versioning

```
v<major>.<minor>.<patch>
```

- **major**: breaking changes
- **minor**: novas features (backward compatible)
- **patch**: bug fixes

### Criar Tag

```bash
git tag -a v1.2.0 -m "Release 1.2.0: Adicionar autenticação JWT"
git push origin v1.2.0
```

**Ver:** `skills/workflow/changelog/SKILL.md` para processo completo de releases.

---

## Regras Gerais

### Nunca Fazer

- ❌ Force push para main
- ❌ Commits diretos em main (sempre via PR, exceto hotfixes)
- ❌ Commits sem mensagem descritiva
- ❌ Commits com código quebrado
- ❌ Commits com secrets
- ❌ Commits sem atualizar CHANGELOG.md

### Sempre Fazer

- ✅ Usar feature branches
- ✅ Commits frequentes e descritivos
- ✅ Revisar código antes de commit
- ✅ Rodar testes antes de commit
- ✅ Atualizar documentação quando necessário
- ✅ **Atualizar CHANGELOG.md antes de commitar**

---

## Boas Práticas Adicionais

### Commits Frequentes

**Fazer commits pequenos e frequentes:**
- Cada commit deve representar uma mudança lógica
- Commits frequentes facilitam rollback
- Commits pequenos facilitam code review

### Antes de Commit

- [ ] Código testado localmente
- [ ] Todos os testes passando
- [ ] Código formatado (black, prettier, etc.)
- [ ] Sem código comentado desnecessário
- [ ] Sem console.log/debugger
- [ ] Sem secrets hardcoded
- [ ] **CHANGELOG.md atualizado**

### Organização de Commits

**Um commit = uma responsabilidade:**
```bash
# ✅ Correto - commits separados
git commit -m "feat: adicionar validação de email"
git commit -m "refactor: mover lógica para controller"
git commit -m "test: adicionar testes para validação"

# ❌ Errado - tudo em um commit
git commit -m "feat: adicionar validação e refatorar controller e testes"
```

---

## Resolução de Problemas

### Conflitos de Merge

```bash
# Atualizar branch local
git pull origin main

# Resolver conflitos manualmente
# Editar arquivos marcados com conflito

# Adicionar arquivos resolvidos
git add .

# Continuar merge
git commit
```

---

## Checklist

- [ ] **CHANGELOG.md atualizado com todas as mudanças em `[Unreleased]`**
- [ ] Review aprovado
- [ ] Testes passando
- [ ] Diff mostrado ao usuário
- [ ] Mensagem segue conventional commits
- [ ] Confirmação obtida
- [ ] Commit executado
- [ ] Push perguntado (se aplicável)
