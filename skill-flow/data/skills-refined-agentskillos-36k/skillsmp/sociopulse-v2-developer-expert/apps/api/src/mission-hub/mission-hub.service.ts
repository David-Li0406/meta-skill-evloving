import {
    Injectable,
    NotFoundException,
    ForbiddenException,
    BadRequestException,
    Logger,
} from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { NotificationsService } from '../notifications/notifications.service';
import {
    SubmitReportDto,
    SendMissionMessageDto,
    CreateInstructionsDto,
} from './dto';
import { MissionStatus, MissionMessageType, MissionTimelineEventType, Prisma } from '@prisma/client';

@Injectable()
export class MissionHubService {
    private readonly logger = new Logger(MissionHubService.name);

    constructor(
        private readonly prisma: PrismaService,
        private readonly notificationsService: NotificationsService,
    ) { }

    // ========================================
    // INSTRUCTIONS
    // ========================================

    /**
     * Create or update instructions for a mission (Client only)
     */
    async createInstructions(missionId: string, clientId: string, dto: CreateInstructionsDto) {
        const mission = await this.findMissionOrThrow(missionId);

        if (mission.clientId !== clientId) {
            throw new ForbiddenException('Seul le client peut créer des consignes');
        }

        const checklist = dto.checklist?.map(item => ({
            ...item,
            completed: false,
        })) || [];

        const instructions = await this.prisma.missionInstruction.upsert({
            where: { missionId },
            create: {
                missionId,
                content: dto.content,
                checklist,
            },
            update: {
                content: dto.content,
                checklist,
            },
        });

        return instructions;
    }

    /**
     * Get instructions for a mission
     */
    async getInstructions(missionId: string) {
        const instructions = await this.prisma.missionInstruction.findUnique({
            where: { missionId },
        });

        if (!instructions) {
            return null;
        }

        return instructions;
    }

    /**
     * Acknowledge mission instructions (Talent only)
     */
    async acknowledgeInstructions(missionId: string, talentId: string) {
        const mission = await this.findMissionOrThrow(missionId);

        if (mission.assignedTalentId !== talentId) {
            throw new ForbiddenException('Seul le talent assigné peut valider les consignes');
        }

        const instructions = await this.prisma.missionInstruction.findUnique({
            where: { missionId },
        });

        if (!instructions) {
            throw new NotFoundException('Aucune consigne trouvée pour cette mission');
        }

        if (instructions.isAcknowledged) {
            return { message: 'Consignes déjà validées', instructions };
        }

        // Update instructions
        const updated = await this.prisma.missionInstruction.update({
            where: { missionId },
            data: {
                isAcknowledged: true,
                acknowledgedAt: new Date(),
            },
        });

        // Log timeline event
        await this.createTimelineEvent(missionId, talentId, MissionTimelineEventType.BRIEFING_READ);

        // Create system message
        await this.createSystemMessage(missionId, '✅ Le talent a validé les consignes de mission');

        // Get talent name for notification
        const talent = await this.prisma.user.findUnique({
            where: { id: talentId },
            select: { profile: { select: { firstName: true, lastName: true } } },
        });
        const talentName = talent?.profile
            ? `${talent.profile.firstName} ${talent.profile.lastName}`
            : 'Le talent';

        // Notify client via WebSocket
        await this.notificationsService.notifyInstructionsAcknowledged(
            missionId,
            mission.clientId,
            talentName,
        );

        this.logger.log(`Instructions acknowledged for mission ${missionId} by talent ${talentId}`);

        return { message: 'Consignes validées avec succès', instructions: updated };
    }

    // ========================================
    // MISSION LIFECYCLE
    // ========================================

    /**
     * Start a mission manually (Talent only)
     */
    async startMission(missionId: string, talentId: string, note?: string) {
        const mission = await this.findMissionOrThrow(missionId);

        if (mission.assignedTalentId !== talentId) {
            throw new ForbiddenException('Seul le talent assigné peut démarrer la mission');
        }

        if (mission.status !== MissionStatus.ASSIGNED) {
            throw new BadRequestException(
                `La mission ne peut pas être démarrée (statut actuel: ${mission.status})`
            );
        }

        // Update mission status
        const updated = await this.prisma.reliefMission.update({
            where: { id: missionId },
            data: { status: MissionStatus.IN_PROGRESS },
        });

        // Log timeline event
        await this.createTimelineEvent(missionId, talentId, MissionTimelineEventType.MISSION_STARTED, {
            note,
        });

        // Create system message
        await this.createSystemMessage(missionId, '🚀 La mission a été démarrée');

        // Get talent name for notification
        const talent = await this.prisma.user.findUnique({
            where: { id: talentId },
            select: { profile: { select: { firstName: true, lastName: true } } },
        });
        const talentName = talent?.profile
            ? `${talent.profile.firstName} ${talent.profile.lastName}`
            : 'Le talent';

        // Notify client via WebSocket
        await this.notificationsService.notifyMissionStarted(
            missionId,
            mission.clientId,
            talentName,
        );

        // Refresh active missions count for both parties
        await this.notificationsService.refreshActiveMissionsCount(mission.clientId);
        await this.notificationsService.refreshActiveMissionsCount(talentId);

        this.logger.log(`Mission ${missionId} started by talent ${talentId}`);

        return { message: 'Mission démarrée avec succès', mission: updated };
    }

    /**
     * Submit final report (Talent only)
     */
    async submitReport(missionId: string, talentId: string, dto: SubmitReportDto) {
        const mission = await this.findMissionOrThrow(missionId);

        if (mission.assignedTalentId !== talentId) {
            throw new ForbiddenException('Seul le talent assigné peut soumettre un rapport');
        }

        if (mission.status !== MissionStatus.IN_PROGRESS) {
            throw new BadRequestException(
                'Le rapport ne peut être soumis que pour une mission en cours'
            );
        }

        // Check if report already exists
        const existingReport = await this.prisma.missionReport.findUnique({
            where: { missionId },
        });

        if (existingReport) {
            throw new BadRequestException('Un rapport a déjà été soumis pour cette mission');
        }

        // Create report
        const report = await this.prisma.missionReport.create({
            data: {
                missionId,
                talentId,
                content: dto.content,
                incidents: dto.incidents,
                hoursWorked: dto.hoursWorked,
            },
        });

        // Update mission status to COMPLETED
        await this.prisma.reliefMission.update({
            where: { id: missionId },
            data: {
                status: MissionStatus.COMPLETED,
                completedAt: new Date(),
            },
        });

        // Log timeline event
        await this.createTimelineEvent(missionId, talentId, MissionTimelineEventType.REPORT_SUBMITTED);

        // Create system message
        await this.createSystemMessage(missionId, '📝 Le rapport de mission a été soumis');

        // Get talent name for notification
        const talent = await this.prisma.user.findUnique({
            where: { id: talentId },
            select: { profile: { select: { firstName: true, lastName: true } } },
        });
        const talentName = talent?.profile
            ? `${talent.profile.firstName} ${talent.profile.lastName}`
            : 'Le talent';

        // Notify client via WebSocket
        await this.notificationsService.notifyReportSubmitted(
            missionId,
            mission.clientId,
            talentName,
        );

        // Emit closure warning (24h countdown starts)
        await this.notificationsService.emitClosureWarningMessage(missionId);

        // Refresh active missions count for both parties
        await this.notificationsService.refreshActiveMissionsCount(mission.clientId);
        await this.notificationsService.refreshActiveMissionsCount(talentId);

        this.logger.log(`Report submitted for mission ${missionId} by talent ${talentId}`);

        return { message: 'Rapport soumis avec succès', report };
    }

    // ========================================
    // CHAT
    // ========================================

    /**
     * Get chat messages for a mission
     */
    async getChatMessages(missionId: string, userId: string) {
        const mission = await this.findMissionOrThrow(missionId);

        // Verify user is part of this mission
        if (mission.clientId !== userId && mission.assignedTalentId !== userId) {
            throw new ForbiddenException('Accès non autorisé à cette conversation');
        }

        const messages = await this.prisma.missionMessage.findMany({
            where: { missionId },
            include: {
                sender: {
                    select: {
                        id: true,
                        role: true,
                        profile: {
                            select: {
                                firstName: true,
                                lastName: true,
                                avatarUrl: true,
                            },
                        },
                        establishment: {
                            select: {
                                name: true,
                                logoUrl: true,
                            },
                        },
                    },
                },
            },
            orderBy: { createdAt: 'asc' },
        });

        return messages;
    }

    /**
     * Send a message in mission chat
     */
    async sendMessage(missionId: string, senderId: string, dto: SendMissionMessageDto) {
        const mission = await this.findMissionOrThrow(missionId);

        // Verify user is part of this mission
        if (mission.clientId !== senderId && mission.assignedTalentId !== senderId) {
            throw new ForbiddenException('Acces non autorise a cette conversation');
        }

        await this.ensureMissionChatOpen(missionId);

        const message = await this.prisma.missionMessage.create({
            data: {
                missionId,
                senderId,
                content: dto.content,
                type: MissionMessageType.TEXT,
            },
            include: {
                sender: {
                    select: {
                        id: true,
                        role: true,
                        profile: {
                            select: {
                                firstName: true,
                                lastName: true,
                                avatarUrl: true,
                            },
                        },
                    },
                },
            },
        });

        // Log timeline event
        await this.createTimelineEvent(missionId, senderId, MissionTimelineEventType.CHAT_MESSAGE);

        // Emit message to mission room via WebSocket
        this.notificationsService.emitMissionMessage(missionId, {
            id: message.id,
            missionId,
            content: message.content,
            type: message.type,
            createdAt: message.createdAt,
            sender: message.sender,
        });

        // Notify the other participant
        const recipientId = mission.clientId === senderId
            ? mission.assignedTalentId
            : mission.clientId;

        if (recipientId) {
            const senderProfile = message.sender?.profile;
            const senderName = senderProfile
                ? `${senderProfile.firstName} ${senderProfile.lastName}`
                : 'Un participant';

            await this.notificationsService.notifyNewMissionMessage(
                missionId,
                recipientId,
                senderName,
            );
        }

        return message;
    }

    // ========================================
    // TIMELINE
    // ========================================

    /**
     * Get mission timeline
     */
    async getTimeline(missionId: string, userId: string) {
        const mission = await this.findMissionOrThrow(missionId);

        // Verify user has access
        if (mission.clientId !== userId && mission.assignedTalentId !== userId) {
            throw new ForbiddenException('Accès non autorisé');
        }

        const events = await this.prisma.missionTimelineEvent.findMany({
            where: { missionId },
            include: {
                user: {
                    select: {
                        id: true,
                        profile: {
                            select: {
                                firstName: true,
                                lastName: true,
                            },
                        },
                    },
                },
            },
            orderBy: { createdAt: 'asc' },
        });

        return events;
    }

    // ========================================
    // ACTIVE MISSIONS
    // ========================================

    /**
     * Get active missions count for a user
     */
    async getActiveMissionsCount(userId: string): Promise<number> {
        const count = await this.prisma.reliefMission.count({
            where: {
                OR: [
                    { clientId: userId },
                    { assignedTalentId: userId },
                ],
                status: {
                    in: [MissionStatus.ASSIGNED, MissionStatus.IN_PROGRESS],
                },
            },
        });

        return count;
    }

    /**
     * Get active missions for a user
     */
    async getActiveMissions(userId: string) {
        const missions = await this.prisma.reliefMission.findMany({
            where: {
                OR: [
                    { clientId: userId },
                    { assignedTalentId: userId },
                ],
                status: {
                    in: [MissionStatus.ASSIGNED, MissionStatus.IN_PROGRESS],
                },
            },
            include: {
                client: {
                    select: {
                        id: true,
                        establishment: {
                            select: {
                                name: true,
                                logoUrl: true,
                            },
                        },
                    },
                },
                assignedTalent: {
                    select: {
                        id: true,
                        profile: {
                            select: {
                                firstName: true,
                                lastName: true,
                                avatarUrl: true,
                            },
                        },
                    },
                },
                instructions: {
                    select: {
                        isAcknowledged: true,
                    },
                },
            },
            orderBy: { startDate: 'asc' },
        });

        return missions;
    }

    // ========================================
    // HELPERS
    // ========================================

    private async ensureMissionChatOpen(missionId: string) {
        const report = await this.prisma.missionReport.findUnique({
            where: { missionId },
            select: { createdAt: true },
        });

        if (!report) {
            return;
        }

        const twentyFourHoursMs = 24 * 60 * 60 * 1000;
        const elapsed = Date.now() - report.createdAt.getTime();

        if (elapsed >= twentyFourHoursMs) {
            throw new ForbiddenException(
                'Le chat est verrouille 24h apres le depot du rapport de mission',
            );
        }
    }

    private async findMissionOrThrow(missionId: string) {
        const mission = await this.prisma.reliefMission.findUnique({
            where: { id: missionId },
        });

        if (!mission) {
            throw new NotFoundException(`Mission ${missionId} non trouvee`);
        }

        return mission;
    }

    private async createTimelineEvent(
        missionId: string,
        userId: string | null,
        type: MissionTimelineEventType,
        metadata?: Record<string, unknown>,
    ) {
        return this.prisma.missionTimelineEvent.create({
            data: {
                missionId,
                userId,
                type,
                metadata: (metadata as Prisma.InputJsonValue) || Prisma.JsonNull,
            },
        });
    }

    private async createSystemMessage(missionId: string, content: string) {
        // For system messages, we don't have a sender (or use a system account)
        // We'll use the mission itself as a marker
        return this.prisma.$executeRaw`
      INSERT INTO "MissionMessage" (id, "missionId", "senderId", content, type, "createdAt")
      SELECT 
        gen_random_uuid()::text,
        ${missionId},
        "clientId",
        ${content},
        'SYSTEM'::"MissionMessageType",
        now()
      FROM "ReliefMission"
      WHERE id = ${missionId}
    `;
    }
}
