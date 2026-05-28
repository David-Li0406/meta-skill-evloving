---
name: improve-command
description: Analyze skill usage and create improvement proposal issue
disable-model-invocation: true
---

Analyze skill usage and create improvement proposal issue

## Prerequisites
- Must be executed in same conversation session after using target skill
- Working repository: Can be any repository where the skill was used
- Issue target repository: https://github.com/toumakido/my-claude (determined dynamically or confirmed with user)

## Parameters

- `$ARGUMENTS`: Target skill name to improve (e.g., `migrate-aws-sdk`, `review-pr`, `improve-command`)
  - Must correspond to a file in `skills/` directory (without `/SKILL.md` path)
  - Can be used recursively to improve improve-command itself

## Usage

```
/improve-command migrate-aws-sdk
/improve-command improve-command  # Recursive usage
```

## Process

1. Validate target skill:
   - Check if `skills/<skill-name>/SKILL.md` exists using Read tool
   - If not found: Display error and list available skills (see Error Handling)
2. Analyze conversation history:
   - Identify when target skill was executed (search for `/skill-name` in conversation)
   - Extract problems encountered during/after execution
   - Identify missing patterns or guidance
   - Note additional steps required beyond skill specification
   - Find workarounds or fixes applied
3. Analyze improvement opportunities from conversation history:
   - User corrections or指摘 (e.g., "周りのフォーマットに合わせて") - indicates missing style guidelines
   - Multiple Edit rejections indicating unclear requirements - count rejections with same file
   - Workarounds or manual interventions required - user ran commands directly
   - Additional questions needed during execution - count AskUserQuestion tool calls during skill execution
   - Post-skill fixes by user - commits/edits after skill completion

   **Check repository type** (for reference links and generalization in later steps):
   - Run: `gh repo view --json isPrivate -q .isPrivate`
   - Store result as `IS_PRIVATE` for use in Steps 5.6 and 5.7
   - If repository is public: Collect PR/commit references for issue body using `gh pr list --limit 5`
   - If repository is private: Skip reference collection (will apply generalization in Step 5.6)
4. Extract improvement opportunities:
   - Missing patterns or examples
   - Insufficient guidance or documentation
   - Additional checks needed
   - Service/library-specific knowledge gaps
   - More efficient approaches
4.5. Categorize issues by improvement scope:

   **Purpose**: Distinguish between skill specification issues and implementation-phase issues

   **Categories**:

   1. **Skill specification issues** (Should be included in improvement proposal):
      - Missing or unclear steps in skill process
      - Insufficient guidance or examples in skill documentation
      - Lack of error handling patterns in skill specification
      - Missing validation steps
      - Unclear decision criteria (e.g., when to apply certain patterns)

      Examples:
      - "Skill doesn't specify how to handle duplicate test data"
      - "No guidance on determining test data distribution strategy"
      - "Missing step for validating type information"

   2. **Implementation-phase issues** (Should be excluded from skill specification):
      - Technology-specific breaking changes (e.g., SDK version differences)
      - Library-specific behavior patterns
      - Domain-specific business logic
      - Project-specific code patterns

      Examples:
      - "SDK version X handles empty strings differently than version Y"
      - "This API requires specific authentication headers"
      - "Business rule X requires validation Y"

   **Action**:
   - Review all identified issues and categorize them
   - Only include skill specification issues in improvement proposal
   - Document excluded implementation-phase issues separately (if requested by user)

4.6. Evaluate severity and confirm with user:
   - Severity levels:
     - Critical/Important: スキル仕様の明確な不足、複数回の指摘 → Proceed to step 5
     - Nice-to-have/None: 軽微な改善、1回のみの指摘、改善点なし → Use AskUserQuestion to confirm before proceeding to step 5
5. Generate structured issue content (if confirmed):
   - Title: `<skill-name>.md の改善提案: [主要な改善点の要約]`
   - Body sections:
     - 概要: Brief summary of improvements
     - 実際に発生した問題: Concrete problems encountered
     - 改善提案: Specific proposals with code samples
     - 期待される効果: Expected benefits
     - 参考: Links to relevant PRs/commits (only if repository is public)
5.5. Present improvement proposal summary to user for confirmation:

   **Purpose**: Ensure proposal aligns with user's intent before creating issue

   **Actions**:
   1. Generate concise summary of improvement proposals (3-5 bullet points)
   2. Present to user using text output (NOT AskUserQuestion, NOT issue creation yet)
   3. Format:
      ```
      ## 改善提案サマリー

      以下の改善をissueとして提案します：

      1. [改善項目1]: [1行の説明]
      2. [改善項目2]: [1行の説明]
      3. [改善項目3]: [1行の説明]

      この内容でissueを作成してよろしいですか？
      追加・削除・修正したい項目があれば教えてください。
      ```
   4. Wait for user confirmation or feedback
   5. Adjust proposal based on feedback
   6. Proceed to Step 6 only after user approval

   **Example**:
   ```
   ## 改善提案サマリー

   以下の改善をissueとして提案します：

   1. テストデータ設計方針の明記: 重複を避ける戦略を追加
   2. フィルター検証用データ生成の必須化: match/non-matchの両方を生成
   3. 型情報検証ステップの追加: 事前検証でコンパイルエラー防止

   この内容でissueを作成してよろしいですか？
   追加・削除・修正したい項目があれば教えてください。
   ```

5.6. Apply generalization for private repositories:

   **Condition**: Only if `IS_PRIVATE` is true

   **Generalization rules**:
   - MUST generalize: Function/variable/type names, table names, business terms
   - KEEP specific: AWS service names (DynamoDB, S3), standard methods (GetItem, Query), language keywords, error patterns (ctx, err)
   - Maintain consistency: same original term → same generic name throughout

   **Actions**:
   1. Identify domain-specific identifiers in issue body (function names ending in Repository/Service/Handler/Manager, business verbs like Register*/Process*/Calculate*)
   2. Replace with generic equivalents (EntityRepository, ProcessRecord, calculateValue)
   3. Track generalization count (functions, repositories, domain terms)

5.7. Confirm generalized content:

   **Condition**: Only if Step 5.6 executed

   **Actions**:
   1. Display summary:
      ```
      privateリポジトリのため一般化しました: 関数名N箇所, Repository名M箇所, ドメイン用語K箇所
      ```
   2. AskUserQuestion with options: "確認する" (show full body) / "このまま作成" (proceed) / "キャンセル" (exit)
   3. If "確認する": Display body, wait for approval before Step 6

6. Create GitHub issue:

   **Flow**:
   - If `IS_PRIVATE` is false (public repository):
     - Proceed directly to issue creation
   - If `IS_PRIVATE` is true (private repository):
     - Steps 5.6 and 5.7 have been executed
     - Use generalized issue body from Step 5.6
     - User has approved content in Step 5.7

   **Actions**:
   - Determine target repository:
     - Check current repository: `gh repo view --json nameWithOwner -q .nameWithOwner`
     - If current repository is toumakido/my-claude: Create issue here
     - Otherwise: Confirm with user or default to https://github.com/toumakido/my-claude
   - Use `gh issue create --repo toumakido/my-claude` with generated content

7. Display created issue URL

## Issue Template Format

```markdown
## 概要

`skills/<skill-name>/SKILL.md` スキルを実際のプロジェクトで使用した結果、いくつかの重要な改善点が判明しました。

## 実際に発生した問題

### 1. [問題カテゴリ]
[具体的な問題の説明]

### 2. [問題カテゴリ]
[具体的な問題の説明]

## 改善提案

### 1. [改善項目]
[具体的な改善内容とコードサンプル]

```markdown
[追加すべきセクションやコード例]
```

### 2. [改善項目]
[具体的な改善内容とコードサンプル]

## 期待される効果

- [効果1]
- [効果2]
- [効果3]

## 参考

(このセクションは作業対象リポジトリがpublicの場合のみ含める)

- PR: [PR URL]
- Commit: [commit hash/URL]
```

## Analysis Guidelines

### Identifying Problems
- Look for multiple commits on same topic (indicates iterative fixes)
- Check PR review comments for gaps in initial implementation
- Identify patterns where manual intervention was required
- Note deviations from skill specification

### Extracting Improvements
- Compare skill specification with actual implementation steps
- Identify missing error handling patterns
- Note service-specific details not covered
- Identify validation steps that would prevent similar issues (e.g., type checks before operations, input validation)

### Prioritizing Suggestions
- Critical: Issues that cause incorrect implementation
- Important: Missing patterns that require manual fixes
- Nice-to-have: Efficiency improvements or better documentation

## Error Handling

- Skill file not found: Display error and list available skills
- No recent usage found: Ask user to confirm skill was used in current session
- No git history: Warn user but continue with conversation analysis only
- gh CLI error: Display error and ask user to check authentication

## Notes

- This skill works best when executed immediately after target skill usage
- Longer conversation history provides more context for analysis
- Include specific code examples in proposals for clarity
- For public repositories: Include PR/commit links as evidence
- For private repositories:
  - Omit PR/commit links from issue (not accessible to public)
  - Generalize code examples to remove confidential information
- Address both technical gaps (missing steps, error handling) and documentation improvements (unclear guidance, missing examples)
