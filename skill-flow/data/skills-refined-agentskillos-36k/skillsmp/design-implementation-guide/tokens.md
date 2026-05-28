# デザイントークン

## トークン定義（tokens.json）

Material 3命名規則で階層化:

```json
{
  "color": {
    "primary": { "value": "#6750A4" },
    "on-primary": { "value": "#FFFFFF" },
    "surface": { "value": "#FEF7FF" },
    "error": { "value": "#BA1A1A" },
    "on-error": { "value": "#FFFFFF" },
    "success": { "value": "#4CAF50" },
    "on-success": { "value": "#FFFFFF" }
  },
  "spacing": {
    "xs": { "value": "4px" },
    "sm": { "value": "8px" },
    "md": { "value": "16px" },
    "lg": { "value": "24px" },
    "xl": { "value": "32px" }
  },
  "typography": {
    "body": {
      "size": { "value": "clamp(1rem, 0.875rem + 0.5vw, 1.125rem)" },
      "line-height": { "value": "1.5" }
    },
    "h1": {
      "size": { "value": "clamp(2rem, 1.5rem + 2vw, 3rem)" },
      "line-height": { "value": "1.2" }
    }
  }
}
```

## Style Dictionary設定

### config.json

```json
{
  "source": ["tokens.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "buildPath": "build/web/",
      "files": [{
        "destination": "tokens.css",
        "format": "css/variables"
      }]
    },
    "ios": {
      "transformGroup": "ios",
      "buildPath": "build/ios/",
      "files": [{
        "destination": "Tokens.swift",
        "format": "ios/swift"
      }]
    },
    "android": {
      "transformGroup": "android",
      "buildPath": "build/android/",
      "files": [{
        "destination": "colors.xml",
        "format": "android/colors"
      }]
    }
  }
}
```

### ビルドコマンド

```bash
style-dictionary build
```

## CSS Custom Property使用

```css
@import url('tokens.css');

button {
  background: var(--color-primary);
  color: var(--color-on-primary);
  padding-inline: var(--spacing-md);
}
```

## ダークモード対応

別トーンパレットで定義:

```json
{
  "color-dark": {
    "primary": { "value": "#D0BCFF" },
    "on-primary": { "value": "#381E72" }
  }
}
```

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: var(--color-dark-primary);
    --color-on-primary: var(--color-dark-on-primary);
  }
}
```

## 流体タイポグラフィ

### clamp()による流体スケール

```css
:root {
  --font-size-body: clamp(1rem, 0.875rem + 0.5vw, 1.125rem);
  --font-size-h1: clamp(2rem, 1.5rem + 2vw, 3rem);

  --space-s: clamp(0.5rem, 0.25rem + 1vw, 1rem);
  --space-m: clamp(1rem, 0.5rem + 2vw, 2rem);
  --space-l: clamp(2rem, 1rem + 4vw, 4rem);
}
```

### 計算例（Utopiaツール）

- 最小画面（320px）で16px
- 最大画面（1280px）で20px
- 計算式: `clamp(1rem, 0.875rem + 0.5vw, 1.25rem)`

## 論理プロパティ

物理方向依存を排除:

| 物理プロパティ（非推奨） | 論理プロパティ（推奨） |
|------------------------|---------------------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-top` | `padding-block-start` |
| `padding-bottom` | `padding-block-end` |
| `width` | `inline-size` |
| `height` | `block-size` |

```css
.container {
  padding-inline: var(--spacing-md);
  padding-block: var(--spacing-sm);
  max-inline-size: 65ch; /* 行長制限 */
}
```

## 可変フォント

```css
@font-face {
  font-family: 'Inter';
  src: url('Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
}
```

## 状態層（State Layer）

Material 3規定に従い半透明で重ねる:

```css
button:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-on-primary);
  opacity: 0.08;
}

button:active::before {
  opacity: 0.12;
}
```

## Figma同期

1. Figma Variablesでトークン名を統一
2. エクスポートしたJSONを `tokens.json` へマージ
3. Style Dictionaryで各プラットフォームへ出力

## 参考

- [Material 3 Color System](https://m3.material.io/styles/color/system/overview)
- [Style Dictionary](https://styledictionary.com/)
- [Design Tokens Community Group](https://www.designtokens.org/)
- [Utopia - Fluid Responsive Design](https://utopia.fyi/)
- [MDN 論理プロパティ](https://developer.mozilla.org/ja/docs/Web/CSS/Guides/Logical_properties_and_values)