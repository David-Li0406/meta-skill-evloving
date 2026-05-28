# Guia: Adicionando Novos Caminhos de Aprendizado

> Passo a passo para criar novos Learning Paths no Plataforma B2B de treinamento técnico corporativo

## Checklist Rapido

- [ ] Definir objetivo e publico-alvo do caminho
- [ ] Listar cursos na ordem ideal de aprendizado
- [ ] Verificar quais cursos ja existem em studyAreas.js
- [ ] Criar areas de estudo faltantes (se necessario)
- [ ] Adicionar caminho em caminhoExemploData.js
- [ ] Testar navegacao no Hub
- [ ] Validar com MCP Chrome DevTools

## Passo 1: Planejamento

### Definir o Caminho

```markdown
Nome: Desenvolvedor Frontend
ID: frontend-developer
Objetivo: Capacitar para desenvolvimento web moderno
Publico: Desenvolvedores iniciantes a intermediarios

Cursos (em ordem):
1. HTML & CSS (fundamentos)
2. JavaScript (programacao)
3. React (framework)
4. TypeScript (tipagem)
5. VSCode & Ferramentas (produtividade)
```

### Verificar Pre-requisitos

```bash
# Listar areas existentes
grep -o '"key": "[^"]*"' src/data/studyAreas.js

# Resultado esperado:
# "key": "bash"
# "key": "c"
# "key": "rust"
# "key": "vscode"
# "key": "claude-code"
```

## Passo 2: Criar Areas Faltantes (se necessario)

Se `html-css`, `javascript`, `react`, `typescript` nao existem:

### Opcao A: Area Placeholder (sem sistema integrado)

```javascript
// studyAreas.js - Adicionar ao array
{
  name: "HTML & CSS",
  icon: "html",
  description: "Fundamentos da web: estrutura e estilo",
  modules: 10,
  hours: 20,
  badge: null,              // Sem badge (nao integrado)
  hasIntegratedApp: false,  // NAO tem LearningSystem
  key: "html-css",
  flashcards: []            // Vazio por enquanto
}
```

### Opcao B: Area Completa (com sistema integrado)

Requer criar:
- `src/components/HtmlCssLearningSystem.jsx`
- `src/data/htmlCssLearningData.js`
- `src/components/HtmlCssNotesView.jsx`

## Passo 3: Adicionar Caminho

```javascript
// caminhoExemploData.js

export const caminhoFrontend = {
  id: 'frontend-developer',
  name: 'Desenvolvedor Frontend',
  icon: 'frontend',
  description: 'Domine as tecnologias do frontend moderno',
  badge: 'novo',

  cursos: [
    {
      ordem: 1,
      areaId: 'html-css',
      nome: 'HTML & CSS',
      icone: 'html',
      descricao: 'Estrutura e estilo para paginas web',
      modules: 10,
      hours: 20,
      disponivel: false,    // Ainda nao tem LearningSystem
      destaque: null
    },
    {
      ordem: 2,
      areaId: 'javascript',
      nome: 'JavaScript',
      icone: 'js',
      descricao: 'Programacao para web interativa',
      modules: 15,
      hours: 30,
      disponivel: false,
      destaque: null
    },
    {
      ordem: 3,
      areaId: 'react',
      nome: 'React',
      icone: 'react',
      descricao: 'Framework para interfaces modernas',
      modules: 20,
      hours: 40,
      disponivel: false,
      destaque: null
    },
    {
      ordem: 4,
      areaId: 'typescript',
      nome: 'TypeScript',
      icone: 'ts',
      descricao: 'Tipagem estatica para JavaScript',
      modules: 12,
      hours: 24,
      disponivel: false,
      destaque: null
    },
    {
      ordem: 5,
      areaId: 'vscode',
      nome: 'VSCode & Ferramentas',
      icone: 'vscode',
      descricao: 'Produtividade no desenvolvimento',
      modules: 8,
      hours: 16,
      disponivel: true,     // JA tem LearningSystem!
      destaque: 'Disponivel agora'
    }
  ],

  get totalCursos() { return this.cursos.length; },
  get cursosDisponiveis() { return this.cursos.filter(c => c.disponivel).length; },
  get totalModules() { return this.cursos.reduce((sum, c) => sum + c.modules, 0); },
  get totalHours() { return this.cursos.reduce((sum, c) => sum + c.hours, 0); },
  get modulesDisponiveis() {
    return this.cursos.filter(c => c.disponivel).reduce((sum, c) => sum + c.modules, 0);
  },
  get hoursDisponiveis() {
    return this.cursos.filter(c => c.disponivel).reduce((sum, c) => sum + c.hours, 0);
  }
};

// IMPORTANTE: Adicionar ao dicionario
export const caminhosPropostos = {
  'backend-developer': caminhoExemplo,
  'frontend-developer': caminhoFrontend   // <-- NOVO
};
```

## Passo 4: Testar Navegacao

```bash
# Iniciar servidor
npm run dev

# No browser:
# 1. http://localhost:3000/
# 2. Verificar se card do novo caminho aparece
# 3. Clicar no caminho
# 4. Verificar lista de cursos
# 5. Clicar em curso disponivel (VSCode)
# 6. Verificar navegacao para /curso/vscode
```

## Passo 5: Validar com MCP

```javascript
// Usar MCP Chrome DevTools
mcp__chrome-devtools__navigate_page({ url: "http://localhost:3000" });
mcp__chrome-devtools__take_snapshot();

// Verificar se caminho aparece
mcp__chrome-devtools__click({ uid: "card-frontend-developer" });
mcp__chrome-devtools__take_snapshot();

// Verificar lista de cursos
// Verificar badges de disponibilidade
```

## Erros Comuns

### 1. Caminho nao aparece no Hub

**Causa:** Nao adicionou ao dicionario `caminhosPropostos`

**Solucao:**
```javascript
export const caminhosPropostos = {
  'backend-developer': caminhoExemplo,
  'frontend-developer': caminhoFrontend  // Adicionar aqui!
};
```

### 2. Curso clicavel nao navega

**Causa:** `disponivel: true` mas `hasIntegratedApp: false` na area

**Solucao:** Criar LearningSystem ou marcar `disponivel: false`

### 3. Estatisticas incorretas

**Causa:** Getters nao definidos no caminho

**Solucao:** Adicionar todos os getters (totalCursos, cursosDisponiveis, etc.)

---

**Arquivo:** `.claude/skills/learning-path-patterns/auxiliary/adding-new-paths.md`
**Criado:** 2025-11-22
