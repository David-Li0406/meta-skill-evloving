---
name: Código Limpo e Refinamento (Aspirador)
description: Skill focada em identificar e corrigir dívidas técnicas, inconsistências de design e problemas de performance no ecossistema Biodiagnóstico.
---

# Skill: Código Limpo e Refinamento (Aspirador)

Esta skill define o protocolo "Aspirador", cujo objetivo é purificar o código-fonte, eliminando redundâncias, corrigindo bugs silenciosos e garantindo que cada linha de código seja eficiente e elegante.

## 🧹 Princípios do Aspirador

1. **Modularização Extrema**: Arquivos com mais de 800 linhas (ex: `state.py`) são considerados "caixas pretas" perigosas. Devem ser fatiados em estados menores e especializados (ex: `StateAnalise`, `StateQC`, `StateFaturamento`).
2. **Design System Purista**: Qualquer estilo CSS declarado fora de `styles.py` ou sem o uso de tokens (`Color`, `Design`, `Spacing`) deve ser "aspirado" e substituído pelas constantes oficiais.
3. **Eliminação de Código Morto**: Funções que não são chamadas ou variáveis globais obsoletas devem ser removidas.
4. **UX de Alinhamento**: Tabelas e grids devem seguir o mesmo padrão de respiro e hover em todas as páginas. Se uma página "parece diferente", ela está quebrada.

## 🛠️ Ferramentas de Limpeza (Scripts)
Use esses "agentes de limpeza" para manter a casa em ordem:

1.  **Organizador de Gavetas** (O Organizador):
    - Comando: `py .agent/skills/codigo-limpo-aspirador/scripts/organizador_arquivos.py`
    - Função: Garante que todos os arquivos seguem o padrão `snake_case`.

2.  **Coletor de Lixo** (O Coletor):
    - Comando: `py .agent/skills/codigo-limpo-aspirador/scripts/coletor_lixo.py`
    - Função: Remove código comentado morto e lista TODOs esquecidos.

3.  **Padronizador de Texto** (O Professor):
    - Comando: `py .agent/skills/codigo-limpo-aspirador/scripts/padronizador_texto.py`
    - Função: Cobra Docstrings em todas as funções públicas.

4.  **Bibliotecário** (O Bibliotecário):
    - Comando: `py .agent/skills/codigo-limpo-aspirador/scripts/bibliotecario.py`
    - Função: Verifica se as dependências (pip) estão desatualizadas.

5.  **Scanner de Segurança** (O Segurança):
    - Comando: `py .agent/skills/codigo-limpo-aspirador/scripts/scanner_seguranca.py`
    - Função: Procura por senhas e chaves de API expostas no código.

## 🛠️ O Protocolo de Refinamento (Passo-a-passo)
1. Rodar os scripts acima para diagnóstico.
2. Corrigir os alertas críticos (Segurança > Lixo > Documentação).
3. **Pre-commit**: Antes de cada commit, rodar o `coletor_lixo.py` para garantir que não estamos subindo sujeira.

## 🚨 Checklist do Aspirador (Antes de entregar)
- O código está mais curto do que antes?
- A performance melhorou ou a legibilidade aumentou?
- O `Reflex Technical Guardrails` foi aplicado em 100% dos arquivos tocados?
- Existe algum comentário "TODO" ou código comentado que poderia ser deletado?
