import { Injectable, Logger, NotFoundException, ForbiddenException } from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { CreateAdminNoteDto } from './dto';
import { GamificationService } from '../growth/gamification.service';

export interface UserFilter {
    role?: string;
    status?: string;
    search?: string;
    isVerified?: boolean;
    clientType?: string;
    page?: number;
    limit?: number;
}

export interface PaginatedResult<T> {
    data: T[];
    meta: {
        total: number;
        page: number;
        limit: number;
        totalPages: number;
    };
}

@Injectable()
export class AdminService {
    private readonly logger = new Logger(AdminService.name);

    constructor(
        private readonly prisma: PrismaService,
        private readonly gamificationService: GamificationService,
    ) { }

    /**
     * Vérifie que l'utilisateur est un admin
     */
    async isAdmin(userId: string): Promise<boolean> {
        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: { role: true },
        });
        return user?.role === 'ADMIN';
    }

    /**
     * Crée une entrée dans le journal d'audit
     */
    async createAuditLog(params: {
        adminId: string;
        action: string;
        targetUserId?: string;
        resourceId?: string;
        resourceType?: string;
        metadata?: any;
        ipAddress?: string;
        userAgent?: string;
    }) {
        return this.prisma.auditLog.create({
            data: {
                adminId: params.adminId,
                action: params.action,
                targetUserId: params.targetUserId,
                resourceId: params.resourceId,
                resourceType: params.resourceType,
                metadata: params.metadata,
                ipAddress: params.ipAddress,
                userAgent: params.userAgent,
            },
        });
    }

    /**
     * Liste tous les utilisateurs avec pagination et filtres (CRM)
     */
    async findAllUsers(filters: UserFilter = {}): Promise<PaginatedResult<any>> {
        const { role, status, search, isVerified, clientType, page = 1, limit = 20 } = filters;
        const skip = (page - 1) * limit;

        const where: any = {};

        if (role) {
            where.role = role;
        }
        if (status) {
            where.status = status;
        }
        if (typeof isVerified === 'boolean') {
            where.isVerified = isVerified;
        }
        if (clientType) {
            where.clientType = clientType;
        }
        if (search) {
            where.OR = [
                { email: { contains: search, mode: 'insensitive' } },
                { profile: { firstName: { contains: search, mode: 'insensitive' } } },
                { profile: { lastName: { contains: search, mode: 'insensitive' } } },
                { establishment: { name: { contains: search, mode: 'insensitive' } } },
            ];
        }

        const [users, total] = await Promise.all([
            this.prisma.user.findMany({
                where,
                skip,
                take: limit,
                include: {
                    profile: {
                        select: { firstName: true, lastName: true, avatarUrl: true, city: true },
                    },
                    establishment: {
                        select: { name: true, type: true, city: true },
                    },
                    _count: {
                        select: {
                            bookingsAsClient: true,
                            bookingsAsProvider: true,
                            adminNotesReceived: true,
                            documents: true,
                        },
                    },
                },
                orderBy: { createdAt: 'desc' },
            }),
            this.prisma.user.count({ where }),
        ]);

        return {
            data: users,
            meta: {
                total,
                page,
                limit,
                totalPages: Math.ceil(total / limit),
            },
        };
    }

    /**
     * Alias pour compatibilité avec l'ancien code
     */
    async listUsers(filters?: { role?: string; status?: string; search?: string }) {
        const result = await this.findAllUsers(filters);
        return result.data;
    }

    /**
     * Récupère un utilisateur avec ses détails complets
     */
    async getUserDetails(userId: string) {
        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            include: {
                profile: true,
                establishment: true,
                documents: {
                    orderBy: { createdAt: 'desc' },
                },
                adminNotesReceived: {
                    include: {
                        admin: {
                            select: { email: true, profile: { select: { firstName: true, lastName: true } } },
                        },
                    },
                    orderBy: { createdAt: 'desc' },
                },
                bookingsAsClient: {
                    take: 10,
                    orderBy: { createdAt: 'desc' },
                    include: {
                        provider: {
                            select: { profile: { select: { firstName: true, lastName: true } } },
                        },
                        service: { select: { name: true } },
                    },
                },
                bookingsAsProvider: {
                    take: 10,
                    orderBy: { createdAt: 'desc' },
                    include: {
                        client: {
                            select: { profile: { select: { firstName: true, lastName: true } }, establishment: { select: { name: true } } },
                        },
                        service: { select: { name: true } },
                    },
                },
                missionsAsClient: {
                    take: 10,
                    orderBy: { createdAt: 'desc' },
                },
                missionsAsTalent: {
                    take: 10,
                    orderBy: { createdAt: 'desc' },
                },
                _count: {
                    select: {
                        bookingsAsClient: true,
                        bookingsAsProvider: true,
                        missionsAsClient: true,
                        missionsAsTalent: true,
                        transactions: true,
                    },
                },
            },
        });

        if (!user) {
            throw new NotFoundException(`Utilisateur ${userId} non trouvé`);
        }

        return user;
    }

    /**
     * Vérifie un utilisateur (isVerified = true) + Log dans AuditLog
     */
    async validateUser(adminId: string, targetUserId: string) {
        const isAdmin = await this.isAdmin(adminId);
        if (!isAdmin) {
            throw new ForbiddenException('Seuls les administrateurs peuvent vérifier les utilisateurs');
        }

        // Vérifier que l'utilisateur existe
        const targetUser = await this.prisma.user.findUnique({ where: { id: targetUserId } });
        if (!targetUser) {
            throw new NotFoundException(`Utilisateur ${targetUserId} non trouvé`);
        }

        // Mise à jour de l'utilisateur
        const user = await this.prisma.user.update({
            where: { id: targetUserId },
            data: {
                isVerified: true,
                status: 'VERIFIED',
            },
        });

        // Log dans AuditLog
        await this.createAuditLog({
            adminId,
            action: 'VALIDATE_USER',
            targetUserId,
            metadata: { previousStatus: targetUser.status },
        });

        this.logger.log(`Utilisateur ${targetUserId} validé par ${adminId}`);

        return user;
    }

    /**
     * Alias pour compatibilité
     */
    async verifyUser(adminId: string, targetUserId: string) {
        return this.validateUser(adminId, targetUserId);
    }

    /**
     * Ajoute une note admin sur un utilisateur + Log
     */
    async addNote(adminId: string, targetUserId: string, content: string) {
        // Vérifier que l'admin est bien admin
        const isAdmin = await this.isAdmin(adminId);
        if (!isAdmin) {
            throw new ForbiddenException('Seuls les administrateurs peuvent ajouter des notes');
        }

        // Vérifier que l'utilisateur cible existe
        const targetUser = await this.prisma.user.findUnique({
            where: { id: targetUserId },
        });
        if (!targetUser) {
            throw new NotFoundException(`Utilisateur ${targetUserId} non trouvé`);
        }

        const note = await this.prisma.adminNote.create({
            data: {
                adminId,
                targetUserId,
                content,
            },
            include: {
                admin: {
                    select: { email: true, profile: { select: { firstName: true, lastName: true } } },
                },
            },
        });

        // Log dans AuditLog
        await this.createAuditLog({
            adminId,
            action: 'ADD_NOTE',
            targetUserId,
            resourceId: note.id,
            resourceType: 'AdminNote',
        });

        this.logger.log(`Note admin créée par ${adminId} sur ${targetUserId}`);

        return note;
    }

    /**
     * Alias pour compatibilité avec DTO
     */
    async createAdminNote(adminId: string, targetUserId: string, dto: CreateAdminNoteDto) {
        return this.addNote(adminId, targetUserId, dto.content);
    }

    /**
     * Récupère les notes d'un utilisateur
     */
    async getUserNotes(targetUserId: string) {
        return this.prisma.adminNote.findMany({
            where: { targetUserId },
            include: {
                admin: {
                    select: { email: true, profile: { select: { firstName: true, lastName: true } } },
                },
            },
            orderBy: { createdAt: 'desc' },
        });
    }

    /**
     * Met à jour le statut d'un document + Log
     */
    async updateDocumentStatus(adminId: string, documentId: string, status: string, comment?: string) {
        const isAdmin = await this.isAdmin(adminId);
        if (!isAdmin) {
            throw new ForbiddenException('Seuls les administrateurs peuvent valider les documents');
        }

        const document = await this.prisma.userDocument.update({
            where: { id: documentId },
            data: {
                status,
                comment,
                validatedAt: new Date(),
                validatedBy: adminId,
            },
        });

        const isIdentityDoc = this.isIdentityDocumentType(document.type);
        if (status === 'APPROVED' && isIdentityDoc) {
            await this.gamificationService.confirmReferralPointsForReferredUser(document.userId);
        }

        // Log dans AuditLog
        await this.createAuditLog({
            adminId,
            action: status === 'APPROVED' ? 'APPROVE_DOCUMENT' : 'REJECT_DOCUMENT',
            targetUserId: document.userId,
            resourceId: documentId,
            resourceType: 'UserDocument',
            metadata: { status, comment },
        });

        this.logger.log(`Document ${documentId} mis à jour: ${status}`);

        return document;
    }

    private isIdentityDocumentType(type: string): boolean {
        const normalized = String(type || '').toUpperCase();
        return normalized === 'ID_CARD' || normalized === 'IDENTITY' || normalized === 'CNI' || normalized === 'PASSPORT';
    }

    /**
     * Récupère l'historique d'audit
     */
    async getAuditLogs(filters?: { adminId?: string; targetUserId?: string; action?: string; page?: number; limit?: number }) {
        const { adminId, targetUserId, action, page = 1, limit = 50 } = filters || {};
        const skip = (page - 1) * limit;

        const where: any = {};
        if (adminId) where.adminId = adminId;
        if (targetUserId) where.targetUserId = targetUserId;
        if (action) where.action = action;

        const [logs, total] = await Promise.all([
            this.prisma.auditLog.findMany({
                where,
                skip,
                take: limit,
                include: {
                    admin: {
                        select: { email: true, profile: { select: { firstName: true, lastName: true } } },
                    },
                    targetUser: {
                        select: { email: true, profile: { select: { firstName: true, lastName: true } } },
                    },
                },
                orderBy: { createdAt: 'desc' },
            }),
            this.prisma.auditLog.count({ where }),
        ]);

        return {
            data: logs,
            meta: {
                total,
                page,
                limit,
                totalPages: Math.ceil(total / limit),
            },
        };
    }

    /**
     * Suspend un utilisateur
     */
    async suspendUser(adminId: string, targetUserId: string, reason?: string) {
        const isAdmin = await this.isAdmin(adminId);
        if (!isAdmin) {
            throw new ForbiddenException('Seuls les administrateurs peuvent suspendre les utilisateurs');
        }

        const user = await this.prisma.user.update({
            where: { id: targetUserId },
            data: { status: 'SUSPENDED' },
        });

        await this.createAuditLog({
            adminId,
            action: 'SUSPEND_USER',
            targetUserId,
            metadata: { reason },
        });

        this.logger.log(`Utilisateur ${targetUserId} suspendu par ${adminId}`);

        return user;
    }

    /**
     * Bannit un utilisateur
     */
    async banUser(adminId: string, targetUserId: string, reason?: string) {
        const isAdmin = await this.isAdmin(adminId);
        if (!isAdmin) {
            throw new ForbiddenException('Seuls les administrateurs peuvent bannir les utilisateurs');
        }

        const user = await this.prisma.user.update({
            where: { id: targetUserId },
            data: { status: 'BANNED' },
        });

        await this.createAuditLog({
            adminId,
            action: 'BAN_USER',
            targetUserId,
            metadata: { reason },
        });

        this.logger.log(`Utilisateur ${targetUserId} banni par ${adminId}`);

        return user;
    }

    /**
     * Met à jour les tags internes d'un utilisateur
     */
    async updateInternalTags(adminId: string, targetUserId: string, tags: string[]) {
        const isAdmin = await this.isAdmin(adminId);
        if (!isAdmin) {
            throw new ForbiddenException('Seuls les administrateurs peuvent modifier les tags');
        }

        const user = await this.prisma.user.update({
            where: { id: targetUserId },
            data: { internalTags: tags },
        });

        await this.createAuditLog({
            adminId,
            action: 'UPDATE_TAGS',
            targetUserId,
            metadata: { tags },
        });

        return user;
    }

    // ===========================================
    // DASHBOARD STATS
    // ===========================================

    /**
     * Récupère les statistiques pour le dashboard admin
     */
    async getDashboardStats() {
        const now = new Date();
        const startOfWeek = new Date(now.getFullYear(), now.getMonth(), now.getDate() - now.getDay());
        const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);

        const [userStats, documentStats, missionStats, financeStats] = await Promise.all([
            // User stats
            this.prisma.user.groupBy({
                by: ['role', 'status'],
                _count: true,
            }),
            // Document stats
            Promise.all([
                this.prisma.userDocument.count({ where: { status: 'PENDING' } }),
                this.prisma.userDocument.count({ where: { status: 'APPROVED', validatedAt: { gte: startOfWeek } } }),
                this.prisma.userDocument.count({ where: { status: 'REJECTED', validatedAt: { gte: startOfWeek } } }),
            ]),
            // Mission stats
            Promise.all([
                this.prisma.reliefMission.count({ where: { status: { in: ['OPEN', 'ASSIGNED', 'IN_PROGRESS'] } } }),
                this.prisma.reliefMission.count({ where: { status: 'COMPLETED', completedAt: { gte: startOfMonth } } }),
                this.prisma.contract.count({ where: { status: 'PENDING' } }), // Litiges = contrats non signés
            ]),
            // Finance stats
            Promise.all([
                this.prisma.transaction.aggregate({
                    where: { status: 'COMPLETED', createdAt: { gte: startOfMonth } },
                    _sum: { amount: true },
                }),
                this.prisma.transaction.aggregate({
                    where: { type: 'PLATFORM_FEE', status: 'COMPLETED', createdAt: { gte: startOfMonth } },
                    _sum: { amount: true },
                }),
            ]),
        ]);

        // Process user stats
        let total = 0, talents = 0, clients = 0, pendingVerification = 0;
        userStats.forEach((stat: any) => {
            total += stat._count;
            if (stat.role === 'TALENT') talents += stat._count;
            if (stat.role === 'CLIENT') clients += stat._count;
            if (stat.status === 'PENDING') pendingVerification += stat._count;
        });

        // New users this week
        const newThisWeek = await this.prisma.user.count({
            where: { createdAt: { gte: startOfWeek } },
        });

        return {
            users: {
                total,
                talents,
                clients,
                pendingVerification,
                newThisWeek,
            },
            documents: {
                pending: documentStats[0],
                approvedThisWeek: documentStats[1],
                rejectedThisWeek: documentStats[2],
            },
            missions: {
                active: missionStats[0],
                completedThisMonth: missionStats[1],
                inDispute: missionStats[2],
            },
            finance: {
                revenueThisMonth: financeStats[0]._sum.amount || 0,
                commissionsThisMonth: financeStats[1]._sum.amount || 0,
                pendingPayouts: 0,
            },
        };
    }

    /**
     * Récupère l'activité récente
     */
    async getRecentActivity(limit = 10) {
        const activities: any[] = [];

        // Recent users
        const recentUsers = await this.prisma.user.findMany({
            take: 5,
            orderBy: { createdAt: 'desc' },
            include: { profile: { select: { firstName: true, lastName: true } } },
        });

        recentUsers.forEach(user => {
            const name = user.profile ? `${user.profile.firstName} ${user.profile.lastName}` : user.email;
            activities.push({
                id: `user-${user.id}`,
                type: 'USER_REGISTERED',
                message: `Nouvel inscrit : ${name}`,
                timestamp: user.createdAt.toISOString(),
                userId: user.id,
            });
        });

        // Recent documents
        const recentDocs = await this.prisma.userDocument.findMany({
            take: 5,
            orderBy: { createdAt: 'desc' },
            include: { user: { include: { profile: { select: { firstName: true, lastName: true } } } } },
        });

        recentDocs.forEach(doc => {
            const name = doc.user.profile ? `${doc.user.profile.firstName} ${doc.user.profile.lastName}` : doc.user.email;
            activities.push({
                id: `doc-${doc.id}`,
                type: 'DOCUMENT_UPLOADED',
                message: `Document uploadé par ${name}`,
                timestamp: doc.createdAt.toISOString(),
                userId: doc.userId,
            });
        });

        // Sort by timestamp and return top N
        return activities
            .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
            .slice(0, limit);
    }

    // ===========================================
    // DOCUMENTS (MODERATION)
    // ===========================================

    /**
     * Liste les documents avec filtres
     */
    async getDocuments(filters: { status?: string; userId?: string; page?: number; limit?: number } = {}) {
        const { status, userId, page = 1, limit = 20 } = filters;
        const skip = (page - 1) * limit;

        const where: any = {};
        if (status) where.status = status;
        if (userId) where.userId = userId;

        const [documents, total] = await Promise.all([
            this.prisma.userDocument.findMany({
                where,
                skip,
                take: limit,
                include: {
                    user: {
                        select: {
                            id: true,
                            email: true,
                            role: true,
                            profile: { select: { firstName: true, lastName: true, avatarUrl: true } },
                            establishment: { select: { name: true } },
                        },
                    },
                },
                orderBy: { createdAt: 'desc' },
            }),
            this.prisma.userDocument.count({ where }),
        ]);

        return {
            documents,
            meta: { total, page, limit, totalPages: Math.ceil(total / limit) },
        };
    }

    // ===========================================
    // MISSIONS
    // ===========================================

    /**
     * Liste les missions avec filtres
     */
    async getMissions(filters: { status?: string; urgency?: string; page?: number; limit?: number } = {}) {
        const { status, urgency, page = 1, limit = 20 } = filters;
        const skip = (page - 1) * limit;

        const where: any = {};
        if (status) where.status = status;
        if (urgency) where.urgencyLevel = urgency;

        const [missions, total] = await Promise.all([
            this.prisma.reliefMission.findMany({
                where,
                skip,
                take: limit,
                include: {
                    client: {
                        select: {
                            id: true,
                            email: true,
                            establishment: { select: { name: true, logoUrl: true } },
                        },
                    },
                    assignedTalent: {
                        select: {
                            id: true,
                            email: true,
                            profile: { select: { firstName: true, lastName: true, avatarUrl: true } },
                        },
                    },
                    contract: { select: { id: true, status: true } },
                    _count: { select: { applications: true } },
                },
                orderBy: [{ urgencyLevel: 'desc' }, { createdAt: 'desc' }],
            }),
            this.prisma.reliefMission.count({ where }),
        ]);

        return {
            missions,
            meta: { total, page, limit, totalPages: Math.ceil(total / limit) },
        };
    }

    /**
     * Détails d'une mission
     */
    async getMissionDetails(missionId: string) {
        const mission = await this.prisma.reliefMission.findUnique({
            where: { id: missionId },
            include: {
                client: {
                    include: {
                        establishment: true,
                        profile: true,
                    },
                },
                assignedTalent: {
                    include: { profile: true },
                },
                applications: {
                    include: {
                        talent: {
                            include: { profile: true },
                        },
                    },
                },
                contract: true,
                bookings: true,
            },
        });

        if (!mission) {
            throw new NotFoundException(`Mission ${missionId} non trouvée`);
        }

        return mission;
    }
}
