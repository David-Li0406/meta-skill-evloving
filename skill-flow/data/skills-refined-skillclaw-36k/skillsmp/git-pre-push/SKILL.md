---
name: git-pre-push
description: ユーザーが「プッシュして」「公開して」「push したい」と言ったときに使う。プッシュ前にブランチと未プッシュコミットを確認するスキル。
---

# Git Pre Push

## 概要

プッシュ前にブランチと未プッシュコミットを確認し、main への push は必ず確認を取る。

## 手順

1. 現在のブランチを確認する。main の場合は push して良いかユーザーに確認する。

```sh
git --no-pager branch
```

2. 作業ツリーの変更有無を確認する。

```sh
git --no-pager status --short
```

3. 上流との差分コミットを確認する。

```sh
git --no-pager log --oneline --decorate --reverse @{u}..HEAD
```

4. 上流がない場合は直近コミットを確認する。

```sh
git --no-pager log --oneline --decorate -n 10
```

5. ユーザーが OK なら push する。

```sh
git push
```
