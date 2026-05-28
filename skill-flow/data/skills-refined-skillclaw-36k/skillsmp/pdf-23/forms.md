**CRÍTICO: Você DEVE concluir estas etapas na ordem. Não pule direto para escrever código.**

Se você precisar preencher um formulário PDF, primeiro verifique se o PDF possui campos de formulário preenchíveis. Execute este script do diretório deste arquivo:
`python scripts/check_fillable_fields <file.pdf>`, e dependendo do resultado vá para "Campos preenchíveis" ou "Campos não preenchíveis" e siga essas instruções.

# Campos preenchíveis

Se o PDF tiver campos de formulário preenchíveis:

- Execute este script do diretório deste arquivo: `python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`. Ele criará um arquivo JSON com uma lista de campos neste formato:

```
[
  {
    "field_id": (ID único para o campo),
    "page": (número da página, baseado em 1),
    "rect": ([esquerda, parte inferior, direita, topo] caixa delimitadora em coordenadas PDF, y=0 é a parte inferior da página),
    "type": ("text", "checkbox", "radio_group", ou "choice"),
  },
  // Checkboxes têm propriedades "checked_value" e "unchecked_value":
  {
    "field_id": (ID único para o campo),
    "page": (número da página, baseado em 1),
    "type": "checkbox",
    "checked_value": (Defina o campo com este valor para marcar a caixa de seleção),
    "unchecked_value": (Defina o campo com este valor para desmarcar a caixa de seleção),
  },
  // Grupos de rádio têm uma lista "radio_options" com as escolhas possíveis.
  {
    "field_id": (ID único para o campo),
    "page": (número da página, baseado em 1),
    "type": "radio_group",
    "radio_options": [
      {
        "value": (defina o campo com este valor para selecionar esta opção de rádio),
        "rect": (caixa delimitadora para o botão de rádio para esta opção)
      },
      // Outras opções de rádio
    ]
  },
  // Campos de múltipla escolha têm uma lista "choice_options" com as escolhas possíveis:
  {
    "field_id": (ID único para o campo),
    "page": (número da página, baseado em 1),
    "type": "choice",
    "choice_options": [
      {
        "value": (defina o campo com este valor para selecionar esta opção),
        "text": (texto de exibição da opção)
      },
      // Outras opções de escolha
    ],
  }
]
```

- Converta o PDF para PNGs (uma imagem para cada página) com este script (execute do diretório deste arquivo):
  `python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
  Em seguida, analise as imagens para determinar o objetivo de cada campo de formulário (certifique-se de converter as coordenadas PDF da caixa delimitadora para coordenadas de imagem).
- Crie um arquivo `field_values.json` neste formato com os valores a serem inseridos para cada campo:

```
[
  {
    "field_id": "last_name", // Deve corresponder ao field_id de `extract_form_field_info.py`
    "description": "O sobrenome do usuário",
    "page": 1, // Deve corresponder ao valor "page" em field_info.json
    "value": "Simpson"
  },
  {
    "field_id": "Checkbox12",
    "description": "Caixa de seleção a ser marcada se o usuário tiver 18 anos ou mais",
    "page": 1,
    "value": "/On" // Se for uma caixa de seleção, use seu valor "checked_value" para marcá-lo. Se for um grupo de botões de rádio, use um dos valores "value" em "radio_options".
  },
  // mais campos
]
```

- Execute o script `fill_fillable_fields.py` do diretório deste arquivo para criar um PDF preenchido:
  `python scripts/fill_fillable_fields.py <input pdf> <field_values.json> <output pdf>`
  Este script verificará se os IDs de campo e valores que você forneceu são válidos; se imprimir mensagens de erro, corrija os campos apropriados e tente novamente.

# Campos não preenchíveis

Se o PDF não tiver campos de formulário preenchíveis, você precisará determinar visualmente onde os dados devem ser adicionados e criar anotações de texto. Siga as etapas abaixo _exatamente_. Você DEVE realizar todas essas etapas para garantir que o formulário seja preenchido com precisão. Detalhes para cada etapa estão abaixo.

- Converta o PDF em imagens PNG e determine as caixas delimitadoras dos campos.
- Crie um arquivo JSON com informações de campo e imagens de validação mostrando as caixas delimitadoras.
- Valide as caixas delimitadoras.
- Use as caixas delimitadoras para preencher o formulário.

## Etapa 1: Análise Visual (OBRIGATÓRIO)

- Converta o PDF em imagens PNG. Execute este script do diretório deste arquivo:
  `python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
  O script criará uma imagem PNG para cada página no PDF.
- Examine cuidadosamente cada imagem PNG e identifique todos os campos do formulário e áreas onde o usuário deve inserir dados. Para cada campo do formulário onde o usuário deve inserir texto, determine caixas delimitadoras tanto para o rótulo do campo do formulário quanto para a área onde o usuário deve inserir texto. As caixas delimitadoras do rótulo e da entrada NÃO DEVEM SE INTERCEPTAR; a caixa de entrada de texto deve incluir apenas a área onde os dados devem ser inseridos. Geralmente, essa área ficará imediatamente ao lado, acima ou abaixo de seu rótulo. As caixas delimitadoras de entrada devem ser altas e largas o suficiente para conter seu texto.

Estes são alguns exemplos de estruturas de formulário que você pode ver:

_Rótulo dentro da caixa_

```
┌────────────────────────┐
│ Nome:                  │
└────────────────────────┘
```

A área de entrada deve estar à direita do rótulo "Nome" e se estender até a borda da caixa.

_Rótulo antes da linha_

```
Email: _______________________
```

A área de entrada deve estar acima da linha e incluir toda a sua largura.

_Rótulo sob a linha_

```
_________________________
Nome
```

A área de entrada deve estar acima da linha e incluir toda a largura da linha. Isso é comum para campos de assinatura e data.

_Rótulo acima da linha_

```
Por favor, insira quaisquer solicitações especiais:
________________________________________________
```

A área de entrada deve se estender da parte inferior do rótulo até a linha e deve incluir toda a largura da linha.

_Caixas de seleção_

```
Você é cidadão dos EUA? Sim □  Não □
```

Para caixas de seleção:

- Procure pequenas caixas quadradas (□) - estas são as caixas de seleção reais para segmentar. Elas podem estar à esquerda ou à direita de seus rótulos.
- Distinga entre texto de rótulo ("Sim", "Não") e os quadrados de caixa de seleção clicáveis.
- A caixa delimitadora de entrada deve cobrir APENAS o pequeno quadrado, não o rótulo de texto.

### Etapa 2: Criar fields.json e imagens de validação (OBRIGATÓRIO)

- Crie um arquivo chamado `fields.json` com informações para os campos do formulário e caixas delimitadoras neste formato:

```
{
  "pages": [
    {
      "page_number": 1,
      "image_width": (largura da imagem da primeira página em pixels),
      "image_height": (altura da imagem da primeira página em pixels),
    },
    {
      "page_number": 2,
      "image_width": (largura da imagem da segunda página em pixels),
      "image_height": (altura da imagem da segunda página em pixels),
    }
    // páginas adicionais
  ],
  "form_fields": [
    // Exemplo para um campo de texto.
    {
      "page_number": 1,
      "description": "O sobrenome do usuário deve ser inserido aqui",
      // Caixas delimitadoras são [esquerda, topo, direita, baixo]. As caixas delimitadoras para o rótulo e entrada de texto não devem se sobrepor.
      "field_label": "Sobrenome",
      "label_bounding_box": [30, 125, 95, 142],
      "entry_bounding_box": [100, 125, 280, 142],
      "entry_text": {
        "text": "Johnson", // Este texto será adicionado como uma anotação no local entry_bounding_box
        "font_size": 14, // opcional, padrão é 14
        "font_color": "000000", // opcional, formato RRGGBB, padrão é 000000 (preto)
      }
    },
    // Exemplo para uma caixa de seleção. ALVO O QUADRADO para a caixa delimitadora de entrada, NÃO O TEXTO
    {
      "page_number": 2,
      "description": "Caixa de seleção que deve ser marcada se o usuário tiver mais de 18 anos",
      "entry_bounding_box": [140, 525, 155, 540],  // Pequena caixa sobre o quadrado da caixa de seleção
      "field_label": "Sim",
      "label_bounding_box": [100, 525, 132, 540],  // Caixa contendo o texto "Sim"
      // Use "X" para marcar uma caixa de seleção.
      "entry_text": {
        "text": "X",
      }
    }
    // entradas de campo de formulário adicionais
  ]
}
```

Crie imagens de validação executando este script do diretório deste arquivo para cada página:
`python scripts/create_validation_image.py <page_number> <path_to_fields.json> <input_image_path> <output_image_path>

As imagens de validação terão retângulos vermelhos onde o texto deve ser inserido e retângulos azuis cobrindo o texto do rótulo.

### Etapa 3: Validar Caixas Delimitadoras (OBRIGATÓRIO)

#### Verificação de interseção automatizada

- Verifique se nenhuma das caixas delimitadoras se cruza e se as caixas delimitadoras de entrada são altas o suficiente verificando o arquivo fields.json com o script `check_bounding_boxes.py` (execute do diretório deste arquivo):
  `python scripts/check_bounding_boxes.py <arquivo JSON>`

Se houver erros, reanalise os campos relevantes, ajuste as caixas delimitadoras e itere até que não haja erros restantes. Lembre-se: caixas delimitadoras de rótulo (azuis) devem conter rótulos de texto, caixas de entrada (vermelhas) não devem.

#### Inspeção manual de imagem

**CRÍTICO: Não prossiga sem inspecionar visualmente as imagens de validação**

- Retângulos vermelhos devem cobrir APENAS áreas de entrada
- Retângulos vermelhos NÃO DEVEM conter nenhum texto
- Retângulos azuis devem conter texto de rótulo
- Para caixas de seleção:
  - O retângulo vermelho DEVE estar centralizado no quadrado da caixa de seleção
  - O retângulo azul deve cobrir o rótulo de texto para a caixa de seleção

- Se algum retângulo parecer errado, corrija fields.json, gere as imagens de validação novamente e verifique novamente. Repita este processo até que as caixas delimitadoras estejam totalmente precisas.

### Etapa 4: Adicionar anotações ao PDF

Execute este script do diretório deste arquivo para criar um PDF preenchido usando as informações em fields.json:
`python scripts/fill_pdf_form_with_annotations.py <input_pdf_path> <path_to_fields.json> <output_pdf_path>
