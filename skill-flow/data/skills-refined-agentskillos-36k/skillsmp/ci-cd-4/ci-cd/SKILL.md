---
name: ci-cd
description: CI/CDパイプラインやGitHub Actionsを設定する際に使用。
---

# CI/CD

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] GitHub Actionsを設定する?
- [ ] CI/CDパイプラインを構築する?
- [ ] 自動テスト・デプロイを設定する?
- [ ] ブランチ保護ルールを設定する?

### 前提条件
- [ ] テストが正常に動作することを確認したか?
- [ ] ビルドコマンドを確認したか?
- [ ] デプロイ先の環境を把握しているか?
- [ ] 必要なシークレットを確認したか?

### 禁止事項の確認
- [ ] シークレットを直接ワークフローに書こうとしていないか?
- [ ] テストなしでデプロイしようとしていないか?
- [ ] `npm install`を使おうとしていないか?(`npm ci`を使う)
- [ ] mainブランチへの直接pushを許可しようとしていないか?

---

## トリガー

- GitHub Actions設定時
- CI/CDパイプライン構築時
- 自動テスト・デプロイ設定時
- ブランチ保護ルール設定時

---

## 🚨 鉄則

**自動化できるものは自動化。手動デプロイは事故の元。**

---

## GitHub Actions基本

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci          # ⚠️ installではなくci
      - run: npm run lint
      - run: npm run test
      - run: npm run build
```

---

## ⚠️ 必須ステップ

```yaml
# PRマージ前に必ず実行
- run: npm run lint      # 静的解析
- run: npm run typecheck # 型チェック
- run: npm run test      # テスト
- run: npm run build     # ビルド確認
```

---

## キャッシュ

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

---

## シークレット

```yaml
# 🚫 直接書かない
env:
  API_KEY: ${{ secrets.API_KEY }}
```

---

## ブランチ保護

```
⚠️ main ブランチ設定:
□ Require PR before merging
□ Require status checks to pass
□ Require up-to-date branches
```

---

## デプロイ

```yaml
deploy:
  needs: test  # テスト成功後のみ
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - run: echo "Deploy to production"
```

---

## 🚫 禁止事項まとめ

- シークレットを直接ワークフローに書く
- テストなしでデプロイ
- `npm install`の使用(`npm ci`を使う)
- mainブランチへの直接push許可
- **rootで作業する** (後述の権限問題を参照)

---

## ⚠️ Docker + 権限の落とし穴

### 問題: root成果物問題

Dockerコンテナ内で `sudo` や `root` で作成したファイルは **root所有** になる。
コンテナ外 (runner ユーザー) から操作すると権限エラーになる。

```yaml
# 🚫 NG: 権限エラーになる
- run: |
    docker run --rm -v $(pwd):/work myimage bash -c "
      sudo ./build.sh  # root で成果物を作成
    "
    cat build/output.txt  # ← Permission denied

# ✅ OK: sudo を使う or 権限を変更
- run: |
    docker run --rm -v $(pwd):/work myimage bash -c "
      sudo ./build.sh
      sudo chown -R $(id -u):$(id -g) /work/build  # 権限を戻す
    "
    cat build/output.txt  # OK
```

### チェックリスト

ワークフロー作成時に確認:

- [ ] Dockerコンテナ内で `sudo` や root 実行していないか?
- [ ] している場合、成果物の権限を戻しているか?
- [ ] コンテナ外で成果物を操作する箇所に `sudo` が必要か?

### 典型的なパターン

| 操作 | 権限問題 | 対策 |
|------|----------|------|
| `docker run ... sudo ./build.sh` | build/ が root 所有 | `chown` で戻す or 外で `sudo` |
| `tee file.txt` | 親ディレクトリが root 所有だと失敗 | `sudo tee` |
| `cp`, `mv`, `rm` | 対象が root 所有だと失敗 | `sudo` 付ける |

### ローカルでの事前確認

**root で作業しない** ルールを徹底すれば、ローカルで権限問題を早期発見できる:

```bash
# ローカルでテスト実行
docker run --rm -v $(pwd):/work myimage bash -c "./build.sh"
ls -la build/  # root所有になっていないか確認
```

---

## set -e 環境での安全なコマンド

`set -euo pipefail` が有効な場合、コマンド失敗でスクリプト全体が終了する。

```yaml
# 🚫 NG: grep がマッチしないと exit 1
- run: |
    set -euo pipefail
    grep "pattern" file.txt  # マッチしないとスクリプト終了

# ✅ OK: || true で失敗を許容
- run: |
    set -euo pipefail
    grep "pattern" file.txt || true  # マッチしなくても続行

# ✅ OK: if で分岐
- run: |
    set -euo pipefail
    if grep -q "pattern" file.txt; then
      echo "Found"
    fi
```

### 失敗を許容すべきコマンド

- `grep` (マッチなしで exit 1)
- `diff` (差分ありで exit 1)
- `rm -f` (ファイルなしで exit 1 になる場合)
- キャッシュ操作 (`cp ... || true`)
