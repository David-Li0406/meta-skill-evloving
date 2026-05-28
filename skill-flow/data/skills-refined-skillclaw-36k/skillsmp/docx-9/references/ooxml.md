# Office Open XML 技術リファレンス

DOCXファイルを直接操作するための技術仕様書。

## 基本構造

DOCXファイルはZIPアーカイブで、以下の構造を持つ：

```
docx/
├── [Content_Types].xml
├── _rels/
│   └── .rels
├── word/
│   ├── document.xml      # メインコンテンツ
│   ├── styles.xml        # スタイル定義
│   ├── numbering.xml     # 番号付け定義
│   ├── settings.xml      # 文書設定
│   ├── fontTable.xml     # フォントテーブル
│   ├── _rels/
│   │   └── document.xml.rels
│   └── media/           # 画像など
└── docProps/
    ├── app.xml
    └── core.xml
```

## XML名前空間

```xml
xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"
```

## 要素順序（厳格）

`<w:pPr>`（段落プロパティ）内の要素順序：

1. `<w:pStyle>`
2. `<w:numPr>`
3. `<w:spacing>`
4. `<w:ind>`
5. `<w:jc>`

## 基本パターン

### 段落

```xml
<w:p>
    <w:pPr>
        <w:jc w:val="center"/>
    </w:pPr>
    <w:r>
        <w:t>テキスト</w:t>
    </w:r>
</w:p>
```

### 見出し

```xml
<w:p>
    <w:pPr>
        <w:pStyle w:val="Heading1"/>
        <w:jc w:val="center"/>
    </w:pPr>
    <w:r>
        <w:t>見出しテキスト</w:t>
    </w:r>
</w:p>
```

### テキストフォーマット

```xml
<!-- 太字 -->
<w:r>
    <w:rPr><w:b/></w:rPr>
    <w:t>太字</w:t>
</w:r>

<!-- 斜体 -->
<w:r>
    <w:rPr><w:i/></w:rPr>
    <w:t>斜体</w:t>
</w:r>

<!-- 下線 -->
<w:r>
    <w:rPr><w:u w:val="single"/></w:rPr>
    <w:t>下線</w:t>
</w:r>

<!-- ハイライト -->
<w:r>
    <w:rPr><w:highlight w:val="yellow"/></w:rPr>
    <w:t>ハイライト</w:t>
</w:r>

<!-- フォント変更 -->
<w:r>
    <w:rPr>
        <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
        <w:sz w:val="24"/>  <!-- ハーフポイント -->
    </w:rPr>
    <w:t>テキスト</w:t>
</w:r>
```

### リスト

```xml
<!-- 番号付きリスト -->
<w:p>
    <w:pPr>
        <w:numPr>
            <w:ilvl w:val="0"/>
            <w:numId w:val="1"/>
        </w:numPr>
    </w:pPr>
    <w:r><w:t>項目1</w:t></w:r>
</w:p>

<!-- 箇条書き -->
<w:p>
    <w:pPr>
        <w:numPr>
            <w:ilvl w:val="0"/>
            <w:numId w:val="2"/>
        </w:numPr>
    </w:pPr>
    <w:r><w:t>項目</w:t></w:r>
</w:p>
```

### テーブル

```xml
<w:tbl>
    <w:tblPr>
        <w:tblW w:w="5000" w:type="pct"/>
    </w:tblPr>
    <w:tblGrid>
        <w:gridCol w:w="2500"/>
        <w:gridCol w:w="2500"/>
    </w:tblGrid>
    <w:tr>
        <w:tc>
            <w:tcPr>
                <w:tcW w:w="2500" w:type="dxa"/>
            </w:tcPr>
            <w:p><w:r><w:t>セル1</w:t></w:r></w:p>
        </w:tc>
        <w:tc>
            <w:tcPr>
                <w:tcW w:w="2500" w:type="dxa"/>
            </w:tcPr>
            <w:p><w:r><w:t>セル2</w:t></w:r></w:p>
        </w:tc>
    </w:tr>
</w:tbl>
```

### ページブレイク

```xml
<w:p>
    <w:r>
        <w:br w:type="page"/>
    </w:r>
</w:p>
```

## Unicode エスケープ

特殊文字はエスケープが必要：

| 文字 | エスケープ |
|------|-----------|
| " " | `&#8220;` `&#8221;` |
| ' | `&#8217;` |
| — | `&#8212;` |
| – | `&#8211;` |
| … | `&#8230;` |

## 変更履歴（Tracked Changes）

### 挿入

```xml
<w:ins w:id="1" w:author="Author" w:date="2024-01-01T00:00:00Z">
    <w:r>
        <w:t>挿入されたテキスト</w:t>
    </w:r>
</w:ins>
```

### 削除

```xml
<w:del w:id="2" w:author="Author" w:date="2024-01-01T00:00:00Z">
    <w:r>
        <w:delText>削除されたテキスト</w:delText>
    </w:r>
</w:del>
```

### 重要なルール

1. **他の著者の変更内を編集しない**: 代わりに、その挿入の中に削除構造をネストする
2. **元のテキストを保持**: 変更を元に戻した後、文書テキストが元のものと一致することを検証
3. **RSID管理**: 各編集セッションには一意のRSID値を使用

### Documentライブラリの使用

```python
from scripts.document import Document

# 文書を初期化
doc = Document(
    unpacked_dir="./unpacked",
    author="Claude",
    author_initials="C",
    rsid="12345678"
)

# 挿入を削除に変換（revert）
doc.revert_insertion(node)

# 削除を挿入に変換（reject）
doc.revert_deletion(node)

# 削除を提案
doc.suggest_deletion(node)

# 保存
doc.save()
```

## 画像

画像を追加するには：

1. `word/media/` にファイルを配置
2. `word/_rels/document.xml.rels` にリレーションシップを追加
3. `[Content_Types].xml` にコンテンツタイプを追加
4. `document.xml` に参照を追加

```xml
<!-- document.xml.rels -->
<Relationship Id="rId10"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    Target="media/image1.png"/>

<!-- document.xml -->
<w:drawing>
    <wp:inline>
        <wp:extent cx="1000000" cy="1000000"/>  <!-- EMU単位 -->
        <a:graphic>
            <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
                <pic:pic>
                    <pic:blipFill>
                        <a:blip r:embed="rId10"/>
                    </pic:blipFill>
                </pic:pic>
            </a:graphicData>
        </a:graphic>
    </wp:inline>
</w:drawing>
```

**EMU計算**: 1インチ = 914400 EMU

## ハイパーリンク

### 外部リンク

```xml
<!-- document.xml.rels -->
<Relationship Id="rId20"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
    Target="https://example.com" TargetMode="External"/>

<!-- document.xml -->
<w:hyperlink r:id="rId20">
    <w:r>
        <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
        <w:t>リンクテキスト</w:t>
    </w:r>
</w:hyperlink>
```

### 内部リンク（ブックマーク）

```xml
<!-- ブックマーク定義 -->
<w:bookmarkStart w:id="0" w:name="section1"/>
<w:r><w:t>セクション1</w:t></w:r>
<w:bookmarkEnd w:id="0"/>

<!-- ブックマークへのリンク -->
<w:hyperlink w:anchor="section1">
    <w:r>
        <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
        <w:t>セクション1へ</w:t>
    </w:r>
</w:hyperlink>
```

## コメント

```xml
<!-- comments.xml -->
<w:comment w:id="1" w:author="Author" w:date="2024-01-01T00:00:00Z">
    <w:p>
        <w:r><w:t>コメントテキスト</w:t></w:r>
    </w:p>
</w:comment>

<!-- document.xml -->
<w:commentRangeStart w:id="1"/>
<w:r><w:t>コメント対象テキスト</w:t></w:r>
<w:commentRangeEnd w:id="1"/>
<w:r>
    <w:commentReference w:id="1"/>
</w:r>
```

## 検証

```bash
# スキーマ検証と変更履歴検証
python ${CLAUDE_PLUGIN_ROOT}/skills/docx/ooxml/scripts/validate.py <unpacked_dir> --original <original.docx>
```
