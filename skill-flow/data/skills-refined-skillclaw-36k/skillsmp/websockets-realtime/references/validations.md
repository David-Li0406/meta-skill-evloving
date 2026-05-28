# Websockets Realtime - Validations

## WebSocket without error handler

### **Id**
no-error-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new WebSocket\([^)]+\)(?![\s\S]*\.onerror)
  - WebSocketServer\([^)]*\)(?![\s\S]*\.on\(["']error)
### **Message**
WebSocket should have error handler
### **Fix Action**
Add ws.onerror or ws.on('error') handler
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## WebSocket without close handler

### **Id**
no-close-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new WebSocket\\([^)]+\\)(?![\\s\\S]*\\.onclose)
### **Message**
WebSocket should handle close events
### **Fix Action**
Add ws.onclose handler with reconnection logic
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Hardcoded WebSocket URL

### **Id**
hardcoded-ws-url
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new WebSocket\(["']ws://localhost
  - new WebSocket\(["']wss://[a-z]+\.
### **Message**
Consider using environment variable for WebSocket URL
### **Fix Action**
Use process.env.NEXT_PUBLIC_WS_URL or similar
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Insecure WebSocket (ws://)

### **Id**
ws-without-wss
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new WebSocket\(['"]ws://
  - WebSocket\([^)]*['"]ws://
### **Message**
Use wss:// for secure WebSocket connections
### **Fix Action**
Change ws:// to wss:// in production
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Sending auth token in message

### **Id**
auth-in-message
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ws\\.send.*token
  - ws\\.send.*auth
  - socket\\.emit.*token
### **Message**
Consider authenticating before connection instead of after
### **Fix Action**
Pass token in URL or use ticket system
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## EventSource/WebSocket without cleanup

### **Id**
event-listener-leak
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useEffect\\([^]*new EventSource[^]*(?!return.*close)
  - useEffect\\([^]*new WebSocket[^]*(?!return.*close)
### **Message**
Close connection in useEffect cleanup
### **Fix Action**
Return cleanup function that calls close()
### **Applies To**
  - *.jsx
  - *.tsx

## setInterval without cleanup in WebSocket handler

### **Id**
missing-interval-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setInterval\\([^)]+\\)(?![\\s\\S]*clearInterval)
### **Message**
Interval may not be cleaned up
### **Fix Action**
Store interval ID and clear on disconnect
### **Applies To**
  - *.js
  - *.ts

## Synchronous broadcast to many clients

### **Id**
sync-broadcast
### **Severity**
info
### **Type**
regex
### **Pattern**
  - forEach.*\\.send\\(
  - for.*of.*\\.send\\(
### **Message**
Consider chunking broadcasts for many clients
### **Fix Action**
Use setImmediate between chunks to yield event loop
### **Applies To**
  - *.js
  - *.ts

## Sending large JSON without consideration

### **Id**
large-json-send
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \\.send\\(JSON\\.stringify\\([^)]{50,}
### **Message**
Large payloads may cause performance issues
### **Fix Action**
Consider pagination, compression, or sending references
### **Applies To**
  - *.js
  - *.ts