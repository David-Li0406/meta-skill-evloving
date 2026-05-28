# WebSocket Communication

Complete guide to real-time bidirectional communication in Flutter using WebSockets.

## Overview

WebSockets provide full-duplex communication channels over a single TCP connection, enabling real-time data exchange between client and server. Unlike HTTP's request-response model, WebSockets maintain a persistent connection allowing either party to send messages at any time.

The `web_socket_channel` package provides Flutter's standard WebSocket implementation with a Stream-based API that integrates naturally with Flutter's reactive architecture.

## When to Use WebSockets

Use WebSockets for:
- **Chat Applications**: Real-time messaging
- **Live Notifications**: Push updates to users
- **Collaborative Editing**: Multiple users editing simultaneously
- **Live Dashboards**: Real-time metrics and analytics
- **Gaming**: Multiplayer game state synchronization
- **Stock Tickers**: Live price updates
- **Location Tracking**: Real-time position updates

Don't use WebSockets for:
- **One-off Requests**: Use HTTP for simple request/response
- **Large File Transfers**: HTTP is more efficient
- **SEO Content**: Search engines can't crawl WebSocket data
- **Cacheable Data**: HTTP caching is more mature

## Installation

Add web_socket_channel to your `pubspec.yaml`:

```yaml
dependencies:
  web_socket_channel: ^2.4.0
```

This package works across all Flutter platforms: mobile, web, and desktop.

## Basic Usage

### Establishing Connection

Connect to a WebSocket server:

```dart
import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  late WebSocketChannel _channel;

  void connect(String url) {
    _channel = WebSocketChannel.connect(
      Uri.parse(url),
    );

    print('WebSocket connected');
  }

  void dispose() {
    _channel.sink.close();
  }
}

// Usage
final service = WebSocketService();
service.connect('wss://echo.websocket.org');
```

### Sending Messages

Send data through the sink:

```dart
class WebSocketService {
  late WebSocketChannel _channel;

  void sendMessage(String message) {
    _channel.sink.add(message);
  }

  void sendJson(Map<String, dynamic> data) {
    _channel.sink.add(jsonEncode(data));
  }

  void sendBinary(List<int> data) {
    _channel.sink.add(data);
  }
}

// Usage
service.sendMessage('Hello, server!');
service.sendJson({
  'type': 'chat',
  'message': 'Hello',
  'userId': '123',
});
```

### Receiving Messages

Listen to the stream for incoming messages:

```dart
class WebSocketService {
  late WebSocketChannel _channel;

  Stream<dynamic> get messages => _channel.stream;

  Stream<String> get stringMessages =>
      _channel.stream.cast<String>();

  Stream<Map<String, dynamic>> get jsonMessages =>
      _channel.stream
          .cast<String>()
          .map((str) => jsonDecode(str) as Map<String, dynamic>);
}

// Usage
service.stringMessages.listen(
  (message) {
    print('Received: $message');
  },
  onError: (error) {
    print('Error: $error');
  },
  onDone: () {
    print('Connection closed');
  },
);
```

## UI Integration

### StreamBuilder

Display WebSocket data with StreamBuilder:

```dart
class ChatWidget extends StatefulWidget {
  final String chatUrl;

  const ChatWidget({required this.chatUrl});

  @override
  _ChatWidgetState createState() => _ChatWidgetState();
}

class _ChatWidgetState extends State<ChatWidget> {
  late WebSocketChannel _channel;
  final List<String> _messages = [];

  @override
  void initState() {
    super.initState();
    _channel = WebSocketChannel.connect(
      Uri.parse(widget.chatUrl),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: StreamBuilder(
            stream: _channel.stream,
            builder: (context, snapshot) {
              if (snapshot.hasError) {
                return Center(
                  child: Text('Error: ${snapshot.error}'),
                );
              }

              if (snapshot.hasData) {
                _messages.add(snapshot.data.toString());
              }

              return ListView.builder(
                itemCount: _messages.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(_messages[index]),
                  );
                },
              );
            },
          ),
        ),
        _buildMessageInput(),
      ],
    );
  }

  Widget _buildMessageInput() {
    final controller = TextEditingController();

    return Padding(
      padding: EdgeInsets.all(8.0),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: controller,
              decoration: InputDecoration(
                hintText: 'Type a message...',
              ),
            ),
          ),
          IconButton(
            icon: Icon(Icons.send),
            onPressed: () {
              if (controller.text.isNotEmpty) {
                _channel.sink.add(controller.text);
                controller.clear();
              }
            },
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _channel.sink.close();
    super.dispose();
  }
}
```

## Production-Ready WebSocket Manager

### Robust Implementation

Build a production-ready WebSocket manager with reconnection, heartbeat, and error handling:

```dart
import 'dart:async';
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';

enum WebSocketStatus {
  connecting,
  connected,
  disconnected,
  reconnecting,
}

class WebSocketManager {
  final String url;
  final Duration reconnectDelay;
  final Duration heartbeatInterval;
  final int maxReconnectAttempts;

  WebSocketChannel? _channel;
  StreamSubscription? _subscription;
  Timer? _heartbeatTimer;
  Timer? _reconnectTimer;

  int _reconnectAttempts = 0;
  WebSocketStatus _status = WebSocketStatus.disconnected;

  final _messageController = StreamController<dynamic>.broadcast();
  final _statusController = StreamController<WebSocketStatus>.broadcast();

  WebSocketManager({
    required this.url,
    this.reconnectDelay = const Duration(seconds: 5),
    this.heartbeatInterval = const Duration(seconds: 30),
    this.maxReconnectAttempts = 5,
  });

  // Public streams
  Stream<dynamic> get messages => _messageController.stream;
  Stream<WebSocketStatus> get status => _statusController.stream;
  WebSocketStatus get currentStatus => _status;

  // Connect to WebSocket
  Future<void> connect() async {
    if (_status == WebSocketStatus.connected ||
        _status == WebSocketStatus.connecting) {
      return;
    }

    _updateStatus(WebSocketStatus.connecting);

    try {
      _channel = WebSocketChannel.connect(
        Uri.parse(url),
      );

      _subscription = _channel!.stream.listen(
        _handleMessage,
        onError: _handleError,
        onDone: _handleDisconnect,
      );

      _updateStatus(WebSocketStatus.connected);
      _reconnectAttempts = 0;
      _startHeartbeat();

      print('WebSocket connected to $url');
    } catch (e) {
      print('WebSocket connection error: $e');
      _updateStatus(WebSocketStatus.disconnected);
      _scheduleReconnect();
    }
  }

  // Send message
  void send(dynamic message) {
    if (_status != WebSocketStatus.connected) {
      print('Cannot send message: WebSocket not connected');
      return;
    }

    try {
      _channel?.sink.add(message);
    } catch (e) {
      print('Error sending message: $e');
    }
  }

  // Send JSON message
  void sendJson(Map<String, dynamic> data) {
    send(jsonEncode(data));
  }

  // Disconnect
  Future<void> disconnect() async {
    _reconnectTimer?.cancel();
    _heartbeatTimer?.cancel();
    await _subscription?.cancel();
    await _channel?.sink.close();

    _updateStatus(WebSocketStatus.disconnected);
    print('WebSocket disconnected');
  }

  // Dispose
  Future<void> dispose() async {
    await disconnect();
    await _messageController.close();
    await _statusController.close();
  }

  // Private methods

  void _handleMessage(dynamic message) {
    _messageController.add(message);
  }

  void _handleError(error) {
    print('WebSocket error: $error');
    _scheduleReconnect();
  }

  void _handleDisconnect() {
    print('WebSocket disconnected');
    _updateStatus(WebSocketStatus.disconnected);
    _scheduleReconnect();
  }

  void _scheduleReconnect() {
    if (_reconnectAttempts >= maxReconnectAttempts) {
      print('Max reconnect attempts reached');
      _updateStatus(WebSocketStatus.disconnected);
      return;
    }

    _updateStatus(WebSocketStatus.reconnecting);
    _reconnectAttempts++;

    // Exponential backoff
    final delay = reconnectDelay * (1 << (_reconnectAttempts - 1));
    print('Reconnecting in ${delay.inSeconds} seconds (attempt $_reconnectAttempts)');

    _reconnectTimer = Timer(delay, () {
      connect();
    });
  }

  void _startHeartbeat() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = Timer.periodic(heartbeatInterval, (timer) {
      if (_status == WebSocketStatus.connected) {
        sendJson({'type': 'ping', 'timestamp': DateTime.now().toIso8601String()});
      }
    });
  }

  void _updateStatus(WebSocketStatus status) {
    _status = status;
    _statusController.add(status);
  }
}
```

### Usage with State Management

Integrate with a state management solution:

```dart
class ChatController extends GetxController {
  late WebSocketManager _wsManager;
  final messages = <ChatMessage>[].obs;
  final connectionStatus = WebSocketStatus.disconnected.obs;

  @override
  void onInit() {
    super.onInit();

    _wsManager = WebSocketManager(
      url: 'wss://chat.example.com/ws',
    );

    // Listen to messages
    _wsManager.messages.listen((message) {
      final data = jsonDecode(message);
      messages.add(ChatMessage.fromJson(data));
    });

    // Listen to status
    _wsManager.status.listen((status) {
      connectionStatus.value = status;
    });

    _wsManager.connect();
  }

  void sendMessage(String text) {
    _wsManager.sendJson({
      'type': 'message',
      'text': text,
      'timestamp': DateTime.now().toIso8601String(),
    });

    // Add optimistic message
    messages.add(ChatMessage(
      id: 'temp_${DateTime.now().millisecondsSinceEpoch}',
      text: text,
      isLocal: true,
      timestamp: DateTime.now(),
    ));
  }

  @override
  void onClose() {
    _wsManager.dispose();
    super.onClose();
  }
}
```

## Authentication

### Token-Based Authentication

Authenticate WebSocket connections:

```dart
class AuthenticatedWebSocketManager extends WebSocketManager {
  final Future<String?> Function() getToken;

  AuthenticatedWebSocketManager({
    required String url,
    required this.getToken,
  }) : super(url: url);

  @override
  Future<void> connect() async {
    final token = await getToken();

    if (token == null) {
      throw Exception('No authentication token available');
    }

    // Option 1: Add token to URL query parameter
    final authenticatedUrl = '$url?token=$token';

    // Option 2: Send token in first message after connection
    // (depends on server implementation)

    _updateStatus(WebSocketStatus.connecting);

    try {
      _channel = WebSocketChannel.connect(
        Uri.parse(authenticatedUrl),
      );

      _subscription = _channel!.stream.listen(
        _handleMessage,
        onError: _handleError,
        onDone: _handleDisconnect,
      );

      // Send authentication message
      sendJson({
        'type': 'auth',
        'token': token,
      });

      _updateStatus(WebSocketStatus.connected);
      _startHeartbeat();
    } catch (e) {
      print('Connection error: $e');
      _scheduleReconnect();
    }
  }
}

// Usage
final wsManager = AuthenticatedWebSocketManager(
  url: 'wss://api.example.com/ws',
  getToken: () async {
    return await SecureStorage().getAccessToken();
  },
);
```

## Message Queue

Handle offline messages with a queue:

```dart
class QueuedWebSocketManager extends WebSocketManager {
  final List<dynamic> _messageQueue = [];
  final int maxQueueSize;

  QueuedWebSocketManager({
    required String url,
    this.maxQueueSize = 100,
  }) : super(url: url);

  @override
  void send(dynamic message) {
    if (_status == WebSocketStatus.connected) {
      // Send immediately
      super.send(message);
      _flushQueue();
    } else {
      // Queue message
      _queueMessage(message);
    }
  }

  void _queueMessage(dynamic message) {
    if (_messageQueue.length >= maxQueueSize) {
      // Remove oldest message
      _messageQueue.removeAt(0);
    }
    _messageQueue.add(message);
    print('Message queued. Queue size: ${_messageQueue.length}');
  }

  void _flushQueue() {
    if (_messageQueue.isEmpty) return;

    print('Flushing ${_messageQueue.length} queued messages');

    while (_messageQueue.isNotEmpty) {
      final message = _messageQueue.removeAt(0);
      super.send(message);
    }
  }

  @override
  Future<void> connect() async {
    await super.connect();
    // Flush queue after successful connection
    if (_status == WebSocketStatus.connected) {
      _flushQueue();
    }
  }
}
```

## Protocol Patterns

### Request-Response Pattern

Implement request-response over WebSocket:

```dart
class RpcWebSocketManager extends WebSocketManager {
  final Map<String, Completer<dynamic>> _pendingRequests = {};
  int _requestId = 0;

  RpcWebSocketManager({required String url}) : super(url: url);

  Future<T> request<T>(
    String method,
    Map<String, dynamic> params,
  ) async {
    final requestId = '${_requestId++}';
    final completer = Completer<T>();

    _pendingRequests[requestId] = completer;

    sendJson({
      'jsonrpc': '2.0',
      'id': requestId,
      'method': method,
      'params': params,
    });

    // Timeout after 30 seconds
    Timer(Duration(seconds: 30), () {
      if (!completer.isCompleted) {
        _pendingRequests.remove(requestId);
        completer.completeError(
          TimeoutException('Request timed out'),
        );
      }
    });

    return completer.future;
  }

  @override
  void _handleMessage(dynamic message) {
    final data = jsonDecode(message);

    // Check if this is a response to a pending request
    if (data['id'] != null) {
      final requestId = data['id'].toString();
      final completer = _pendingRequests.remove(requestId);

      if (completer != null) {
        if (data['error'] != null) {
          completer.completeError(data['error']);
        } else {
          completer.complete(data['result']);
        }
        return;
      }
    }

    // Regular message
    super._handleMessage(message);
  }
}

// Usage
final wsManager = RpcWebSocketManager(
  url: 'wss://api.example.com/ws',
);

try {
  final user = await wsManager.request(
    'getUser',
    {'userId': '123'},
  );
  print('User: $user');
} catch (e) {
  print('Error: $e');
}
```

### Pub-Sub Pattern

Subscribe to channels:

```dart
class PubSubWebSocketManager extends WebSocketManager {
  final Map<String, StreamController<dynamic>> _channels = {};

  PubSubWebSocketManager({required String url}) : super(url: url);

  Stream<dynamic> subscribe(String channel) {
    if (!_channels.containsKey(channel)) {
      _channels[channel] = StreamController.broadcast();

      // Send subscribe message
      sendJson({
        'type': 'subscribe',
        'channel': channel,
      });
    }

    return _channels[channel]!.stream;
  }

  void unsubscribe(String channel) {
    _channels[channel]?.close();
    _channels.remove(channel);

    sendJson({
      'type': 'unsubscribe',
      'channel': channel,
    });
  }

  void publish(String channel, dynamic data) {
    sendJson({
      'type': 'publish',
      'channel': channel,
      'data': data,
    });
  }

  @override
  void _handleMessage(dynamic message) {
    final data = jsonDecode(message);

    if (data['channel'] != null) {
      final channel = data['channel'];
      final controller = _channels[channel];

      if (controller != null) {
        controller.add(data['data']);
        return;
      }
    }

    super._handleMessage(message);
  }

  @override
  Future<void> dispose() async {
    for (final controller in _channels.values) {
      await controller.close();
    }
    _channels.clear();
    await super.dispose();
  }
}

// Usage
final wsManager = PubSubWebSocketManager(
  url: 'wss://api.example.com/ws',
);

// Subscribe to channel
wsManager.subscribe('chat:room123').listen((message) {
  print('New chat message: $message');
});

// Publish to channel
wsManager.publish('chat:room123', {
  'text': 'Hello, everyone!',
  'user': 'John',
});
```

## Testing

Test WebSocket code with mocks:

```dart
import 'package:test/test.dart';
import 'package:mockito/mockito.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class MockWebSocketChannel extends Mock implements WebSocketChannel {}
class MockWebSocketSink extends Mock implements WebSocketSink {}

void main() {
  group('WebSocketManager', () {
    test('sends message when connected', () {
      final mockChannel = MockWebSocketChannel();
      final mockSink = MockWebSocketSink();

      when(mockChannel.sink).thenReturn(mockSink);

      final manager = WebSocketManager(
        url: 'wss://test.com',
      );

      // Inject mock channel for testing
      manager.channel = mockChannel;
      manager.updateStatus(WebSocketStatus.connected);

      manager.send('test message');

      verify(mockSink.add('test message')).called(1);
    });

    test('queues message when disconnected', () {
      final manager = QueuedWebSocketManager(
        url: 'wss://test.com',
      );

      manager.send('test message');

      expect(manager.queueLength, 1);
    });
  });
}
```

## Best Practices

1. **Connection Management**: Always close WebSocket connections in dispose()
2. **Reconnection Logic**: Implement exponential backoff for reconnection attempts
3. **Heartbeat**: Send periodic ping messages to keep connection alive
4. **Error Handling**: Handle connection errors, message errors, and timeouts
5. **Message Queue**: Queue messages sent while disconnected
6. **Stream Disposal**: Cancel stream subscriptions to prevent memory leaks
7. **Authentication**: Secure WebSocket connections with tokens
8. **Protocol**: Define clear message protocols (JSON-RPC, pub-sub, etc.)
9. **UI Feedback**: Show connection status to users
10. **Testing**: Mock WebSocket channels for unit tests

## Common Pitfalls

- **Memory Leaks**: Not canceling stream subscriptions or closing channels
- **Infinite Reconnects**: Not limiting reconnection attempts
- **Blocking UI**: Processing large messages on the main thread
- **No Heartbeat**: Connection dies silently without keepalive
- **Missing Error Handling**: Not handling connection failures gracefully
- **Unsecured Connections**: Using ws:// instead of wss:// in production
- **No Queue**: Losing messages sent while disconnected
- **Synchronous Processing**: Blocking the WebSocket thread with heavy processing

## Conclusion

WebSockets enable powerful real-time features in Flutter applications. The web_socket_channel package provides a solid foundation, but production applications require additional patterns like reconnection logic, message queuing, and proper error handling. Follow the patterns in this guide to build robust, reliable real-time features that work well even under poor network conditions.
