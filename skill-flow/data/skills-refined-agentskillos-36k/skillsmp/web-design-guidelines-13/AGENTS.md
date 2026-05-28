# 網頁介面設計指南

**版本 1.0.0**  
Vercel  
2026 年 1 月

> **注意：**  
> 此文件主要供 AI 代理和大型語言模型在維護、產生或重構網頁介面程式碼時參考。
> 人類開發者也可能會覺得有用，但此處的指導方針已針對 AI 輔助工作流程的自動化和一致性進行最佳化。

---

## 摘要

針對網頁介面設計的全面最佳實踐指南，專為 AI 代理和大型語言模型設計。包含 100+ 條規則，涵蓋無障礙性、效能、表單、動畫、排版、圖片、導航、深色模式、觸控互動和國際化等類別。每條規則都包含詳細說明、真實範例，用於指導自動化程式碼審查和產生。

---

## 指南來源

此 skill 會動態從以下來源獲取最新的網頁介面指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

## 使用方式

當需要審查 UI 程式碼時：

1. 使用 WebFetch 從上述網址獲取最新指南
2. 讀取指定的檔案或元件
3. 套用指南中的所有規則
4. 以 `檔案:行號` 格式報告發現的問題

## 主要類別

指南涵蓋以下主要領域：

### 無障礙性（Accessibility）

- ARIA 標籤和語義化 HTML
- 鍵盤導航支援
- 螢幕閱讀器相容性
- 色彩對比度

### 焦點狀態

- 可見的焦點指示器
- focus-visible 模式
- 焦點管理

### 表單

- autocomplete 屬性
- 驗證和錯誤處理
- 標籤關聯
- 輸入類型

### 動畫

- prefers-reduced-motion 支援
- compositor-friendly 轉換
- 效能最佳化

### 排版

- 使用彎引號（curly quotes）
- 省略號（ellipsis）
- tabular-nums 用於數字對齊
- 字型載入最佳化

### 圖片

- 尺寸屬性
- 延遲載入
- alt 文字
- 回應式圖片

### 效能

- 虛擬化長列表
- 避免 layout thrashing
- preconnect 提示
- 資源優先級

### 導航與狀態

- URL 反映應用程式狀態
- 深度連結支援
- 歷史記錄管理
- 載入狀態

### 深色模式與主題

- color-scheme 設定
- theme-color meta 標籤
- CSS 自訂屬性
- 主題切換

### 觸控與互動

- touch-action 屬性
- tap-highlight 控制
- 觸控目標大小
- 手勢支援

### 本地化與國際化

- Intl.DateTimeFormat
- Intl.NumberFormat
- 語言方向（RTL/LTR）
- 文化敏感排序

---

## 審查流程

1. **獲取指南**：使用 WebFetch 從來源網址獲取最新規則
2. **讀取檔案**：載入需要審查的檔案
3. **套用規則**：逐一檢查每條規則
4. **報告問題**：以簡潔格式輸出發現的問題

## 輸出格式

使用簡潔的 `檔案:行號` 格式報告問題，便於開發者快速定位和修復。

---

詳細的規則內容和範例請參閱來源網址：
https://github.com/vercel-labs/web-interface-guidelines
