---
name: docker-troubleshoot
description: Dockerトラブルシュート - lima/Docker Desktop接続エラー、コンテナ起動失敗の診断・解決
---

## 診断フロー

```
1. Docker daemon確認
   docker version → 接続エラー?
   ↓
2. 環境特定
   - lima → limactl status
   - Docker Desktop → アプリ起動確認
   - Rancher Desktop → .rd/docker.sock
   ↓
3. 問題別対処
```

## よくあるエラーと解決策

### 1. Cannot connect to Docker daemon

```bash
# lima使用時
limactl start default
export DOCKER_HOST="unix://$HOME/.lima/default/sock/docker.sock"

# Rancher Desktop使用時
export DOCKER_HOST="unix://$HOME/.rd/docker.sock"

# Docker Desktop使用時
# → アプリを起動
```

### 2. Address already in use

```bash
# ポート使用プロセス特定
lsof -i :3306 | grep LISTEN
# プロセス終了
kill -9 {PID}
```

### 3. lima VM問題

```bash
# VM再起動
limactl stop default && limactl start default

# VM削除・再作成（最終手段）
limactl delete default
limactl start --name=default template://docker
```

### 4. docker compose起動失敗

```bash
# 全コンテナ停止・削除
docker compose down --remove-orphans
docker system prune -f

# 再起動
docker compose up -d
```

## 確認コマンド

| 確認項目 | コマンド |
|---------|---------|
| daemon接続 | `docker version` |
| lima状態 | `limactl list` |
| 起動中コンテナ | `docker ps` |
| ポート確認 | `docker port {container}` |
| ログ確認 | `docker logs {container}` |
