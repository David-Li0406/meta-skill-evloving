# docx-js ライブラリチュートリアル

JavaScript/TypeScript で .docx ファイルを生成するためのガイド。

## セットアップ

```bash
npm install docx
```

```typescript
import {
    Document,
    Packer,
    Paragraph,
    TextRun,
    HeadingLevel,
    Table,
    TableRow,
    TableCell,
    WidthType,
    BorderStyle,
    AlignmentType,
    NumberFormat,
    LevelFormat,
    ImageRun,
    ExternalHyperlink,
    InternalHyperlink,
    Bookmark,
    PageBreak,
    Header,
    Footer,
    TableOfContents,
    ShadingType,
} from 'docx';
```

## テキストフォーマット

```typescript
new Paragraph({
    children: [
        new TextRun({ text: "太字", bold: true }),
        new TextRun({ text: "斜体", italics: true }),
        new TextRun({ text: "下線", underline: {} }),
        new TextRun({ text: "取り消し線", strike: true }),
        new TextRun({ text: "上付き", superScript: true }),
        new TextRun({ text: "下付き", subScript: true }),
        new TextRun({
            text: "カラーテキスト",
            color: "FF0000",
            highlight: "yellow",
        }),
    ],
});
```

**重要**: 改行には `\n` ではなく、別の `Paragraph` を使用する。

## スタイリング

### 見出し

```typescript
new Paragraph({
    text: "見出し1",
    heading: HeadingLevel.HEADING_1,
});

new Paragraph({
    text: "見出し2",
    heading: HeadingLevel.HEADING_2,
});
```

### カスタムスタイル

```typescript
const doc = new Document({
    styles: {
        paragraphStyles: [
            {
                id: "myStyle",
                name: "My Style",
                basedOn: "Normal",
                next: "Normal",
                run: {
                    font: "Arial",
                    size: 24,  // ハーフポイント単位（12pt = 24）
                    color: "333333",
                },
                paragraph: {
                    spacing: { after: 200 },
                },
            },
        ],
    },
    sections: [{ children: [
        new Paragraph({
            text: "カスタムスタイルのテキスト",
            style: "myStyle",
        }),
    ]}],
});
```

**推奨フォント**: Arial（デフォルト）

## リスト

```typescript
const doc = new Document({
    numbering: {
        config: [
            {
                reference: "bullet-list",
                levels: [
                    {
                        level: 0,
                        format: LevelFormat.BULLET,
                        text: "\u2022",  // 弾丸記号
                        alignment: AlignmentType.LEFT,
                    },
                ],
            },
            {
                reference: "number-list",
                levels: [
                    {
                        level: 0,
                        format: LevelFormat.DECIMAL,
                        text: "%1.",
                        alignment: AlignmentType.LEFT,
                    },
                ],
            },
        ],
    },
    sections: [{
        children: [
            new Paragraph({
                text: "項目1",
                numbering: { reference: "bullet-list", level: 0 },
            }),
            new Paragraph({
                text: "項目2",
                numbering: { reference: "bullet-list", level: 0 },
            }),
        ],
    }],
});
```

**重要**: Unicode記号ではなく、`LevelFormat.BULLET` を使用する。異なる `reference` は独立したリストになる。

## テーブル

```typescript
new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
        new TableRow({
            children: [
                new TableCell({
                    width: { size: 3000, type: WidthType.DXA },  // DXA = 1/20ポイント
                    children: [new Paragraph("セル1")],
                    shading: {
                        type: ShadingType.CLEAR,  // 必須
                        fill: "CCCCCC",
                    },
                    borders: {
                        top: { style: BorderStyle.SINGLE, size: 1 },
                        bottom: { style: BorderStyle.SINGLE, size: 1 },
                        left: { style: BorderStyle.SINGLE, size: 1 },
                        right: { style: BorderStyle.SINGLE, size: 1 },
                    },
                    margins: {
                        top: 100,
                        bottom: 100,
                        left: 100,
                        right: 100,
                    },
                }),
                new TableCell({
                    width: { size: 3000, type: WidthType.DXA },
                    children: [new Paragraph("セル2")],
                }),
            ],
        }),
    ],
});
```

**重要**: `shading` には `type: ShadingType.CLEAR` が必須。

## 画像

```typescript
import * as fs from 'fs';

new Paragraph({
    children: [
        new ImageRun({
            data: fs.readFileSync("image.png"),
            transformation: {
                width: 200,
                height: 150,
            },
            type: "png",  // 必須: "png", "jpg", "gif", "bmp"
        }),
    ],
});
```

**重要**: `type` パラメータは必須。

## ハイパーリンク

### 外部リンク

```typescript
new Paragraph({
    children: [
        new ExternalHyperlink({
            children: [
                new TextRun({
                    text: "Googleへ",
                    style: "Hyperlink",
                }),
            ],
            link: "https://google.com",
        }),
    ],
});
```

### 内部リンク（ブックマーク）

```typescript
// ブックマークを設定
new Paragraph({
    children: [
        new Bookmark({
            id: "section1",
            children: [new TextRun("セクション1")],
        }),
    ],
});

// ブックマークへのリンク
new Paragraph({
    children: [
        new InternalHyperlink({
            children: [new TextRun({ text: "セクション1へ", style: "Hyperlink" })],
            anchor: "section1",
        }),
    ],
});
```

## 目次

```typescript
const doc = new Document({
    features: {
        updateFields: true,  // Word起動時に更新
    },
    sections: [{
        children: [
            new TableOfContents("目次", {
                hyperlink: true,
                headingStyleRange: "1-3",
            }),
            new Paragraph({
                text: "章1",
                heading: HeadingLevel.HEADING_1,  // カスタムスタイルは追加しない
            }),
        ],
    }],
});
```

**重要**: TOCには `HeadingLevel` スタイルを使用。カスタムスタイルを追加しない。

## ヘッダー・フッター

```typescript
const doc = new Document({
    sections: [{
        headers: {
            default: new Header({
                children: [new Paragraph("ヘッダーテキスト")],
            }),
        },
        footers: {
            default: new Footer({
                children: [new Paragraph("フッターテキスト")],
            }),
        },
        children: [new Paragraph("本文")],
    }],
});
```

## ページブレイク

```typescript
new Paragraph({
    children: [new PageBreak()],
});
```

**重要**: `PageBreak` は `Paragraph` の中にネストする必要がある。

## ファイル保存

```typescript
import * as fs from 'fs';

Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("output.docx", buffer);
});

// または Base64
Packer.toBase64String(doc).then((base64) => {
    console.log(base64);
});
```

## よくある間違い

| 間違い | 正しい方法 |
|--------|-----------|
| `PageBreak` を直接使用 | `Paragraph` の中にネスト |
| `shading` で `type` を省略 | `ShadingType.CLEAR` を指定 |
| `ImageRun` で `type` を省略 | ファイルタイプを明示 |
| TOCでカスタムスタイル | `HeadingLevel` のみ使用 |
| Unicode弾丸を使用 | `LevelFormat.BULLET` を使用 |
