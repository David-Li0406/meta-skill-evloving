---
name: websocket-realtime
description: WebSocket、SSE、リアルタイム機能を実装する際に使用。
---

# WebSocket & Real-time

## 📋 実行前チェック(必須)

### このスキルを使うべきか?
- [ ] WebSocketを実装する?
- [ ] SSE(Server-Sent Events)を実装する?
- [ ] リアルタイム通信機能を実装する?
- [ ] 再接続ロジックを設計する?

### 前提条件
- [ ] プロトコル(WebSocket/SSE)を選定したか?
- [ ] 認証方式を決定したか?
- [ ] 再接続戦略を検討したか?

### 禁止事項の確認
- [ ] 再接続ロジックなしで実装しようとしていないか?
- [ ] 認証なしで接続を許可しようとしていないか?
- [ ] メッセージのバリデーションを省略しようとしていないか?

---

## トリガー

- WebSocket実装時
- SSE(Server-Sent Events)実装時
- リアルタイム通信機能時
- 再接続ロジック設計時

---

## 🚨 鉄則

**接続は切れる前提で設計。再接続ロジック必須。**

---

## WebSocket (Socket.io)

```typescript
// サーバー
import { Server } from 'socket.io';

const io = new Server(server, {
  cors: { origin: process.env.CLIENT_URL }
});

io.on('connection', (socket) => {
  // ⚠️ 認証確認
  if (!socket.handshake.auth.token) {
    socket.disconnect();
    return;
  }
  
  socket.on('message', (data) => {
    // ⚠️ バリデーション
    if (!isValidMessage(data)) return;
    
    io.emit('message', data);
  });
});
```

---

## 再接続ロジック

```typescript
// クライアント
const socket = io({
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000
});

socket.on('disconnect', () => {
  console.log('Disconnected, attempting reconnect...');
});

socket.on('reconnect', (attemptNumber) => {
  console.log(`Reconnected after ${attemptNumber} attempts`);
});
```

---

## SSE (Server-Sent Events)

```typescript
// サーバー
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  
  const sendEvent = (data) => {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };
  
  // クリーンアップ
  req.on('close', () => {
    // リソース解放
  });
});
```

---

## 🚫 禁止事項まとめ

- 再接続ロジックなし
- 認証なしの接続許可
- メッセージバリデーション省略
- クリーンアップ処理忘れ
