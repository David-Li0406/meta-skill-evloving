# Real-time Updates

## Server-Sent Events (SSE)

### Price Stream
```python
from flask import Response
import json
import time

@app.route("/stream/prices/<symbol>")
def stream_prices(symbol):
    def generate():
        while True:
            price = get_current_price(symbol)
            data = json.dumps({
                "symbol": symbol,
                "price": price,
                "timestamp": time.time()
            })
            yield f"data: {data}\n\n"
            time.sleep(1)
    
    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
```

### Client Usage
```javascript
const eventSource = new EventSource('/stream/prices/BTC/USDT');

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(`Price: ${data.price}`);
};
```

## WebSocket Support

### WebSocket Server
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    emit('connected', {'status': 'ok'})

@socketio.on('subscribe')
def handle_subscribe(data):
    symbol = data['symbol']
    # Subscribe to price updates
    emit('subscribed', {'symbol': symbol})

@socketio.on('disconnect')
def handle_disconnect():
    # Cleanup subscriptions
    pass
```

### Push Updates
```python
def broadcast_price_update(symbol, price):
    socketio.emit('price_update', {
        'symbol': symbol,
        'price': price,
        'timestamp': time.time()
    })
```

### Client Usage
```javascript
const socket = io('http://localhost:5000');

socket.on('connect', () => {
    socket.emit('subscribe', {symbol: 'BTC/USDT'});
});

socket.on('price_update', (data) => {
    console.log(`${data.symbol}: ${data.price}`);
});
```
