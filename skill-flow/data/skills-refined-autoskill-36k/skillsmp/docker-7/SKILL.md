---
name: docker
description: Dockerfileやdocker-compose設定を作成する際に使用。
---

# Docker

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] Dockerfileを作成する?
- [ ] docker-composeを設定する?
- [ ] コンテナ化を検討する?
- [ ] マルチステージビルドを行う?

### 前提条件
- [ ] ベースイメージを選定したか?
- [ ] 必要なポートを把握しているか?
- [ ] 環境変数を整理したか?

### 禁止事項の確認
- [ ] latestタグを使おうとしていないか?
- [ ] rootユーザーで実行しようとしていないか?
- [ ] 機密情報をイメージに含めようとしていないか?
- [ ] 不要なファイルをコピーしようとしていないか?

---

## トリガー

- Dockerfile作成時
- docker-compose設定時
- コンテナ化検討時
- マルチステージビルド時

---

## 🚨 鉄則

**イメージは小さく、レイヤーは少なく、セキュリティを意識。**

---

## Dockerfile

```dockerfile
# ⚠️ 具体的なバージョンを指定
FROM node:20-alpine

WORKDIR /app

# 依存関係を先にコピー(キャッシュ効率化)
COPY package*.json ./
RUN npm ci --only=production

# アプリケーションコード
COPY . .

# 非rootユーザー
USER node

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

---

## マルチステージビルド

```dockerfile
# ビルドステージ
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN npm ci && npm run build

# 実行ステージ
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./
RUN npm ci --only=production
USER node
CMD ["node", "dist/index.js"]
```

---

## .dockerignore

```
node_modules
.git
.env
*.log
```

---

## 🚫 禁止事項まとめ

- latestタグの使用
- rootユーザーでの実行
- 機密情報のイメージ含有
- 不要ファイルのコピー
