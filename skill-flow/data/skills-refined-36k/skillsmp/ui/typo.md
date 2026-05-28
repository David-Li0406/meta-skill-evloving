---
name: 排版規範
description: 完整的排版系統，包含字型選擇、階層、行高
---

# 🔤 排版規範

## 字型選擇

### 字型類別

| 類別 | 特色 | 適用場景 |
|-----|------|---------|
| 無襯線 (Sans-serif) | 現代、簡潔 | 網頁主流、科技 |
| 襯線 (Serif) | 傳統、優雅 | 編輯、法律、奢華 |
| 等寬 (Monospace) | 程式碼 | 程式碼、技術文件 |
| 手寫 (Script) | 個性、藝術 | 標題、裝飾（謹慎使用）|
| 展示 (Display) | 醒目、獨特 | 大標題（謹慎使用）|

### 推薦字型

#### 西文無襯線
| 字型 | 風格 | 來源 |
|-----|------|-----|
| Inter | 現代、清晰 | Google Fonts |
| Roboto | Google 風格 | Google Fonts |
| Open Sans | 友善、易讀 | Google Fonts |
| Poppins | 圓潤、現代 | Google Fonts |
| Nunito | 圓潤、友善 | Google Fonts |
| SF Pro | Apple 風格 | Apple |
| Outfit | 幾何、現代 | Google Fonts |
| DM Sans | 幾何、簡潔 | Google Fonts |

#### 西文襯線
| 字型 | 風格 | 來源 |
|-----|------|-----|
| Playfair Display | 優雅、對比 | Google Fonts |
| Merriweather | 易讀、書籍 | Google Fonts |
| Lora | 現代、柔和 | Google Fonts |
| Source Serif Pro | Adobe 風格 | Google Fonts |

#### 中文字型
| 字型 | 風格 | 來源 |
|-----|------|-----|
| Noto Sans TC | 思源黑體 | Google Fonts |
| Noto Serif TC | 思源宋體 | Google Fonts |
| 台北黑體 | 台灣設計 | 免費 |
| jf open 粉圓 | 可愛圓體 | justfont |
| 思源柔黑體 | 圓潤黑體 | 免費 |

### 字型堆疊

```css
:root {
  /* 無襯線 */
  --font-sans: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  
  /* 襯線 */
  --font-serif: 'Playfair Display', 'Noto Serif TC', Georgia,
    'Times New Roman', serif;
  
  /* 等寬 */
  --font-mono: 'Fira Code', 'JetBrains Mono', Consolas,
    'Courier New', monospace;
}
```

---

## 字型大小

### 模數比例 (Modular Scale)

使用數學比例建立和諧的字型階層：

| 比例 | 數值 | 適用風格 |
|-----|------|---------|
| Minor Second | 1.067 | 微小差異 |
| Major Second | 1.125 | 小差異 |
| Minor Third | 1.200 | 常用 |
| Major Third | 1.250 | 常用 |
| Perfect Fourth | 1.333 | 明顯對比 |
| Golden Ratio | 1.618 | 強烈對比 |

### 字型大小系統

```css
:root {
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px - 基準 */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  --text-5xl: 3rem;      /* 48px */
  --text-6xl: 3.75rem;   /* 60px */
  --text-7xl: 4.5rem;    /* 72px */
}
```

### 響應式字型

```css
/* 使用 clamp() 實現流體字型 */
:root {
  --text-hero: clamp(2.5rem, 5vw + 1rem, 4.5rem);
  --text-h1: clamp(2rem, 4vw + 0.5rem, 3rem);
  --text-h2: clamp(1.5rem, 3vw + 0.5rem, 2.25rem);
  --text-h3: clamp(1.25rem, 2vw + 0.5rem, 1.75rem);
}

h1 {
  font-size: var(--text-h1);
}
```

---

## 行高 (Line Height)

### 基本原則

| 用途 | 行高 | 說明 |
|-----|------|-----|
| 標題 | 1.1 - 1.3 | 緊湊，視覺重量 |
| 正文 | 1.5 - 1.7 | 舒適閱讀 |
| 小字 | 1.4 - 1.5 | 適中 |

```css
:root {
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}

h1, h2, h3 {
  line-height: var(--leading-tight);
}

p {
  line-height: var(--leading-relaxed);
}
```

---

## 字重 (Font Weight)

### 標準字重

| 數值 | 名稱 | 用途 |
|-----|------|-----|
| 100 | Thin | 極細（謹慎使用）|
| 200 | Extra Light | 很細 |
| 300 | Light | 細體 |
| 400 | Regular | 正常內文 |
| 500 | Medium | 強調 |
| 600 | Semi Bold | 小標題 |
| 700 | Bold | 標題 |
| 800 | Extra Bold | 大標題 |
| 900 | Black | 極粗 |

### 建議搭配

```css
:root {
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}

h1 { font-weight: var(--font-bold); }
h2 { font-weight: var(--font-semibold); }
h3 { font-weight: var(--font-semibold); }
p { font-weight: var(--font-normal); }
```

---

## 字距 (Letter Spacing)

```css
:root {
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;
}

/* 大標題可稍微緊縮 */
h1 {
  letter-spacing: var(--tracking-tight);
}

/* 全大寫需增加間距 */
.uppercase {
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
}
```

---

## 段落設定

### 行寬 (Line Length)

最佳閱讀行寬：45-75 個字元（中文約 20-35 個字）

```css
.prose {
  max-width: 65ch; /* 約 65 個字元 */
}

.prose-zh {
  max-width: 35em; /* 中文約 35 個字 */
}
```

### 段落間距

```css
p {
  margin-bottom: 1em;
}

p + p {
  margin-top: 1.5em;
}
```

### 首行縮排（中文）

```css
.chinese-article p {
  text-indent: 2em;
}

.chinese-article p + p {
  margin-top: 0;
}
```

---

## 標題階層

### 語意與視覺

```html
<!-- 每頁只有一個 h1 -->
<h1>頁面主標題</h1>
  <h2>主要區塊標題</h2>
    <h3>子區塊標題</h3>
      <h4>更細節的標題</h4>
```

### 樣式定義

```css
h1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  margin-bottom: 1.5rem;
}

h2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  margin-top: 3rem;
  margin-bottom: 1rem;
}

h3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-snug);
  margin-top: 2rem;
  margin-bottom: 0.75rem;
}

h4 {
  font-size: var(--text-xl);
  font-weight: var(--font-medium);
  line-height: var(--leading-snug);
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}
```

---

## 中英混排

### 原則

1. **字型搭配**：選擇 x-height 相近的中英文字型
2. **標點處理**：使用正確的中文標點
3. **間距處理**：中英文之間自動加空格（可用 CSS 或 JS）

### CSS 設定

```css
/* 中英混排優化 */
body {
  font-family: var(--font-sans);
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 調整英文字型的基線對齊 */
:lang(zh) {
  font-feature-settings: "palt";
}
```

---

## 字型載入

### 最佳實踐

```html
<!-- 預連線字型服務 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 載入字型 -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
```

### 字型顯示策略

```css
@font-face {
  font-family: 'Inter';
  font-display: swap; /* 先顯示備用字型，載入後替換 */
}
```

| 值 | 行為 |
|---|------|
| auto | 瀏覽器決定 |
| block | 隱藏文字直到載入 |
| swap | 先用備用，載入後替換 |
| fallback | 短暫隱藏，然後用備用 |
| optional | 如果快取有就用，否則用備用 |
