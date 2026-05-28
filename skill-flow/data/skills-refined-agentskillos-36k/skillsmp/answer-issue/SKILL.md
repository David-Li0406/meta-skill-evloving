---
name: answer-issue
description: Efficiently answer question about GitHub issue
---

Efficiently answer question about GitHub issue $ARGUMENTS

## Prerequisites
- $ARGUMENTS format: `<issue_number> <user_prompt>`
  - Example: `123 この問題の原因を調査して`
  - Example: `456 どのファイルが関連しているか教えて`

## Purpose

Efficiently investigate and answer questions about structured GitHub issues without necessarily implementing fixes. Optimized for issues created by `/structure-issue` or `/restructure-issue`.

## Process

1. Parse arguments: extract issue number and user prompt
   - Split `$ARGUMENTS` by first space: `issue_number = first_token`, `user_prompt = remaining_text`
   - Example: `"123 この問題の原因を調査して"` → issue_number=`"123"`, user_prompt=`"この問題の原因を調査して"`
   - If no space found: treat entire `$ARGUMENTS` as issue_number, prompt user for question
2. Fetch issue: `gh issue view <issue_number> --json title,body,labels,comments`
3. Parse structured issue content:
   - Bug: 概要、再現手順、期待される動作、実際の動作、エラーメッセージ、環境情報
   - Feature: 概要、背景・目的、期待される動作
   - Enhancement: 概要、現状の問題点、期待される改善結果
4. Based on user prompt, determine investigation type:
   - Root cause analysis: "原因を調査"
   - Related files search: "関連ファイル", "どこを修正"
   - Implementation approach: "実装方法", "どうやって直す"
   - Impact assessment: "影響範囲", "副作用"
   - General questions: その他の質問
5. Use appropriate tools efficiently:
   - For codebase exploration (finding files by concept/feature): Use Task tool with subagent_type=Explore
   - For specific file/function search (known name): Use Grep/Glob directly
   - For reading file contents: Use Read tool
   - For log pattern analysis: Use Grep tool with specific patterns
6. Provide structured answer:
   ```
   ## 調査結果

   [direct answer to user prompt]

   ## 関連情報

   [supporting details, file locations with line numbers, code snippets]

   ## 推奨される次のステップ

   [actionable recommendations]
   ```
7. If fix is needed, suggest: `/work-on-issue <issue_number>`

## Notes

- Optimize for speed (do not over-investigate)
- Provide actionable answers with file:line references
- Stay focused on user's prompt (do not implement unless asked)
