# リファレンス

## 色の変換

RGB(0-255) → Figma(0-1) に変換:

| CSS                   | Figma                                    |
| --------------------- | ---------------------------------------- |
| rgb(31, 37, 38)       | { r: 0.122, g: 0.145, b: 0.149 }         |
| rgba(31, 37, 38, 0.8) | { r: 0.122, g: 0.145, b: 0.149, a: 0.8 } |
| #ffffff               | { r: 1, g: 1, b: 1 }                     |
| #f59325               | { r: 0.96, g: 0.576, b: 0.145 }          |

**計算式**: `figmaValue = cssValue / 255`

## Alignment マッピング

### justify-content → primaryAxisAlignItems

| CSS justify-content | Figma primaryAxisAlignItems |
| ------------------- | --------------------------- |
| flex-start          | MIN                         |
| flex-end            | MAX                         |
| center              | CENTER                      |
| space-between       | SPACE_BETWEEN               |

### align-items → counterAxisAlignItems

| CSS align-items | Figma counterAxisAlignItems |
| --------------- | --------------------------- |
| flex-start      | MIN                         |
| flex-end        | MAX                         |
| center          | CENTER                      |

## TalkToFigma API リファレンス

### フレーム作成

```javascript
create_frame({
  name: "フレーム名",
  parentId: "親ID",        // オプション
  x: 0, y: 0,
  width: 100, height: 100,
  layoutMode: "VERTICAL",  // or "HORIZONTAL", "NONE"
  fillColor: { r: 1, g: 1, b: 1 },
  strokeColor: { r: 0, g: 0, b: 0, a: 0.1 },
  strokeWeight: 1,
  paddingTop: 0,
  paddingRight: 0,
  paddingBottom: 0,
  paddingLeft: 0,
  itemSpacing: 0,
  primaryAxisAlignItems: "MIN",     // MIN, MAX, CENTER, SPACE_BETWEEN
  counterAxisAlignItems: "MIN"      // MIN, MAX, CENTER, BASELINE
})
```

### テキスト作成

```javascript
create_text({
  name: "テキスト名",
  parentId: "親ID",
  x: 0, y: 0,
  text: "テキスト内容",
  fontSize: 15,
  fontWeight: 400,  // 400=Regular, 600=Semi Bold, 700=Bold
  fontColor: { r: 0, g: 0, b: 0, a: 1 }
})
```

### レイアウト設定

```javascript
set_layout_sizing({
  nodeId: "ID",
  layoutSizingHorizontal: "FILL",  // FIXED, HUG, FILL
  layoutSizingVertical: "HUG"
})

set_corner_radius({
  nodeId: "ID",
  radius: 4
})

set_padding({
  nodeId: "ID",
  paddingTop: 16,
  paddingRight: 16,
  paddingBottom: 16,
  paddingLeft: 16
})

set_item_spacing({
  nodeId: "ID",
  itemSpacing: 8
})
```

### その他

```javascript
resize_node({
  nodeId: "ID",
  width: 100,
  height: 100
})

set_focus({
  nodeId: "ID"
})

set_fill_color({
  nodeId: "ID",
  r: 1, g: 1, b: 1, a: 1
})
```

## chrome-devtools API リファレンス

### ページ操作

```javascript
navigate_page({ url: "https://example.com" })
take_snapshot()
take_screenshot()
```

### フォーム操作

```javascript
fill_form({
  elements: [
    { uid: "1_3", value: "email@example.com" },
    { uid: "1_5", value: "password" }
  ]
})

click({ uid: "1_6" })
```

### スクリプト実行

```javascript
evaluate_script({
  function: "() => { return document.title; }"
})

// 引数付き
evaluate_script({
  function: "(el) => { return el.textContent; }",
  args: [{ uid: "選択されたuid" }]
})
```
