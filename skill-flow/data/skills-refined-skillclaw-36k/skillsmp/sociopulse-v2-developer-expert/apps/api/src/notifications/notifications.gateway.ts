import {
    WebSocketGateway,
    WebSocketServer,
    OnGatewayConnection,
    OnGatewayDisconnect,
    OnGatewayInit,
    SubscribeMessage,
    MessageBody,
    ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';

interface AuthenticatedSocket extends Socket {
    userId: string;
}

@WebSocketGateway({
    cors: {
        origin: '*',
        credentials: true,
    },
    namespace: '/',
})
export class NotificationsGateway implements OnGatewayInit, OnGatewayConnection, OnGatewayDisconnect {
    @WebSocketServer()
    server: Server;

    private readonly logger = new Logger(NotificationsGateway.name);
    private connectedUsers = new Map<string, Set<string>>(); // userId -> Set of socketIds

    constructor(
        private readonly jwtService: JwtService,
        private readonly configService: ConfigService,
    ) { }

    afterInit(): void {
        this.logger.log('🔌 WebSocket Gateway initialized on namespace /');
    }

    /**
     * Handle new WebSocket connections with JWT authentication
     */
    async handleConnection(client: Socket): Promise<void> {
        try {
            // Extract token from handshake auth or query
            const token =
                client.handshake.auth?.token ||
                client.handshake.headers?.authorization?.replace('Bearer ', '') ||
                client.handshake.query?.token;

            if (!token) {
                this.logger.warn(`Connection rejected: No token provided (socket: ${client.id})`);
                client.emit('error', { message: 'Authentication required' });
                client.disconnect();
                return;
            }

            // Verify JWT
            const secret = this.configService.get<string>('JWT_SECRET');
            const payload = await this.jwtService.verifyAsync(token, { secret });

            if (!payload?.sub) {
                throw new UnauthorizedException('Invalid token payload');
            }

            // Attach userId to socket
            (client as AuthenticatedSocket).userId = payload.sub;

            // Join user's personal room
            const userRoom = `user_${payload.sub}`;
            client.join(userRoom);

            // Track connected sockets for this user
            if (!this.connectedUsers.has(payload.sub)) {
                this.connectedUsers.set(payload.sub, new Set());
            }
            this.connectedUsers.get(payload.sub)!.add(client.id);

            this.logger.log(`Client connected: ${client.id} (user: ${payload.sub})`);

            // Emit connection success
            client.emit('connected', { userId: payload.sub, room: userRoom });
        } catch (error) {
            this.logger.error(`Connection failed: ${error.message}`);
            client.emit('error', { message: 'Authentication failed' });
            client.disconnect();
        }
    }

    /**
     * Handle WebSocket disconnections
     */
    handleDisconnect(client: Socket): void {
        const userId = (client as AuthenticatedSocket).userId;

        if (userId) {
            // Remove socket from user's connected sockets
            const userSockets = this.connectedUsers.get(userId);
            if (userSockets) {
                userSockets.delete(client.id);
                if (userSockets.size === 0) {
                    this.connectedUsers.delete(userId);
                }
            }
            this.logger.log(`Client disconnected: ${client.id} (user: ${userId})`);
        } else {
            this.logger.log(`Client disconnected: ${client.id}`);
        }
    }

    /**
     * Join a mission room to receive mission-specific events
     */
    @SubscribeMessage('joinMissionRoom')
    handleJoinMissionRoom(
        @ConnectedSocket() client: AuthenticatedSocket,
        @MessageBody() data: { missionId: string },
    ): void {
        if (!data?.missionId) {
            client.emit('error', { message: 'missionId required' });
            return;
        }

        const roomName = `mission_${data.missionId}`;
        client.join(roomName);
        this.logger.log(`User ${client.userId} joined room: ${roomName}`);
        client.emit('joinedRoom', { room: roomName });
    }

    /**
     * Leave a mission room
     */
    @SubscribeMessage('leaveMissionRoom')
    handleLeaveMissionRoom(
        @ConnectedSocket() client: AuthenticatedSocket,
        @MessageBody() data: { missionId: string },
    ): void {
        if (!data?.missionId) {
            client.emit('error', { message: 'missionId required' });
            return;
        }

        const roomName = `mission_${data.missionId}`;
        client.leave(roomName);
        this.logger.log(`User ${client.userId} left room: ${roomName}`);
        client.emit('leftRoom', { room: roomName });
    }

    // ========================================
    // PUBLIC METHODS FOR NotificationsService
    // ========================================

    /**
     * Emit notification to a specific user
     */
    emitToUser(userId: string, event: string, data: unknown): void {
        const room = `user_${userId}`;
        this.server.to(room).emit(event, data);
        this.logger.debug(`Emitted "${event}" to ${room}`);
    }

    /**
     * Emit event to a mission room
     */
    emitToMission(missionId: string, event: string, data: unknown): void {
        const room = `mission_${missionId}`;
        this.server.to(room).emit(event, data);
        this.logger.debug(`Emitted "${event}" to ${room}`);
    }

    /**
     * Check if a user has any connected sockets
     */
    isUserOnline(userId: string): boolean {
        return this.connectedUsers.has(userId) && this.connectedUsers.get(userId)!.size > 0;
    }

    /**
     * Get count of currently connected unique users
     */
    getConnectedUsersCount(): number {
        return this.connectedUsers.size;
    }
}
