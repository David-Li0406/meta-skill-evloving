---
name: structure-issue
description: Create clear GitHub issue from user prompt
---

Create clear GitHub issue from user prompt: $ARGUMENTS

## Process

1. Analyze prompt, determine type (bug/feature/enhancement)
2. Use AskUserQuestion for minimal required info
3. Create title format: `[Bug] ログイン時に無限ループが発生` or `[Feature] ダークモード対応`
4. Create body using templates below
5. Show to user for confirmation
6. Create with `gh issue create`

## Templates

- Bug: 概要, 再現手順, 期待される動作, 実際の動作, 環境情報
- Feature: 概要, 背景・目的, 期待される動作
- Enhancement: 概要, 現状の問題点, 期待される改善結果

## Follow-up

Show issue number/URL and suggest `/work-on-issue [number]`

Focus on problem definition only, not implementation details
