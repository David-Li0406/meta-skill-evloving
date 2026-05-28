# DOCX 函式庫教學

使用 JavaScript/TypeScript 產生 .docx 檔案。

**重要：開始前請閱讀整份文件。** 關鍵的格式規則和常見陷阱貫穿全文——跳過章節可能導致檔案損壞或渲染問題。

## 設定
假設 docx 已全域安裝
如未安裝：`npm install -g docx`

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Media,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, TableOfContents, HeadingLevel, BorderStyle, WidthType, TabStopType,
        TabStopPosition, UnderlineType, ShadingType, VerticalAlign, SymbolRun, PageNumber,
        FootnoteReferenceRun, Footnote, PageBreak } = require('docx');

// 建立與儲存
const doc = new Document({ sections: [{ children: [/* 內容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer)); // Node.js
Packer.toBlob(doc).then(blob => { /* 下載邏輯 */ }); // 瀏覽器
```

## 文字與格式
```javascript
// 重要：換行永遠不要使用 \n - 請使用獨立的 Paragraph 元素
// ❌ 錯誤：new TextRun("第一行\n第二行")
// ✅ 正確：new Paragraph({ children: [new TextRun("第一行")] }), new Paragraph({ children: [new TextRun("第二行")] })

// 包含所有格式選項的基本文字
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 200 },
  indent: { left: 720, right: 720 },
  children: [
    new TextRun({ text: "粗體", bold: true }),
    new TextRun({ text: "斜體", italics: true }),
    new TextRun({ text: "底線", underline: { type: UnderlineType.DOUBLE, color: "FF0000" } }),
    new TextRun({ text: "有顏色", color: "FF0000", size: 28, font: "Arial" }), // Arial 預設
    new TextRun({ text: "螢光標記", highlight: "yellow" }),
    new TextRun({ text: "刪除線", strike: true }),
    new TextRun({ text: "x2", superScript: true }),
    new TextRun({ text: "H2O", subScript: true }),
    new TextRun({ text: "小型大寫", smallCaps: true }),
    new SymbolRun({ char: "2022", font: "Symbol" }), // 項目符號 •
    new SymbolRun({ char: "00A9", font: "Arial" })   // 版權符號 © - Arial 用於符號
  ]
})
```

## 樣式與專業格式

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt 預設
    paragraphStyles: [
      // 文件標題樣式 - 覆寫內建 Title 樣式
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      // 重要：使用確切的 ID 覆寫內建標題樣式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" }, // 16pt
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // 目錄必要
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" }, // 14pt
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
      // 自訂樣式使用您自己的 ID
      { id: "myStyle", name: "My Style", basedOn: "Normal",
        run: { size: 28, bold: true, color: "000000" },
        paragraph: { spacing: { after: 120 }, alignment: AlignmentType.CENTER } }
    ],
    characterStyles: [{ id: "myCharStyle", name: "My Char Style",
      run: { color: "FF0000", bold: true, underline: { type: UnderlineType.SINGLE } } }]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("文件標題")] }), // 使用覆寫的 Title 樣式
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("標題 1")] }), // 使用覆寫的 Heading1 樣式
      new Paragraph({ style: "myStyle", children: [new TextRun("自訂段落樣式")] }),
      new Paragraph({ children: [
        new TextRun("一般文字包含 "),
        new TextRun({ text: "自訂字元樣式", style: "myCharStyle" })
      ]})
    ]
  }]
});
```

**專業字型組合：**
- **Arial（標題）+ Arial（內文）** - 最普遍支援，乾淨且專業
- **Times New Roman（標題）+ Arial（內文）** - 經典襯線標題搭配現代無襯線內文
- **Georgia（標題）+ Verdana（內文）** - 針對螢幕閱讀優化，優雅對比

**關鍵樣式原則：**
- **覆寫內建樣式**：使用確切的 ID 如 "Heading1"、"Heading2"、"Heading3" 來覆寫 Word 內建的標題樣式
- **HeadingLevel 常數**：`HeadingLevel.HEADING_1` 使用 "Heading1" 樣式，`HeadingLevel.HEADING_2` 使用 "Heading2" 樣式，依此類推
- **包含 outlineLevel**：設定 H1 為 `outlineLevel: 0`，H2 為 `outlineLevel: 1`，依此類推以確保目錄正常運作
- **使用自訂樣式**而非行內格式以保持一致性
- **設定預設字型**使用 `styles.default.document.run.font` - Arial 是普遍支援的
- **建立視覺層級**使用不同字型大小（標題 > 子標題 > 內文）
- **新增適當間距**使用 `before` 和 `after` 段落間距
- **謹慎使用顏色**：標題和各級標題（標題 1、標題 2 等）預設使用黑色（000000）和灰色調
- **設定一致的邊界**（1440 = 1 英吋是標準）


## 清單（務必使用正式清單 - 絕不使用 Unicode 項目符號）
```javascript
// 項目符號 - 務必使用 numbering 設定，不要用 unicode 符號
// 關鍵：使用 LevelFormat.BULLET 常數，不是 "bullet" 字串
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullet-list",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "first-numbered-list",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "second-numbered-list", // 不同的 reference = 從 1 重新開始
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    children: [
      // 項目符號清單項目
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("第一個項目")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("第二個項目")] }),
      // 編號清單項目
      new Paragraph({ numbering: { reference: "first-numbered-list", level: 0 },
        children: [new TextRun("第一個編號項目")] }),
      new Paragraph({ numbering: { reference: "first-numbered-list", level: 0 },
        children: [new TextRun("第二個編號項目")] }),
      // ⚠️ 關鍵：不同的 reference = 獨立的清單，從 1 重新開始
      // 相同的 reference = 延續之前的編號
      new Paragraph({ numbering: { reference: "second-numbered-list", level: 0 },
        children: [new TextRun("重新從 1 開始（因為使用不同的 reference）")] })
    ]
  }]
});

// ⚠️ 關鍵編號規則：每個 reference 建立一個獨立的編號清單
// - 相同的 reference = 延續編號（1, 2, 3... 然後 4, 5, 6...）
// - 不同的 reference = 從 1 重新開始（1, 2, 3... 然後 1, 2, 3...）
// 為每個獨立的編號區段使用唯一的 reference 名稱！

// ⚠️ 關鍵：絕不使用 unicode 項目符號 - 它們會建立無法正常運作的假清單
// new TextRun("• 項目")           // 錯誤
// new SymbolRun({ char: "2022" }) // 錯誤
// ✅ 務必使用 LevelFormat.BULLET 的 numbering 設定來建立真正的 Word 清單
```

## 表格
```javascript
// 包含邊界、框線、標題和項目符號的完整表格
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

new Table({
  columnWidths: [4680, 4680], // ⚠️ 關鍵：在表格層級設定欄寬 - 數值單位為 DXA（點的二十分之一）
  margins: { top: 100, bottom: 100, left: 180, right: 180 }, // 為所有儲存格設定一次
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同時在每個儲存格設定寬度
          // ⚠️ 關鍵：務必使用 ShadingType.CLEAR 以防止 Word 中出現黑色背景
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "標題", bold: true, size: 22 })]
          })]
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同時在每個儲存格設定寬度
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "項目符號", bold: true, size: 22 })]
          })]
        })
      ]
    }),
    new TableRow({
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同時在每個儲存格設定寬度
          children: [new Paragraph({ children: [new TextRun("一般資料")] })]
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 同時在每個儲存格設定寬度
          children: [
            new Paragraph({
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("第一個項目")]
            }),
            new Paragraph({
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("第二個項目")]
            })
          ]
        })
      ]
    })
  ]
})
```

**重要：表格寬度與框線**
- 同時使用 `columnWidths: [width1, width2, ...]` 陣列和每個儲存格的 `width: { size: X, type: WidthType.DXA }`
- 數值單位為 DXA（點的二十分之一）：1440 = 1 英吋，Letter 可用寬度 = 9360 DXA（1 英吋邊界）
- 將框線套用至個別 `TableCell` 元素，而非 `Table` 本身

**預先計算的欄寬（Letter 尺寸含 1 英吋邊界 = 總共 9360 DXA）：**
- **2 欄：** `columnWidths: [4680, 4680]`（等寬）
- **3 欄：** `columnWidths: [3120, 3120, 3120]`（等寬）

## 連結與導航
```javascript
// 目錄（需要標題）- 關鍵：只使用 HeadingLevel，不使用自訂樣式
// ❌ 錯誤：new Paragraph({ heading: HeadingLevel.HEADING_1, style: "customHeader", children: [new TextRun("標題")] })
// ✅ 正確：new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("標題")] })
new TableOfContents("目錄", { hyperlink: true, headingStyleRange: "1-3" }),

// 外部連結
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Google", style: "Hyperlink" })],
    link: "https://www.google.com"
  })]
}),

// 內部連結與書籤
new Paragraph({
  children: [new InternalHyperlink({
    children: [new TextRun({ text: "前往章節", style: "Hyperlink" })],
    anchor: "section1"
  })]
}),
new Paragraph({
  children: [new TextRun("章節內容")],
  bookmark: { id: "section1", name: "section1" }
}),
```

## 圖片與媒體
```javascript
// 包含尺寸和定位的基本圖片
// 關鍵：務必指定 'type' 參數 - 這是 ImageRun 必要的
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new ImageRun({
    type: "png", // 新要求：必須指定圖片類型（png、jpg、jpeg、gif、bmp、svg）
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150, rotation: 0 }, // 旋轉角度
    altText: { title: "標誌", description: "公司標誌", name: "名稱" } // 重要：三個欄位都是必要的
  })]
})
```

## 分頁符號
```javascript
// 手動分頁符號
new Paragraph({ children: [new PageBreak()] }),

// 段落前分頁符號
new Paragraph({
  pageBreakBefore: true,
  children: [new TextRun("這將從新頁面開始")]
})

// ⚠️ 關鍵：絕不單獨使用 PageBreak - 這會建立 Word 無法開啟的無效 XML
// ❌ 錯誤：new PageBreak()
// ✅ 正確：new Paragraph({ children: [new PageBreak()] })
```

## 頁首/頁尾與頁面設定
```javascript
const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, // 1440 = 1 英吋
        size: { orientation: PageOrientation.LANDSCAPE },
        pageNumbers: { start: 1, formatType: "decimal" } // "upperRoman"、"lowerRoman"、"upperLetter"、"lowerLetter"
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun("頁首文字")]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun("第 "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" 頁，共 "), new TextRun({ children: [PageNumber.TOTAL_PAGES] }), new TextRun(" 頁")]
      })] })
    },
    children: [/* 內容 */]
  }]
});
```

## 定位點
```javascript
new Paragraph({
  tabStops: [
    { type: TabStopType.LEFT, position: TabStopPosition.MAX / 4 },
    { type: TabStopType.CENTER, position: TabStopPosition.MAX / 2 },
    { type: TabStopType.RIGHT, position: TabStopPosition.MAX * 3 / 4 }
  ],
  children: [new TextRun("靠左\t置中\t靠右")]
})
```

## 常數與快速參考
- **底線：** `SINGLE`、`DOUBLE`、`WAVY`、`DASH`
- **框線：** `SINGLE`、`DOUBLE`、`DASHED`、`DOTTED`
- **編號：** `DECIMAL`（1,2,3）、`UPPER_ROMAN`（I,II,III）、`LOWER_LETTER`（a,b,c）
- **定位點：** `LEFT`、`CENTER`、`RIGHT`、`DECIMAL`
- **符號：** `"2022"`（•）、`"00A9"`（©）、`"00AE"`（®）、`"2122"`（™）、`"00B0"`（°）、`"F070"`（✓）、`"F0FC"`（✗）

## 關鍵問題與常見錯誤
- **關鍵：PageBreak 必須永遠在 Paragraph 內** - 單獨的 PageBreak 會建立 Word 無法開啟的無效 XML
- **務必使用 ShadingType.CLEAR 設定表格儲存格底色** - 絕不使用 ShadingType.SOLID（會導致黑色背景）
- 測量單位為 DXA（1440 = 1 英吋）| 每個表格儲存格需要至少 1 個 Paragraph | 目錄只需要 HeadingLevel 樣式
- **務必使用自訂樣式**搭配 Arial 字型以呈現專業外觀和適當的視覺層級
- **務必設定預設字型**使用 `styles.default.document.run.font` - 建議使用 Arial
- **務必使用 columnWidths 陣列設定表格**加上個別儲存格寬度以確保相容性
- **絕不使用 unicode 符號作為項目符號** - 務必使用正式的 numbering 設定搭配 `LevelFormat.BULLET` 常數（不是 "bullet" 字串）
- **絕不在任何地方使用 \n 換行** - 務必使用獨立的 Paragraph 元素來換行
- **務必在 Paragraph children 中使用 TextRun 物件** - 絕不直接在 Paragraph 上使用 text 屬性
- **關鍵 - 圖片**：ImageRun 必須要有 `type` 參數 - 務必指定 "png"、"jpg"、"jpeg"、"gif"、"bmp" 或 "svg"
- **關鍵 - 項目符號**：必須使用 `LevelFormat.BULLET` 常數，不是 "bullet" 字串，並包含 `text: "•"` 作為項目符號字元
- **關鍵 - 編號**：每個 numbering reference 會建立一個獨立的清單。相同 reference = 延續編號（1,2,3 然後 4,5,6）。不同 reference = 從 1 重新開始（1,2,3 然後 1,2,3）。為每個獨立的編號區段使用唯一的 reference 名稱！
- **關鍵 - 目錄**：使用 TableOfContents 時，標題必須只使用 HeadingLevel - 不要在標題段落加入自訂樣式，否則目錄會損壞
- **表格**：設定 `columnWidths` 陣列加上個別儲存格寬度，將框線套用至儲存格而非表格
- **在表格層級設定表格邊界**以獲得一致的儲存格內距（避免每個儲存格重複設定）
