# [コンポーネント名] Specification

## Meta
- **Component ID**: `<component-id>`
- **Last updated**: YYYY-MM-DD
- **Owner**: (誰が仕様を管理?)
- **Status**: Draft / Review / Approved

---

## 1. Intent(目的)
このコンポーネントは何のために存在するか?どんな場面で使われるか?

- (例)ユーザーの主要アクションをトリガーするためのボタン
- (例)ステータスを視覚的に伝えるためのバッジ
- (例)データを一覧表示し、ソート・フィルタ・ページネーションを提供するテーブル

---

## 2. Anatomy(構造)
コンポーネントの構成要素を記述。

```
┌──────────────────────────────┐
│ [Icon] Label [Badge]          │ ← Container
│                                │
│ Helper Text (optional)         │
└──────────────────────────────┘
```

### 構成要素
- **Container**: 全体を囲む要素
- **Icon** (optional): 左側のアイコン
- **Label**: メインテキスト
- **Badge** (optional): 右側のバッジ
- **Helper Text** (optional): 補助テキスト

---

## 3. Variants(バリアント)
見た目のバリエーション。用途に応じて使い分ける。

| Variant   | Use Case                          | Example              |
|-----------|-----------------------------------|----------------------|
| primary   | 主要アクション(1画面1つ推奨)       | 「保存」「作成」     |
| secondary | 副次的アクション                   | 「キャンセル」       |
| ghost     | 軽微なアクション、リンク的         | 「詳細を見る」       |
| danger    | 削除・破壊的アクション             | 「削除」             |

---

## 4. States(状態)
インタラクション時の状態変化。

| State    | Description                           | Visual Changes                     |
|----------|---------------------------------------|------------------------------------|
| default  | 通常状態                              | 基本スタイル                       |
| hover    | マウスホバー時                        | 背景色を少し暗く/明るく             |
| active   | クリック時                            | 背景色をさらに暗く                 |
| focus    | キーボードフォーカス時                | フォーカスリングを表示             |
| disabled | 無効化時                              | グレーアウト、cursor: not-allowed  |
| loading  | 非同期処理中                          | Spinner表示、disabled状態と同じ    |
| error    | エラー状態(Inputなど)                 | 赤いボーダー、エラーメッセージ表示 |
| success  | 成功状態(Inputなど)                   | 緑のボーダー、チェックアイコン表示 |

---

## 5. Props / API(プロパティ)
開発実装時のAPI設計。

| Prop         | Type                              | Default   | Required | Description                      |
|--------------|-----------------------------------|-----------|----------|----------------------------------|
| variant      | 'primary' \| 'secondary' \| ...   | 'primary' | No       | ボタンのバリアント               |
| size         | 'sm' \| 'md' \| 'lg'              | 'md'      | No       | サイズ                           |
| disabled     | boolean                           | false     | No       | 無効化                           |
| loading      | boolean                           | false     | No       | ローディング状態                 |
| icon         | ReactNode                         | undefined | No       | 左側のアイコン                   |
| iconPosition | 'left' \| 'right'                 | 'left'    | No       | アイコンの位置                   |
| fullWidth    | boolean                           | false     | No       | 幅を100%にする                   |
| onClick      | (e: Event) => void                | undefined | No       | クリックハンドラ                 |
| children     | ReactNode                         | -         | Yes      | ラベルテキスト                   |

---

## 6. Spacing & Typography(余白とタイポ)
コンポーネント内外の余白、フォント設定。

### Spacing
| Size | Padding (x/y) | Height | Min Width |
|------|---------------|--------|-----------|
| sm   | 8px / 4px     | 32px   | 64px      |
| md   | 12px / 8px    | 40px   | 80px      |
| lg   | 16px / 12px   | 48px   | 96px      |

### Typography
| Size | Font Size | Font Weight | Line Height |
|------|-----------|-------------|-------------|
| sm   | 14px      | 500         | 20px        |
| md   | 16px      | 500         | 24px        |
| lg   | 18px      | 500         | 28px        |

---

## 7. Colors(色)
バリアントごとの色設定。トークンを参照。

### Primary
- Background: `tokens.color.primary.500`
- Text: `tokens.color.white`
- Hover: `tokens.color.primary.600`
- Active: `tokens.color.primary.700`

### Secondary
- Background: `tokens.color.gray.200`
- Text: `tokens.color.gray.900`
- Hover: `tokens.color.gray.300`
- Active: `tokens.color.gray.400`

### Danger
- Background: `tokens.color.red.500`
- Text: `tokens.color.white`
- Hover: `tokens.color.red.600`
- Active: `tokens.color.red.700`

---

## 8. Accessibility(アクセシビリティ)
最低限の配慮事項。

- **セマンティクス**: `<button>` タグを使用(リンク的な場合は `<a>` + role="button")
- **フォーカス**: フォーカスリングを必ず表示(outline: 2px solid)
- **キーボード**: Enter/Spaceでトリガー
- **スクリーンリーダー**: aria-label(アイコンのみの場合)、aria-disabled(disabled時)
- **コントラスト**: WCAG AA準拠(4.5:1以上)

---

## 9. Do / Don't(使い方のルール)
コンポーネントを正しく使うためのガイドライン。

### Do ✅
- 1画面に primary ボタンは1つまで
- ラベルは「動詞+目的語」で明確に(例:「保存する」「ユーザーを削除」)
- 破壊的アクションには danger バリアントを使う
- ローディング中は disabled + loading 状態にし、二重送信を防ぐ

### Don't ❌
- primary ボタンを複数並べない(どれが主要か分からなくなる)
- ラベルが曖昧な「OK」「送信」だけにしない
- danger バリアントを通常のアクションに使わない(ユーザーを怖がらせる)
- disabled 状態で理由を説明しない(ツールチップで「〇〇を選択してください」)

---

## 10. Examples(使用例)
実際の使用シーンをコード例で示す。

### 基本的な使用
```tsx
<Button variant="primary" size="md">
  保存する
</Button>
```

### アイコン付き
```tsx
<Button variant="secondary" icon={<PlusIcon />}>
  新規作成
</Button>
```

### ローディング状態
```tsx
<Button variant="primary" loading disabled>
  保存中...
</Button>
```

### フルワイド
```tsx
<Button variant="primary" fullWidth>
  ログイン
</Button>
```

---

## 11. Design Tokens(トークン参照)
このコンポーネントが参照するトークン一覧。

- `tokens.color.primary.*`
- `tokens.color.gray.*`
- `tokens.color.red.*`
- `tokens.spacing.sm` / `md` / `lg`
- `tokens.borderRadius.md`
- `tokens.fontSize.sm` / `md` / `lg`
- `tokens.fontWeight.medium`

---

## 12. Related Components(関連コンポーネント)
似たコンポーネントや、一緒に使われるコンポーネント。

- `IconButton`: アイコンのみのボタン
- `ButtonGroup`: 複数のボタンをグループ化
- `Link`: リンク的な見た目のボタン

---

## 13. Open Questions(未確定事項)
実装前に確定すべき事項。

- [ ] (例)Ripple effectを入れるか?
- [ ] (例)Tooltipを内包するか?それとも別コンポーネントとして組み合わせるか?
- [ ] (例)アイコンのサイズはどう決める?固定?propsで指定?

---

## 14. Links(関連リンク)
- デザインシステム: `docs/design-system/`
- Storybook: (実装後のStorybook URL)
- Figma: (Figmaコンポーネントへのリンク)
