---
name: web-accessibility-and-design-implementation
description: Use this skill when implementing web accessibility standards (WCAG/ARIA) and design tokens for interactive UI components like forms and error displays.
---

# Web Accessibility and Design Implementation Skill

## 📋 目次

1. [概要](#概要)
2. [使う場面](#使う場面)
3. [12のルール](#12のルール)
4. [QAチェックリスト](#qaチェックリスト)
5. [公式ドキュメント・参考リソース](#公式ドキュメント・参考リソース)
6. [実践例](#実践例)

---

## 概要

このSkillは、Webアクセシビリティと一貫性を重視したUI実装のガイドラインを提供します。WCAG 2.1準拠、セマンティックHTML、ARIA属性、キーボード操作、コントラスト比、デザイントークンの実装に関するベストプラクティスを含みます。

---

## 使う場面

- 新規UIコンポーネント（フォーム・ボタン・エラー表示）を作成する際
- 既存コンポーネントのアクセシビリティ（ARIA・キーボード操作・コントラスト）を修正する際
- デザイントークンをWeb/iOS/Android各プラットフォームへ自動出力する際
- レスポンシブ環境でタイポ・余白を流体スケールで統一する際
- 多言語・縦書き・RTL対応でレイアウトを論理プロパティへ移行する際

---

## 12のルール

1. **トークンを明示せよ**: 色・余白・文字サイズは全てCSS Custom Propertyで定義し、生値を直書きするな。
2. **コントラスト比を数値で保証せよ**: 本文は4.5:1以上（WCAG AA）、18pt以上または太字14pt以上は3:1以上を維持せよ。
3. **可変フォントとclamp()で流体スケールを実装せよ**: 文字サイズは `clamp(1rem, 0.875rem + 0.5vw, 1.125rem)` のように下限・可変・上限を明記せよ。
4. **論理プロパティで物理方向依存を排除せよ**: `margin-left` → `margin-inline-start`、`padding-top` → `padding-block-start` を用いよ。
5. **全インタラクティブ要素をキーボード到達可能にせよ**: `<button>`, `<a>`, `<input>` 等のネイティブ要素を優先せよ。
6. **状態（hover/focus/active/disabled）を視覚とARIAで二重に伝達せよ**: `:focus-visible` でフォーカスリングを表示し、`aria-disabled="true"` でスクリーンリーダーへ通知せよ。
7. **エラーは要約→詳細の順で構造化せよ**: フォーム送信失敗時、ページ上部に `role="alert"` でエラー数と各フィールドへのアンカーリンクを配置せよ。
8. **エラーメッセージは行動を明示せよ**: ❌「入力が無効です」→ ✅「メールアドレスに@を含めてください」。
9. **同期検証はaria-live、非同期はrole="status"を使い分けよ**: 入力中のリアルタイム検証は `aria-live="polite"`、非同期API応答は `role="status"` を使用せよ。
10. **最小タッチターゲットを守れ**: モバイルは44×44px、デスクトップは24×24pxの最小タッチターゲットを確保せよ。
11. **レスポンシブブレークポイントは流体スケールで不要とせよ**: `clamp()` による連続スケールで段階的変化を排除せよ。
12. **プラットフォーム出力は自動化せよ**: `tokens.json` からStyle Dictionaryで各形式を生成し、手動コピーを禁止せよ。

---

## QAチェックリスト

1. **Tab**キーで全インタラクティブ要素へ順番に到達できる
2. エラー発生時、フォーカスがエラー要約（`role="alert"`）へ自動移動する
3. 各エラーメッセージが対応する入力フィールドに`aria-describedby`で紐付いている
4. 本文のコントラスト比が4.5:1以上
5. キーボードのみで全コンポーネントの状態が識別可能
6. ビューポート幅320px～1280pxで文字サイズ・余白が`clamp()`により連続的に変化する
7. `margin-inline-start`等の論理プロパティを使用
8. 状態色が各トーンで一貫したコントラスト比を保つ
9. `tokens.json`がStyle Dictionary経由で各形式へ出力可能
10. 各ルールに参照元ソースのURLを付与

---

## 公式ドキュメント・参考リソース

- **[WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)** - W3Cアクセシビリティガイドライン
- **[WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)** - ARIAパターンガイド
- **[WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)** - コントラスト比チェック
- **[Style Dictionary](https://styledictionary.com/)** - デザイントークン管理
- **[Utopia - Fluid Responsive Design](https://utopia.fyi/)** - 流体レスポンシブデザイン

---

## 実践例

### Example 1: アクセシブルなボタン

```tsx
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  'aria-label'?: string
}

export function Button({ children, onClick, disabled, 'aria-label': ariaLabel }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-label={ariaLabel}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {children}
    </button>
  )
}
```

### Example 2: アクセシブルなフォーム

```tsx
export function ContactForm() {
  return (
    <form>
      <div>
        <label htmlFor="name">Name *</label>
        <input
          id="name"
          type="text"
          required
          aria-required="true"
        />
      </div>

      <div>
        <label htmlFor="email">Email *</label>
        <input
          id="email"
          type="email"
          required
          aria-required="true"
          aria-describedby="email-help"
        />
        <span id="email-help" className="text-sm text-gray-600">
          We'll never share your email.
        </span>
      </div>

      <div role="group" aria-labelledby="contact-method">
        <span id="contact-method">Preferred contact method</span>
        <label>
          <input type="radio" name="contact" value="email" />
          Email
        </label>
        <label>
          <input type="radio" name="contact" value="phone" />
          Phone
        </label>
      </div>

      <button type="submit">Submit</button>
    </form>
  )
}
```

### Example 3: アクセシブルなモーダル

```tsx
'use client'

import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'

interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousActiveElement = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement
      modalRef.current?.focus()
    } else {
      previousActiveElement.current?.focus()
    }
  }, [isOpen])

  if (!isOpen) return null

  return createPortal(
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
      onClick={onClose}
    >
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
        className="bg-white p-6 rounded-lg max-w-md w-full"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 id="modal-title" className="text-2xl font-bold mb-4">
          {title}
        </h2>
        {children}
        <button
          onClick={onClose}
          aria-label="Close modal"
          className="mt-4 px-4 py-2 bg-gray-200 rounded"
        >
          Close
        </button>
      </div>
    </div>,
    document.body
  )
}
```

---

_Last updated: 2025-12-26_