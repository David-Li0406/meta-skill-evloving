# デバッグレポートテンプレート

Debuggerが出力するデバッグレポートの標準形式。

## レポート構成

デバッグレポートは以下のセクションで構成されます：

1. **問題概要**: エラーの基本情報
2. **エラー詳細**: スタックトレース、再現手順
3. **根本原因分析**: 5 Whysによる分析
4. **修正案**: 複数アプローチとPros/Cons
5. **テスト戦略**: 追加すべきテストケース
6. **Next Actions**: 具体的な作業順序
7. **再発防止策**: 短期・中期・長期の対策
8. **関連情報**: 影響ファイル、参照ドキュメント

---

## テンプレート

```markdown
# Debug Report

**日時**: {YYYY-MM-DD HH:mm}
**報告者**: Debugger Agent
**優先度**: {🔴 P0 / 🟡 P1 / 🔵 P2}

---

## 🐛 問題概要

**エラータイプ**: {runtime-error / test-failure / type-error / build-error / logic-error / integration-error / performance-issue}
**影響レイヤー**: {ui / lib / data-io / test / config}
**重要度**: {P0 / P1 / P2}

**症状**:
{brief-description}

---

## 📍 エラー詳細

**ファイル**: {file-path}:{line-number}
**テストケース**: {test-case-name}（該当する場合）

**エラーメッセージ**:
```
{error-message}
```

**スタックトレース**:
```
{stack-trace}
```

**再現手順**:
1. {step1}
2. {step2}
3. {step3}

**発生頻度**: {毎回 / 時々 / 稀}

**環境情報**:
- Node.js: {version}
- ブラウザ: {browser}（該当する場合）
- OS: {os}

---

## 🔍 根本原因分析

### 5 Whys分析

**現象**: {symptom}

**Why1**: なぜ{question1}？
→ {answer1}

**Why2**: なぜ{question2}？
→ {answer2}

**Why3**: なぜ{question3}？
→ {answer3}

**Why4**: なぜ{question4}？（必要な場合）
→ {answer4}

**Why5**: なぜ{question5}？（必要な場合）
→ {answer5}

### 原因の区別

| 種類 | 内容 |
| :--- | :--- |
| **直接原因** | {immediate-cause} |
| **根本原因** | {root-cause} |

### レイヤー別分析

**影響レイヤー**: {ui / lib / data-io}

**レイヤー固有の問題**:
- {issue1}
- {issue2}

**アーキテクチャ違反**:
- {violation}（該当する場合）

### 影響範囲

**現在の影響**:
- {current-impact1}
- {current-impact2}

**潜在的な影響**:
- {potential-impact1}
- {potential-impact2}

---

## 💡 修正案

### 推奨アプローチ（Approach A）

**優先度**: {immediate / scheduled / backlog}
**作業時間**: {estimated-time}

```typescript
// Before
{before-code}

// After
{after-code}
```

**Pros**:
- ✅ {pro1}
- ✅ {pro2}
- ✅ {pro3}

**Cons**:
- {con1}（該当する場合）

---

### 代替アプローチ（Approach B）

**作業時間**: {estimated-time}

```typescript
// Before
{before-code}

// After
{after-code}
```

**Pros**:
- ✅ {pro1}
- ✅ {pro2}

**Cons**:
- ⚠️ {con1}
- ⚠️ {con2}

---

## 🧪 テスト戦略

### 追加すべきテストケース

```typescript
describe('{test-suite-name}', () => {
  it('{test-case-1}', () => {
    expect({assertion}).toBe({expected});
  });

  it('{test-case-2}', () => {
    expect({assertion}).toBe({expected});
  });

  it('{test-case-3}', () => {
    expect({assertion}).toBe({expected});
  });
});
```

### E2Eテストの修正（該当する場合）

```typescript
// {e2e-test-modification}
```

---

## 🎯 Next Actions

1. ✅ **Approach Aで修正**（{time1}）
2. ✅ **エッジケーステストを追加**（{time2}）
3. ✅ **テスト実行して確認**（{time3}）
   ```bash
   npm run typecheck
   npm test
   ```
4. 📝 **{documentation-update}**（{time4}）

**総作業時間**: 約{total-time}

---

## 📚 再発防止策

### 短期的対策（immediate）

1. {immediate-action1}
2. {immediate-action2}

### 中期的対策（1-2週間）

1. {medium-action1}
2. {medium-action2}

### 長期的対策（継続的改善）

1. {long-action1}
2. {long-action2}

---

## 🔗 関連情報

**影響を受けるファイル**:
- {file1}
- {file2}

**関連ドキュメント**:
- {doc1}
- {doc2}

**関連エージェント**:
- @CodeReviewer（修正後のレビュー）
- @ArchitectureGuardian（アーキテクチャ違反の場合）
- @GeneratorMaintainer（テンプレート修正が必要な場合）

---

**策定者**: Debugger Agent
**承認**: 修正実施前にコードレビュー推奨
```

---

## レポート作成のガイドライン

### 問題概要

- **簡潔**: 1-2文で要約
- **具体的**: 何が起きているかを明確に
- **優先度**: P0/P1/P2を明記

### エラー詳細

- **完全な情報**: エラーメッセージとスタックトレースは省略しない
- **再現手順**: 誰でも再現できるように具体的に
- **環境情報**: 必要な場合のみ記載

### 根本原因分析

- **5 Whys**: 最低3回の「なぜ？」を実行
- **直接原因と根本原因の区別**: 現象と原因を混同しない
- **影響範囲**: 波及効果を考慮

### 修正案

- **複数アプローチ**: 最低2つの選択肢を提示
- **Pros/Cons**: メリット・デメリットを明確に
- **コード例**: Before/Afterを必ず示す

### テスト戦略

- **具体的**: テストコード例を含める
- **エッジケース**: 境界値テストを追加
- **網羅性**: 失敗シナリオも含める

### Next Actions

- **具体的**: 実行可能な単位に分解
- **時間見積もり**: 各タスクの所要時間を記載
- **順序**: 依存関係を考慮した順序

### 再発防止策

- **3段階**: 短期・中期・長期に分類
- **実行可能**: 具体的なアクションを提示
- **プロセス改善**: 個人ではなくプロセスの問題として捉える

---

## レポート例

### 例1: lib層のゼロ除算エラー

```markdown
# Debug Report

**日時**: 2025-01-19 15:45
**報告者**: Debugger Agent
**優先度**: 🟡 P1

---

## 🐛 問題概要

**エラータイプ**: test-failure
**影響レイヤー**: lib
**重要度**: P1

**症状**:
progressCalculator のユニットテストが失敗。total が 0 の場合に NaN を返す。

---

## 📍 エラー詳細

**ファイル**: app/lib/dashboard/progressCalculator.ts:18
**テストケース**: "should return 0 when total is 0"

**エラーメッセージ**:
```
Expected: 0
Received: NaN
```

**再現手順**:
1. npm test を実行
2. progressCalculator.test.ts のテストが失敗

**発生頻度**: 毎回

---

## 🔍 根本原因分析

### 5 Whys分析

**現象**: NaN が返される

**Why1**: なぜ NaN が返されるか？
→ total が 0 で除算している

**Why2**: なぜ total が 0 になるか？
→ テストケースで total: 0 を渡している

**Why3**: なぜその場合を想定していなかったか？
→ エッジケースのテストが不足

### 原因の区別

| 種類 | 内容 |
| :--- | :--- |
| **直接原因** | 0 による除算 |
| **根本原因** | エッジケースの考慮不足 |

---

## 💡 修正案

### 推奨アプローチ（Approach A）

**優先度**: immediate
**作業時間**: 10分

```typescript
// Before
export function progressCalculator(completed: number, total: number): number {
  const progress = (completed / total) * 100;
  return Math.min(progress, 100);
}

// After
export function progressCalculator(completed: number, total: number): number {
  if (total === 0) {
    return 0;
  }
  const progress = (completed / total) * 100;
  return Math.min(progress, 100);
}
```

**Pros**:
- ✅ シンプルで読みやすい
- ✅ パフォーマンスへの影響なし

---

## 🧪 テスト戦略

```typescript
describe('progressCalculator edge cases', () => {
  it('should return 0 when total is 0', () => {
    expect(progressCalculator(0, 0)).toBe(0);
  });
});
```

---

## 🎯 Next Actions

1. ✅ **Approach Aで修正**（5分）
2. ✅ **エッジケーステストを追加**（5分）
3. ✅ **テスト実行して確認**（2分）

**総作業時間**: 約12分

---

## 📚 再発防止策

### 短期的対策

1. progressCalculator のエッジケーステスト追加

### 中期的対策

1. TDD_WORK_FLOW.md にエッジケースチェックリスト追加

### 長期的対策

1. lib層の数値計算関数テンプレートにガード節を標準装備
```

---

## レポートの品質基準

### ✅ 良いレポート

- **明確**: 誰が読んでも理解できる
- **具体的**: コード例と手順が含まれる
- **実行可能**: Next Actionsがすぐ実行できる
- **教育的**: 再発防止策が提案されている

### ❌ 悪いレポート

- **曖昧**: 何が問題かわからない
- **抽象的**: コード例がない
- **実行不可**: 次に何をすべきかわからない
- **対症療法**: 根本原因を追求していない
