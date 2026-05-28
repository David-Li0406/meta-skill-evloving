# Style Guide

## Meta
- **Project**: [プロジェクト名]
- **Last updated**: YYYY-MM-DD
- **Status**: Draft / Review / Approved

---

## 1. Typography(タイポグラフィ)

### Font Family
- **Primary**: (例) Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- **Monospace**: (例) "SF Mono", "Consolas", "Liberation Mono", monospace

### Font Size Scale
| Token           | Size   | Use Case                          |
|-----------------|--------|-----------------------------------|
| text-xs         | 12px   | キャプション、補助テキスト        |
| text-sm         | 14px   | ボディ(小)、ラベル                |
| text-base       | 16px   | ボディ(標準)                      |
| text-lg         | 18px   | リード文、強調テキスト            |
| text-xl         | 20px   | 小見出し(H4)                      |
| text-2xl        | 24px   | 見出し(H3)                        |
| text-3xl        | 30px   | 見出し(H2)                        |
| text-4xl        | 36px   | 大見出し(H1)                      |

### Font Weight
| Token           | Weight | Use Case                          |
|-----------------|--------|-----------------------------------|
| font-normal     | 400    | 通常テキスト                      |
| font-medium     | 500    | ラベル、ボタン                    |
| font-semibold   | 600    | 小見出し                          |
| font-bold       | 700    | 見出し、強調                      |

### Line Height
| Token           | Height | Use Case                          |
|-----------------|--------|-----------------------------------|
| leading-tight   | 1.25   | 見出し                            |
| leading-normal  | 1.5    | ボディテキスト                    |
| leading-relaxed | 1.75   | 長文、リード文                    |

---

## 2. Colors(色)

### Primary(メインカラー)
| Token              | Hex       | Use Case                     |
|--------------------|-----------|------------------------------|
| primary-50         | #f0f9ff   | 背景(最薄)                   |
| primary-100        | #e0f2fe   | 背景(薄)                     |
| primary-500        | #0ea5e9   | メインアクション、リンク     |
| primary-600        | #0284c7   | ホバー時                     |
| primary-700        | #0369a1   | アクティブ時                 |

### Neutral(グレースケール)
| Token              | Hex       | Use Case                     |
|--------------------|-----------|------------------------------|
| gray-50            | #f9fafb   | 背景(最薄)                   |
| gray-100           | #f3f4f6   | 背景(薄)、カード             |
| gray-200           | #e5e7eb   | ボーダー、区切り線           |
| gray-500           | #6b7280   | 補助テキスト                 |
| gray-700           | #374151   | ボディテキスト               |
| gray-900           | #111827   | 見出し、強調テキスト         |

### Semantic(意味を持つ色)
| Token              | Hex       | Use Case                     |
|--------------------|-----------|------------------------------|
| success-500        | #10b981   | 成功メッセージ、完了状態     |
| warning-500        | #f59e0b   | 警告メッセージ、注意喚起     |
| error-500          | #ef4444   | エラーメッセージ、削除       |
| info-500           | #3b82f6   | 情報メッセージ               |

---

## 3. Spacing(余白)

### Spacing Scale
| Token    | Size   | Example Use Case                     |
|----------|--------|--------------------------------------|
| space-1  | 4px    | アイコンとテキストの間               |
| space-2  | 8px    | 要素間の最小余白                     |
| space-3  | 12px   | ボタン内パディング                   |
| space-4  | 16px   | カード内パディング                   |
| space-6  | 24px   | セクション間                         |
| space-8  | 32px   | 大きなセクション間                   |
| space-12 | 48px   | ページ上部余白                       |
| space-16 | 64px   | メジャーセクション間                 |

---

## 4. Layout(レイアウト)

### Container Width
| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| sm         | 640px     | 16px    |
| md         | 768px     | 24px    |
| lg         | 1024px    | 32px    |
| xl         | 1280px    | 32px    |
| 2xl        | 1536px    | 32px    |

### Grid System
- **Columns**: 12カラム(デスクトップ) / 4カラム(モバイル)
- **Gutter**: 24px(デスクトップ) / 16px(モバイル)

---

## 5. Border Radius(角丸)

| Token          | Size   | Use Case                     |
|----------------|--------|------------------------------|
| rounded-none   | 0px    | 角丸なし                     |
| rounded-sm     | 2px    | 小さな要素(Badge)            |
| rounded        | 4px    | 標準(Button, Input)          |
| rounded-md     | 6px    | カード                       |
| rounded-lg     | 8px    | モーダル                     |
| rounded-full   | 9999px | 円形(Avatar, Pill Button)    |

---

## 6. Shadow(影)

| Token          | Value                                  | Use Case                     |
|----------------|----------------------------------------|------------------------------|
| shadow-sm      | 0 1px 2px rgba(0,0,0,0.05)             | 軽い浮遊感(Button)           |
| shadow         | 0 1px 3px rgba(0,0,0,0.1)              | カード                       |
| shadow-md      | 0 4px 6px rgba(0,0,0,0.1)              | ドロップダウン               |
| shadow-lg      | 0 10px 15px rgba(0,0,0,0.1)            | モーダル                     |
| shadow-xl      | 0 20px 25px rgba(0,0,0,0.1)            | 大きなモーダル               |

---

## 7. Icons(アイコン)

### Icon Library
- **Primary**: (例) Heroicons / Lucide / Material Icons
- **Style**: Outline / Solid
- **License**: MIT

### Icon Sizes
| Size | Dimensions | Use Case                     |
|------|------------|------------------------------|
| xs   | 12x12px    | インラインアイコン           |
| sm   | 16x16px    | ボタン内アイコン             |
| md   | 20x20px    | ナビゲーション               |
| lg   | 24x24px    | 見出しアイコン               |
| xl   | 32x32px    | 強調アイコン                 |

---

## 8. Animation(アニメーション)

### Duration
| Token              | Time  | Use Case                     |
|--------------------|-------|------------------------------|
| duration-fast      | 150ms | ホバー、フォーカス           |
| duration-normal    | 300ms | 標準トランジション           |
| duration-slow      | 500ms | モーダル、スライド           |

### Easing
| Token              | Curve                  | Use Case                     |
|--------------------|------------------------|------------------------------|
| ease-in            | cubic-bezier(0.4,0,1,1)| フェードアウト               |
| ease-out           | cubic-bezier(0,0,0.2,1)| フェードイン                 |
| ease-in-out        | cubic-bezier(0.4,0,0.2,1)| 標準                      |

---

## 9. Component Guidelines(コンポーネント方針)

### Button
- プライマリボタンは1画面1つまで
- ラベルは「動詞+目的語」で明確に
- 最小タップ領域:44x44px(モバイル)

### Input
- ラベルは必須(視覚的に隠す場合もaria-labelで)
- エラーメッセージはフィールド直下に表示
- フォーカス時はボーダーを強調

### Card
- パディング:16px(モバイル) / 24px(デスクトップ)
- 影:shadow / shadow-md
- ホバー時:shadow-lg

### Modal
- 背景オーバーレイ:rgba(0,0,0,0.5)
- 最大幅:600px
- モバイルでは全画面表示

### Toast
- 右上または下部中央に表示
- 自動非表示:3秒
- アクション付きの場合は5秒

---

## 10. Accessibility(アクセシビリティ)

### Color Contrast
- 通常テキスト:4.5:1以上(WCAG AA)
- 大きなテキスト(18px+):3:1以上
- UI要素:3:1以上

### Focus Visible
- フォーカスリング:2px solid primary-500
- オフセット:2px
- すべてのインタラクティブ要素に適用

### Keyboard Navigation
- Tab順序が論理的
- Enter/Spaceでアクション
- Escでモーダル/ドロップダウンを閉じる

---

## 11. Responsive Breakpoints(レスポンシブ)

| Breakpoint | Min Width | Target Device          |
|------------|-----------|------------------------|
| sm         | 640px     | 大きなスマホ           |
| md         | 768px     | タブレット             |
| lg         | 1024px    | ノートPC               |
| xl         | 1280px    | デスクトップ           |
| 2xl        | 1536px    | 大画面デスクトップ     |

### Design Approach
- モバイルファースト(min-width media queries)
- 主要ブレークポイント:768px / 1024px
- コンテンツに応じて柔軟に調整
