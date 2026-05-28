# HTML 轉 PowerPoint 指南

使用 `html2pptx.js` 函式庫將 HTML 投影片轉換為具有精確定位的 PowerPoint 簡報。

## 目錄

1. [建立 HTML 投影片](#建立-html-投影片)
2. [使用 html2pptx 函式庫](#使用-html2pptx-函式庫)
3. [使用 PptxGenJS](#使用-pptxgenjs)

---

## 建立 HTML 投影片

每個 HTML 投影片必須包含正確的 body 尺寸:

### 版面尺寸

- **16:9**(預設):`width: 720pt; height: 405pt`
- **4:3**:`width: 720pt; height: 540pt`
- **16:10**:`width: 720pt; height: 450pt`

### 支援的元素

- `<p>`、`<h1>`-`<h6>` - 帶樣式的文字
- `<ul>`、`<ol>` - 清單(絕不使用手動項目符號 •、-、*)
- `<b>`、`<strong>` - 粗體文字(行內格式化)
- `<i>`、`<em>` - 斜體文字(行內格式化)
- `<u>` - 底線文字(行內格式化)
- `<span>` - 帶 CSS 樣式的行內格式化(粗體、斜體、底線、顏色)
- `<br>` - 換行
- `<div>` 帶背景/邊框 - 變成形狀
- `<img>` - 圖片
- `class="placeholder"` - 圖表預留空間(返回 `{ id, x, y, w, h }`)

### 關鍵文字規則

**所有文字必須在 `<p>`、`<h1>`-`<h6>`、`<ul>` 或 `<ol>` 標籤內:**
- ✅ 正確:`<div><p>這裡是文字</p></div>`
- ❌ 錯誤:`<div>這裡是文字</div>` - **文字不會出現在 PowerPoint 中**
- ❌ 錯誤:`<span>文字</span>` - **文字不會出現在 PowerPoint 中**
- 在 `<div>` 或 `<span>` 中沒有文字標籤的文字將被靜默忽略

**絕不使用手動項目符號(•、-、* 等)** - 改用 `<ul>` 或 `<ol>` 清單

**僅使用普遍可用的網頁安全字型:**
- ✅ 網頁安全字型:`Arial`、`Helvetica`、`Times New Roman`、`Georgia`、`Courier New`、`Verdana`、`Tahoma`、`Trebuchet MS`、`Impact`、`Comic Sans MS`
- ❌ 錯誤:`'Segoe UI'`、`'SF Pro'`、`'Roboto'`、自訂字型 - **可能導致渲染問題**

### 樣式

- 在 body 上使用 `display: flex` 以防止邊距塌陷破壞溢出驗證
- 使用 `margin` 控制間距(padding 包含在尺寸中)
- 行內格式化:使用 `<b>`、`<i>`、`<u>` 標籤或帶 CSS 樣式的 `<span>`
  - `<span>` 支援:`font-weight: bold`、`font-style: italic`、`text-decoration: underline`、`color: #rrggbb`
  - `<span>` 不支援:`margin`、`padding`(PowerPoint 文字執行不支援)
  - 範例:`<span style="font-weight: bold; color: #667eea;">粗體藍色文字</span>`
- Flexbox 可用 - 位置從渲染的版面計算
- 在 CSS 中使用帶 `#` 前綴的十六進位顏色
- **文字對齊**:需要時使用 CSS `text-align`(`center`、`right` 等)作為 PptxGenJS 文字格式化的提示(如果文字長度略有偏差)

### 形狀樣式(僅限 DIV 元素)

**重要:背景、邊框和陰影僅適用於 `<div>` 元素,不適用於文字元素(`<p>`、`<h1>`-`<h6>`、`<ul>`、`<ol>`)**

- **背景**:僅在 `<div>` 元素上使用 CSS `background` 或 `background-color`
  - 範例:`<div style="background: #f0f0f0;">` - 建立帶背景的形狀
- **邊框**:`<div>` 元素上的 CSS `border` 轉換為 PowerPoint 形狀邊框
  - 支援統一邊框:`border: 2px solid #333333`
  - 支援部分邊框:`border-left`、`border-right`、`border-top`、`border-bottom`(渲染為線條形狀)
  - 範例:`<div style="border-left: 8pt solid #E76F51;">`
- **邊框圓角**:`<div>` 元素上的 CSS `border-radius` 用於圓角
  - `border-radius: 50%` 或更高建立圓形形狀
  - 低於 50% 的百分比相對於形狀的較小尺寸計算
  - 支援 px 和 pt 單位(例如,`border-radius: 8pt;`、`border-radius: 12px;`)
  - 範例:100x200px 方塊上的 `<div style="border-radius: 25%;">` = 100px 的 25% = 25px 圓角半徑
- **方塊陰影**:`<div>` 元素上的 CSS `box-shadow` 轉換為 PowerPoint 陰影
  - 僅支援外陰影(內陰影被忽略以防止損壞)
  - 範例:`<div style="box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);">`
  - 注意:PowerPoint 不支援內嵌/內陰影,將被跳過

### 圖示和漸層

- **關鍵:絕不使用 CSS 漸層(`linear-gradient`、`radial-gradient`)** - 它們不會轉換到 PowerPoint
- **始終先使用 Sharp 建立漸層/圖示 PNG,然後在 HTML 中引用**
- 對於漸層:將 SVG 光柵化為 PNG 背景圖片
- 對於圖示:將 react-icons SVG 光柵化為 PNG 圖片
- 所有視覺效果必須在 HTML 渲染之前預先渲染為點陣圖

**使用 Sharp 光柵化圖示:**

```javascript
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const { FaHome } = require('react-icons/fa');

async function rasterizeIconPng(IconComponent, color, size = "256", filename) {
  const svgString = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: `#${color}`, size: size })
  );

  // 使用 Sharp 將 SVG 轉換為 PNG
  await sharp(Buffer.from(svgString))
    .png()
    .toFile(filename);

  return filename;
}

// 用法:在 HTML 中使用前光柵化圖示
const iconPath = await rasterizeIconPng(FaHome, "4472c4", "256", "home-icon.png");
// 然後在 HTML 中引用:<img src="home-icon.png" style="width: 40pt; height: 40pt;">
```

**使用 Sharp 光柵化漸層:**

```javascript
const sharp = require('sharp');

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

  await sharp(Buffer.from(svg))
    .png()
    .toFile(filename);

  return filename;
}

// 用法:在 HTML 之前建立漸層背景
const bgPath = await createGradientBackground("gradient-bg.png");
// 然後在 HTML 中:<body style="background-image: url('gradient-bg.png');">
```

### 範例

```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #f5f5f5; font-family: Arial, sans-serif;
  display: flex;
}
.content { margin: 30pt; padding: 40pt; background: #ffffff; border-radius: 8pt; }
h1 { color: #2d3748; font-size: 32pt; }
.box {
  background: #70ad47; padding: 20pt; border: 3px solid #5a8f37;
  border-radius: 12pt; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.25);
}
</style>
</head>
<body>
<div class="content">
  <h1>食譜標題</h1>
  <ul>
    <li><b>項目:</b> 描述</li>
  </ul>
  <p>帶有<b>粗體</b>、<i>斜體</i>、<u>底線</u>的文字。</p>
  <div id="chart" class="placeholder" style="width: 350pt; height: 200pt;"></div>

  <!-- 文字必須在 <p> 標籤中 -->
  <div class="box">
    <p>5</p>
  </div>
</div>
</body>
</html>
```

## 使用 html2pptx 函式庫

### 相依套件

這些函式庫已全域安裝並可使用:
- `pptxgenjs`
- `playwright`
- `sharp`

### 基本用法

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';  // 必須與 HTML body 尺寸匹配

const { slide, placeholders } = await html2pptx('slide1.html', pptx);

// 將圖表新增到預留位置區域
if (placeholders.length > 0) {
    slide.addChart(pptx.charts.LINE, chartData, placeholders[0]);
}

await pptx.writeFile('output.pptx');
```

### API 參考

#### 函式簽名
```javascript
await html2pptx(htmlFile, pres, options)
```

#### 參數
- `htmlFile`(字串):HTML 檔案路徑(絕對或相對)
- `pres`(pptxgen):已設定版面的 PptxGenJS 簡報實例
- `options`(物件,選用):
  - `tmpDir`(字串):產生檔案的臨時目錄(預設:`process.env.TMPDIR || '/tmp'`)
  - `slide`(物件):要重複使用的現有投影片(預設:建立新投影片)

#### 返回值
```javascript
{
    slide: pptxgenSlide,           // 建立/更新的投影片
    placeholders: [                 // 預留位置位置陣列
        { id: string, x: number, y: number, w: number, h: number },
        ...
    ]
}
```

### 驗證

函式庫會自動驗證並在拋出之前收集所有錯誤:

1. **HTML 尺寸必須與簡報版面匹配** - 報告尺寸不符
2. **內容不得溢出 body** - 報告溢出的精確測量值
3. **CSS 漸層** - 報告不支援的漸層用法
4. **文字元素樣式** - 報告文字元素上的背景/邊框/陰影(僅允許在 div 上)

**所有驗證錯誤會一起收集並報告**在單一錯誤訊息中,讓您可以一次修復所有問題而非逐一修復。

### 使用預留位置

```javascript
const { slide, placeholders } = await html2pptx('slide.html', pptx);

// 使用第一個預留位置
slide.addChart(pptx.charts.BAR, data, placeholders[0]);

// 按 ID 尋找
const chartArea = placeholders.find(p => p.id === 'chart-area');
slide.addChart(pptx.charts.LINE, data, chartArea);
```

### 完整範例

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Your Name';
    pptx.title = 'My Presentation';

    // 投影片 1:標題
    const { slide: slide1 } = await html2pptx('slides/title.html', pptx);

    // 投影片 2:帶圖表的內容
    const { slide: slide2, placeholders } = await html2pptx('slides/data.html', pptx);

    const chartData = [{
        name: 'Sales',
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        values: [4500, 5500, 6200, 7100]
    }];

    slide2.addChart(pptx.charts.BAR, chartData, {
        ...placeholders[0],
        showTitle: true,
        title: 'Quarterly Sales',
        showCatAxisTitle: true,
        catAxisTitle: 'Quarter',
        showValAxisTitle: true,
        valAxisTitle: 'Sales ($000s)'
    });

    // 儲存
    await pptx.writeFile({ fileName: 'presentation.pptx' });
    console.log('簡報建立成功!');
}

createPresentation().catch(console.error);
```

## 使用 PptxGenJS

使用 `html2pptx` 將 HTML 轉換為投影片後,您將使用 PptxGenJS 新增動態內容,如圖表、圖片和其他元素。

### ⚠️ 關鍵規則

#### 顏色
- **絕不使用 `#` 前綴**與 PptxGenJS 中的十六進位顏色 - 會導致檔案損壞
- ✅ 正確:`color: "FF0000"`、`fill: { color: "0066CC" }`
- ❌ 錯誤:`color: "#FF0000"`(破壞文件)

### 新增圖片

始終從實際圖片尺寸計算長寬比:

```javascript
// 取得圖片尺寸:identify image.png | grep -o '[0-9]* x [0-9]*'
const imgWidth = 1860, imgHeight = 1519;  // 來自實際檔案
const aspectRatio = imgWidth / imgHeight;

const h = 3;  // 最大高度
const w = h * aspectRatio;
const x = (10 - w) / 2;  // 在 16:9 投影片上置中

slide.addImage({ path: "chart.png", x, y: 1.5, w, h });
```

### 新增文字

```javascript
// 帶格式的富文字
slide.addText([
    { text: "粗體 ", options: { bold: true } },
    { text: "斜體 ", options: { italic: true } },
    { text: "普通" }
], {
    x: 1, y: 2, w: 8, h: 1
});
```

### 新增形狀

```javascript
// 矩形
slide.addShape(pptx.shapes.RECTANGLE, {
    x: 1, y: 1, w: 3, h: 2,
    fill: { color: "4472C4" },
    line: { color: "000000", width: 2 }
});

// 圓形
slide.addShape(pptx.shapes.OVAL, {
    x: 5, y: 1, w: 2, h: 2,
    fill: { color: "ED7D31" }
});

// 圓角矩形
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 1, y: 4, w: 3, h: 1.5,
    fill: { color: "70AD47" },
    rectRadius: 0.2
});
```

### 新增圖表

**大多數圖表需要:**使用 `catAxisTitle`(類別)和 `valAxisTitle`(值)的軸標籤。

**圖表資料格式:**
- 對簡單長條圖/折線圖使用**包含所有標籤的單一資料系列**
- 每個系列建立一個單獨的圖例項目
- Labels 陣列定義 X 軸值

**時間序列資料 - 選擇正確的粒度:**
- **< 30 天**:使用每日分組(例如,"10-01"、"10-02")- 避免建立單點圖表的月度聚合
- **30-365 天**:使用每月分組(例如,"2024-01"、"2024-02")
- **> 365 天**:使用每年分組(例如,"2023"、"2024")
- **驗證**:僅有 1 個資料點的圖表可能表示該時間週期的聚合不正確

```javascript
const { slide, placeholders } = await html2pptx('slide.html', pptx);

// 正確:包含所有標籤的單一系列
slide.addChart(pptx.charts.BAR, [{
    name: "Sales 2024",
    labels: ["Q1", "Q2", "Q3", "Q4"],
    values: [4500, 5500, 6200, 7100]
}], {
    ...placeholders[0],  // 使用預留位置位置
    barDir: 'col',       // 'col' = 垂直長條,'bar' = 水平
    showTitle: true,
    title: 'Quarterly Sales',
    showLegend: false,   // 單一系列不需要圖例
    // 必要的軸標籤
    showCatAxisTitle: true,
    catAxisTitle: 'Quarter',
    showValAxisTitle: true,
    valAxisTitle: 'Sales ($000s)',
    // 選用:控制縮放(根據資料範圍調整最小值以獲得更好的視覺化)
    valAxisMaxVal: 8000,
    valAxisMinVal: 0,  // 對計數/金額使用 0;對於群集資料(例如,4500-7100),考慮從接近最小值開始
    valAxisMajorUnit: 2000,  // 控制 y 軸標籤間距以防止擁擠
    catAxisLabelRotate: 45,  // 如果擁擠則旋轉標籤
    dataLabelPosition: 'outEnd',
    dataLabelColor: '000000',
    // 對單一系列圖表使用單一顏色
    chartColors: ["4472C4"]  // 所有長條相同顏色
});
```

#### 散佈圖

**重要**:散佈圖資料格式不尋常 - 第一個系列包含 X 軸值,後續系列包含 Y 值:

```javascript
// 準備資料
const data1 = [{ x: 10, y: 20 }, { x: 15, y: 25 }, { x: 20, y: 30 }];
const data2 = [{ x: 12, y: 18 }, { x: 18, y: 22 }];

const allXValues = [...data1.map(d => d.x), ...data2.map(d => d.x)];

slide.addChart(pptx.charts.SCATTER, [
    { name: 'X-Axis', values: allXValues },  // 第一個系列 = X 值
    { name: 'Series 1', values: data1.map(d => d.y) },  // 僅 Y 值
    { name: 'Series 2', values: data2.map(d => d.y) }   // 僅 Y 值
], {
    x: 1, y: 1, w: 8, h: 4,
    lineSize: 0,  // 0 = 無連接線
    lineDataSymbol: 'circle',
    lineDataSymbolSize: 6,
    showCatAxisTitle: true,
    catAxisTitle: 'X Axis',
    showValAxisTitle: true,
    valAxisTitle: 'Y Axis',
    chartColors: ["4472C4", "ED7D31"]
});
```

#### 折線圖

```javascript
slide.addChart(pptx.charts.LINE, [{
    name: "Temperature",
    labels: ["Jan", "Feb", "Mar", "Apr"],
    values: [32, 35, 42, 55]
}], {
    x: 1, y: 1, w: 8, h: 4,
    lineSize: 4,
    lineSmooth: true,
    // 必要的軸標籤
    showCatAxisTitle: true,
    catAxisTitle: 'Month',
    showValAxisTitle: true,
    valAxisTitle: 'Temperature (°F)',
    // 選用:Y 軸範圍(根據資料範圍設定最小值以獲得更好的視覺化)
    valAxisMinVal: 0,     // 對於從 0 開始的範圍(計數、百分比等)
    valAxisMaxVal: 60,
    valAxisMajorUnit: 20,  // 控制 y 軸標籤間距以防止擁擠(例如,10、20、25)
    // valAxisMinVal: 30,  // 建議:對於群集在某範圍內的資料(例如,32-55 或評分 3-5),從接近最小值開始軸以顯示變化
    // 選用:圖表顏色
    chartColors: ["4472C4", "ED7D31", "A5A5A5"]
});
```

#### 圓餅圖(不需要軸標籤)

**關鍵**:圓餅圖需要**單一資料系列**,所有類別在 `labels` 陣列中,對應的值在 `values` 陣列中。

```javascript
slide.addChart(pptx.charts.PIE, [{
    name: "Market Share",
    labels: ["Product A", "Product B", "Other"],  // 所有類別在一個陣列中
    values: [35, 45, 20]  // 所有值在一個陣列中
}], {
    x: 2, y: 1, w: 6, h: 4,
    showPercent: true,
    showLegend: true,
    legendPos: 'r',  // 右側
    chartColors: ["4472C4", "ED7D31", "A5A5A5"]
});
```

#### 多資料系列

```javascript
slide.addChart(pptx.charts.LINE, [
    {
        name: "Product A",
        labels: ["Q1", "Q2", "Q3", "Q4"],
        values: [10, 20, 30, 40]
    },
    {
        name: "Product B",
        labels: ["Q1", "Q2", "Q3", "Q4"],
        values: [15, 25, 20, 35]
    }
], {
    x: 1, y: 1, w: 8, h: 4,
    showCatAxisTitle: true,
    catAxisTitle: 'Quarter',
    showValAxisTitle: true,
    valAxisTitle: 'Revenue ($M)'
});
```

### 圖表顏色

**關鍵**:使用**不帶** `#` 前綴的十六進位顏色 - 包含 `#` 會導致檔案損壞。

**將圖表顏色與您選擇的設計調色盤對齊**,確保資料視覺化有足夠的對比度和區分度。調整顏色以:
- 相鄰系列之間強烈對比
- 在投影片背景上可讀性
- 無障礙性(避免僅使用紅綠組合)

```javascript
// 範例:受海洋調色盤啟發的圖表顏色(調整對比度)
const chartColors = ["16A085", "FF6B9D", "2C3E50", "F39C12", "9B59B6"];

// 單一系列圖表:對所有長條/點使用一種顏色
slide.addChart(pptx.charts.BAR, [{
    name: "Sales",
    labels: ["Q1", "Q2", "Q3", "Q4"],
    values: [4500, 5500, 6200, 7100]
}], {
    ...placeholders[0],
    chartColors: ["16A085"],  // 所有長條相同顏色
    showLegend: false
});

// 多系列圖表:每個系列取得不同顏色
slide.addChart(pptx.charts.LINE, [
    { name: "Product A", labels: ["Q1", "Q2", "Q3"], values: [10, 20, 30] },
    { name: "Product B", labels: ["Q1", "Q2", "Q3"], values: [15, 25, 20] }
], {
    ...placeholders[0],
    chartColors: ["16A085", "FF6B9D"]  // 每個系列一種顏色
});
```

### 新增表格

表格可以使用基本或進階格式化新增:

#### 基本表格

```javascript
slide.addTable([
    ["標題 1", "標題 2", "標題 3"],
    ["第 1 列, 第 1 欄", "第 1 列, 第 2 欄", "第 1 列, 第 3 欄"],
    ["第 2 列, 第 1 欄", "第 2 列, 第 2 欄", "第 2 列, 第 3 欄"]
], {
    x: 0.5,
    y: 1,
    w: 9,
    h: 3,
    border: { pt: 1, color: "999999" },
    fill: { color: "F1F1F1" }
});
```

#### 帶自訂格式的表格

```javascript
const tableData = [
    // 帶自訂樣式的標題列
    [
        { text: "產品", options: { fill: { color: "4472C4" }, color: "FFFFFF", bold: true } },
        { text: "營收", options: { fill: { color: "4472C4" }, color: "FFFFFF", bold: true } },
        { text: "成長", options: { fill: { color: "4472C4" }, color: "FFFFFF", bold: true } }
    ],
    // 資料列
    ["產品 A", "$50M", "+15%"],
    ["產品 B", "$35M", "+22%"],
    ["產品 C", "$28M", "+8%"]
];

slide.addTable(tableData, {
    x: 1,
    y: 1.5,
    w: 8,
    h: 3,
    colW: [3, 2.5, 2.5],  // 欄寬
    rowH: [0.5, 0.6, 0.6, 0.6],  // 列高
    border: { pt: 1, color: "CCCCCC" },
    align: "center",
    valign: "middle",
    fontSize: 14
});
```

#### 帶合併儲存格的表格

```javascript
const mergedTableData = [
    [
        { text: "Q1 結果", options: { colspan: 3, fill: { color: "4472C4" }, color: "FFFFFF", bold: true } }
    ],
    ["產品", "銷售", "市場佔有率"],
    ["產品 A", "$25M", "35%"],
    ["產品 B", "$18M", "25%"]
];

slide.addTable(mergedTableData, {
    x: 1,
    y: 1,
    w: 8,
    h: 2.5,
    colW: [3, 2.5, 2.5],
    border: { pt: 1, color: "DDDDDD" }
});
```

### 表格選項

常見表格選項:
- `x, y, w, h` - 位置和尺寸
- `colW` - 欄寬陣列(英吋)
- `rowH` - 列高陣列(英吋)
- `border` - 邊框樣式:`{ pt: 1, color: "999999" }`
- `fill` - 背景顏色(不帶 # 前綴)
- `align` - 文字對齊:"left"、"center"、"right"
- `valign` - 垂直對齊:"top"、"middle"、"bottom"
- `fontSize` - 文字大小
- `autoPage` - 內容溢出時自動建立新投影片
