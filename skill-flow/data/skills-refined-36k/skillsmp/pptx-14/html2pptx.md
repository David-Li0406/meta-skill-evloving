# Guia de HTML para PowerPoint

Converta slides HTML em apresentações do PowerPoint com posicionamento preciso usando a biblioteca `html2pptx.js`.

## Índice

1. [Criando Slides HTML](#criando-slides-html)
2. [Usando a Biblioteca html2pptx](#usando-a-biblioteca-html2pptx)
3. [Usando PptxGenJS](#usando-pptxgenjs)

---

## Criando Slides HTML

Todo slide HTML deve incluir dimensões de corpo adequadas:

### Dimensões de Layout

- **16:9** (padrão): `width: 720pt; height: 405pt`
- **4:3**: `width: 720pt; height: 540pt`
- **16:10**: `width: 720pt; height: 450pt`

### Elementos Suportados

- `<p>`, `<h1>`-`<h6>` - Texto com estilo
- `<ul>`, `<ol>` - Listas (nunca use marcadores manuais •, -, \*)
- `<b>`, `<strong>` - Texto em negrito (formatação inline)
- `<i>`, `<em>` - Texto em itálico (formatação inline)
- `<u>` - Texto sublinhado (formatação inline)
- `<span>` - Formatação inline com estilos CSS (negrito, itálico, sublinhado, cor)
- `<br>` - Quebras de linha
- `<div>` com bg/border - Torna-se forma
- `<img>` - Imagens
- `class="placeholder"` - Espaço reservado para gráficos (retorna `{ id, x, y, w, h }`)

### Regras de Texto Críticas

**TODO o texto DEVE estar dentro de tags `<p>`, `<h1>`-`<h6>`, `<ul>`, ou `<ol>`:**

- ✅ Correto: `<div><p>Texto aqui</p></div>`
- ❌ Errado: `<div>Texto aqui</div>` - **Texto NÃO aparecerá no PowerPoint**
- ❌ Errado: `<span>Texto</span>` - **Texto NÃO aparecerá no PowerPoint**
- Texto em `<div>` ou `<span>` sem uma tag de texto será ignorado silenciosamente

**NUNCA use símbolos de marcador manuais (•, -, \*, etc.)** - Use listas `<ul>` ou `<ol>`

**USE APENAS fontes seguras para web que estejam universalmente disponíveis:**

- ✅ Fontes seguras para web: `Arial`, `Helvetica`, `Times New Roman`, `Georgia`, `Courier New`, `Verdana`, `Tahoma`, `Trebuchet MS`, `Impact`, `Comic Sans MS`
- ❌ Errado: `'Segoe UI'`, `'SF Pro'`, `'Roboto'`, fontes personalizadas - **Pode causar problemas de renderização**

### Estilo

- Use `display: flex` no corpo para evitar que o colapso de margem quebre a validação de estouro
- Use `margin` para espaçamento (padding incluído no tamanho)
- Formatação inline: Use tags `<b>`, `<i>`, `<u>` OU `<span>` com estilos CSS
  - `<span>` suporta: `font-weight: bold`, `font-style: italic`, `text-decoration: underline`, `color: #rrggbb`
  - `<span>` NÃO suporta: `margin`, `padding` (não suportado em execuções de texto do PowerPoint)
  - Exemplo: `<span style="font-weight: bold; color: #667eea;">Texto azul em negrito</span>`
- Flexbox funciona - posições calculadas a partir do layout renderizado
- Use cores hexadecimais com prefixo `#` em CSS
- **Alinhamento de texto**: Use CSS `text-align` (`center`, `right`, etc.) quando necessário como uma dica para o PptxGenJS para formatação de texto se os comprimentos do texto estiverem ligeiramente incorretos

### Estilo de Forma (apenas elementos DIV)

**IMPORTANTE: Fundos, bordas e sombras funcionam apenas em elementos `<div>`, NÃO em elementos de texto (`<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`)**

- **Fundos**: CSS `background` ou `background-color` apenas em elementos `<div>`
  - Exemplo: `<div style="background: #f0f0f0;">` - Cria uma forma com fundo
- **Bordas**: CSS `border` em elementos `<div>` converte para bordas de forma do PowerPoint
  - Suporta bordas uniformes: `border: 2px solid #333333`
  - Suporta bordas parciais: `border-left`, `border-right`, `border-top`, `border-bottom` (renderizado como formas de linha)
  - Exemplo: `<div style="border-left: 8pt solid #E76F51;">`
- **Raio da borda**: CSS `border-radius` em elementos `<div>` para cantos arredondados
  - `border-radius: 50%` ou superior cria forma circular
  - Porcentagens <50% calculadas em relação à dimensão menor da forma
  - Suporta unidades px e pt (por exemplo, `border-radius: 8pt;`, `border-radius: 12px;`)
  - Exemplo: `<div style="border-radius: 25%;">` em caixa 100x200px = 25% de 100px = raio de 25px
- **Sombras de caixa**: CSS `box-shadow` em elementos `<div>` converte para sombras do PowerPoint
  - Suporta apenas sombras externas (sombras internas são ignoradas para evitar corrupção)
  - Exemplo: `<div style="box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);">`
  - Nota: Sombras inset/internas não são suportadas pelo PowerPoint e serão ignoradas

### Ícones e Gradientes

- **CRÍTICO: Nunca use gradientes CSS (`linear-gradient`, `radial-gradient`)** - Eles não convertem para PowerPoint
- **SEMPRE crie PNGs de gradiente/ícone PRIMEIRO usando Sharp, depois referencie em HTML**
- Para gradientes: Rasterize SVG para imagens de fundo PNG
- Para ícones: Rasterize ícones SVG react-icons para imagens PNG
- Todos os efeitos visuais devem ser pré-renderizados como imagens raster antes da renderização HTML

**Rasterizando Ícones com Sharp:**

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaHome } = require("react-icons/fa");

async function rasterizeIconPng(IconComponent, color, size = "256", filename) {
  const svgString = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: `#${color}`, size: size }),
  );

  // Converter SVG para PNG usando Sharp
  await sharp(Buffer.from(svgString)).png().toFile(filename);

  return filename;
}

// Uso: Rasterize ícone antes de usar em HTML
const iconPath = await rasterizeIconPng(
  FaHome,
  "4472c4",
  "256",
  "home-icon.png",
);
// Então referencie em HTML: <img src="home-icon.png" style="width: 40pt; height: 40pt;">
```

**Rasterizando Gradientes com Sharp:**

```javascript
const sharp = require("sharp");

async function createGradientBackground(filename) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="562.5">
    <defs>
      <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#COLOR1"/>
        <stop offset="100%" style="stop-color:#COLOR2"/>
      </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="url(#g)"/>
  </svg>`;

  await sharp(Buffer.from(svg)).png().toFile(filename);

  return filename;
}

// Uso: Crie fundo gradiente antes do HTML
const bgPath = await createGradientBackground("gradient-bg.png");
// Então em HTML: <body style="background-image: url('gradient-bg.png');">
```

### Exemplo

```html
<!DOCTYPE html>
<html>
  <head>
    <style>
      html {
        background: #ffffff;
      }
      body {
        width: 720pt;
        height: 405pt;
        margin: 0;
        padding: 0;
        background: #f5f5f5;
        font-family: Arial, sans-serif;
        display: flex;
      }
      .content {
        margin: 30pt;
        padding: 40pt;
        background: #ffffff;
        border-radius: 8pt;
      }
      h1 {
        color: #2d3748;
        font-size: 32pt;
      }
      .box {
        background: #70ad47;
        padding: 20pt;
        border: 3px solid #5a8f37;
        border-radius: 12pt;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.25);
      }
    </style>
  </head>
  <body>
    <div class="content">
      <h1>Recipe Title</h1>
      <ul>
        <li><b>Item:</b> Description</li>
      </ul>
      <p>Text with <b>bold</b>, <i>italic</i>, <u>underline</u>.</p>
      <div
        id="chart"
        class="placeholder"
        style="width: 350pt; height: 200pt;"
      ></div>

      <!-- Texto DEVE estar em tags <p> -->
      <div class="box">
        <p>5</p>
      </div>
    </div>
  </body>
</html>
```

## Usando a Biblioteca html2pptx

### Dependências

Estas bibliotecas foram instaladas globalmente e estão disponíveis para uso:

- `pptxgenjs`
- `playwright`
- `sharp`

### Uso Básico

```javascript
const pptxgen = require("pptxgenjs");
const html2pptx = require("./html2pptx");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9"; // Deve corresponder às dimensões do corpo HTML

const { slide, placeholders } = await html2pptx("slide1.html", pptx);

// Adicionar gráfico à área de placeholder
if (placeholders.length > 0) {
  slide.addChart(pptx.charts.LINE, chartData, placeholders[0]);
}

await pptx.writeFile("output.pptx");
```

### Referência da API

#### Assinatura de Função

```javascript
await html2pptx(htmlFile, pres, options);
```

#### Parâmetros

- `htmlFile` (string): Caminho para o arquivo HTML (absoluto ou relativo)
- `pres` (pptxgen): Instância de apresentação PptxGenJS com layout já definido
- `options` (objeto, opcional):
  - `tmpDir` (string): Diretório temporário para arquivos gerados (padrão: `process.env.TMPDIR || '/tmp'`)
  - `slide` (objeto): Slide existente para reutilizar (padrão: cria novo slide)

#### Retornos

```javascript
{
    slide: pptxgenSlide,           // O slide criado/atualizado
    placeholders: [                 // Array de posições de placeholder
        { id: string, x: number, y: number, w: number, h: number },
        ...
    ]
}
```

### Validação

A biblioteca valida e coleta automaticamente todos os erros antes de lançar:

1. **Dimensões HTML devem corresponder ao layout da apresentação** - Relata incompatibilidades de dimensão
2. **Conteúdo não deve estourar o corpo** - Relata estouro com medidas exatas
3. **Gradientes CSS** - Relata uso de gradiente não suportado
4. **Estilo de elemento de texto** - Relata fundos/bordas/sombras em elementos de texto (apenas permitido em divs)

**Todos os erros de validação são coletados e relatados juntos** em uma única mensagem de erro, permitindo que você corrija todos os problemas de uma vez em vez de um por um.

### Trabalhando com Placeholders

```javascript
const { slide, placeholders } = await html2pptx("slide.html", pptx);

// Use primeiro placeholder
slide.addChart(pptx.charts.BAR, data, placeholders[0]);

// Encontre por ID
const chartArea = placeholders.find((p) => p.id === "chart-area");
slide.addChart(pptx.charts.LINE, data, chartArea);
```

### Exemplo Completo

```javascript
const pptxgen = require("pptxgenjs");
const html2pptx = require("./html2pptx");

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "Seu Nome";
  pptx.title = "Minha Apresentação";

  // Slide 1: Título
  const { slide: slide1 } = await html2pptx("slides/title.html", pptx);

  // Slide 2: Conteúdo com gráfico
  const { slide: slide2, placeholders } = await html2pptx(
    "slides/data.html",
    pptx,
  );

  const chartData = [
    {
      name: "Sales",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [4500, 5500, 6200, 7100],
    },
  ];

  slide2.addChart(pptx.charts.BAR, chartData, {
    ...placeholders[0],
    showTitle: true,
    title: "Vendas Trimestrais",
    showCatAxisTitle: true,
    catAxisTitle: "Trimestre",
    showValAxisTitle: true,
    valAxisTitle: "Vendas ($000s)",
  });

  // Salvar
  await pptx.writeFile({ fileName: "presentation.pptx" });
  console.log("Apresentação criada com sucesso!");
}

createPresentation().catch(console.error);
```

## Usando PptxGenJS

Depois de converter HTML para slides com `html2pptx`, você usará PptxGenJS para adicionar conteúdo dinâmico como gráficos, imagens e elementos adicionais.

### ⚠️ Regras Críticas

#### Cores

- **NUNCA use prefixo `#`** com cores hexadecimais no PptxGenJS - causa corrupção de arquivo
- ✅ Correto: `color: "FF0000"`, `fill: { color: "0066CC" }`
- ❌ Errado: `color: "#FF0000"` (quebra o documento)

### Adicionando Imagens

Sempre calcule proporções a partir das dimensões reais da imagem:

```javascript
// Obter dimensões da imagem: identify image.png | grep -o '[0-9]* x [0-9]*'
const imgWidth = 1860,
  imgHeight = 1519; // Do arquivo real
const aspectRatio = imgWidth / imgHeight;

const h = 3; // Altura máxima
const w = h * aspectRatio;
const x = (10 - w) / 2; // Centralizar em slide 16:9

slide.addImage({ path: "chart.png", x, y: 1.5, w, h });
```

### Adicionando Texto

```javascript
// Rich text com formatação
slide.addText(
  [
    { text: "Negrito ", options: { bold: true } },
    { text: "Itálico ", options: { italic: true } },
    { text: "Normal" },
  ],
  {
    x: 1,
    y: 2,
    w: 8,
    h: 1,
  },
);
```

### Adicionando Formas

```javascript
// Retângulo
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 1,
  y: 1,
  w: 3,
  h: 2,
  fill: { color: "4472C4" },
  line: { color: "000000", width: 2 },
});

// Círculo
slide.addShape(pptx.shapes.OVAL, {
  x: 5,
  y: 1,
  w: 2,
  h: 2,
  fill: { color: "ED7D31" },
});

// Retângulo Arredondado
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 1,
  y: 4,
  w: 3,
  h: 1.5,
  fill: { color: "70AD47" },
  rectRadius: 0.2,
});
```

### Adicionando Gráficos

**Necessário para a maioria dos gráficos:** Rótulos de eixo usando `catAxisTitle` (categoria) e `valAxisTitle` (valor).

**Formato de Dados do Gráfico:**

- Use **uma única série com todos os rótulos** para gráficos de barras/linhas simples
- Cada série cria uma entrada de legenda separada
- Array de rótulos define valores do eixo X

**Dados de Série Temporal - Escolha a Granularidade Correta:**

- **< 30 dias**: Use agrupamento diário (por exemplo, "10-01", "10-02") - evite agregação mensal que cria gráficos de ponto único
- **30-365 dias**: Use agrupamento mensal (por exemplo, "2024-01", "2024-02")
- **> 365 dias**: Use agrupamento anual (por exemplo, "2023", "2024")
- **Validar**: Gráficos com apenas 1 ponto de dados provavelmente indicam agregação incorreta para o período de tempo

```javascript
const { slide, placeholders } = await html2pptx("slide.html", pptx);

// CORRETO: Série única com todos os rótulos
slide.addChart(
  pptx.charts.BAR,
  [
    {
      name: "Sales 2024",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [4500, 5500, 6200, 7100],
    },
  ],
  {
    ...placeholders[0], // Use posição de placeholder
    barDir: "col", // 'col' = barras verticais, 'bar' = horizontal
    showTitle: true,
    title: "Vendas Trimestrais",
    showLegend: false, // Nenhuma legenda necessária para série única
    // Rótulos de eixo necessários
    showCatAxisTitle: true,
    catAxisTitle: "Trimestre",
    showValAxisTitle: true,
    valAxisTitle: "Vendas ($000s)",
    // Opcional: Controle de escala (ajuste min com base no intervalo de dados para melhor visualização)
    valAxisMaxVal: 8000,
    valAxisMinVal: 0, // Use 0 para contagens/valores; para dados agrupados (ex: 4500-7100), considere começar mais perto do valor min
    valAxisMajorUnit: 2000, // Controle espaçamento de rótulo do eixo y para evitar aglomeração
    catAxisLabelRotate: 45, // Gire rótulos se aglomerado
    dataLabelPosition: "outEnd",
    dataLabelColor: "000000",
    // Use única cor para gráficos de série única
    chartColors: ["4472C4"], // Todas as barras da mesma cor
  },
);
```

#### Gráfico de Dispersão

**IMPORTANTE**: O formato de dados de gráfico de dispersão é incomum - a primeira série contém valores do eixo X, séries subsequentes contêm valores Y:

```javascript
// Preparar dados
const data1 = [
  { x: 10, y: 20 },
  { x: 15, y: 25 },
  { x: 20, y: 30 },
];
const data2 = [
  { x: 12, y: 18 },
  { x: 18, y: 22 },
];

const allXValues = [...data1.map((d) => d.x), ...data2.map((d) => d.x)];

slide.addChart(
  pptx.charts.SCATTER,
  [
    { name: "X-Axis", values: allXValues }, // Primeira série = valores X
    { name: "Series 1", values: data1.map((d) => d.y) }, // Apenas valores Y
    { name: "Series 2", values: data2.map((d) => d.y) }, // Apenas valores Y
  ],
  {
    x: 1,
    y: 1,
    w: 8,
    h: 4,
    lineSize: 0, // 0 = sem linhas de conexão
    lineDataSymbol: "circle",
    lineDataSymbolSize: 6,
    showCatAxisTitle: true,
    catAxisTitle: "X Axis",
    showValAxisTitle: true,
    valAxisTitle: "Y Axis",
    chartColors: ["4472C4", "ED7D31"],
  },
);
```

#### Gráfico de Linhas

```javascript
slide.addChart(
  pptx.charts.LINE,
  [
    {
      name: "Temperature",
      labels: ["Jan", "Feb", "Mar", "Apr"],
      values: [32, 35, 42, 55],
    },
  ],
  {
    x: 1,
    y: 1,
    w: 8,
    h: 4,
    lineSize: 4,
    lineSmooth: true,
    // Rótulos de eixo necessários
    showCatAxisTitle: true,
    catAxisTitle: "Mês",
    showValAxisTitle: true,
    valAxisTitle: "Temperatura (°F)",
    // Opcional: Intervalo do eixo Y (defina min com base no intervalo de dados para melhor visualização)
    valAxisMinVal: 0, // Para intervalos começando em 0 (contagens, porcentagens, etc.)
    valAxisMaxVal: 60,
    valAxisMajorUnit: 20, // Controle espaçamento de rótulo do eixo y para evitar aglomeração (ex: 10, 20, 25)
    // valAxisMinVal: 30,  // PREFERIDO: Para dados agrupados em um intervalo (ex: 32-55 ou classificações 3-5), inicie eixo mais perto do valor min para mostrar variação
    // Opcional: Cores do gráfico
    chartColors: ["4472C4", "ED7D31", "A5A5A5"],
  },
);
```

#### Gráfico de Pizza (Nenhum rótulo de eixo necessário)

**CRÍTICO**: Gráficos de pizza exigem uma **única série de dados** com todas as categorias no array `labels` e valores correspondentes no array `values`.

```javascript
slide.addChart(
  pptx.charts.PIE,
  [
    {
      name: "Market Share",
      labels: ["Product A", "Product B", "Other"], // Todas as categorias em um array
      values: [35, 45, 20], // Todos os valores em um array
    },
  ],
  {
    x: 2,
    y: 1,
    w: 6,
    h: 4,
    showPercent: true,
    showLegend: true,
    legendPos: "r", // direita
    chartColors: ["4472C4", "ED7D31", "A5A5A5"],
  },
);
```

#### Múltiplas Séries de Dados

```javascript
slide.addChart(
  pptx.charts.LINE,
  [
    {
      name: "Product A",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [10, 20, 30, 40],
    },
    {
      name: "Product B",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [15, 25, 20, 35],
    },
  ],
  {
    x: 1,
    y: 1,
    w: 8,
    h: 4,
    showCatAxisTitle: true,
    catAxisTitle: "Trimestre",
    showValAxisTitle: true,
    valAxisTitle: "Receita ($M)",
  },
);
```

### Cores do Gráfico

**CRÍTICO**: Use cores hexadecimais **sem** o prefixo `#` - incluir `#` causa corrupção de arquivo.

**Alinhe as cores do gráfico com sua paleta de design escolhida**, garantindo contraste e distinção suficientes para visualização de dados. Ajuste cores para:

- Forte contraste entre séries adjacentes
- Legibilidade contra planos de fundo de slides
- Acessibilidade (evite combinações apenas vermelho-verde)

```javascript
// Exemplo: Cores de gráfico inspiradas na paleta Oceano (ajustadas para contraste)
const chartColors = ["16A085", "FF6B9D", "2C3E50", "F39C12", "9B59B6"];

// Gráfico de série única: Use uma cor para todas as barras/pontos
slide.addChart(
  pptx.charts.BAR,
  [
    {
      name: "Sales",
      labels: ["Q1", "Q2", "Q3", "Q4"],
      values: [4500, 5500, 6200, 7100],
    },
  ],
  {
    ...placeholders[0],
    chartColors: ["16A085"], // Todas as barras da mesma cor
    showLegend: false,
  },
);

// Gráfico multi-série: Cada série recebe uma cor diferente
slide.addChart(
  pptx.charts.LINE,
  [
    { name: "Product A", labels: ["Q1", "Q2", "Q3"], values: [10, 20, 30] },
    { name: "Product B", labels: ["Q1", "Q2", "Q3"], values: [15, 25, 20] },
  ],
  {
    ...placeholders[0],
    chartColors: ["16A085", "FF6B9D"], // Uma cor por série
  },
);
```

### Adicionando Tabelas

Tabelas podem ser adicionadas com formatação básica ou avançada:

#### Tabela Básica

```javascript
slide.addTable(
  [
    ["Header 1", "Header 2", "Header 3"],
    ["Row 1, Col 1", "Row 1, Col 2", "Row 1, Col 3"],
    ["Row 2, Col 1", "Row 2, Col 2", "Row 2, Col 3"],
  ],
  {
    x: 0.5,
    y: 1,
    w: 9,
    h: 3,
    border: { pt: 1, color: "999999" },
    fill: { color: "F1F1F1" },
  },
);
```

#### Tabela com Formatação Personalizada

```javascript
const tableData = [
  // Linha de cabeçalho com estilo personalizado
  [
    {
      text: "Produto",
      options: { fill: { color: "4472C4" }, color: "FFFFFF", bold: true },
    },
    {
      text: "Receita",
      options: { fill: { color: "4472C4" }, color: "FFFFFF", bold: true },
    },
    {
      text: "Crescimento",
      options: { fill: { color: "4472C4" }, color: "FFFFFF", bold: true },
    },
  ],
  // Linhas de dados
  ["Produto A", "$50M", "+15%"],
  ["Produto B", "$35M", "+22%"],
  ["Produto C", "$28M", "+8%"],
];

slide.addTable(tableData, {
  x: 1,
  y: 1.5,
  w: 8,
  h: 3,
  colW: [3, 2.5, 2.5], // Larguras das colunas
  rowH: [0.5, 0.6, 0.6, 0.6], // Alturas das linhas
  border: { pt: 1, color: "CCCCCC" },
  align: "center",
  valign: "middle",
  fontSize: 14,
});
```

#### Tabela com Células Mescladas

```javascript
const mergedTableData = [
  [
    {
      text: "Resultados Q1",
      options: {
        colspan: 3,
        fill: { color: "4472C4" },
        color: "FFFFFF",
        bold: true,
      },
    },
  ],
  ["Produto", "Vendas", "Market Share"],
  ["Produto A", "$25M", "35%"],
  ["Produto B", "$18M", "25%"],
];

slide.addTable(mergedTableData, {
  x: 1,
  y: 1,
  w: 8,
  h: 2.5,
  colW: [3, 2.5, 2.5],
  border: { pt: 1, color: "DDDDDD" },
});
```

### Opções de Tabela

Opções comuns de tabela:

- `x, y, w, h` - Posição e tamanho
- `colW` - Array de larguras de coluna (em polegadas)
- `rowH` - Array de alturas de linha (em polegadas)
- `border` - Estilo da borda: `{ pt: 1, color: "999999" }`
- `fill` - Cor de fundo (sem prefixo #)
- `align` - Alinhamento de texto: "left", "center", "right"
- `valign` - Alinhamento vertical: "top", "middle", "bottom"
- `fontSize` - Tamanho do texto
- `autoPage` - Cria novos slides automaticamente se o conteúdo estourar
