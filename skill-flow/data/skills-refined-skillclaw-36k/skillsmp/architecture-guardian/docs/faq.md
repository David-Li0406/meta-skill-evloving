# よくある質問（FAQ）

ArchitectureGuardianに関するよくある質問と回答。

## Q1: ArchitectureGuardianとCodeReviewerの違いは？

**A**:

- **ArchitectureGuardian**: **設計の守護神**。アーキテクチャ設計と高レベルの違反検出（3大層、TDDフロー、Remix原則）を担う。**「どう作るべきか」**を教える。
- **CodeReviewer**: **品質の審査員**。詳細なコードレビュー（命名規則、TypeScript品質、テストカバレッジ、スコアリング）を担う。**「正しく作られているか」**を評価する。

**使い分け**:

| タイミング | 使うエージェント | 理由 |
| :--- | :--- | :--- |
| 開発の最初（設計段階） | ArchitectureGuardian | アーキテクチャ設計を相談 |
| 実装中（アーキテクチャ疑問） | ArchitectureGuardian | アーキテクチャ違反をチェック |
| 実装後（コード品質確認） | CodeReviewer | 詳細なコードレビュー |
| エラー発生時 | Debugger | エラー解析と修正方針 |

---

## Q2: ArchitectureGuardianはいつ使うべき？

**A**:

### ✅ 使うべきタイミング

1. **新機能の設計を相談したい時**（開発の最初）
   - 例: `@ArchitectureGuardian 「ダッシュボード画面の設計を提案して」`

2. **アーキテクチャ違反をチェックしたい時**
   - 例: `@ArchitectureGuardian 「app/lib/auth/login.ts のアーキテクチャをチェックして」`

3. **どのサブエージェントを使うべきか迷った時**
   - 例: `@ArchitectureGuardian 「どのサブエージェントを使えばいい？」`

4. **設計思想について質問がある時**
   - 例: `@ArchitectureGuardian 「なぜlib層で副作用を実行してはいけないのか？」`

### ❌ 使わない方が良いタイミング

1. **詳細なコード品質チェック** → `@CodeReviewer` を使用
2. **エラー解析** → `@Debugger` を使用
3. **ファイル生成** → `@GeneratorOperator` を使用
4. **テンプレート管理** → `@GeneratorMaintainer` を使用

---

## Q3: 自動起動はいつ発動する？

**A**:

CodeReviewerがアーキテクチャ違反（3大層違反、TDD違反、Remix違反等）を検知した際に自動的に発動します。手動で呼び出す必要はありません。

**自動起動の例**:

```text
@CodeReviewer 「ダッシュボード機能のレビューをお願いします」
  ↓
CodeReviewer: アーキテクチャ違反を検知
  ↓
ArchitectureGuardian: 自動起動（修正ガイダンスを提示）
```

**自動起動される違反の種類**:

- 3大層アーキテクチャ違反（lib層でfetch等）
- TDD違反（テストがない、E2Eテストがない等）
- Remixアーキテクチャ違反（useEffectで副作用実行等）
- テンプレート起点違反（手動でファイル作成等）
- デザイントークン違反（ハードコードされた色・サイズ等）

---

## Q4: ArchitectureGuardianが推薦するサブエージェントを無視してもいい？

**A**:

もちろん。ArchitectureGuardianの推薦はあくまで提案です。ただし、推薦理由を確認すると、より良い判断ができます。

**推薦を無視してもよいケース**:

- 状況を自分でよく理解している
- 推薦と異なるアプローチを試したい
- 推薦されたエージェントが利用できない

**推薦に従うメリット**:

- 開発フローに沿った最適なエージェントを選択できる
- エージェントの使い分けを学習できる
- 開発効率が向上する

---

## Q5: 設計提案を受けた後、必ずその通りに実装しなければならない？

**A**:

いいえ。ArchitectureGuardianの設計提案はあくまで推奨案です。プロジェクトの状況に応じて調整してください。

**ただし、以下は厳守してください**:

- ✅ 3大層アーキテクチャの責務分離
- ✅ lib層での副作用禁止
- ✅ テンプレート起点コーディング

**調整可能な部分**:

- ファイル名（命名規則を守る範囲で）
- 機能の優先順位（MVPを維持する範囲で）
- テストの詳細度（最低基準を満たす範囲で）

---

## Q6: ArchitectureGuardianの違反レポートに納得できない場合は？

**A**:

以下の手順で確認してください：

1. **設計思想の背景を確認**
   - `@ArchitectureGuardian 「なぜこれが違反なのか教えて」`
   - 参照ドキュメント（`docs/ARCHITECTURE_MANIFESTO2.md`等）を確認

2. **具体例を確認**
   - 違反レポートの「具体例」セクションを確認
   - Before/Afterのコードを比較

3. **それでも納得できない場合**
   - プロジェクトチームに相談
   - 設計思想自体の見直しを提案

**重要**: 設計思想は絶対的なものではなく、プロジェクトの状況に応じて進化します。改善提案は歓迎されます。

---

## Q7: ArchitectureGuardianは複数の機能を同時にチェックできる？

**A**:

はい、可能です。ただし、1つずつチェックすることを推奨します。

**1つずつチェックする理由**:

- 違反レポートが明確になる
- 修正が容易になる
- 学習効果が高まる

**複数チェックの例**:

```text
@ArchitectureGuardian 「以下のファイルのアーキテクチャをチェックして」
- app/lib/auth/login.ts
- app/lib/dashboard/progressCalculator.ts
- app/routes/dashboard/index.tsx
```

---

## Q8: ArchitectureGuardianと直接対話して学習できる？

**A**:

はい。教育モードで設計思想を学ぶことができます。

**学習方法**:

1. **設計思想の背景を質問**
   - `@ArchitectureGuardian 「3大層アーキテクチャの目的は？」`

2. **具体例を要求**
   - `@ArchitectureGuardian 「lib層の良い例と悪い例を教えて」`

3. **参照ドキュメントを確認**
   - ArchitectureGuardianが案内する参照ドキュメントを読む

**推奨学習トピック**:

- 3大層アーキテクチャ
- Outside-In TDD
- Remixアーキテクチャ
- デザイントークンシステム

---

## Q9: ArchitectureGuardianの知識は更新される？

**A**:

はい。プロジェクトドキュメントが更新されると、ArchitectureGuardianの知識も自動的に更新されます。

**更新対象のドキュメント**:

- `docs/ARCHITECTURE_MANIFESTO2.md`（3大層アーキテクチャ）
- `scripts/generate/config.json`（テンプレート定義）
- `docs/design-token-specification.md`（デザイントークン）
- その他のプロジェクトドキュメント

**知識更新の仕組み**:

ArchitectureGuardianは実行時にプロジェクトドキュメントを参照するため、ドキュメントが更新されれば自動的に最新の知識が反映されます。

---

## Q10: ArchitectureGuardianのパフォーマンスは？

**A**:

ArchitectureGuardianは軽量な静的解析を行うため、パフォーマンスへの影響は最小限です。

**処理時間の目安**:

- 設計提案: 数秒〜十数秒
- 違反検出（単一ファイル）: 数秒
- 違反検出（複数ファイル）: 十数秒〜数十秒

**パフォーマンス向上のヒント**:

- 1つずつチェックする
- 具体的なファイルを指定する
- 必要な時のみ起動する（自動起動を活用）

---

## その他の質問

上記以外の質問がある場合は、以下の方法で確認してください：

1. **SKILL.mdを確認**: `.claude/skills/architecture-guardian/SKILL.md`
2. **参照ドキュメントを確認**: `docs/knowledge-base.md`
3. **具体的な質問**: `@ArchitectureGuardian 「〜について教えて」`
