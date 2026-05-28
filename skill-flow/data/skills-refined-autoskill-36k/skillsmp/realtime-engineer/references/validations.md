# Realtime Engineer - Validations

## WebSocket Without Reconnection

### **Id**
missing-reconnection-logic
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new WebSocket\([^)]+\)(?!.*reconnect|Reconnect)
  - WebSocket\([^)]+\)(?!.*onclose.*reconnect)
### **Message**
WebSocket created without reconnection handling. Connections WILL drop.
### **Fix Action**
Implement reconnection with exponential backoff and jitter
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## WebSocket Without Heartbeat

### **Id**
missing-heartbeat
### **Severity**
error
### **Type**
regex
### **Pattern**
  - WebSocket(?!.*ping|heartbeat|keepalive)
### **Message**
WebSocket without heartbeat. Half-open connections will go undetected.
### **Fix Action**
Add ping/pong heartbeat every 25-30 seconds
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Reconnection Without Jitter

### **Id**
reconnect-without-jitter
### **Severity**
error
### **Type**
regex
### **Pattern**
  - reconnect.*setTimeout\(.*\d{4}\)(?!.*random|jitter|Math\.random)
  - backoff(?!.*jitter|random)
### **Message**
Reconnection without jitter causes thundering herd on server restart.
### **Fix Action**
Add 0-30% random jitter to reconnection delay
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Presence Without Grace Period

### **Id**
presence-immediate-removal
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - disconnect.*delete.*user(?!.*timeout|setTimeout|grace)
  - disconnect.*emit.*leave(?!.*delay|timeout)
### **Message**
User removed immediately on disconnect. Causes flickering during network blips.
### **Fix Action**
Add 5-10 second grace period before removing user from presence
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Message Queue Without Size Limit

### **Id**
unbounded-message-queue
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - queue\.push\((?!.*length|size|max|limit)
  - messages\.push\((?!.*limit|max)
### **Message**
Unbounded message queue. Slow clients will cause memory exhaustion.
### **Fix Action**
Implement queue size limit with drop strategy (oldest or newest)
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Database Query Inside Broadcast Loop

### **Id**
broadcast-n-queries
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*members.*await.*db\.
  - forEach.*user.*await.*query
  - map.*member.*await.*fetch
### **Message**
O(n) database queries in broadcast loop. Will not scale.
### **Fix Action**
Cache user data, batch queries, or precompute permissions
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## SSE Without Retry Header

### **Id**
sse-missing-retry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - text/event-stream(?!.*retry:)
  - Content-Type.*event-stream(?!.*retry)
### **Message**
SSE stream without retry header. Browser may flood server on error.
### **Fix Action**
Send 'retry: 10000' header to control reconnection interval
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## SSE Without Event IDs

### **Id**
sse-missing-event-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - res\.write\(['"]data:(?!.*id:)
  - event-stream(?!.*lastEventId|Last-Event-ID)
### **Message**
SSE without event IDs. Clients cannot resume after reconnection.
### **Fix Action**
Include 'id:' field with each event for resumable streams
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Multi-client Without Message Ordering

### **Id**
missing-message-ordering
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - broadcast(?!.*seq|order|clock|timestamp)
  - emit\(['"]message(?!.*order)
### **Message**
No message ordering. Concurrent edits may arrive out of order.
### **Fix Action**
Add sequence numbers or vector clocks for causal ordering
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Room Join Without Message Backfill

### **Id**
join-without-backfill
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - join.*room.*subscribe(?!.*history|recent|backfill)
  - addMember(?!.*getMessages|loadHistory)
### **Message**
Room join without backfill. Messages during join window will be lost.
### **Fix Action**
Subscribe first, then backfill recent messages with deduplication
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Sending Large Binary as JSON

### **Id**
websocket-binary-json
### **Severity**
info
### **Type**
regex
### **Pattern**
  - JSON\.stringify.*buffer|binary|image
  - send\(JSON.*base64
### **Message**
Sending binary data as JSON wastes bandwidth (33% overhead from base64).
### **Fix Action**
Use WebSocket binary frames for images, files, or audio
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Socket.IO Without Redis Adapter

### **Id**
socket-io-no-adapter
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new Server\((?!.*adapter|redis)
  - io\((?!.*adapter)
### **Message**
Socket.IO without Redis adapter. Will not scale horizontally.
### **Fix Action**
Use @socket.io/redis-adapter for multi-server deployment
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Polling Instead of Push

### **Id**
polling-as-realtime
### **Severity**
info
### **Type**
regex
### **Pattern**
  - setInterval.*fetch\(|axios\.
  - poll.*setInterval
### **Message**
Polling API every N seconds is not real-time. Consider SSE or WebSocket.
### **Fix Action**
Use SSE for server push, WebSocket only if bidirectional needed
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Cursor Updates Too Frequent

### **Id**
cursor-high-frequency
### **Severity**
info
### **Type**
regex
### **Pattern**
  - mousemove.*send\(|emit\(
  - on.*move.*broadcast
### **Message**
Sending cursor on every mousemove will flood the server.
### **Fix Action**
Throttle cursor updates to 10-20ms using requestAnimationFrame
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx