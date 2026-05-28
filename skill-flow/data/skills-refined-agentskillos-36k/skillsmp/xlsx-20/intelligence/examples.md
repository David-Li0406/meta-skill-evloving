# Exemplos Práticos de Inteligência XLS

Este documento ilustra cenários reais de detecção e mapeamento para guiar a implementação e testes.

## Cenário 1: Planilha com Cabeçalhos de Relatório (Metadados)

Muitas planilhas exportadas de sistemas legado (SAPs, ERPs antigos) contêm cabeçalhos de "impressão".

### Input

```csv
Linha 1: RELATÓRIO DE VENDAS MENSAIS - 2024
Linha 2: Gerado em: 15/10/2024 por Admin
Linha 3: Filtros: Todos | Status: Ativo
Linha 4:
Linha 5: CÓDIGO | CLIENTE        | DATA VENDA | VALOR TOTAL | STATUS
Linha 6: 00152  | PADARIA JOÃO   | 01/10/2024 | 1.500,00    | PAGO
Linha 7: 00153  | MERCADO LIVRE  | 02/10/2024 | 500,00      | PENDENTE
```

### Processo de Detecção

1.  **Linhas 1-3**: Ignoradas.
    - Contêm poucas colunas preenchidas (densidade baixa).
    - Não correspondem a keywords conhecidas.
2.  **Linha 4**: Ignorada (vazia).
3.  **Linha 5**: **DETECTADA COMO CABEÇALHO**.
    - Densidade alta (5 colunas preenchidas).
    - Keywords fortes: "CÓDIGO" (ID), "CLIENTE" (Nome), "DATA VENDA" (Data), "VALOR" (Money).
    - Linha 6 contém dados consistentes com os tipos inferidos (Número, Texto, Data, Money).

---

## Cenário 2: Cabeçalhos Ambíguos e Sinônimos

### Input

```csv
Nome Completo | Zap | End. | Nasc. | Doc.
Maria Silva   | 11999999999 | Rua A | 1990-01-01 | 12345678900
```

### Processo de Mapeamento

| Coluna Input | Análise dos Dados       | Match Semântico                       | Decisão Final | Confiança  |
| ------------ | ----------------------- | ------------------------------------- | ------------- | ---------- |
| **Zap**      | Padrão Celular (11 dig) | Sinônimo gíria de "WhatsApp/Telefone" | **phone**     | Alta (90%) |
| **End.**     | Texto livre             | Abreviação de "Endereço"              | **address**   | Alta (85%) |
| **Nasc.**    | Data ISO                | Abreviação de "Nascimento"            | **birthdate** | Alta (85%) |
| **Doc.**     | CPF Válido (11 dig)     | Abreviação de "Documento"             | **cpf**       | Alta (95%) |

---

## Cenário 3: Colunas "Lixo" ou Desconhecidas

### Input

```csv
ID | Nome | Coluna1 | Check | Obs Interna
1  | Ana  | X       | OK    | Cliente VIP
```

### Processo

1.  **ID** -> `id` (Alta)
2.  **Nome** -> `name` (Alta)
3.  **Coluna1** -> ???
    - Sem match semântico.
    - Dados "X" não definitivos.
    - **Ação**: Marcar como `ignored` ou perguntar ao usuário.
4.  **Check** -> ???
    - Sem match claro com campos do sistema.
    - **Ação**: Marcar como `ignored`.
5.  **Obs Interna** -> `notes`
    - "Obs" match parcial com "Observations/Notes".
    - **Ação**: Sugerir `notes` com confiança Média.

---

## Cenário 4: Datas Ambíguas

### Input

```csv
Data
02/05/2024
```

### Problema

É 2 de Maio (DMY) ou 5 de Fevereiro (MDY)?

### Processo de Inteligência

1.  Observar outras linhas: `02/05/2024`, `15/05/2024`.
2.  `15` não pode ser mês. Logo, o formato **TEM** que ser DMY.
3.  Se todos os valores forem ambíguos (ex: `01/01` até `12/12`), verificar locale do sistema ou perguntar.
4.  **Decisão**: Inferir `DF_DD_MM_YYYY` com base na linha `15/05`.

---

## Exemplo de Código de Detecção (Conceitual)

```typescript
function detectHeader(rows: any[][]): number {
  let bestRowIndex = -1;
  let maxScore = 0;

  rows.slice(0, 20).forEach((row, index) => {
    let score = calculateRowScore(row, rows[index + 1]); // Analisa linha + dados abaixo
    if (score > maxScore) {
      maxScore = score;
      bestRowIndex = index;
    }
  });

  return maxScore > MIN_THRESHOLD ? bestRowIndex : 0; // Fallback para 0
}
```
