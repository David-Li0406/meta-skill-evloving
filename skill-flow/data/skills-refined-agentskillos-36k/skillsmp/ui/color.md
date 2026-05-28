---
name: 色彩系統
description: 完整的色彩系統建立指南，包含調色板、對比度、色彩心理學
---

# 🎨 色彩系統

## 色彩結構

### 主要色彩 (Primary Colors)

主色是品牌的核心識別色，應用於：
- Logo、主要按鈕
- 重要連結、強調文字
- 頁首、主要導航

```css
:root {
  --color-primary-50: #eff6ff;   /* 最淺 */
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;  /* 主要 */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;  /* 最深 */
}
```

### 輔助色 (Secondary Colors)

輔色用於次要元素，與主色形成對比：
- 次要按鈕、標籤
- 背景區塊
- 圖表配色

### 強調色 (Accent Colors)

強調色用於引起注意：
- CTA 按鈕
- 促銷標籤
- 重要通知

### 中性色 (Neutral Colors)

中性色用於文字、背景、邊框：

```css
:root {
  /* 灰階 */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
}
```

### 語意色 (Semantic Colors)

傳達特定意義的顏色：

| 類型 | 顏色 | 用途 |
|-----|------|-----|
| Success | 綠色 | 成功、完成、正確 |
| Warning | 黃色 | 警告、注意 |
| Error | 紅色 | 錯誤、危險、刪除 |
| Info | 藍色 | 資訊、提示 |

```css
:root {
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
}
```

---

## 色彩對比度

### WCAG 標準

| 等級 | 一般文字 | 大文字 |
|-----|---------|-------|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

> 大文字：18pt 以上，或 14pt 粗體

### 檢測工具
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Contrast Checker](https://coolors.co/contrast-checker)
- Chrome DevTools 內建檢測

### 常見問題

❌ **錯誤示範**
```css
/* 對比度不足 */
.bad {
  background: #f0f0f0;
  color: #999999; /* 對比度 2.8:1 */
}
```

✅ **正確示範**
```css
/* 對比度足夠 */
.good {
  background: #f0f0f0;
  color: #595959; /* 對比度 5.3:1 */
}
```

---

## 色彩心理學

### 顏色與情感

| 顏色 | 正面聯想 | 常用產業 |
|-----|---------|---------|
| 🔵 藍色 | 信任、專業、冷靜 | 金融、科技、醫療 |
| 🟢 綠色 | 自然、成長、健康 | 環保、健康、金融 |
| 🔴 紅色 | 熱情、緊急、能量 | 餐飲、娛樂、促銷 |
| 🟡 黃色 | 樂觀、溫暖、注意 | 兒童、食品、警示 |
| 🟣 紫色 | 奢華、創意、神秘 | 美妝、創意、皇室 |
| 🟠 橙色 | 活力、友善、創新 | 娛樂、科技、運動 |
| ⚫ 黑色 | 高級、權威、神秘 | 時尚、奢侈品、科技 |
| ⚪ 白色 | 純淨、簡約、現代 | 醫療、科技、極簡 |

### 產業色彩慣例

| 產業 | 常用主色 | 原因 |
|-----|---------|-----|
| 金融 | 藍、綠 | 信任、穩定 |
| 醫療 | 藍、綠、白 | 乾淨、專業 |
| 科技 | 藍、紫 | 創新、未來 |
| 食品 | 紅、橙、黃 | 食慾、溫暖 |
| 環保 | 綠、棕 | 自然、永續 |
| 時尚 | 黑、金 | 高級、品味 |
| 兒童 | 多彩 | 活潑、有趣 |

---

## 配色方法

### 1. 單色配色 (Monochromatic)
使用同一色相的不同明度/飽和度

```
主色 → 淺色變體 → 深色變體
#3b82f6 → #93c5fd → #1d4ed8
```

**適用**：極簡、專業、統一感

### 2. 互補色配色 (Complementary)
使用色環對面的顏色

```
藍色 ↔ 橙色
#3b82f6 ↔ #f97316
```

**適用**：高對比、活力、CTA

### 3. 類似色配色 (Analogous)
使用色環相鄰的顏色

```
藍 → 青 → 綠
#3b82f6 → #14b8a6 → #22c55e
```

**適用**：和諧、自然、舒適

### 4. 三等分配色 (Triadic)
使用色環上等距的三個顏色

```
紅 → 藍 → 黃
#ef4444 → #3b82f6 → #eab308
```

**適用**：活力、多元、兒童

---

## 深色模式

### 原則

1. **不是單純反轉**：深色模式需要重新設計，不是黑白反轉
2. **降低對比**：深色背景上使用較淡的文字（不是純白）
3. **減少飽和度**：高飽和色在深色背景上會刺眼
4. **層次用明度**：用微妙的灰色差異區分層次

### 深色配色示例

```css
:root[data-theme="dark"] {
  --bg-primary: #0f172a;      /* 主背景 */
  --bg-secondary: #1e293b;    /* 次背景 */
  --bg-tertiary: #334155;     /* 卡片背景 */
  
  --text-primary: #f1f5f9;    /* 主文字 */
  --text-secondary: #94a3b8;  /* 次文字 */
  --text-muted: #64748b;      /* 輔助文字 */
  
  --border: #334155;          /* 邊框 */
}
```

---

## 漸層

### 類型

1. **線性漸層** (Linear Gradient)
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

2. **放射漸層** (Radial Gradient)
```css
background: radial-gradient(circle, #667eea 0%, #764ba2 100%);
```

3. **錐形漸層** (Conic Gradient)
```css
background: conic-gradient(from 0deg, #667eea, #764ba2, #667eea);
```

### 流行漸層配色

| 名稱 | 配色 |
|-----|------|
| 日落 | `#ff6b6b → #feca57` |
| 海洋 | `#667eea → #764ba2` |
| 薄荷 | `#11998e → #38ef7d` |
| 粉紫 | `#ee9ca7 → #ffdde1` |
| 深夜 | `#232526 → #414345` |
| 極光 | `#00d2ff → #3a7bd5` |

---

## 配色工具推薦

| 工具 | 用途 |
|-----|------|
| [Coolors](https://coolors.co) | 生成調色板 |
| [Adobe Color](https://color.adobe.com) | 色彩理論工具 |
| [Realtime Colors](https://realtimecolors.com) | 即時預覽 |
| [Happy Hues](https://www.happyhues.co) | 配色靈感 |
| [ColorHunt](https://colorhunt.co) | 配色靈感 |
| [Khroma](http://khroma.co) | AI 配色 |
