# Tutorial da Biblioteca DOCX

Gere arquivos .docx com JavaScript/TypeScript.

**Importante: Leia este documento inteiro antes de começar.** Regras críticas de formatação e armadilhas comuns são cobertas por toda parte - pular seções pode resultar em arquivos corrompidos ou problemas de renderização.

## Configuração

Assume que o docx já está instalado globalmente
Se não instalado: `npm install -g docx`

```javascript
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  ImageRun,
  Media,
  Header,
  Footer,
  AlignmentType,
  PageOrientation,
  LevelFormat,
  ExternalHyperlink,
  InternalHyperlink,
  TableOfContents,
  HeadingLevel,
  BorderStyle,
  WidthType,
  TabStopType,
  TabStopPosition,
  UnderlineType,
  ShadingType,
  VerticalAlign,
  SymbolRun,
  PageNumber,
  FootnoteReferenceRun,
  Footnote,
  PageBreak,
} = require("docx");

// Criar e Salvar
const doc = new Document({
  sections: [
    {
      children: [
        /* conteúdo */
      ],
    },
  ],
});
Packer.toBuffer(doc).then((buffer) => fs.writeFileSync("doc.docx", buffer)); // Node.js
Packer.toBlob(doc).then((blob) => {
  /* lógica de download */
}); // Browser
```

## Texto e Formatação

```javascript
// IMPORTANTE: Nunca use \n para quebras de linha - sempre use elementos Paragraph separados
// ❌ ERRADO: new TextRun("Linha 1\nLinha 2")
// ✅ CORRETO: new Paragraph({ children: [new TextRun("Linha 1")] }), new Paragraph({ children: [new TextRun("Linha 2")] })

// Texto básico com todas as opções de formatação
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 200 },
  indent: { left: 720, right: 720 },
  children: [
    new TextRun({ text: "Negrito", bold: true }),
    new TextRun({ text: "Itálico", italics: true }),
    new TextRun({
      text: "Sublinhado",
      underline: { type: UnderlineType.DOUBLE, color: "FF0000" },
    }),
    new TextRun({ text: "Colorido", color: "FF0000", size: 28, font: "Arial" }), // Padrão Arial
    new TextRun({ text: "Realçado", highlight: "yellow" }),
    new TextRun({ text: "Tachado", strike: true }),
    new TextRun({ text: "x2", superScript: true }),
    new TextRun({ text: "H2O", subScript: true }),
    new TextRun({ text: "CAIXA ALTA", smallCaps: true }),
    new SymbolRun({ char: "2022", font: "Symbol" }), // Marcador •
    new SymbolRun({ char: "00A9", font: "Arial" }), // Copyright © - Arial para símbolos
  ],
});
```

## Estilos e Formatação Profissional

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt padrão
    paragraphStyles: [
      // Estilo de título do documento - substituir estilo de título embutido
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: {
          spacing: { before: 240, after: 120 },
          alignment: AlignmentType.CENTER,
        },
      },
      // IMPORTANTE: Substituir estilos de cabeçalho embutidos usando seus IDs exatos
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" }, // 16pt
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 },
      }, // Necessário para TOC
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" }, // 14pt
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 },
      },
      // Estilos personalizados usam seus próprios IDs
      {
        id: "myStyle",
        name: "My Style",
        basedOn: "Normal",
        run: { size: 28, bold: true, color: "000000" },
        paragraph: { spacing: { after: 120 }, alignment: AlignmentType.CENTER },
      },
    ],
    characterStyles: [
      {
        id: "myCharStyle",
        name: "My Char Style",
        run: {
          color: "FF0000",
          bold: true,
          underline: { type: UnderlineType.SINGLE },
        },
      },
    ],
  },
  sections: [
    {
      properties: {
        page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
      },
      children: [
        new Paragraph({
          heading: HeadingLevel.TITLE,
          children: [new TextRun("Título do Documento")],
        }), // Usa estilo Title substituído
        new Paragraph({
          heading: HeadingLevel.HEADING_1,
          children: [new TextRun("Cabeçalho 1")],
        }), // Usa estilo Heading1 substituído
        new Paragraph({
          style: "myStyle",
          children: [new TextRun("Estilo de parágrafo personalizado")],
        }),
        new Paragraph({
          children: [
            new TextRun("Normal com "),
            new TextRun({
              text: "estilo de caractere personalizado",
              style: "myCharStyle",
            }),
          ],
        }),
      ],
    },
  ],
});
```

**Combinações de Fontes Profissionais:**

- **Arial (Cabeçalhos) + Arial (Corpo)** - Mais universalmente suportado, limpo e profissional
- **Times New Roman (Cabeçalhos) + Arial (Corpo)** - Cabeçalhos serif clássicos com corpo sans-serif moderno
- **Georgia (Cabeçalhos) + Verdana (Corpo)** - Otimizado para leitura em tela, contraste elegante

**Princípios Chave de Estilo:**

- **Substituir estilos embutidos**: Use IDs exatos como "Heading1", "Heading2", "Heading3" para substituir os estilos de cabeçalho embutidos do Word
- **Constantes HeadingLevel**: `HeadingLevel.HEADING_1` usa estilo "Heading1", `HeadingLevel.HEADING_2` usa estilo "Heading2", etc.
- **Incluir outlineLevel**: Defina `outlineLevel: 0` para H1, `outlineLevel: 1` para H2, etc. para garantir que o TOC funcione corretamente
- **Use estilos personalizados** em vez de formatação inline para consistência
- **Defina uma fonte padrão** usando `styles.default.document.run.font` - Arial é universalmente suportada
- **Estabeleça hierarquia visual** com diferentes tamanhos de fonte (títulos > cabeçalhos > corpo)
- **Adicione espaçamento adequado** com espaçamento de parágrafo `before` e `after`
- **Use cores com moderação**: Padrão para preto (000000) e tons de cinza para títulos e cabeçalhos (cabeçalho 1, cabeçalho 2, etc.)
- **Defina margens consistentes** (1440 = 1 polegada é o padrão)

## Listas (SEMPRE USE LISTAS ADEQUADAS - NUNCA USE MARCADORES UNICODE)

```javascript
// Marcadores - SEMPRE use a configuração de numeração, NÃO símbolos unicode
// CRÍTICO: Use a constante LevelFormat.BULLET, NÃO a string "bullet"
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
        ],
      },
      {
        reference: "first-numbered-list",
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
        ],
      },
      {
        reference: "second-numbered-list", // Referência diferente = reinicia em 1
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
        ],
      },
    ],
  },
  sections: [
    {
      children: [
        // Itens da lista com marcadores
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("Primeiro ponto")],
        }),
        new Paragraph({
          numbering: { reference: "bullet-list", level: 0 },
          children: [new TextRun("Segundo ponto")],
        }),
        // Itens da lista numerada
        new Paragraph({
          numbering: { reference: "first-numbered-list", level: 0 },
          children: [new TextRun("Primeiro item numerado")],
        }),
        new Paragraph({
          numbering: { reference: "first-numbered-list", level: 0 },
          children: [new TextRun("Segundo item numerado")],
        }),
        // ⚠️ CRÍTICO: Referência diferente = lista INDEPENDENTE que reinicia em 1
        // Mesma referência = CONTINUA numeração anterior
        new Paragraph({
          numbering: { reference: "second-numbered-list", level: 0 },
          children: [
            new TextRun("Começa em 1 novamente (porque referência diferente)"),
          ],
        }),
      ],
    },
  ],
});

// ⚠️ REGRA DE NUMERAÇÃO CRÍTICA: Cada referência cria uma lista numerada INDEPENDENTE
// - Mesma referência = continua a numeração (1, 2, 3... depois 4, 5, 6...)
// - Referência diferente = reinicia em 1 (1, 2, 3... depois 1, 2, 3...)
// Use nomes de referência exclusivos para cada seção numerada separada!

// ⚠️ CRÍTICO: NUNCA use marcadores unicode - eles criam listas falsas que não funcionam corretamente
// new TextRun("• Item")           // ERRADO
// new SymbolRun({ char: "2022" }) // ERRADO
// ✅ SEMPRE use configuração de numeração com LevelFormat.BULLET para listas reais do Word
```

## Tabelas

```javascript
// Tabela completa com margens, bordas, cabeçalhos e marcadores
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = {
  top: tableBorder,
  bottom: tableBorder,
  left: tableBorder,
  right: tableBorder,
};

new Table({
  columnWidths: [4680, 4680], // ⚠️ CRÍTICO: Defina larguras de coluna no nível da tabela - valores em DXA (vigdésimos de um ponto)
  margins: { top: 100, bottom: 100, left: 180, right: 180 }, // Definir uma vez para todas as células
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // TAMBÉM defina largura em cada célula
          // ⚠️ CRÍTICO: Sempre use ShadingType.CLEAR para evitar fundos pretos no Word.
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "Cabeçalho", bold: true, size: 22 }),
              ],
            }),
          ],
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // TAMBÉM defina largura em cada célula
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: "Pontos", bold: true, size: 22 })],
            }),
          ],
        }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // TAMBÉM defina largura em cada célula
          children: [
            new Paragraph({ children: [new TextRun("Dados regulares")] }),
          ],
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // TAMBÉM defina largura em cada célula
          children: [
            new Paragraph({
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("Primeiro ponto")],
            }),
            new Paragraph({
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("Segundo ponto")],
            }),
          ],
        }),
      ],
    }),
  ],
});
```

**IMPORTANTE: Largura e Bordas da Tabela**

- Use AMBOS array `columnWidths: [width1, width2, ...]` E `width: { size: X, type: WidthType.DXA }` em cada célula
- Valores em DXA (vigdésimos de um ponto): 1440 = 1 polegada, Letra largura utilizável = 9360 DXA (com margens de 1")
- Aplique bordas a elementos `TableCell` individuais, NÃO à `Table` em si

**Larguras de Coluna Pré-computadas (Tamanho carta com margens de 1" = 9360 DXA total):**

- **2 colunas:** `columnWidths: [4680, 4680]` (largura igual)
- **3 colunas:** `columnWidths: [3120, 3120, 3120]` (largura igual)

## Links e Navegação

```javascript
// TOC (requer cabeçalhos) - CRÍTICO: Use HeadingLevel apenas, NÃO estilos personalizados
// ❌ ERRADO: new Paragraph({ heading: HeadingLevel.HEADING_1, style: "customHeader", children: [new TextRun("Title")] })
// ✅ CORRETO: new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] })
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }),

// Link externo
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Google", style: "Hyperlink" })],
    link: "https://www.google.com"
  })]
}),

// Link interno & marcador
new Paragraph({
  children: [new InternalHyperlink({
    children: [new TextRun({ text: "Ir para Seção", style: "Hyperlink" })],
    anchor: "section1"
  })]
}),
new Paragraph({
  children: [new TextRun("Conteúdo da Seção")],
  bookmark: { id: "section1", name: "section1" }
}),
```

## Imagens e Mídia

```javascript
// Imagem básica com dimensionamento e posicionamento
// CRÍTICO: Sempre especifique o parâmetro 'type' - é OBRIGATÓRIO para ImageRun
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [
    new ImageRun({
      type: "png", // NOVO REQUISITO: Deve especificar o tipo de imagem (png, jpg, jpeg, gif, bmp, svg)
      data: fs.readFileSync("image.png"),
      transformation: { width: 200, height: 150, rotation: 0 }, // rotação em graus
      altText: {
        title: "Logo",
        description: "Logotipo da empresa",
        name: "Nome",
      }, // IMPORTANTE: Todos os três campos são obrigatórios
    }),
  ],
});
```

## Quebras de Página

```javascript
// Quebra de página manual
(new Paragraph({ children: [new PageBreak()] }),
  // Quebra de página antes do parágrafo
  new Paragraph({
    pageBreakBefore: true,
    children: [new TextRun("Isso começa em uma nova página")],
  }));

// ⚠️ CRÍTICO: NUNCA use PageBreak sozinho - criará XML inválido que o Word não pode abrir
// ❌ ERRADO: new PageBreak()
// ✅ CORRETO: new Paragraph({ children: [new PageBreak()] })
```

## Cabeçalhos/Rodapés e Configuração de Página

```javascript
const doc = new Document({
  sections: [
    {
      properties: {
        page: {
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, // 1440 = 1 polegada
          size: { orientation: PageOrientation.LANDSCAPE },
          pageNumbers: { start: 1, formatType: "decimal" }, // "upperRoman", "lowerRoman", "upperLetter", "lowerLetter"
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              children: [new TextRun("Texto do Cabeçalho")],
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun("Página "),
                new TextRun({ children: [PageNumber.CURRENT] }),
                new TextRun(" de "),
                new TextRun({ children: [PageNumber.TOTAL_PAGES] }),
              ],
            }),
          ],
        }),
      },
      children: [
        /* conteúdo */
      ],
    },
  ],
});
```

## Tabulações

```javascript
new Paragraph({
  tabStops: [
    { type: TabStopType.LEFT, position: TabStopPosition.MAX / 4 },
    { type: TabStopType.CENTER, position: TabStopPosition.MAX / 2 },
    { type: TabStopType.RIGHT, position: (TabStopPosition.MAX * 3) / 4 },
  ],
  children: [new TextRun("Esquerda\tCentro\tDireita")],
});
```

## Constantes e Referência Rápida

- **Sublinhados:** `SINGLE`, `DOUBLE`, `WAVY`, `DASH`
- **Bordas:** `SINGLE`, `DOUBLE`, `DASHED`, `DOTTED`
- **Numeração:** `DECIMAL` (1,2,3), `UPPER_ROMAN` (I,II,III), `LOWER_LETTER` (a,b,c)
- **Tabulações:** `LEFT`, `CENTER`, `RIGHT`, `DECIMAL`
- **Símbolos:** `"2022"` (•), `"00A9"` (©), `"00AE"` (®), `"2122"` (™), `"00B0"` (°), `"F070"` (✓), `"F0FC"` (✗)

## Problemas Críticos e Erros Comuns

- **CRÍTICO: PageBreak deve SEMPRE estar dentro de um Paragraph** - PageBreak autônomo cria XML inválido que o Word não pode abrir
- **SEMPRE use ShadingType.CLEAR para sombreamento de célula de tabela** - Nunca use ShadingType.SOLID (causa fundo preto).
- Medidas em DXA (1440 = 1 polegada) | Cada célula de tabela precisa de ≥1 Paragraph | TOC requer estilos HeadingLevel apenas
- **SEMPRE use estilos personalizados** com fonte Arial para aparência profissional e hierarquia visual adequada
- **SEMPRE defina uma fonte padrão** usando `styles.default.document.run.font` - Arial recomendado
- **SEMPRE use array columnWidths para tabelas** + larguras de célula individuais para compatibilidade
- **NUNCA use símbolos unicode para marcadores** - sempre use configuração de numeração adequada com constante `LevelFormat.BULLET` (NÃO a string "bullet")
- **NUNCA use \n para quebras de linha em qualquer lugar** - sempre use elementos Paragraph separados para cada linha
- **SEMPRE use objetos TextRun dentro de filhos Paragraph** - nunca use propriedade de texto diretamente no Paragraph
- **CRÍTICO para imagens**: ImageRun REQUER parâmetro `type` - sempre especifique "png", "jpg", "jpeg", "gif", "bmp", ou "svg"
- **CRÍTICO para marcadores**: Deve usar constante `LevelFormat.BULLET`, não string "bullet", e incluir `text: "•"` para o caractere de marcador
- **CRÍTICO para numeração**: Cada referência de numeração cria uma lista INDEPENDENTE. Mesma referência = continua numeração (1,2,3 depois 4,5,6). Referência diferente = reinicia em 1 (1,2,3 depois 1,2,3). Use nomes de referência exclusivos para cada seção numerada separada!
- **CRÍTICO para TOC**: Ao usar TableOfContents, os cabeçalhos devem usar HeadingLevel APENAS - NÃO adicione estilos personalizados a parágrafos de cabeçalho ou o TOC quebrará
- **Tabelas**: Defina array `columnWidths` + larguras de célula individuais, aplique bordas às células, não à tabela
- **Defina margens de tabela no nível da TABLE** para preenchimento de célula consistente (evita repetição por célula)
