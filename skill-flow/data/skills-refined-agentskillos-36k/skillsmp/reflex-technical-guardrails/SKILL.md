---
name: Reflex Technical Guardrails
description: Regras técnicas, correções de sintaxe e padrões de compilação para o framework Reflex (Radix Themes).
---

# Skill: Reflex Technical Guardrails

Esta skill serve como um "Linter" de conhecimento para evitar erros comuns de compilação e tipagem no framework Reflex, especialmente ao usar Radix Themes.

## 🛑 Regras de Ouro (Evite erros de compilação)

### 1. Integridade de Estado (State Integrity) - **CRÍTICO**
A causa #1 de falhas é chamar variáveis ou métodos na UI (`State.minha_var`) que não existem ou foram renomeados no `state.py`.
- **Regra**: Antes de adicionar qualquer `State.xyz` na UI, vá ao `state.py` e defina `xyz`.
- **Validação**: Execute o script de integridade (`scripts/check_integrity.py`) para varrer o projeto em busca de chamadas órfãs.
- **HMR Optimization**: Evite definir variáveis pesadas no `State` se elas não precisarem ser acessadas pela UI. Use `computed_vars` para transformações e mantenha o estado "magro" para evitar lentidão no hot-reload.

### 2. Acesso em Loops (Listas vs Dicionários)
Ao iterar sobre listas com `rx.foreach`:
- Se a lista contém **Dicionários** (`List[Dict]`), use `item["chave"]`.
- Se a lista contém **Objetos Pydantic/SQLModel** (`List[Result]`), use `item.chave`.
- **Erro comum**: `TypeError: 'ObjectItemOperation' not subscriptable`. Isso acontece ao tentar `item["chave"]` em um objeto.

### 3. Componentes Customizados (`ui.py`)
Nunca assuma que um componente existe.
- Ao usar `ui.novo_componente`, verifique **obrigatoriamente** se ele está definido em `biodiagnostico_app/components/ui.py`.
- Se não estiver, crie-o primeiro ou use um componente nativo `rx.*`.
- **Component Wrapping**: Se precisar de uma prop Radix não disponível no Reflex, use `rx.Component.create` ou passe via dicionário `custom_attrs`.

### 4. Ícones (Lucide)
Padrão atual do Reflex para ícones Lucide:
- Use **underscores `_`** ou **hífens `-`** dependendo da versão, mas atente para renomeações:
  - `alert_circle` -> `circle_alert`
  - `check_circle` -> `circle_check`
  - `x_circle` -> `circle_x`
  - `alert_triangle` -> `triangle_alert`
  - Sempre verifique o log de erro se o ícone não aparecer; o Reflex sugere o nome correto.

### 5. Spacing e Unidades CSS
A prop `spacing` em componentes como `rx.vstack`, `rx.hstack` e `rx.grid` **só aceita valores de "0" a "9"** (tokens Radix).
- **PROIBIDO**: `rx.vstack(spacing=Spacing.MD)` ou `rx.vstack(spacing="1rem")`.
- **CORRETO**: `rx.vstack(style={"gap": Spacing.MD})` - Use sempre o dicionário `style` para unidades customizadas.

### 6. Propriedades Responsivas (Breakpoints)
Propriedades que mudam conforme o tamanho da tela (como `columns` no Grid ou `display`) não aceitam mais listas `["1", "3"]`.
- **PROIBIDO**: `rx.grid(columns=["1", "3"])`.
- **CORRETO**: `rx.grid(columns={"initial": "1", "md": "3"})`.

### 7. Importação Mandatária
Todo arquivo de página ou componente Reflex **deve** conter os seguintes imports básicos:
- `import reflex as rx`
- `from ..styles import ...` (ou caminho equivalente para acessar o design system, incluindo `Color`).

### 8. Logs de Erro como Guia
Se o servidor Reflex falhar, o log é a fonte da verdade:
- `AttributeError: No reflex attribute X` -> O componente X não existe ou mudou de nome.
- `AttributeError: type object 'State' has no attribute 'X'` -> Você esqueceu de definir a variável no State.

### 9. Tipagem de Variáveis de Estado (Type Mismatch)
O Reflex é estrito com tipos em condicionais (`rx.cond`).
- **Erro**: `TypeError: Unsupported Operand type(s) for >=: StringCastedVar, int`.
- **Causa**: Você definiu uma variável como `str` no State (ex: `value: str = "+2%"`), mas tentou comparar com número na UI (`value >= 0`).
- **Correção**: Armazene dados brutos como `int/float` (`value: float = 2.0`) e formate apenas na exibição (`f"{value}%"`), ou crie uma computed var formatada (`formatted_value`).

## 🔍 Processo de Validação
Antes de finalizar qualquer tarefa, eu (Antigravity) executarei este checklist:
1. **Verificação de Integridade**: Use `python .agent/skills/reflex-technical-guardrails/scripts/check_integrity.py`.
2. **Pré-Check Completo**: Execute `python .agent/skills/reflex-technical-guardrails/scripts/pre_push_check.py` para validar tudo de uma vez.
3. **Teste de Execução**: Sempre execute `reflex run` no diretório do app. Se houver erro, corrija antes de entregar.
4. Existem grids com colunas definidas em lista? (Corrigir para dict).
5. Os nomes dos ícones seguem o padrão sugerido pelo compilador nos logs?
6. Variáveis usadas em `rx.cond(var > X)` são numéricas no State?

## 🛠️ Scripts Úteis
- `scripts/check_integrity.py`: Script CRÍTICO para validar se todas as chamadas `State.*` na UI possuem definição correspondente no `state.py`.
- `scripts/pre_push_check.py`: Wrapper que executa integridade, validação e testes unitários. Use antes de subir código.

