# [Feature/Epic Name] - Mockup Pack

## Meta
- **Project**: [プロジェクト名]
- **Created**: YYYY-MM-DD
- **Last updated**: YYYY-MM-DD
- **Owner**: [担当者名]
- **Status**: Draft / Review / Approved

---

## 1. Purpose(目的)
このモックアップを作成した目的は何か?

- [ ] 合意形成(ステークホルダー間で見た目を確認)
- [ ] 開発引き渡し(実装可能な仕様として)
- [ ] ブランド検証(ビジュアルアイデンティティの確認)
- [ ] 投資家向けデモ
- [ ] ユーザーテスト用

---

## 2. Scope(対象画面)
このモックアップで扱う画面一覧。

### 対象画面一覧
| Screen ID           | Screen Name            | Priority | Status      | Spec File                        |
|---------------------|------------------------|----------|-------------|----------------------------------|
| `dashboard`         | ダッシュボード         | High     | Completed   | `screens/dashboard__spec.md`     |
| `user-list`         | ユーザー一覧           | High     | Completed   | `screens/user-list__spec.md`     |
| `user-detail`       | ユーザー詳細           | Medium   | In Progress | `screens/user-detail__spec.md`   |
| `settings`          | 設定                   | Low      | Pending     | `screens/settings__spec.md`      |

### 対象外画面
- 管理者専用画面(別途作成予定)
- レポート出力画面(優先度低)

---

## 3. Target Devices(対象デバイス)
主要ブレークポイントと対応デバイス。

| Breakpoint | Width     | Target Device          | Status      |
|------------|-----------|------------------------|-------------|
| Desktop    | ≥1024px   | ノートPC、デスクトップ | Completed   |
| Tablet     | 768-1023px| タブレット             | Completed   |
| Mobile     | <768px    | スマートフォン         | In Progress |

---

## 4. Design Foundation(デザインの基盤)
このモックアップで使用しているデザイン基盤。

### Design System
- 既存のデザインシステム: [リンク or "なし"]
- UIライブラリ: (例) Tailwind CSS / shadcn/ui / MUI / Chakra UI
- アイコンライブラリ: (例) Heroicons / Lucide / Material Icons

### Key Files
- **Style Guide**: `style-guide.md`
- **Design Tokens**: `tokens.json`
- **Component Specs**: `components/`
- **Screen Specs**: `screens/`
- **State Matrix**: `state-matrix.md`
- **Copy**: `copy/strings.md`

---

## 5. Key Design Decisions(重要なデザイン判断)
このモックアップで行った主要な設計判断と、その理由。

### 1. [判断事項の見出し]
- **決定内容**: (例)プライマリカラーを青(#0ea5e9)にした
- **理由**: ブランドカラーと一致、アクセシビリティ基準を満たす
- **代替案**: 緑系も検討したが、エラー色(赤)との区別が難しい

### 2. [判断事項の見出し]
- **決定内容**: (例)テーブルの密度を"medium"にした
- **理由**: データ量が多いため、コンパクトに表示する必要がある
- **代替案**: "comfortable"も試したが、スクロールが多くなりすぎた

### 3. [判断事項の見出し]
- **決定内容**: (例)エラーメッセージをフィールド直下に表示
- **理由**: ユーザーが一目で問題箇所を特定できる
- **代替案**: モーダルで一括表示も検討したが、修正しづらい

---

## 6. Assumptions(暫定仮定)
不明な点を暫定的に仮定して進めた事項。確定次第、更新する。

- [ ] ユーザー名は最大20文字と仮定(API仕様未確定)
- [ ] アバター画像は必須と仮定(未確認)
- [ ] ページネーションは20件/ページと仮定(パフォーマンス未検証)
- [ ] 削除時は確認モーダルを出すと仮定(UX未議論)

---

## 7. Open Questions(未確定事項)
実装前に確定すべき事項。

| Question                                      | Owner       | Due Date   | Status     |
|-----------------------------------------------|-------------|------------|------------|
| アバター画像がない場合、何を表示する?         | Design Team | 2025-01-15 | Open       |
| ソート順はユーザーごとに保存する?             | Product     | 2025-01-20 | Open       |
| モバイルでテーブルをどう表示する?(カード化?) | Dev Team    | 2025-01-25 | Discussing |
| エラー時のリトライ回数は?                     | Backend     | 2025-01-30 | Open       |

---

## 8. Dependencies(依存関係)
このモックアップの実装に必要な前提条件。

### Technical Dependencies
- [ ] API仕様の確定(`/api/users`, `/api/users/:id`)
- [ ] 認証システムの実装(JWT)
- [ ] 画像アップロード機能

### Design Dependencies
- [ ] ブランドカラーの最終確定
- [ ] アイコンライブラリのライセンス確認
- [ ] フォント(Webフォント)のライセンス確認

### Other Dependencies
- [ ] 利用規約・プライバシーポリシーのテキスト確定
- [ ] エラーメッセージの文言確定

---

## 9. Implementation Notes(実装時の注意)
開発者に伝えるべき注意点。

### Performance
- テーブルは仮想スクロール(virtualization)を推奨(1000件以上の場合)
- 画像は遅延読み込み(lazy loading)を使用
- アバター画像はキャッシュする

### Accessibility
- すべてのボタンにaria-labelを付与
- フォームにはaria-describedbyでエラーメッセージを関連付け
- モーダルは開いた時にフォーカスをトラップ

### SEO
- (該当する場合のみ記載)

---

## 10. Testing Checklist(テスト項目)
実装後に確認すべき項目。

### Visual Testing
- [ ] 各画面がモックアップ通りに表示される
- [ ] 各状態(通常/空/ローディング/エラー/成功)が正しく表示される
- [ ] レスポンシブ対応が主要ブレークポイントで機能する

### Interaction Testing
- [ ] ホバー/フォーカス/アクティブ状態が機能する
- [ ] キーボード操作(Tab/Enter/Space/Esc)が機能する
- [ ] バリデーションが正しく動作する
- [ ] 非同期処理中のローディング状態が正しく表示される

### Accessibility Testing
- [ ] コントラストがWCAG AA準拠
- [ ] スクリーンリーダーで主要操作が可能
- [ ] キーボードだけで全操作が可能

---

## 11. Related Documents(関連ドキュメント)
- **PRD**: `docs/prd/YYYY-MM-DD-<slug>.md`
- **画面遷移図**: `docs/flow/<flow-name>.md`
- **API仕様**: `docs/api/<api-spec>.md`
- **ユーザーフロー**: `docs/user-flow/<flow>.md`
- **デザインシステム**: `docs/design-system/`
- **Figma**: [Figmaファイルへのリンク]

---

## 12. Changelog(変更履歴)

### 2025-01-08
- 初版作成
- Dashboard, User List, User Detail の画面仕様を追加

### 2025-01-10
- State matrixを追加
- ComponentsにButton, Card, Tableを追加

### 2025-01-15
- レスポンシブ対応の仕様を詳細化
- Open Questionsを更新
