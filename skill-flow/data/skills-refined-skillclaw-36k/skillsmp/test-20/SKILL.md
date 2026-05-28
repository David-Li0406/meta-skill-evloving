---
name: test
description: test skill
disable-model-invocation: true
user-invocable: true
context: fork
agent: test
allowed-tools: Read, Grep
hooks: test
---

this is test skill

- disable-model-invocation: Claude Codeからの呼び出しを不可にする
- user-invocable: ユーザからの呼び出しを許可する
- context: forkに設定するとフォークされたサブエージェントのコンテキストで動作する（過去の会話履歴を引き継がない）
- agent: contextがforkの時にどのサブエージェントを利用するか
- hooks: フック
https://code.claude.com/docs/en/skills