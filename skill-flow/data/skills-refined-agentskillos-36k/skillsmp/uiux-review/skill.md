---
name: uiux-review
description: UI/UXレビュー - Material Design 3 + WCAG 2.2 AA + Nielsen 10原則で実装に直結するレビュー
requires-guidelines:
  - ui-ux
  - nextjs-react
  - tailwind
  - shadcn
---

# UI/UXデザインレビュー

## 使用タイミング

- **UIコンポーネント実装時**
- **アクセシビリティチェック時**
- **デザインシステム構築時**
- **レビュー・改善提案時**

---

## 鉄板3原則レビュー（優先順）

### 1️⃣ Material Design 3（コンポーネント実装）⭐

**レビュー観点**:
- コンポーネント状態の完全性（8種：default, hover, focus, active, disabled, loading, error, success）
- デザイントークンの一貫性
- スペーシング（4pxベース）

### 2️⃣ WCAG 2.2 AA（アクセシビリティ）⭐

**レビュー観点**:
- コントラスト比（4.5:1以上）
- キーボード操作（Tab/Enter/Escape）
- フォーカス表示（2px以上のリング）
- タッチターゲット（44x44px以上）

### 3️⃣ Nielsen 10原則（ユーザビリティ）⭐

**レビュー観点**:
- システム状態の可視化
- 一貫性と標準
- エラー防止と回復

---

## レビュー手順

### Step 1: Material Design 3チェック

#### 🔴 Critical確認事項
- [ ] コンポーネント状態8種定義済み
- [ ] デザイントークン使用（カスタムカラー乱用なし）
- [ ] スペーシング4pxベース（4, 8, 12, 16, 24, 32, 48）
- [ ] 角丸M3準拠（sm:8px, md:12px, lg:16px）

### Step 2: WCAG 2.2 AAチェック

#### 🔴 Critical確認事項
- [ ] コントラスト比4.5:1以上（通常テキスト）
- [ ] コントラスト比3:1以上（UIコンポーネント）
- [ ] キーボード操作可能（Tab, Enter, Escape）
- [ ] フォーカス表示明確（2px以上のリング）
- [ ] タッチターゲット44x44px以上
- [ ] 画像にalt属性
- [ ] フォームにlabel要素
- [ ] 色だけに依存しない情報伝達

### Step 3: Nielsen 10原則チェック

#### 🟡 Warning確認事項
- [ ] 1. システム状態の可視化（Loading, Progress）
- [ ] 2. 現実世界とのマッチ（自然な言葉）
- [ ] 3. ユーザー制御と自由（Undo, Cancel）
- [ ] 4. 一貫性と標準（統一されたUI）
- [ ] 5. エラー防止（確認ダイアログ）
- [ ] 6. 再認識 > 想起（アイコン+ラベル）
- [ ] 7. 柔軟性と効率性（ショートカット）
- [ ] 8. 美的でミニマル（情報過多を避ける）
- [ ] 9. エラー認識・診断・回復（具体的なメッセージ）
- [ ] 10. ヘルプとドキュメント（ツールチップ）

---


## 出力形式

### レビュー結果

```
## UI/UXレビュー結果

### 1️⃣ Material Design 3

🔴 **Critical**: `Button.tsx:15` - コンポーネント状態未定義
- 問題: hover/focus/disabled状態が未定義
- 修正案: [コード例]

🟡 **Warning**: `Card.tsx:8` - デザイントークン不使用
- 問題: カスタムカラー#6750A4を直接指定
- 改善案: bg-primary使用

### 2️⃣ WCAG 2.2 AA

🔴 **Critical**: `Form.tsx:42` - フォームラベルなし
- 問題: input要素にlabel紐付けなし
- 修正案: [コード例]

🔴 **Critical**: `Hero.tsx:20` - コントラスト比不足
- 問題: text-gray-300 on bg-gray-200 (2.1:1)
- 修正案: text-gray-900使用（7:1）

### 3️⃣ Nielsen 10原則

🟡 **Warning**: `DeleteButton.tsx:5` - エラー防止不足
- 問題: 確認なしで削除実行（原則5違反）
- 改善案: AlertDialog追加

📊 **Summary**:
- Material Design 3: Critical 1件 / Warning 1件
- WCAG 2.2 AA: Critical 2件 / Warning 0件
- Nielsen 10原則: Warning 1件

✅ **総合評価**: Critical問題を優先的に修正してください
```

---

## プロジェクト別対応

### 管理画面（SaaS）

**追加チェック**:
- デジタル庁デザインシステム参照
- 日本語文言の適切性
- フォーム設計パターン

### 一般ユーザー向けWebサービス

**追加チェック**:
- M3 Expressive活用
- 視覚的魅力（シェイプ、モーション）
- LP/マーケティングサイト最適化

---

## 詳細実装例

詳細な実装例とNG/OK比較は以下を参照:
- `~/.claude/guidelines-archive/design/ui-ux-guidelines.md` - Material Design 3詳細仕様
- `~/.claude/guidelines/languages/nextjs-react.md` - React実装パターン
- `~/.claude/guidelines/languages/tailwind.md` - Tailwind CSS v4
- `~/.claude/guidelines/languages/shadcn.md` - shadcn/ui v2.5

---

## 外部知識ベース

最新情報確認には context7 を活用:
- [Material Design 3](https://m3.material.io/)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [デジタル庁デザインシステム](https://design.digital.go.jp/)
- shadcn/ui公式
- Radix UI（アクセシビリティパターン）

