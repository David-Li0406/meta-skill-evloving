import { Injectable, Logger } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { PrismaService } from '../common/prisma/prisma.service';
import { NotificationsGateway } from './notifications.gateway';

export interface NotificationPayload {
    type: string;
    title: string;
    message: string;
    actionUrl?: string;
    metadata?: Record<string, unknown>;
}

export interface MissionMessagePayload {
    id: string;
    missionId: string;
    content: string;
    type: 'TEXT' | 'SYSTEM';
    createdAt: Date | string;
    sender?: {
        id: string;
        role: string;
        profile?: {
            firstName: string;
            lastName: string;
            avatarUrl?: string;
        };
        establishment?: {
            name: string;
            logoUrl?: string;
        };
    };
}

@Injectable()
export class NotificationsService {
    private readonly logger = new Logger(NotificationsService.name);

    constructor(
        private readonly prisma: PrismaService,
        private readonly gateway: NotificationsGateway,
    ) { }

    // ========================================
    // NOTIFICATIONS
    // ========================================

    /**
     * Send a notification to a user (persisted + real-time)
     */
    async sendNotification(userId: string, payload: NotificationPayload): Promise<void> {
        try {
            // Persist notification to database
            const notification = await this.prisma.notification.create({
                data: {
                    userId,
                    type: payload.type,
                    title: payload.title,
                    message: payload.message,
                    link: payload.actionUrl,
                    metadata: (payload.metadata as Prisma.InputJsonValue) || Prisma.JsonNull,
                },
            });

            // Emit to user's socket connection
            this.gateway.emitToUser(userId, 'notification', {
                id: notification.id,
                type: payload.type,
                title: payload.title,
                message: payload.message,
                actionUrl: payload.actionUrl,
                createdAt: notification.createdAt,
            });

            this.logger.log(`Notification sent to user ${userId}: ${payload.type}`);
        } catch (error) {
            this.logger.error(`Failed to send notification: ${error.message}`);
        }
    }

    async listNotifications(userId: string, unreadOnly = false) {
        return this.prisma.notification.findMany({
            where: {
                userId,
                ...(unreadOnly ? { isRead: false } : {}),
            },
            orderBy: { createdAt: 'desc' },
            take: 100,
        });
    }

    async markAllAsRead(userId: string) {
        const result = await this.prisma.notification.updateMany({
            where: { userId, isRead: false },
            data: {
                isRead: true,
                readAt: new Date(),
            },
        });

        return { updated: result.count };
    }

    // ========================================
    // MISSION CHAT
    // ========================================

    /**
     * Emit a mission message to all participants in the mission room
     */
    emitMissionMessage(missionId: string, message: MissionMessagePayload): void {
        this.gateway.emitToMission(missionId, 'missionMessage', message);
        this.logger.debug(`Mission message emitted to mission ${missionId}`);
    }

    // ========================================
    // ACTIVE MISSIONS COUNT
    // ========================================

    /**
     * Emit active missions count update to a user
     */
    emitActiveMissionsCountUpdate(userId: string, count: number): void {
        this.gateway.emitToUser(userId, 'activeMissionsCountUpdate', { count });
        this.logger.debug(`Active missions count update sent to user ${userId}: ${count}`);
    }

    /**
     * Recalculate and emit active missions count for a user
     */
    async refreshActiveMissionsCount(userId: string): Promise<void> {
        const count = await this.prisma.reliefMission.count({
            where: {
                OR: [
                    { clientId: userId },
                    { assignedTalentId: userId },
                ],
                status: {
                    in: ['ASSIGNED', 'IN_PROGRESS'],
                },
            },
        });

        this.emitActiveMissionsCountUpdate(userId, count);
    }

    // ========================================
    // MISSION EVENT NOTIFICATIONS
    // ========================================

    /**
     * Notify when talent acknowledges instructions
     */
    async notifyInstructionsAcknowledged(
        missionId: string,
        clientId: string,
        talentName: string,
    ): Promise<void> {
        await this.sendNotification(clientId, {
            type: 'INSTRUCTIONS_ACKNOWLEDGED',
            title: 'Consignes validées',
            message: `${talentName} a validé les consignes de la mission`,
            actionUrl: `/dashboard/missions/${missionId}/tracking`,
        });
    }

    /**
     * Notify when talent starts the mission
     */
    async notifyMissionStarted(
        missionId: string,
        clientId: string,
        talentName: string,
    ): Promise<void> {
        await this.sendNotification(clientId, {
            type: 'MISSION_STARTED',
            title: 'Mission démarrée',
            message: `${talentName} a démarré la mission`,
            actionUrl: `/dashboard/missions/${missionId}/tracking`,
        });
    }

    /**
     * Notify when talent submits report
     */
    async notifyReportSubmitted(
        missionId: string,
        clientId: string,
        talentName: string,
    ): Promise<void> {
        await this.sendNotification(clientId, {
            type: 'REPORT_SUBMITTED',
            title: 'Rapport de mission',
            message: `${talentName} a soumis le rapport de fin de mission`,
            actionUrl: `/dashboard/missions/${missionId}/tracking`,
        });
    }

    /**
     * Notify about new chat message (for the other participant)
     */
    async notifyNewMissionMessage(
        missionId: string,
        recipientId: string,
        senderName: string,
    ): Promise<void> {
        await this.sendNotification(recipientId, {
            type: 'NEW_MISSION_MESSAGE',
            title: 'Nouveau message',
            message: `${senderName} vous a envoyé un message`,
            actionUrl: `/dashboard/missions/${missionId}/tracking`,
        });
    }

    // ========================================
    // 24H CLOSURE LOGIC
    // ========================================

    private readonly CLOSURE_DELAY_MS = 24 * 60 * 60 * 1000; // 24 hours

    /**
     * Get chat status for a mission (locked state and closure time)
     */
    async getChatStatus(missionId: string): Promise<{
        isLocked: boolean;
        closesAt?: Date;
        lockMessage?: string;
    }> {
        const report = await this.prisma.missionReport.findUnique({
            where: { missionId },
        });

        if (!report) {
            return { isLocked: false };
        }

        const closesAt = new Date(report.createdAt.getTime() + this.CLOSURE_DELAY_MS);
        const isLocked = Date.now() > closesAt.getTime();

        return {
            isLocked,
            closesAt: isLocked ? undefined : closesAt,
            lockMessage: isLocked
                ? '🔒 Mission clôturée. La messagerie est désormais en lecture seule.'
                : undefined,
        };
    }

    /**
     * Check if mission chat is open (throws if locked)
     */
    async assertChatOpen(missionId: string): Promise<void> {
        const status = await this.getChatStatus(missionId);
        if (status.isLocked) {
            throw new Error(
                'La messagerie de cette mission est clôturée. Le chat devient lecture seule 24h après la soumission du rapport.',
            );
        }
    }

    /**
     * Create closure warning system message when report is submitted
     */
    async emitClosureWarningMessage(missionId: string): Promise<void> {
        const closesAt = new Date(Date.now() + this.CLOSURE_DELAY_MS);
        const formattedTime = closesAt.toLocaleString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit',
            day: 'numeric',
            month: 'long',
        });

        // Create and emit system message
        const systemMessage = await this.prisma.missionMessage.create({
            data: {
                missionId,
                senderId: (await this.prisma.reliefMission.findUnique({
                    where: { id: missionId },
                    select: { clientId: true },
                }))?.clientId || '',
                content: `⚠️ La mission est terminée. La messagerie fermera automatiquement le ${formattedTime}.`,
                type: 'SYSTEM',
            },
        });

        this.emitMissionMessage(missionId, {
            id: systemMessage.id,
            missionId,
            content: systemMessage.content,
            type: 'SYSTEM',
            createdAt: systemMessage.createdAt,
        });

        // Emit mission locked event with closure time
        this.gateway.emitToMission(missionId, 'missionClosing', {
            closesAt,
            message: `La messagerie fermera automatiquement le ${formattedTime}.`,
        });
    }

    /**
     * Emit final lock message when chat becomes read-only
     */
    async emitFinalLockMessage(missionId: string): Promise<void> {
        const systemMessage = await this.prisma.missionMessage.create({
            data: {
                missionId,
                senderId: (await this.prisma.reliefMission.findUnique({
                    where: { id: missionId },
                    select: { clientId: true },
                }))?.clientId || '',
                content: '🔒 Mission clôturée. La messagerie est désormais en lecture seule.',
                type: 'SYSTEM',
            },
        });

        this.emitMissionMessage(missionId, {
            id: systemMessage.id,
            missionId,
            content: systemMessage.content,
            type: 'SYSTEM',
            createdAt: systemMessage.createdAt,
        });

        this.gateway.emitToMission(missionId, 'missionLocked', {
            message: '🔒 Mission clôturée. La messagerie est désormais en lecture seule.',
        });
    }
}
