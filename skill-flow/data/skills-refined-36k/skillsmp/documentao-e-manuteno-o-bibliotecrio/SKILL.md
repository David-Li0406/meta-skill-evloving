---
name: Documentação e Manutenção (O Bibliotecário)
description: Skill focada em manter a documentação (README, guias, comentários) sempre sincronizada com o estado atual do código.
version: 1.0.0
---

# 📚 O Bibliotecário - Guardião da Documentação

Esta skill define os protocolos para garantir que a documentação do projeto `cursor-bio-compulabxsimus` nunca fique obsoleta. Um código sem documentação atualizada é um código morto.

## 🎯 Objetivos
1.  **Sincronia Total**: Garantir que `README.md` reflita exatamente as *features*, *stack* e *instruções* atuais.
2.  **Clareza Didática**: Manter a linguagem acessível, profissional e bem formatada.
3.  **Manutenção Pró-ativa**: Atualizar a documentação IMEDIATAMENTE após mudanças estruturais ou novas funcionalidades.

## 🛠️ Ferramentas da Skill

### `scripts/generate_tree.py`
Script para gerar automaticamente a árvore de arquivos do projeto para inclusão no README.
*Uso:* `python .agent/skills/documentacao-keeper-bibliotecario/scripts/generate_tree.py`

## 📋 Protocolo de Atualização do README

Sempre que houver alterações significativas no código, verifique e atualize as seguintes seções do `README.md`:

### 1. Status e Badges
*   Verifique se as badges (Status, Framework, AI, DB) refletem a realidade.
*   Atualize a versão se aplicável.

### 2. Funcionalidades (Features)
*   **Adicionou uma nova feature?** Adicione um bullet point descrevendo-a na seção correta.
*   **Removeu/Depreciou algo?** Remova ou marque como depreciado.
*   Use emojis para manter o visual consistente (ex: ✅, 🚀, 🛠️).

### 3. Tech Stack
*   Se uma nova biblioteca importante (ex: Supabase, n8n, Pandas) foi adicionada, inclua na tabela de Tech Stack.

### 4. Estrutura de Arquivos
*   **CRÍTICO**: Se criou pastas ou moveu arquivos importantes, rode o script `generate_tree.py` e atualize o bloco de código de estrutura.
*   Mantenha a árvore limpa (exclua `__pycache__`, `.git`, etc.).

### 5. Instalação e Execução
*   Se os comandos para rodar o projeto mudaram (ex: de `streamlit run` para `reflex run`), ISSO É URGENTE. Atualize imediatamente.
*   Verifique requisitos de `.env` ou chaves de API.

## 🧠 Checklist Mental (Quando Ativar esta Skill?)

Pergunte-se sempre após terminar uma *task* de código:
- [ ] "Eu criei um arquivo novo que o usuário precisa saber?"
- [ ] "Eu mudei a forma como o app inicia?"
- [ ] "Eu adicionei uma dependência nova no `requirements.txt`?"
- [ ] "A descrição do projeto no README ainda faz sentido com o que acabei de codar?"

Se a resposta for **SIM** para qualquer uma, execute uma atualização de documentação.

## 📝 Padrão de Commit para Docs
Ao atualizar documentação, use prefixos claros:
- `docs: Atualiza README com novas instruções de setup`
- `docs: Adiciona guia de migração para SQL`
