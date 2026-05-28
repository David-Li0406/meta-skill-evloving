---
name: 間距系統
description: 完整的間距與佈局系統
---

# 📏 間距系統

## 間距比例

### 8px 基準系統

使用 8 的倍數建立一致的間距：

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
  --space-32: 8rem;     /* 128px */
}
```

### 間距用途

| 間距 | 用途 |
|-----|------|
| 1-2 (4-8px) | 圖標間距、緊密元素 |
| 3-4 (12-16px) | 元件內部間距 |
| 5-6 (20-24px) | 元件之間間距 |
| 8-12 (32-48px) | 區塊間距 |
| 16-24 (64-96px) | 區域間距 |
| 24+ (96px+) | 頁面區塊間距 |

---

## 元件間距

### 內距 (Padding)

```css
/* 按鈕 */
.btn-sm { padding: var(--space-2) var(--space-3); }
.btn-md { padding: var(--space-3) var(--space-4); }
.btn-lg { padding: var(--space-4) var(--space-6); }

/* 卡片 */
.card { padding: var(--space-6); }
.card-compact { padding: var(--space-4); }
.card-spacious { padding: var(--space-8); }

/* 容器 */
.container {
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

@media (min-width: 768px) {
  .container {
    padding-left: var(--space-6);
    padding-right: var(--space-6);
  }
}
```

### 外距 (Margin)

```css
/* 標題 */
h1 { margin-bottom: var(--space-6); }
h2 { margin-top: var(--space-12); margin-bottom: var(--space-4); }
h3 { margin-top: var(--space-8); margin-bottom: var(--space-3); }

/* 段落 */
p { margin-bottom: var(--space-4); }

/* 列表項目 */
li + li { margin-top: var(--space-2); }

/* 區塊 */
section { margin-bottom: var(--space-16); }
```

---

## 網格系統

### 12 欄網格

```css
.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6);
}

.col-1 { grid-column: span 1; }
.col-2 { grid-column: span 2; }
.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-8 { grid-column: span 8; }
.col-12 { grid-column: span 12; }
```

### 響應式網格

```css
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
}

@media (min-width: 768px) and (max-width: 1024px) {
  .grid {
    grid-template-columns: repeat(6, 1fr);
  }
}
```

### Gap 間距

```css
.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }
.gap-8 { gap: var(--space-8); }
```

---

## 容器寬度

```css
:root {
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
}

.container {
  width: 100%;
  max-width: var(--container-xl);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

.container-narrow {
  max-width: var(--container-md);
}

.container-wide {
  max-width: var(--container-2xl);
}
```

---

## Flexbox 佈局

### 常用模式

```css
/* 水平置中 */
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 兩端對齊 */
.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 垂直堆疊 */
.flex-col {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* 水平堆疊 */
.flex-row {
  display: flex;
  flex-direction: row;
  gap: var(--space-4);
}

/* 換行 */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}
```

---

## 堆疊間距 (Stack)

垂直堆疊元素的統一間距：

```css
/* 堆疊容器 */
.stack > * + * {
  margin-top: var(--stack-space, var(--space-4));
}

.stack-sm { --stack-space: var(--space-2); }
.stack-md { --stack-space: var(--space-4); }
.stack-lg { --stack-space: var(--space-6); }
.stack-xl { --stack-space: var(--space-8); }
```

使用：
```html
<div class="stack stack-lg">
  <h2>標題</h2>
  <p>段落一</p>
  <p>段落二</p>
</div>
```

---

## 區域間距

### 區塊間距模式

```css
:root {
  --section-space-sm: var(--space-12);  /* 48px */
  --section-space-md: var(--space-16);  /* 64px */
  --section-space-lg: var(--space-24);  /* 96px */
}

section {
  padding-top: var(--section-space-md);
  padding-bottom: var(--section-space-md);
}

@media (min-width: 768px) {
  section {
    padding-top: var(--section-space-lg);
    padding-bottom: var(--section-space-lg);
  }
}
```

---

## 響應式間距

### 使用 clamp()

```css
:root {
  /* 流體間距 */
  --space-fluid-sm: clamp(0.5rem, 1vw, 1rem);
  --space-fluid-md: clamp(1rem, 2vw, 2rem);
  --space-fluid-lg: clamp(2rem, 4vw, 4rem);
  --space-fluid-xl: clamp(3rem, 6vw, 6rem);
}

section {
  padding: var(--space-fluid-xl) var(--space-fluid-md);
}
```

---

## 間距工具類

```css
/* Margin */
.m-0 { margin: 0; }
.m-4 { margin: var(--space-4); }
.mt-4 { margin-top: var(--space-4); }
.mr-4 { margin-right: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
.ml-4 { margin-left: var(--space-4); }
.mx-4 { margin-left: var(--space-4); margin-right: var(--space-4); }
.my-4 { margin-top: var(--space-4); margin-bottom: var(--space-4); }

/* Padding */
.p-0 { padding: 0; }
.p-4 { padding: var(--space-4); }
.pt-4 { padding-top: var(--space-4); }
.pr-4 { padding-right: var(--space-4); }
.pb-4 { padding-bottom: var(--space-4); }
.pl-4 { padding-left: var(--space-4); }
.px-4 { padding-left: var(--space-4); padding-right: var(--space-4); }
.py-4 { padding-top: var(--space-4); padding-bottom: var(--space-4); }

/* Auto */
.mx-auto { margin-left: auto; margin-right: auto; }
.ml-auto { margin-left: auto; }
.mr-auto { margin-right: auto; }
```

---

## 視覺節奏

### 原則

1. **一致性**：整個網站使用相同的間距系統
2. **層次性**：相關元素間距小，無關元素間距大
3. **呼吸感**：適當留白，避免擁擠
4. **對齊**：元素邊緣對齊，建立視覺秩序

### 常見錯誤

❌ **錯誤**
- 間距不一致（這裡 10px，那裡 15px）
- 過於擁擠，沒有呼吸空間
- 間距過大，元素失去關聯

✅ **正確**
- 使用統一的間距系統
- 相關元素緊密，區塊明確分隔
- 間距隨螢幕大小調整
