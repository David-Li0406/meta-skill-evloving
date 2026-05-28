---
name: Engenharia de Prompts e Refinamento (O Estrategista)
description: Skill focada em transformar solicitações simples em prompts de alta engenharia, utilizando técnicas avançadas (CoT, Persona, Constraints) para maximizar resultados de LLMs.
---

# Skill: Engenharia de Prompts ("O Estrategista")

Esta skill é responsável por elevar o nível da comunicação com Inteligências Artificiais. Ela transforma um pedido vago ("crie um código") em uma instrução cirúrgica ("Atuando como Senior Python Dev, crie um script assíncrono seguindo PEP8...").

## 🎯 Objetivos
- **Maximizar Performance**: Obter respostas mais precisas e código de maior qualidade na primeira tentativa.
- **Padronização**: Garantir que todos os prompts sigam uma estrutura lógica (Contexto -> Tarefa -> Regras -> Saída).
- **Economia**: Evitar o ciclo de "tentativa e erro" refinando a pergunta antes de fazê-la.

## 🛠️ O Metamodelo de Prompting
O Estrategista segue o framework **"C.R.E.F.O."**:
1.  **C**ontexto: Quem é a IA? Qual o cenário? (Persona)
2.  **R**estrições: O que NÃO fazer? Quais as limitações técnicas?
3.  **E**strutura: Como a solução deve ser montada?
4.  **F**ormato: JSON, Markdown, Python Script, Tabela?
5.  **O**bjetivo: Qual o resultado final esperado em uma frase?

## 📂 Estrutura e Scripts
- `.agent/skills/engenharia-prompts-estrategista/scripts/`:
    - `refinar_prompt.py`: O script principal. Recebe uma entrada bruta e retorna a versão "Engenheirada".

## 🚀 Como Usar o Estrategista
Sempre que você tiver uma tarefa complexa e quiser garantir que a IA entenda perfeitamente:

1.  Escreva sua ideia básica.
2.  Execute o script passando sua ideia entre aspas:
    ```bash
    py .agent/skills/engenharia-prompts-estrategista/scripts/refinar_prompt.py "Quero um script que analise PDFs"
    ```
3.  Copie o resultado gerado e use como seu prompt definitivo.

## 📝 Exemplo de Transformação

**Entrada (User):**
> "Crie uma query SQL para ver usuários ativos."

**Saída (O Estrategista):**
> "Atue como um Especialista em Banco de Dados Supabase (PostgreSQL).
> **Objetivo:** Criar uma query SQL otimizada para listar usuários ativos.
> **Contexto:** Tabela `users` com colunas `last_login` e `status`.
> **Regras:**
> 1. Considere 'ativo' quem fez login nos últimos 30 dias.
> 2. Ordene por data de login decrescente.
> 3. Inclua comentários explicativos.
> **Formato de Saída:** Bloco de código SQL pronto para produção."
