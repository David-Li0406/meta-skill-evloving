/**
 * =============================================================================
 * SEED INTERCEPTION GUARD - Scarcity Feed Algorithm (Pre-Launch FOMO Strategy)
 * =============================================================================
 * 
 * PURPOSE: Create "Full Visibility, Zero Availability" experience
 * + TRACK every "Fake Door Hit" for investor presentations
 * 
 * METRICS TRACKED:
 * - Who tried to interact (user ID, role, email)
 * - What they tried to interact with (seed talent/mission)
 * - Estimated value of the blocked interaction
 * - Geographic distribution (city)
 * - Time patterns (when do users try to convert?)
 * 
 * USAGE:
 * @UseGuards(JwtAuthGuard, SeedInterceptionGuard)
 * @SeedAction('CONTACT_TALENT')  // or 'APPLY_MISSION', 'BOOK_SERVICE'
 * async myEndpoint() { }
 */

import {
    Injectable,
    CanActivate,
    ExecutionContext,
    ForbiddenException,
    Logger,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { PrismaService } from '../prisma/prisma.service';

// =============================================================================
// SEED ACTION TYPES
// =============================================================================

export type SeedActionType =
    | 'CONTACT_TALENT'   // Client trying to message a seed talent
    | 'APPLY_MISSION'    // Talent trying to apply to a seed mission
    | 'BOOK_SERVICE'     // Client trying to book a seed service
    | 'START_CHAT';      // Any user trying to start chat with seed user

// =============================================================================
// FOMO MESSAGES (Localized French)
// =============================================================================

const FOMO_MESSAGES: Record<SeedActionType, { code: string; message: string }> = {
    CONTACT_TALENT: {
        code: 'SEED_TALENT_BUSY',
        message: '⚠️ Ce talent est actuellement en mission longue durée. Ajoutez-le à vos favoris pour être notifié de son retour.',
    },
    APPLY_MISSION: {
        code: 'SEED_MISSION_FILLED',
        message: '❌ Trop tard ! Cette mission vient d\'être pourvue à l\'instant. Activez vos notifications pour être le premier la prochaine fois.',
    },
    BOOK_SERVICE: {
        code: 'SEED_SERVICE_UNAVAILABLE',
        message: '📅 Cet intervenant est complet pour les prochaines semaines. Inscrivez-vous sur la liste d\'attente !',
    },
    START_CHAT: {
        code: 'SEED_USER_UNAVAILABLE',
        message: '⏳ Cet utilisateur n\'est pas disponible actuellement. Explorez d\'autres profils sur la plateforme !',
    },
};

// =============================================================================
// ESTIMATED VALUES (For investor presentations - in EUR)
// =============================================================================

const ESTIMATED_VALUES: Record<SeedActionType, number> = {
    CONTACT_TALENT: 150,   // Average booking value
    APPLY_MISSION: 280,    // Average mission value (day rate)
    BOOK_SERVICE: 200,     // Average workshop booking
    START_CHAT: 50,        // Lower value - just inquiry
};

// =============================================================================
// DECORATOR KEY
// =============================================================================

export const SEED_ACTION_KEY = 'seedAction';

// =============================================================================
// TARGET INFO TYPE
// =============================================================================

interface TargetInfo {
    isSeed: boolean;
    targetName?: string;
    targetType?: string;
    city?: string;
    jobTitle?: string;
    hourlyRate?: number;
}

// =============================================================================
// SEED INTERCEPTION GUARD
// =============================================================================

@Injectable()
export class SeedInterceptionGuard implements CanActivate {
    private readonly logger = new Logger(SeedInterceptionGuard.name);

    constructor(
        private reflector: Reflector,
        private prisma: PrismaService,
    ) { }

    async canActivate(context: ExecutionContext): Promise<boolean> {
        const seedAction = this.reflector.getAllAndOverride<SeedActionType>(
            SEED_ACTION_KEY,
            [context.getHandler(), context.getClass()],
        );

        // No @SeedAction decorator = no interception needed
        if (!seedAction) {
            return true;
        }

        const request = context.switchToHttp().getRequest();
        const user = request.user;

        // Admin bypass - admins can interact with seed data for testing
        if (user?.role === 'ADMIN') {
            return true;
        }
        // Extract target IDs based on action type
        const targetId = this.extractTargetId(request, seedAction);
        if (!targetId) {
            return true; // No target = no interception
        }

        // Check if target is a seed account/mission + get rich metadata
        const targetInfo = await this.getTargetInfo(targetId, seedAction);

        if (targetInfo.isSeed) {
            const fomoResponse = FOMO_MESSAGES[seedAction];

            // 🎯 TRACK THE FAKE DOOR HIT - C'EST DE L'OR EN BARRE !
            await this.trackFakeDoorHit({
                user,
                request,
                seedAction,
                targetId,
                targetInfo,
                fomoMessage: fomoResponse.message,
            });

            throw new ForbiddenException({
                statusCode: 403,
                error: 'Seed Interception',
                code: fomoResponse.code,
                message: fomoResponse.message,
            });
        }

        return true;
    }

    /**
     * 🎯 TRACK FAKE DOOR HIT - Analytics for Investor Dashboard
     * This is GOLD for demonstrating product-market fit!
     */
    private async trackFakeDoorHit(data: {
        user: any;
        request: any;
        seedAction: SeedActionType;
        targetId: string;
        targetInfo: TargetInfo;
        fomoMessage: string;
    }): Promise<void> {
        try {
            const { user, request, seedAction, targetId, targetInfo, fomoMessage } = data;

            // Calculate estimated value
            let estimatedValue = ESTIMATED_VALUES[seedAction];
            if (targetInfo.hourlyRate) {
                // For missions, use actual hourly rate × 7h (average day)
                estimatedValue = targetInfo.hourlyRate * 7;
            }

            // Extract request metadata
            const userAgent = request.headers?.['user-agent'] || null;
            const ipAddress = request.ip || request.headers?.['x-forwarded-for'] || null;
            const referer = request.headers?.['referer'] || null;

            // Map action to target type
            const targetTypeMap: Record<SeedActionType, string> = {
                CONTACT_TALENT: 'SEED_TALENT',
                START_CHAT: 'SEED_USER',
                APPLY_MISSION: 'SEED_MISSION',
                BOOK_SERVICE: 'SEED_SERVICE',
            };

            // 📊 PERSIST THE EVENT TO DATABASE
            await this.prisma.analyticsEvent.create({
                data: {
                    eventType: 'FAKE_DOOR_HIT',
                    eventAction: seedAction,
                    
                    // Actor (who tried to interact)
                    userId: user?.id || null,
                    userRole: user?.role || 'ANONYMOUS',
                    userEmail: user?.email || null,
                    
                    // Target (what they tried to interact with)
                    targetType: targetTypeMap[seedAction],
                    targetId,
                    targetName: targetInfo.targetName || null,
                    
                    // Context (geographic & job data)
                    city: targetInfo.city || null,
                    jobTitle: targetInfo.jobTitle || null,
                    
                    // Request metadata (for fraud detection & analytics)
                    userAgent,
                    ipAddress,
                    referer,
                    
                    // Business value indicators
                    estimatedValue,
                    fomoMessage,
                },
            });

            // 📝 LOG FOR REAL-TIME MONITORING (visible in server logs)
            this.logger.log(
                `🎯 FAKE_DOOR_HIT | ${seedAction} | ` +
                `User: ${user?.email || 'anonymous'} (${user?.role || 'N/A'}) | ` +
                `Target: ${targetInfo.targetName || targetId} | ` +
                `Est. Value: ${estimatedValue}€ | ` +
                `City: ${targetInfo.city || 'unknown'}`
            );

        } catch (error) {
            // Don't fail the request if analytics fails - just log
            this.logger.error(`Failed to track fake door hit: ${error.message}`);
        }
    }

    /**
     * Extract target ID from request based on action type
     */
    private extractTargetId(request: any, action: SeedActionType): string | null {
        const { params, body } = request;

        switch (action) {
            case 'CONTACT_TALENT':
            case 'START_CHAT':
                // Check body.recipientId or params.userId
                return body?.recipientId || body?.talentId || params?.userId || params?.talentId || null;

            case 'APPLY_MISSION':
                // Check params.missionId or body.missionId
                return params?.missionId || body?.missionId || params?.id || null;

            case 'BOOK_SERVICE':
                // Check body.serviceId or params.serviceId
                return body?.serviceId || params?.serviceId || null;

            default:
                return null;
        }
    }

    /**
     * Get target info with rich metadata for analytics
     * Returns both isSeed status AND contextual data for investor reports
     */
    private async getTargetInfo(targetId: string, action: SeedActionType): Promise<TargetInfo> {
        try {
            switch (action) {
                case 'CONTACT_TALENT':
                case 'START_CHAT': {
                    const user = await this.prisma.user.findUnique({
                        where: { id: targetId },
                        select: {
                            isSeed: true,
                            profile: {
                                select: {
                                    firstName: true,
                                    lastName: true,
                                    city: true,
                                    headline: true,
                                    hourlyRate: true,
                                },
                            },
                        },
                    });
                    return {
                        isSeed: user?.isSeed ?? false,
                        targetName: user?.profile 
                            ? `${user.profile.firstName} ${user.profile.lastName}` 
                            : undefined,
                        targetType: 'SEED_TALENT',
                        city: user?.profile?.city || undefined,
                        jobTitle: user?.profile?.headline || undefined,
                        hourlyRate: user?.profile?.hourlyRate || undefined,
                    };
                }

                case 'APPLY_MISSION': {
                    const mission = await this.prisma.reliefMission.findUnique({
                        where: { id: targetId },
                        select: {
                            isSeed: true,
                            title: true,
                            jobTitle: true,
                            city: true,
                            hourlyRate: true,
                            client: {
                                select: {
                                    establishment: {
                                        select: { name: true },
                                    },
                                },
                            },
                        },
                    });
                    return {
                        isSeed: mission?.isSeed ?? false,
                        targetName: mission?.client?.establishment?.name 
                            ? `${mission.client.establishment.name} - ${mission.title}`
                            : mission?.title,
                        targetType: 'SEED_MISSION',
                        city: mission?.city || undefined,
                        jobTitle: mission?.jobTitle || undefined,
                        hourlyRate: mission?.hourlyRate || undefined,
                    };
                }

                case 'BOOK_SERVICE': {
                    const service = await this.prisma.service.findUnique({
                        where: { id: targetId },
                        select: {
                            name: true,
                            basePrice: true,
                            profile: {
                                select: {
                                    firstName: true,
                                    lastName: true,
                                    city: true,
                                    user: {
                                        select: { isSeed: true },
                                    },
                                },
                            },
                        },
                    });
                    return {
                        isSeed: service?.profile?.user?.isSeed ?? false,
                        targetName: service?.profile
                            ? `${service.profile.firstName} ${service.profile.lastName} - ${service.name}`
                            : service?.name,
                        targetType: 'SEED_SERVICE',
                        city: service?.profile?.city || undefined,
                        hourlyRate: service?.basePrice || undefined,
                    };
                }

                default:
                    return { isSeed: false };
            }
        } catch {
            return { isSeed: false };
        }
    }
}
