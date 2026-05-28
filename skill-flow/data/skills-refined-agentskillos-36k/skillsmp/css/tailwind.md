---
name: Tailwind CSS 指南
description: Tailwind CSS 開發最佳實踐
---

# 🌊 Tailwind CSS 指南

## 安裝

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## 設定

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{html,js,jsx,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#64748b',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
```

---

## 常用類別

### 佈局
```html
<div class="flex items-center justify-between">
<div class="grid grid-cols-3 gap-4">
<div class="container mx-auto px-4">
```

### 間距
```html
<div class="p-4 m-2">          <!-- padding/margin -->
<div class="px-4 py-2">        <!-- x/y 軸 -->
<div class="mt-4 mb-8">        <!-- 單方向 -->
<div class="space-y-4">        <!-- 子元素間距 -->
```

### 文字
```html
<p class="text-lg font-bold text-gray-800">
<p class="text-center leading-relaxed">
```

### 背景與邊框
```html
<div class="bg-white rounded-lg shadow-md border border-gray-200">
```

---

## 元件範例

### 按鈕
```html
<button class="px-4 py-2 bg-blue-500 text-white rounded-lg 
               hover:bg-blue-600 transition-colors">
  按鈕
</button>
```

### 卡片
```html
<div class="bg-white rounded-xl shadow-lg p-6">
  <h3 class="text-xl font-semibold mb-2">標題</h3>
  <p class="text-gray-600">內容</p>
</div>
```

---

## @apply 抽取

```css
/* 當類別太長時 */
.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded-lg 
         hover:bg-blue-600 transition-colors;
}
```

---

## 最佳實踐

1. **使用設計 Token**：在 config 定義色彩、間距
2. **元件化**：抽取重複的類別組合
3. **響應式**：使用 `sm:` `md:` `lg:` 前綴
4. **狀態**：使用 `hover:` `focus:` `active:`
5. **深色模式**：使用 `dark:` 前綴
