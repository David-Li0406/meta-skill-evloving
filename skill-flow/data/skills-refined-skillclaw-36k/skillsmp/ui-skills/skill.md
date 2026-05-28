---
name: ui-skills
description: UI Skills - Tailwind CSS/motion/react特化のエージェント向けUI構築制約
requires-guidelines:
  - nextjs-react
  - tailwind
  - shadcn
---

# UI Skills: エージェント向けUI構築制約

## 使用タイミング

- Tailwind CSS/React実装時
- アニメーション実装レビュー時
- アクセシブルコンポーネント構築時

**公式**: https://github.com/ibelick/ui-skills

---

## テクノロジースタック

| 要素 | 要件 | 詳細 |
|------|------|------|
| スタイリング | **MUST** | Tailwind CSS defaults |
| アニメーション | **MUST** | `motion/react` |
| クラス管理 | **MUST** | `cn`（`clsx` + `tailwind-merge`） |

---

## ルール早見表

### Components

| 区分 | ルール |
|------|--------|
| 🔴 MUST | アクセシブルコンポーネントプリミティブ使用（Base UI, React Aria, Radix） |
| 🔴 MUST | アイコンのみボタンに`aria-label` |
| 🔴 NEVER | 同一インタラクション内で複数プリミティブシステム混在 |
| 🔴 NEVER | キーボード・フォーカス動作の手動実装 |

### Interaction

| 区分 | ルール |
|------|--------|
| 🔴 MUST | 破壊的アクション → `AlertDialog`必須 |
| 🔴 MUST | エラーはアクション発生場所の隣に表示 |
| 🔴 MUST | 固定要素に`safe-area-inset`尊重 |
| 🔴 NEVER | `h-screen`使用（`h-dvh`に置換） |
| 🔴 NEVER | `input`/`textarea`のペースト禁止 |
| 🟡 SHOULD | ローディングは構造的スケルトン表示 |

### Animation

| 区分 | ルール |
|------|--------|
| 🔴 MUST | 明示的リクエストなしのアニメーション追加禁止 |
| 🔴 MUST | `transform`, `opacity`のみアニメート |
| 🔴 NEVER | レイアウト属性の動画化（`width`, `height`, `margin`等） |
| 🔴 NEVER | インタラクションフィードバック200ms超 |
| 🟡 SHOULD | `prefers-reduced-motion`尊重 |

### Typography

| 区分 | ルール |
|------|--------|
| 🔴 MUST | 見出し → `text-balance` |
| 🔴 MUST | 本文・段落 → `text-pretty` |
| 🔴 MUST | データ表示 → `tabular-nums` |
| 🔴 NEVER | 明示要求なしの`letter-spacing`変更 |

### Layout

| 区分 | ルール |
|------|--------|
| 🔴 MUST | 固定z-indexスケール（任意`z-[999]`禁止） |
| 🟡 SHOULD | 正方形要素は`size-*`（`w-* h-*`より優先） |

### Performance

| 区分 | ルール |
|------|--------|
| 🔴 NEVER | 大規模`blur()`/`backdrop-filter`の動画化 |
| 🔴 NEVER | アクティブアニメーション外での`will-change` |
| 🔴 NEVER | レンダーロジックで可能な処理に`useEffect` |

### Design

| 区分 | ルール |
|------|--------|
| 🔴 MUST | 空状態に明確な次アクションを用意 |
| 🔴 NEVER | 明示要求なしのグラデーション |
| 🔴 NEVER | 紫色/マルチカラーグラデーション |
| 🟡 SHOULD | 既存テーマ/Tailwind標準色を優先 |

---

## 主要パターン

```tsx
// アイコンボタン
<button aria-label="Close menu"><X className="size-4" /></button>

// h-dvh使用
<div className="h-dvh">...</div>

// 破壊的アクション
<AlertDialog>
  <AlertDialogTrigger asChild><Button variant="destructive">Delete</Button></AlertDialogTrigger>
  <AlertDialogContent>...</AlertDialogContent>
</AlertDialog>

// アニメーション（transform/opacityのみ）
<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }} />
```

---

## チェックリスト

- [ ] アクセシブルコンポーネントプリミティブ使用
- [ ] アイコンボタンに`aria-label`
- [ ] 破壊的アクションに`AlertDialog`
- [ ] `h-screen` → `h-dvh`
- [ ] アニメーションは`transform`/`opacity`のみ
- [ ] 不要な`useEffect`なし
- [ ] Tailwind標準色優先

---

## 出力形式

```markdown
## UI Skillsレビュー結果

### 🔴 Critical Violations
**`Button.tsx:15`** - アクセシブルコンポーネント未使用 → Radix UI Buttonに置換

### 🟡 Warnings
**`Card.tsx:8`** - カスタムカラー使用 → `bg-primary`推奨

### ✅ Summary
Critical: 1件 / Warning: 1件
```

---

## 参考リンク

- [ui-skills](https://github.com/ibelick/ui-skills)
- [Base UI](https://base-ui.com/)
- [React Aria](https://react-spectrum.adobe.com/react-aria/)
- [Radix UI](https://www.radix-ui.com/)
- [motion/react](https://motion.dev/)
