# アーキテクチャチェック項目定義

5種類のアーキテクチャチェック項目の詳細定義。

## チェック項目一覧

| # | チェック種類 | 目的 |
| :--- | :--- | :--- |
| 1 | 3大層アーキテクチャチェック | 層の責務分離を検証 |
| 2 | TDDチェック | テスト駆動開発の実践を検証 |
| 3 | テンプレート起点チェック | ファイル生成方法を検証 |
| 4 | デザイントークンチェック | スタイリング規約を検証 |
| 5 | Remixアーキテクチャチェック | Remix原則の遵守を検証 |

---

## 1. 3大層アーキテクチャチェック

### 目的

UI層・lib層・data-io層の責務分離を検証する。

### チェック項目

#### 1.1 lib層のチェック

- [ ] lib層が他層をimportしていないか？
  - ❌ NG: `import { SomeComponent } from '~/routes/...'`
  - ❌ NG: `import { someService } from '~/data-io/...'`
  - ✅ OK: `import { anotherUtil } from '~/lib/...'`

- [ ] lib層に副作用（fetch、localStorage等）がないか？
  - ❌ NG: `await fetch(...)`
  - ❌ NG: `localStorage.setItem(...)`
  - ❌ NG: `window.location.href = ...`
  - ✅ OK: 純粋関数のみ

#### 1.2 UI層のチェック

- [ ] UI層にビジネスロジック（複雑な計算、バリデーション）がないか？
  - ❌ NG: コンポーネント内で複雑な計算
  - ❌ NG: コンポーネント内でバリデーションロジック
  - ✅ OK: lib層の関数を呼び出すのみ

#### 1.3 data-io層のチェック

- [ ] data-io層がUIコードをimportしていないか？
  - ❌ NG: `import { SomeComponent } from '~/routes/...'`
  - ❌ NG: `import { useHook } from '~/components/...'`
  - ✅ OK: lib層のimportは可能

### 重要度

🔴 Critical

### 参照

`docs/ARCHITECTURE_MANIFESTO2.md`

---

## 2. TDDチェック

### 目的

テスト駆動開発が実践されていることを検証する。

### チェック項目

- [ ] テストファイルが存在するか？
  - E2Eテスト: `tests/e2e/screen/{feature}.spec.ts`
  - ユニットテスト: `tests/unit/lib/{feature}/{logic}.test.ts`

- [ ] E2Eテストが先に書かれているか？
  - E2Eテストが存在し、コミット履歴で実装より先に作成されている

- [ ] ユニットテストのカバレッジが80%以上か？
  - lib層の関数に対するテストカバレッジ

### 重要度

🟡 Warning

### 参照

- `develop/service-name/GUIDING_PRINCIPLES.md` (Outside-In TDD)
- `docs/E2E_TEST_CRITERIA.md`
- `docs/ユニットテストの最低基準.md`

---

## 3. テンプレート起点チェック

### 目的

ファイルがテンプレートから生成されたものか検証する。

### チェック項目

- [ ] ファイルがテンプレートから生成されたものか？
  - テンプレート定義: `scripts/generate/config.json`
  - 生成コマンド: `npm run generate`

- [ ] 手動作成されたファイル（規約違反）がないか？
  - 特定のパターンに従わないファイル名
  - テンプレートにない構造

### 重要度

🟡 Warning

### 参照

`scripts/generate/README.md`

---

## 4. デザイントークンチェック

### 目的

スタイリング規約の遵守を検証する。

### チェック項目

- [ ] ハードコードされた色・サイズ値がないか？
  - ❌ NG: `style={{ color: '#ff0000' }}`
  - ❌ NG: `style={{ fontSize: '16px' }}`
  - ✅ OK: Tailwindクラス使用

- [ ] CSS変数（`var(--token-name)`）を使用しているか？
  - カスタムスタイルが必要な場合のみCSS変数を使用
  - ❌ NG: `color: #ff0000;`
  - ✅ OK: `color: var(--color-primary);`

### 重要度

🔵 Info

### 参照

- `docs/design-token-specification.md`
- `docs/CSS_structure/STYLING_CHARTER.md`

---

## 5. Remixアーキテクチャチェック

### 目的

Remixの思想に沿った実装になっているか検証する。

### チェック項目

- [ ] loader/actionが適切に使われているか？
  - データ取得は`loader`で実行
  - データ変更は`action`で実行
  - ✅ OK: `export async function loader({ request }: LoaderArgs) { ... }`
  - ✅ OK: `export async function action({ request }: ActionArgs) { ... }`

- [ ] useEffectで副作用を実行していないか？
  - ❌ NG: `useEffect(() => { fetch(...) }, [])`
  - ✅ OK: loader/actionで副作用を実行

- [ ] 段階的強化の原則に従っているか？
  - JavaScriptなしでも基本機能が動作するか
  - フォーム送信は`<Form>`コンポーネントを使用
  - ❌ NG: `onClick`でfetch実行
  - ✅ OK: `<Form method="post">`でaction実行

### 重要度

🟡 Warning

### 参照

- Remix公式ドキュメント
- `CLAUDE.md` (Remixの特性)

---

## チェック実行順序

以下の順序でチェックを実行することを推奨：

1. **3大層アーキテクチャチェック** (🔴 Critical)
2. **TDDチェック** (🟡 Warning)
3. **Remixアーキテクチャチェック** (🟡 Warning)
4. **テンプレート起点チェック** (🟡 Warning)
5. **デザイントークンチェック** (🔵 Info)

## 違反の重要度定義

| 重要度 | 定義 | 対応 |
| :--- | :--- | :--- |
| 🔴 Critical | アーキテクチャの根幹に関わる違反 | 必ず修正が必要 |
| 🟡 Warning | 品質に影響する違反 | 修正を推奨 |
| 🔵 Info | 改善の余地あり | 参考情報として提示 |
