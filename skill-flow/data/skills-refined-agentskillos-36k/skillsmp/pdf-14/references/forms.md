# PDFフォーム記入ガイド

PDFフォームの記入には2つのパスがある。最初にフォームタイプを判定し、適切なパスを選択する。

## 初期判定

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/check_fillable_fields.py <file.pdf>
```

## パス1: フィル可能フィールドがある場合

インタラクティブなフォームフィールドを持つPDFの場合。

### ステップ1: フィールド情報の抽出

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/extract_form_field_info.py input.pdf fields.json
```

出力される `fields.json` の形式：
```json
[
  {
    "field_id": "name",
    "page": 1,
    "type": "text",
    "rect": [100, 700, 300, 720]
  },
  {
    "field_id": "agree",
    "page": 1,
    "type": "checkbox",
    "checked_value": "/Yes",
    "unchecked_value": "/Off"
  },
  {
    "field_id": "gender",
    "page": 1,
    "type": "radio_group",
    "radio_options": [
      {"value": "/Male", "rect": [100, 600, 120, 620]},
      {"value": "/Female", "rect": [150, 600, 170, 620]}
    ]
  }
]
```

### ステップ2: 値を設定

`field_values.json` を作成：
```json
[
  {"field_id": "name", "page": 1, "value": "山田太郎"},
  {"field_id": "agree", "page": 1, "value": "/Yes"},
  {"field_id": "gender", "page": 1, "value": "/Male"}
]
```

### ステップ3: フォームを記入

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/fill_fillable_fields.py input.pdf field_values.json output.pdf
```

## パス2: フィル可能フィールドがない場合

フォームフィールドが埋め込まれていないPDFの場合、テキストアノテーションとして追加する。

### ステップ1: PDFを画像に変換

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/convert_pdf_to_images.py input.pdf ./images/
```

### ステップ2: 視覚解析でフィールド位置を特定

画像を分析し、各入力フィールドの位置を特定する。以下の情報が必要：

- ページ番号
- ラベルのバウンディングボックス（青枠で表示）
- 入力エリアのバウンディングボックス（赤枠で表示）
- フィールドの説明

### ステップ3: fields.json の作成

```json
{
  "pages": [
    {
      "page_number": 1,
      "image_width": 1000,
      "image_height": 1414
    }
  ],
  "form_fields": [
    {
      "page_number": 1,
      "description": "氏名フィールド",
      "label_bounding_box": [50, 100, 100, 120],
      "entry_bounding_box": [110, 100, 300, 120],
      "entry_text": {
        "text": "山田太郎",
        "font": "Arial",
        "font_size": 12,
        "font_color": "000000"
      }
    }
  ]
}
```

**バウンディングボックス形式**: `[left, top, right, bottom]`（画像座標系、左上原点）

### ステップ4: バウンディングボックスの検証

```bash
# 自動チェック
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/check_bounding_boxes.py fields.json

# 視覚的検証画像の生成
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/create_validation_image.py 1 fields.json ./images/page_1.png validation.png
```

検証画像を確認：
- 赤い矩形が入力エリアのみをカバーしているか
- 青い矩形がラベルのみをカバーしているか
- 矩形同士が重なっていないか

### ステップ5: PDFにアノテーションを追加

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/pdf/scripts/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```

## 重要な注意事項

### バウンディングボックスのルール

1. **重複禁止**: ラベルと入力エリアのボックスは重なってはいけない
2. **高さ制限**: 入力ボックスの高さはフォントサイズより大きくする必要がある
3. **座標系**: 画像座標（左上原点）を使用、PDF座標（左下原点）ではない

### トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| テキストが切れる | `entry_bounding_box` を広げる |
| フォントサイズエラー | `font_size` を小さくするか、ボックスを高くする |
| 位置がずれる | 画像サイズ（`image_width`, `image_height`）を確認 |
| チェックボックスが動かない | `checked_value` の正確な値を使用（`/Yes` など） |

### フィールドタイプ別の値設定

| タイプ | 値の例 |
|--------|--------|
| text | `"任意のテキスト"` |
| checkbox | `"/Yes"`, `"/Off"` |
| radio_group | 選択肢の `value`（例: `"/Option1"`） |
| choice | 選択肢の `value` |
