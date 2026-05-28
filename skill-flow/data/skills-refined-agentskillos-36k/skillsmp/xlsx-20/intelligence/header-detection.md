# Detecção Inteligente de Cabeçalhos em Planilhas

A detecção precisa da linha de cabeçalho é o primeiro passo crítico na importação de dados. Planilhas do mundo real raramente seguem o formato ideal "primeira linha = cabeçalho".

## Estratégias de Detecção

### 1. Análise Semântica

Não dependa apenas de correspondência exata. Use análise semântica para identificar candidatos a cabeçalho.

#### Normalização

Antes de comparar, normalize o texto:

- **Remove Acentos**: `comercial` == `comércial`
- **Lowercase**: `NOME` == `nome`
- **Trim**: `Nome` == `Nome`
- **Caracteres Especiais**: `E-mail` == `Email`

#### Similaridade de Strings

Use algoritmos de distância para tolerar erros de digitação:

- **Levenshtein**: Para erros de digitação (ex: "Telefome" vs "Telefone")
- **Jaro-Winkler**: Melhor para strings curtas e prefixos comuns
- **Threshold**: Recomenda-se aceitar similaridade > 0.85

#### Sinônimos e Variações

Mantenha um dicionário de sinônimos comuns:

- **CPF**: "Documento", "CPF/CNPJ", "Doc", "Id Fiscal"
- **Telefone**: "Celular", "Móvel", "Zap", "WhatsApp", "Phone", "Tel"
- **Email**: "Correio Eletrônico", "E-mail", "Mail"
- **Nome**: "Cliente", "Aluno", "Lead", "Nome Completo"

### 2. Análise de Padrões de Dados

Frequentemente, a linha de cabeçalho é a única linha de _texto_ seguida por linhas de _dados formatados_.

#### Padrões Regex Comuns

Analise as primeiras 5-10 linhas de dados abaixo de cada candidato a cabeçalho:

- **CPF**: `^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$`
- **Email**: `^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$`
- **Telefone BR**: `^(\(?\d{2}\)?\s?)?(9\s?)?\d{4}-?\d{4}$`
- **Data**: `^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$` ou Serial Excel (float > 10000)
- **Monetário**: `^R?\$?\s?\d{1,3}(\.?\d{3})*,\d{2}$`

#### Heurística de Tipo

Se a Linha X contém "Data Nasc" e as linhas X+1, X+2 contêm datas válidas (ou inteiros que parecem datas), a confiança de que X é o cabeçalho aumenta drasticamente.

### 3. Análise Contextual

O contexto da planilha fornece pistas valiosas.

#### Densidade

- Linhas de cabeçalho tendem a ter mais colunas preenchidas do que linhas de metadados (títulos, datas de geração).
- Linhas de cabeçalho raramente têm células mescladas verticais (embora horizontais ocorram).

#### Consistência de Formato

- Cabeçalhos são quase sempre Texto/String.
- Colunas de dados tendem a ter tipos consistentes (apenas números, apenas datas).
- Se uma linha contém números ou datas, provavelmente **não** é o cabeçalho.

#### Posição

- Geralmente está no primeiro terço do arquivo.
- Frequentemente precedida por linhas vazias ou linhas com apenas 1 coluna preenchida (título do relatório).

### Algoritmo de Scoring Sugerido

Para cada linha `L` nas primeiras 20 linhas:

1.  **Score Base**: +10 se for a primeira linha não vazia.
2.  **Densidade**: +1 por coluna não vazia.
3.  **Tipo**: -50 se contiver datas ou floats complexos (provavelmente dados).
4.  **Matches de Palavra-Chave**: +20 por cada match com cabeçalho conhecido (ex: "Nome", "Email").
5.  **Dados Subsequentes**: +30 se a linha abaixo contiver dados que correspondem semanticamente aos tipos esperados (ex: coluna "Email" tem emails abaixo).

A linha com maior score > Threshold é o cabeçalho.
