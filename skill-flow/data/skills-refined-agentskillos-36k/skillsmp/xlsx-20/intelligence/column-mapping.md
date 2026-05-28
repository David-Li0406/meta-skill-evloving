# Mapeamento Inteligente de Colunas

Após identificar a linha de cabeçalho, o próximo desafio é mapear as colunas da planilha (Source) para os campos do sistema (Target).

## Sistema de Pontuação Multi-Fator

Não use uma decisão binária (match/no-match). Calcule um **Score de Confiança** (0-100%) para cada possível mapeamento baseada em múltiplos fatores.

### Pesos Sugeridos

| Fator                      | Peso | Descrição                                         |
| -------------------------- | ---- | ------------------------------------------------- |
| **Similaridade Semântica** | 40%  | O nome da coluna parece com o campo alvo?         |
| **Padrão de Dados**        | 30%  | Os dados na coluna correspondem ao tipo esperado? |
| **Posição Contextual**     | 15%  | A ordem das colunas faz sentido?                  |
| **Frequência de Uso**      | 15%  | Esse nome de coluna é comum para esse campo?      |

### Fator 1: Similaridade Semântica (0-100)

Compare o nome da coluna normalizado com a lista de palavras-chave do campo.

- Match exato (normalizado): 100 pontos
- Sinônimo conhecido: 90 pontos
- Levenshtein > 0.8: 70-80 pontos
- Contém a palavra (ex: "Telefone Residencial" contém "Telefone"): 60 pontos

### Fator 2: Padrão de Dados (0-100)

Amostre 5 valores não-vazios da coluna.

- Regex exato (ex: CPF válido): 100 pontos
- Formato compatível (ex: é numérico para campo Idade): 50 pontos
- Formato incompatível (ex: texto para campo Numérico): -100 pontos (fator de veto)

### Fator 3: Posição (0-100)

Se "Nome" foi encontrado na Coluna A e "Sobrenome" na Coluna B, a probabilidade da Coluna C ser "Email" aumenta se esse for um padrão comum.

### Fator 4: Frequência (0-100)

Baseado no histórico de importações. Se 90% dos usuários usam "Cel" para "Telefone Celular", esse match ganha pontos extras.

## Decisão e Fallback

### Classificação de Confiança

1.  **Alta (Score > 85)**: Mapeamento Automático. Não precisa perguntar ao usuário.
2.  **Média (Score 60-85)**: Sugestão Fortemente Recomendada. "Achamos que X é Y, confirmar?"
3.  **Ambígua (Scores próximos)**: Se "Tel 1" e "Tel 2" ambos podem ser "Telefone Principal", peça desambiguação clara.
4.  **Baixa (Score < 60)**: Não mapear automaticamente. Sugerir "Ignorar" ou marcar como desconhecido.

## Base de Conhecimento Expandida

Para máxima eficácia, o sistema deve conhecer variações.

### Exemplo: Campo "Telefone"

- **EN**: Phone, Mobile, Cell, Cellphone, Tel
- **PT-BR**: Telefone, Celular, Tel, Fone, Movel, Contato, Wpp, Whats, WhatsApp, Zap
- **Erros Comuns**: Telefome, Celuar, Tlf
- **Abreviações**: Cel, Tel, T.

### Exemplo: Campo "Valor"

- **Keywords**: Preço, Valor, Custo, Total, R$, Amount, Price
- **Variações**: Valor Total, Valor Unit., Custo Final

## Estratégias de Desambiguação

### Colunas Duplicadas

Se a planilha tem "Telefone" e "Celular", e o sistema só tem 1 campo "telefone":

1.  Verifique qual tem mais dados preenchidos (densidade).
2.  Verifique qual tem dados mais recentes (se houver datas).
3.  Combine-os se o sistema permitir múltiplos telefones.
4.  Caso contrário, priorize "Celular" sobre "Telefone" em contextos B2C.

### Colunas Não Mapeadas

Sempre alerte o usuário sobre colunas na planilha que **não** foram mapeadas para nada, para evitar perda de dados acidental.
