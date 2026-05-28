# Data Modeling - Learning Path Patterns

> Guia detalhado para modelagem de dados de Caminhos de Aprendizado

## Schema Completo

### Caminho Proposto (caminhoExemploData.js)

```javascript
const caminhoSchema = {
  // Identificacao unica
  id: string,           // 'backend-developer', 'frontend-developer'
  name: string,         // 'Desenvolvedor Backend'
  icon: string,         // Emoji ou nome de icone
  description: string,  // Descricao curta do caminho
  badge: string | null, // 'exemplo', 'popular', 'novo', null

  // Sequencia de cursos (REFERENCIAS, nao dados duplicados)
  cursos: [
    {
      ordem: number,        // 1, 2, 3... Posicao na sequencia
      areaId: string,       // Referencia a studyAreas.js (key)
      nome: string,         // Display name
      icone: string,        // Emoji do curso
      descricao: string,    // Descricao curta
      modules: number,      // Total de modulos
      hours: number,        // Horas estimadas
      disponivel: boolean,  // true = clicavel, false = "Em breve"
      destaque: string | null // Badge especial ('Padrao de referencia')
    }
  ],

  // Getters computados (calculados automaticamente)
  totalCursos: number,       // cursos.length
  cursosDisponiveis: number, // cursos.filter(c => c.disponivel).length
  totalModules: number,      // sum(cursos[].modules)
  totalHours: number,        // sum(cursos[].hours)
  modulesDisponiveis: number,
  hoursDisponiveis: number
};
```

### Area de Estudo (studyAreas.js)

```javascript
const areaSchema = {
  name: string,              // 'Bash'
  icon: string,              // Emoji
  description: string,       // Descricao
  modules: number,           // Total modulos
  hours: number,             // Horas estimadas
  badge: string | null,      // 'Integrado', 'Novo', null
  hasIntegratedApp: boolean, // Tem LearningSystem dedicado?
  key: string,               // ID unico para navegacao
  flashcards: FlashCard[]    // Dados REAIS de flashcards
};
```

## Relacionamento entre Schemas

```
                    +-------------------+
                    |  caminhosPropostos |
                    |  (dicionario)      |
                    +-------------------+
                            |
                            | has many
                            v
                    +-------------------+
                    |  Caminho          |
                    |  - id             |
                    |  - cursos[]       |
                    +-------------------+
                            |
                            | references (via areaId)
                            v
                    +-------------------+
                    |  studyAreas       |
                    |  - key            |
                    |  - flashcards     |
                    |  - sections       |
                    +-------------------+
```

## Regras de Negocio

### 1. Unicidade de areaId

Cada `areaId` em um caminho DEVE existir em `studyAreas.js`:

```javascript
// VALIDO
{ areaId: 'bash', ... }  // 'bash' existe em studyAreas

// INVALIDO
{ areaId: 'python', ... }  // 'python' NAO existe ainda
```

### 2. Ordem deve ser sequencial

```javascript
// VALIDO
cursos: [
  { ordem: 1, ... },
  { ordem: 2, ... },
  { ordem: 3, ... }
]

// INVALIDO (gaps)
cursos: [
  { ordem: 1, ... },
  { ordem: 5, ... },  // Gap!
  { ordem: 10, ... }
]
```

### 3. Disponibilidade segue sistema integrado

```javascript
// Se hasIntegratedApp: true em studyAreas
// PODE ser disponivel: true no caminho

// Se hasIntegratedApp: false em studyAreas
// DEVE ser disponivel: false no caminho
```

## Exemplos de Queries Comuns

### Buscar caminho por ID

```javascript
const path = caminhosPropostos['backend-developer'];
```

### Listar cursos disponiveis

```javascript
const disponiveis = path.cursos.filter(c => c.disponivel);
```

### Calcular progresso

```javascript
const progresso = {
  total: path.totalCursos,
  disponiveis: path.cursosDisponiveis,
  percentual: (path.cursosDisponiveis / path.totalCursos) * 100
};
```

### Buscar area de estudo pelo curso

```javascript
const curso = path.cursos.find(c => c.areaId === 'bash');
const area = studyAreas.find(a => a.key === curso.areaId);
// area.flashcards, area.sections, etc.
```

---

**Arquivo:** `.claude/skills/learning-path-patterns/auxiliary/data-modeling.md`
**Criado:** 2025-11-22
