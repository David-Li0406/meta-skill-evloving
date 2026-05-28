# Reverb Channels

## Channel Types

### Public Channels

```php
// Everyone can listen
public function broadcastOn(): array
{
    return [
        new Channel('orders'),
    ];
}
```

```js
Echo.channel('orders')
    .listen('.order.created', (e) => {
        console.log(e.order);
    });
```

### Private Channels

```php
// routes/channels.php
Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::find($orderId)->user_id;
});
```

```php
// Event
public function broadcastOn(): array
{
    return [
        new PrivateChannel('orders.' . $this->order->id),
    ];
}
```

```js
Echo.private('orders.123')
    .listen('.status.updated', (e) => {
        console.log(e.order.status);
    });
```

### Presence Channels

```php
// routes/channels.php
Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```

```js
Echo.join('chat.1')
    .here((users) => {
        console.log('Users in room:', users);
    })
    .joining((user) => {
        console.log(user.name + ' joined');
    })
    .leaving((user) => {
        console.log(user.name + ' left');
    })
    .listen('.message.sent', (e) => {
        console.log(e.message);
    });
```

## Client Events (User-to-User)

```js
// Enable in Echo config
Echo.private('chat.1')
    .whisper('typing', { user: 'John' });

Echo.private('chat.1')
    .listenForWhisper('typing', (e) => {
        console.log(e.user + ' is typing...');
    });
```

## Broadcasting Queue

```php
// Broadcast on specific queue
class OrderShipped implements ShouldBroadcast
{
    public function broadcastQueue(): string
    {
        return 'broadcasts';
    }
}

// Broadcast immediately (no queue)
class OrderShipped implements ShouldBroadcastNow
{
    // ...
}
```

## Frontend Setup

```js
// resources/js/bootstrap.js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT,
    wssPort: import.meta.env.VITE_REVERB_PORT,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```
