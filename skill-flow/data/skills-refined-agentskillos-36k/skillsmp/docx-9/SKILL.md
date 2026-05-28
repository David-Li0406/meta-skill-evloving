---
name: docx
description: |
  このスキルは、ユーザーが「Word文書を作成」「DOCXを編集」「文書に変更履歴を追加」「Word文書からテキストを抽出」「DOCXを分析」「Wordテンプレートを使用」「文書を比較」などを要求した際に使用する。
---

# Word文書（DOCX）処理スキル

Word文書（.docx）の作成、編集、分析機能を提供する。DOCXファイルはXML構造を含むZIPアーカイブである。

## 依存関係

```bash
# コマンドラインツール
brew install pandoc  # macOS
apt-get install pandoc libreoffice  # Ubuntu/Debian

# Pythonライブラリ
pip install defusedxml

# Node.js ライブラリ
npm install docx
```

## 主要ワークフロー

### 1. テキスト読み取り

```bash
# Markdownに変換（変更履歴を保持）
pandoc --track-changes=all file.docx -o output.md
```

### 2. 新規文書作成

`references/docx-js.md` を**必ず読んでから**、docx-jsライブラリを使用する。

```typescript
import { Document, Paragraph, TextRun, Packer } from 'docx';
import * as fs from 'fs';

const doc = new Document({
    sections: [{
        children: [
            new Paragraph({
                children: [
                    new TextRun({ text: "見出し", bold: true, size: 28 }),
                ],
            }),
            new Paragraph({
                children: [
                    new TextRun("本文テキスト"),
                ],
            }),
        ],
    }],
});

Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("output.docx", buffer);
});
```

### 3. 既存文書の編集

`references/ooxml.md` を**必ず読んでから**、以下の手順で編集する：

1. **展開**: `python ${CLAUDE_PLUGIN_ROOT}/skills/docx/ooxml/scripts/unpack.py <file.docx> <dir>`
2. **編集**: Documentライブラリで `word/document.xml` を編集
3. **パック**: `python ${CLAUDE_PLUGIN_ROOT}/skills/docx/ooxml/scripts/pack.py <dir> <output.docx>`

### 4. 変更履歴（Redlining）

変更履歴付きの編集を行う場合、`references/ooxml.md` のTracked Changes実装セクションを参照。

**重要なルール**:
- 変更されるテキストのみをマーク
- 変更されない `<w:r>` 要素は保持
- 関連する変更を3〜10個のバッチにグループ化
- 編集前に `document.xml` を grep で確認

## クリティカルな原則

1. **最小限の編集**: 実際に変更されるテキストのみをマークする
2. **バッチ戦略**: 関連する変更をセクション、タイプ、または位置でグループ化
3. **検証**: スクリプト作成前に document.xml を grep、実装後に全変更を検証

## 詳細リファレンス

- JavaScript docxライブラリ: `references/docx-js.md`
- Office Open XML技術仕様: `references/ooxml.md`

## クイックリファレンス

| 操作 | ツール/方法 |
|------|-------------|
| テキスト抽出 | `pandoc` |
| 新規作成 | `docx` (npm) |
| 既存編集 | OOXML + Documentライブラリ |
| 変更履歴 | Documentライブラリ |
| 検証 | `validate.py` |

## スクリプト一覧

| スクリプト | 説明 |
|-----------|------|
| `ooxml/scripts/unpack.py` | DOCXをディレクトリに展開 |
| `ooxml/scripts/pack.py` | ディレクトリをDOCXにパック |
| `ooxml/scripts/validate.py` | XSDスキーマと変更履歴を検証 |
| `scripts/utilities.py` | XML編集ユーティリティ |
| `scripts/document.py` | 変更履歴・コメント管理 |
