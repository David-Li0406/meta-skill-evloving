# NestJS WebSocket Patterns

## Gateway Setup

```typescript
import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  OnGatewayConnection,
  OnGatewayDisconnect,
  ConnectedSocket,
  MessageBody,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({
  cors: { origin: '*' },
  namespace: '/chat',
})
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  handleConnection(client: Socket) {
    console.log(`Client connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    console.log(`Client disconnected: ${client.id}`);
  }

  @SubscribeMessage('message')
  handleMessage(
    @ConnectedSocket() client: Socket,
    @MessageBody() data: { room: string; message: string },
  ) {
    this.server.to(data.room).emit('message', {
      sender: client.id,
      message: data.message,
    });
  }

  @SubscribeMessage('join')
  handleJoin(
    @ConnectedSocket() client: Socket,
    @MessageBody() room: string,
  ) {
    client.join(room);
    client.emit('joined', room);
  }
}
```

## Authentication

```typescript
@WebSocketGateway()
export class AuthenticatedGateway implements OnGatewayConnection {
  constructor(private authService: AuthService) {}

  async handleConnection(client: Socket) {
    try {
      const token = client.handshake.auth.token;
      const user = await this.authService.validateToken(token);
      client.data.user = user;
    } catch {
      client.disconnect();
    }
  }

  @SubscribeMessage('protected-event')
  handleProtected(@ConnectedSocket() client: Socket) {
    const user = client.data.user;
    return { user: user.name };
  }
}
```

## Broadcasting

```typescript
@Injectable()
export class NotificationsService {
  constructor(
    @Inject('CHAT_GATEWAY')
    private gateway: ChatGateway,
  ) {}

  // Broadcast to all
  broadcastToAll(event: string, data: any) {
    this.gateway.server.emit(event, data);
  }

  // To specific room
  broadcastToRoom(room: string, event: string, data: any) {
    this.gateway.server.to(room).emit(event, data);
  }

  // To specific client
  sendToClient(clientId: string, event: string, data: any) {
    this.gateway.server.to(clientId).emit(event, data);
  }
}
```

## Module Setup

```typescript
@Module({
  providers: [
    ChatGateway,
    {
      provide: 'CHAT_GATEWAY',
      useExisting: ChatGateway,
    },
  ],
  exports: ['CHAT_GATEWAY'],
})
export class WebSocketModule {}
```
