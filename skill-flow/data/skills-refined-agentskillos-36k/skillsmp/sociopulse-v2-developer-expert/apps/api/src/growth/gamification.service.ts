import { BadRequestException, Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { PointLogStatus } from '@prisma/client';
import { PointActionType } from './dto';

type AwardPointsResult = {
    awarded: boolean;
    amount: number;
    status: PointLogStatus;
    points: number;
    pendingPoints: number;
};

@Injectable()
export class GamificationService {
    private readonly logger = new Logger(GamificationService.name);

    constructor(private readonly prisma: PrismaService) {}

    async awardPoints(userId: string, action: PointActionType, referenceId?: string): Promise<AwardPointsResult> {
        const resolvedReferenceId = referenceId?.trim() || action;

        if (action === PointActionType.PROFILE_PHOTO) {
            const profile = await this.prisma.profile.findUnique({
                where: { userId },
                select: { avatarUrl: true },
            });

            if (!profile?.avatarUrl) {
                throw new BadRequestException('Ajoutez une photo de profil avant de valider cette quête.');
            }
        }

        const awardAmount = this.getPointsAmount(action);
        const status: PointLogStatus = PointLogStatus.CONFIRMED;

        const result = await this.prisma.$transaction(async (tx) => {
            const existing = await tx.pointLog.findUnique({
                where: {
                    userId_action_referenceId: {
                        userId,
                        action,
                        referenceId: resolvedReferenceId,
                    },
                },
            });

            if (existing) {
                const [user, pending] = await Promise.all([
                    tx.user.findUnique({ where: { id: userId }, select: { points: true } }),
                    tx.pointLog.aggregate({
                        where: { userId, status: PointLogStatus.PENDING },
                        _sum: { amount: true },
                    }),
                ]);

                return {
                    awarded: false,
                    points: user?.points ?? 0,
                    pendingPoints: pending._sum.amount ?? 0,
                };
            }

            await tx.pointLog.create({
                data: {
                    userId,
                    action,
                    referenceId: resolvedReferenceId,
                    amount: awardAmount,
                    status,
                    confirmedAt: status === PointLogStatus.CONFIRMED ? new Date() : null,
                },
            });

            const user = await tx.user.update({
                where: { id: userId },
                data: {
                    points: { increment: awardAmount },
                },
                select: { points: true },
            });

            const pending = await tx.pointLog.aggregate({
                where: { userId, status: PointLogStatus.PENDING },
                _sum: { amount: true },
            });

            return {
                awarded: true,
                points: user.points,
                pendingPoints: pending._sum.amount ?? 0,
            };
        });

        if (result.awarded) {
            this.logger.log(`Awarded ${awardAmount} points to ${userId} for ${action}`);
        }

        return {
            awarded: result.awarded,
            amount: awardAmount,
            status,
            points: result.points,
            pendingPoints: result.pendingPoints,
        };
    }

    async createPendingReferralPoints(referrerId: string, referredUserId: string): Promise<void> {
        const action = 'REFERRAL';
        const amount = 200;

        await this.prisma.pointLog.upsert({
            where: {
                userId_action_referenceId: {
                    userId: referrerId,
                    action,
                    referenceId: referredUserId,
                },
            },
            create: {
                userId: referrerId,
                action,
                referenceId: referredUserId,
                amount,
                status: PointLogStatus.PENDING,
            },
            update: {},
        });
    }

    async confirmReferralPointsForReferredUser(referredUserId: string): Promise<{ confirmed: boolean; referrerId?: string }> {
        const referred = await this.prisma.user.findUnique({
            where: { id: referredUserId },
            select: { referrerId: true },
        });

        if (!referred?.referrerId) return { confirmed: false };

        const referrerId = referred.referrerId;
        const action = 'REFERRAL';

        const confirmed = await this.prisma.$transaction(async (tx) => {
            const log = await tx.pointLog.findUnique({
                where: {
                    userId_action_referenceId: {
                        userId: referrerId,
                        action,
                        referenceId: referredUserId,
                    },
                },
            });

            if (!log) {
                await tx.pointLog.create({
                    data: {
                        userId: referrerId,
                        action,
                        referenceId: referredUserId,
                        amount: 200,
                        status: PointLogStatus.CONFIRMED,
                        confirmedAt: new Date(),
                    },
                });

                await tx.user.update({
                    where: { id: referrerId },
                    data: { points: { increment: 200 } },
                });

                return true;
            }

            if (log.status === PointLogStatus.CONFIRMED) return false;
            if (log.status !== PointLogStatus.PENDING) return false;

            await tx.pointLog.update({
                where: { id: log.id },
                data: { status: PointLogStatus.CONFIRMED, confirmedAt: new Date() },
            });

            await tx.user.update({
                where: { id: referrerId },
                data: { points: { increment: log.amount } },
            });

            return true;
        });

        if (confirmed) {
            this.logger.log(`Confirmed referral points for referrer ${referrerId} (referred ${referredUserId})`);
        }

        return { confirmed, referrerId };
    }

    private getPointsAmount(action: PointActionType): number {
        switch (action) {
            case PointActionType.PROFILE_PHOTO:
                return 50;
        }
    }
}

