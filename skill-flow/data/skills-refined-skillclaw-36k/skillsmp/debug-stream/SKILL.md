---
name: debug_stream
description: Guide for debugging stream distribution and client connection issues
---

# Analyze Stream & Clients

This skill helps you debug issues in `src/client_manager.rs` and `src/main.rs`, specifically regarding multiple clients, network drops, or chunk distribution.

## 🧠 Context
The streaming architecture is a Pub/Sub model:
1.  **Publisher**: The Encoder loop sends H.264 NAL units (chunks) to a `tokio::sync::broadcast` channel.
2.  **Subscriber**: Each HTTP request to `/ws` (or root) spawns a subscriber that listens to this channel and yields bytes to the TCP socket.

## 🛠️ Common Issues

### 1. Clients Disconnecting Immediately
**Symptom**: Browser opens, then closes connection or shows error.
**Cause**:
-   **Lagging Receiver**: `tokio::sync::broadcast` returns `RecvError::Lagged` if the client reads too slowly and the buffer fills up.
-   **Header Mismatch**: Client expects `Content-Type: video/h264` or specific CORS headers.

**Fix**:
-   Increase channel capacity in `main.rs` (default might be 16 or 32).
-   Handle `Lagged` error gracefully (currently it might drop the stream).

### 2. Stream Stuttering
**Cause**: Network jitter or TCP Head-of-Line blocking.
**Analysis**:
-   Check `client_manager.rs` dispatch loop.
-   Ensure we are sending "small enough" chunks, or `Chunked` transfer encoding is working correctly.

### 3. No Stats Update
**Symptom**: `/stats` returns 0 active clients despite opened tabs.
**Cause**: The `ClientManager` reference counting might be broken or the drop guard is not firing.
**Check**: Look for `Arc<AtomicUsize>` usage for connected client count.

## 🚀 Key Code Paths

### `src/client_manager.rs`

-   **`ClientManager` struct**: Holds the broadcast sender.
-   **`subscribe()`**: Returns a `Receiver` for a new client.

### `src/main.rs` (Handler)

-   **`stream_handler`**:
    -   Calls `client_manager.subscribe()`.
    -   Loops over `rx.recv()`.
    -   Yields `Bytes` to the Axum body body stream.

## 🧪 Verification
Use `curl` to consume the stream without a browser:
```bash
curl -v http://localhost:8080 > /dev/null
```
Watch the server logs for "New client connected" / "Client disconnected".
