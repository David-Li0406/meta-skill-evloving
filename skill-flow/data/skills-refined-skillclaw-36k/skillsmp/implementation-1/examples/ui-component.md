# Exemplo: Implementação de Componente de UI

**Solicitação do Usuário**: "Implemente o novo componente de busca a partir da spec de design"

## Fluxo

### 1. Encontrar a Spec
```
Glob
pattern: "**/*search*spec*.md"

Encontrado: "docs/specs/global-search-redesign.md"
```

### 2. Ler e Analisar a Spec
```
Read
file_path: "docs/specs/global-search-redesign.md"
```

**Requisitos**:
- Busca instantânea com chamadas de API com debounce
- Navegação por teclado (setas ↑↓, Enter, Esc)
- Histórico de buscas recentes
- Categorias de resultado (páginas, pessoas, arquivos)
- Responsivo para mobile
- Acessibilidade (labels ARIA, leitor de tela)

### 3. Criar Plano de Implementação
```
Write
file_path: "docs/planos/global-search-component.md"
content: "[Plano com fases]"
```

**Fases do plano**:
- Fase 1: Estrutura base do componente
- Fase 2: Integração com API e debounce
- Fase 3: Navegação por teclado
- Fase 4: Buscas recentes
- Fase 5: Polimento e acessibilidade

### 4. Criar Tarefas
```
TodoWrite
todos: [
  {
    "content": "Criar componente SearchInput",
    "activeForm": "Criando componente SearchInput",
    "status": "pending"
  },
  {
    "content": "Implementar hook useDebounce",
    "activeForm": "Implementando hook useDebounce",
    "status": "pending"
  },
  {
    "content": "Adicionar navegação por teclado",
    "activeForm": "Adicionando navegação por teclado",
    "status": "pending"
  },
  {
    "content": "LocalStorage para buscas recentes",
    "activeForm": "Implementando LocalStorage para buscas recentes",
    "status": "pending"
  },
  {
    "content": "UI de categorização de resultados",
    "activeForm": "Criando UI de categorização de resultados",
    "status": "pending"
  },
  {
    "content": "Auditoria de acessibilidade",
    "activeForm": "Executando auditoria de acessibilidade",
    "status": "pending"
  },
  {
    "content": "Estilos responsivos para mobile",
    "activeForm": "Criando estilos responsivos para mobile",
    "status": "pending"
  }
]
```

### 5. Implementar e Acompanhar

Conforme cada tarefa é concluída, atualizar o status no TodoWrite.

## Principais Entregas

**Plano de Implementação** (docs/planos/global-search-component.md)
**7 Tarefas do Componente** (no TodoWrite)
**Atualizações de Progresso** (via TodoWrite)

## Fatores de Sucesso
- Quebra clara do componente
- Separação de responsabilidades (lógica, UI, acessibilidade)
- Cada tarefa tem escopo bem definido
- Spec de design referenciada continuamente
- Acessibilidade incluída desde o início, não como afterthought
- Progresso acompanhado via TodoWrite
