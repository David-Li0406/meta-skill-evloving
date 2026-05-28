# Figma フレーム作成ルール

## フレーム命名規則

### ページ構造（ルートレベル）

```
Header, Sidebar, Main, Aside, Footer
```

### セクション構造（機能名 + 構造名）

```
PostHeader, PostBody, PostFooter, PostActions
CardHeader, CardBody, CardFooter
```

- ルートレベル以外は親要素名をプレフィックスに付ける
- `Body` に統一（`Content` は使わない）

### リスト構造（HogeList パターン）

```
MemberList > MemberListItem
PostList > PostListItem
```

### テーブル構造

```
Table > TableHeader / TableBody > TableRow > TableCell
MemberTable > MemberTableHeader / MemberTableBody > ...
```

### グループ（複数形）

単純なグループのみ複数形を使用:

```
Buttons, Icons, Avatars, Tags
```

### Margin Container

margin の再現には `MC_` プレフィックスを使用:

```
MC_Title, MC_BodyText, MC_Footer
```

### 避けるべきパターン

| NG | 理由 | 代替案 |
|----|------|--------|
| `Container` (単独) | 何を含むか不明 | `MemberContainer` や具体的な名前 |
| `Right`, `Left`, `Top`, `Bottom` | 位置依存でレイアウト変更に弱い | `Aside`, `SubColumn`, `InfoPanel` |
| `Content` / `Body` 混在 | 一貫性がない | `Body` に統一 |
| `Wrapper`, `Box`, `Item` (単独) | 曖昧 | 具体的な名前を付ける |
| `Btn`, `Hdr`, `Txt` など略語 | 可読性が低い | `Button`, `Header`, `Text` |
| `Header1`, `Button2` など連番 | 意味が不明 | 役割名を付ける |
| `BlueButton`, `LargeText` | スタイル依存 | `PrimaryButton`, `Title` など役割名 |
| `Header > Header` (同名ネスト) | 混乱する | 親名をプレフィックスに |

**例外**: `Container` や位置名はどうしても必要な場合は使用可

---

## 重要: スクリプト出力値をそのまま使う

`extract-ui.js` の出力は **Figma 形式に変換済み**。取得した値をそのまま使用する:

```javascript
// スクリプトの出力例
{
  styles: {
    backgroundColor: { r: 0.122, g: 0.145, b: 0.149 },  // そのまま fillColor に使用
    color: { r: 0.122, g: 0.145, b: 0.149, a: 0.65 },   // そのまま fontColor に使用
    fontSize: 15,           // そのまま fontSize に使用
    fontWeight: 600,        // そのまま fontWeight に使用
    layoutMode: "VERTICAL", // そのまま layoutMode に使用
    paddingTop: 20,         // そのまま paddingTop に使用
    gap: 8,                 // そのまま itemSpacing に使用
    // ...
  }
}

// Figma API への適用
create_frame({
  fillColor: styles.backgroundColor,  // 変換不要
  layoutMode: styles.layoutMode,      // 変換不要
  paddingTop: styles.paddingTop,      // 変換不要
  itemSpacing: styles.gap,            // gap → itemSpacing
})

create_text({
  fontSize: styles.fontSize,          // 変換不要
  fontWeight: styles.fontWeight,      // 変換不要
  fontColor: styles.color,            // 変換不要
})
```

## Auto Layout 設定

| CSS                    | Figma layoutMode |
| ---------------------- | ---------------- |
| flex-direction: column | VERTICAL         |
| flex-direction: row    | HORIZONTAL       |

### 重要: Auto Layout フレーム作成時の初期化

スタイルを設定する前に、必ず以下の値をリセットしてから設定すること:

```javascript
// フレーム作成時にデフォルト値をリセット
create_frame({
  name: "フレーム名",
  layoutMode: "VERTICAL",
  itemSpacing: 0,      // gap をリセット
  paddingTop: 0,       // padding をリセット
  paddingRight: 0,
  paddingBottom: 0,
  paddingLeft: 0
  // fillColor, strokeColor は指定しなければデフォルトで透明
})

// その後、必要なスタイルを設定
set_item_spacing({ nodeId: "ID", itemSpacing: 8 })  // 実際の gap
set_padding({ nodeId: "ID", paddingTop: 16, ... })  // 実際の padding
set_fill_color({ nodeId: "ID", r: 1, g: 1, b: 1 })  // 実際の fill
```

## Sizing ルール（fill 優先）

- 親が auto layout の子要素: `layoutSizingHorizontal: FILL`
- 高さは内容に応じる: `layoutSizingVertical: HUG`
- 固定サイズが必要な場合のみ: `FIXED`

**注意**: `create_frame` 時に FILL は設定できない。作成後に `set_layout_sizing` で設定。

## Margin の再現

CSS の margin は `MC_<要素名>` という命名規則のフレームで再現する。
MC (Margin Container) は **margin をつける要素の親フレーム** として作成し、margin の値を padding として設定する。

**命名規則:**
- 囲う要素が `Title` → `MC_Title`
- 囲う要素が `BodyText` → `MC_BodyText`
- 囲う要素が `Footer` → `MC_Footer`

**構造:**

```
MC_Title (auto layout, HUG)
  └── Title
```

**設定:**

- layoutMode: 親の方向に合わせる（VERTICAL or HORIZONTAL）
- layoutSizingHorizontal: FILL
- layoutSizingVertical: HUG
- padding: margin の値を設定

```javascript
// Title に marginTop: 24px を再現する場合
create_frame({
  name: "MC_Title",
  parentId: "親フレームID",
  layoutMode: "VERTICAL",
  paddingTop: 24  // marginTop の値を paddingTop として設定
})
set_layout_sizing({ layoutSizingHorizontal: "FILL", layoutSizingVertical: "HUG" })

// Title を MC_Title の子として作成
create_text({
  name: "Title",
  parentId: "MC_TitleのID",
  text: "テキスト"
})
```

## テキスト要素

```javascript
create_text({
  text: "テキスト内容",
  fontSize: 15,
  fontWeight: 600,  // Semi Bold
  fontColor: { r: 0.122, g: 0.145, b: 0.149, a: 1 }
})
```

### テキスト折り返し

テキストの幅を制限して折り返しを有効化:

```javascript
resize_node({
  nodeId: "テキストノードID",
  width: 260,  // 親フレームの幅に合わせる
  height: 40   // 行数 × lineHeight
})
```

## 実装例

```javascript
// 1. コンテナ作成
create_frame({
  x: 0, y: 0, width: 312, height: 326,
  name: "Card",
  layoutMode: "VERTICAL",
  fillColor: { r: 1, g: 1, b: 1 },
  strokeColor: { r: 0.122, g: 0.145, b: 0.149, a: 0.1 },
  strokeWeight: 1
})
set_corner_radius({ nodeId: "ID", radius: 4 })

// 2. 画像プレースホルダー
create_frame({
  name: "ImagePlaceholder",
  parentId: "コンテナID",
  width: 312, height: 160,
  layoutMode: "HORIZONTAL",
  fillColor: { r: 0.91, g: 0.918, b: 0.918 }
})
set_layout_sizing({ nodeId: "ID", layoutSizingHorizontal: "FILL", layoutSizingVertical: "FIXED" })

// 3. Body フレーム（padding付き）
create_frame({
  name: "Body",
  parentId: "コンテナID",
  layoutMode: "VERTICAL",
  paddingTop: 16, paddingRight: 16, paddingBottom: 16, paddingLeft: 16
})
set_layout_sizing({ nodeId: "ID", layoutSizingHorizontal: "FILL", layoutSizingVertical: "HUG" })
```
