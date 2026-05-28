# Websocket Realtime - Validations

## WebSocket Without Reconnection

### **Id**
ws-no-reconnection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - new WebSocket\([^)]+\)(?![\s\S]{0,500}reconnect)
  - new WebSocket\([^)]+\)(?![\s\S]{0,500}onclose.*connect)
### **Message**
WebSocket created without reconnection logic. Connections will stay dead after drops.
### **Fix Action**
Implement exponential backoff reconnection in onclose handler
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## WebSocket Without Heartbeat

### **Id**
ws-no-heartbeat
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new WebSocket\([^)]+\)(?![\s\S]{0,500}ping|heartbeat)
  - WebSocket\.Server(?![\s\S]{0,500}ping)
### **Message**
WebSocket without heartbeat. Idle connections may be dropped by proxies.
### **Fix Action**
Add ping/pong every 30 seconds to keep connections alive
### **Applies To**
  - **/*.ts
  - **/*.js

## WebSocket Without Error Handler

### **Id**
ws-no-error-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new WebSocket\([^)]+\)(?![\s\S]{0,200}\.onerror)
  - WebSocket\([^)]+\);(?![\s\S]{0,200}onerror)
### **Message**
WebSocket without error handler. Errors will go unnoticed.
### **Fix Action**
Add onerror handler to log and handle connection errors
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## WebSocket Without Authentication

### **Id**
ws-no-auth
### **Severity**
error
### **Type**
regex
### **Pattern**
  - on\(['"]connection['"].*\)(?![\s\S]{0,300}auth|token|verify|jwt)
  - wss\.on\(['"]connection['"](?![\s\S]{0,300}authenticate)
### **Message**
WebSocket connection handler without authentication check.
### **Fix Action**
Verify auth token on connection before allowing messages
### **Applies To**
  - **/*.ts
  - **/*.js

## WebSocket Without Rate Limiting

### **Id**
ws-no-rate-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - on\(['"]message['"](?![\s\S]{0,300}rate|limit|throttle)
### **Message**
WebSocket message handler without rate limiting.
### **Fix Action**
Add per-connection rate limiting to prevent abuse
### **Applies To**
  - **/*.ts
  - **/*.js

## Unsafe JSON.parse in Message Handler

### **Id**
ws-unsafe-json-parse
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - on\(['"]message['"].*JSON\.parse(?![\s\S]{0,100}try|catch)
  - JSON\.parse\(.*\.data(?![\s\S]{0,50}catch)
### **Message**
JSON.parse without try-catch in message handler. Malformed messages will crash.
### **Fix Action**
Wrap JSON.parse in try-catch and send error to client
### **Applies To**
  - **/*.ts
  - **/*.js

## No Message Schema Validation

### **Id**
ws-no-message-validation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - JSON\.parse\([^)]+\)(?![\s\S]{0,200}schema|validate|safeParse|parse\()
### **Message**
Parsed message not validated against schema.
### **Fix Action**
Validate message structure with Zod or similar before processing
### **Applies To**
  - **/*.ts
  - **/*.js

## Event Listener Without Cleanup

### **Id**
ws-event-listener-leak
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - addEventListener(?![\s\S]{0,500}removeEventListener)
  - \.on\(['"]\w+['"](?![\s\S]{0,500}\.off\(|\.removeListener)
### **Message**
Event listener added without corresponding removal. May cause memory leak.
### **Fix Action**
Remove listeners in cleanup/disconnect handler
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Interval Without Cleanup

### **Id**
ws-interval-not-cleared
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setInterval\([^)]+\)(?![\s\S]{0,300}clearInterval)
### **Message**
setInterval without clearInterval. Will cause memory leak on disconnect.
### **Fix Action**
Store interval ID and clear it in onclose/cleanup
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Send Without Buffer Check

### **Id**
ws-no-buffer-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.send\([^)]+\)(?![\s\S]{0,200}bufferedAmount)
### **Message**
WebSocket send without checking buffer. May cause backpressure issues.
### **Fix Action**
Check ws.bufferedAmount before sending high-frequency messages
### **Applies To**
  - **/*.ts
  - **/*.js

## Broadcasting to All Connections

### **Id**
ws-broadcast-all
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.clients\.forEach\([^)]*send
  - connections\.forEach\([^)]*send
### **Message**
Broadcasting to all connections. Consider using rooms/channels for efficiency.
### **Fix Action**
Implement room-based broadcasting to reduce unnecessary messages
### **Applies To**
  - **/*.ts
  - **/*.js

## Send Without Ready State Check

### **Id**
ws-send-without-ready-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.send\([^)]+\)(?![\s\S]{0,100}readyState|OPEN)
### **Message**
WebSocket send without checking readyState. Will throw if not open.
### **Fix Action**
Check ws.readyState === WebSocket.OPEN before sending
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Close Without Status Code

### **Id**
ws-close-code-missing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.close\(\)(?!\d)
### **Message**
WebSocket closed without status code. Consider providing meaningful close code.
### **Fix Action**
Use appropriate close code: ws.close(1000, 'Normal closure')
### **Applies To**
  - **/*.ts
  - **/*.js

## Fixed Reconnection Delay

### **Id**
ws-constant-reconnect-delay
### **Severity**
info
### **Type**
regex
### **Pattern**
  - setTimeout.*connect.*\d{4}\)
  - reconnect.*setTimeout.*1000
### **Message**
Fixed reconnection delay may cause thundering herd on server restart.
### **Fix Action**
Use exponential backoff with jitter for reconnection
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Unlimited Reconnection Attempts

### **Id**
ws-no-max-reconnect
### **Severity**
info
### **Type**
regex
### **Pattern**
  - reconnect(?![\s\S]{0,200}max|limit|attempts)
### **Message**
Reconnection without max attempts. Client may retry forever.
### **Fix Action**
Limit reconnection attempts and show user error after max
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Socket.IO Without Disconnect Handler

### **Id**
socketio-no-disconnect-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - io\.on\(['"]connection['"](?![\s\S]{0,500}disconnect)
### **Message**
Socket.IO connection without disconnect handler.
### **Fix Action**
Add socket.on('disconnect') to clean up resources
### **Applies To**
  - **/*.ts
  - **/*.js

## Socket.IO Emit Without Acknowledgment

### **Id**
socketio-emit-without-ack
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.emit\(['"][^'"]+['"],\s*[^,)]+\)(?!.*=>)
### **Message**
Socket.IO emit without callback. Consider using ack for important messages.
### **Fix Action**
Add callback for delivery confirmation: emit('event', data, (ack) => {})
### **Applies To**
  - **/*.ts
  - **/*.js

## SSE Without Retry Header

### **Id**
sse-no-retry
### **Severity**
info
### **Type**
regex
### **Pattern**
  - text/event-stream(?![\s\S]{0,200}retry:)
### **Message**
SSE without retry directive. Client will use default reconnection timing.
### **Fix Action**
Set retry interval: res.write('retry: 3000\n')
### **Applies To**
  - **/*.ts
  - **/*.js

## SSE Without Keepalive

### **Id**
sse-no-heartbeat
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - text/event-stream(?![\s\S]{0,500}heartbeat|interval|setInterval)
### **Message**
SSE without heartbeat. Connection may be dropped by proxies.
### **Fix Action**
Send heartbeat comment every 30s: res.write(': heartbeat\n\n')
### **Applies To**
  - **/*.ts
  - **/*.js