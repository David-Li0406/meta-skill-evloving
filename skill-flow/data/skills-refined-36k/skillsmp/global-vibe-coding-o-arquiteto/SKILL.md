---
name: Global Vibe Coding (O Arquiteto)
description: A 'Constituição' do desenvolvimento. Define os 6 princípios fundamentais (PLANNING, DRY, KISS, YAGNI, Features, SoC) para garantir código limpo, escalável e com 'Vibe'.
---

# Skill: Global Vibe Coding (O Arquiteto)

Esta skill é a autoridade máxima em arquitetura e estilo de código no projeto. Ela define **COMO** construímos, não apenas **O QUE** construímos.

## 🏛️ Os 6 Pilares (A Constituição)

### 1. PLANNING (O Mapa)
**"Planejar antes de construir."**
- **Regra**: Nenhum bloco de código complexo é gerado sem um plano ou tarefa clara.
- **Ação**:
    - Antes de começar uma feature nova: Atualize `task.md`.
    - Tarefas médias/grandes (>3 arquivos): Crie `implementation_plan.md`.
    - **Nunca** comece a codar cegamente baseado em um prompt vago. Pergunte, planeje, depois execute.

### 2. DRY (O Eco)
**"Don't Repeat Yourself (Não se Repita)."**
- **Regra**: Se você copiou e colou a lógica 3 vezes, refatore agora.
- **Ação**:
    - Texto/Formatação repetida -> `utils/`.
    - UI repetida -> Componente em `components/`.
    - Props de estilo repetidos -> `styles.py` ou wrapper component.
- **Exemplo**: Não repita `style={"margin_top": "10px"}` 20 vezes. Crie um `Spacer(sm)`.

### 3. KISS (A Navalha)
**"Keep It Simple, Stupid (Mantenha Simples, Estúpido)."**
- **Regra**: A complexidade é um bug. A solução mais óbvia (legível) ganha.
- **Ação**:
    - Prefira funções puras e nomes de variáveis descritivos.
    - Evite abstrações prematuras (Factories, AbstractBaseClasses) a menos que estritamente necessário.
    - Se um júnior não consegue ler, reescreva.

### 4. YAGNI (O Lixo)
**"You Aren't Gonna Need It (Você Não Vai Precisar Disso)."**
- **Regra**: Codifique para o HOJE, não para um futuro hipotético.
- **Ação**:
    - **Delete** código comentado imediatamente. Não deixe cemitérios de código.
    - Não adicione parâmetros em funções "para uso futuro".
    - Remova imports e dependências não utilizadas.

### 5. Feature Based Folder (A Cidade)
**"Organize por Valor de Negócio, não por Stack Tecnológico."**
- **Regra**: Arquivos que mudam juntos, ficam juntos.
- **Estrutura Alvo**:
  ```text
  /features
    /auth
      login_screen.py
      auth_state.py
    /qc
      dashboard_screen.py
      westgard_logic.py
  ```
- **Transição**: Para novas features, use esta estrutura. Para código legado, refatore gradualmente.

### 6. Separation of Concerns (Os Muros)
**"Dividir e Conquistar."**
- **Regra**: UI não sabe de Banco de Dados. Banco de Dados não sabe de HTML.
- **Divisão Sagrada (Reflex)**:
    - **UI (View)**: Apenas `rx.Component`. Recebe dados, mostra dados. **Zero SQL**.
    - **State (Controller)**: `rx.State`. Recebe eventos da UI, chama Services, atualiza var.
    - **Service (Model/Logic)**: Pure Python. Faz queries SQL, chama APIs externas.

## 🛡️ Checklist de Qualidade (O Vibe Check)
Antes de dar um `task_boundary` como concluído, pergunte-se:
1. [ ] Eu planejei isso antes de escrever?
2. [ ] Copiei código? Se sim, abstraí?
3. [ ] Está simples o suficiente?
4. [ ] Tem código morto ou inútil? (YAGNI)
5. [ ] A lógica de banco de dados vazou para a UI? (SoC)
