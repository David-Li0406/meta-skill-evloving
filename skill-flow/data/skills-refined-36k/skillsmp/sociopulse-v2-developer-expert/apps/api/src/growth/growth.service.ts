import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { TagCategory, PointLogStatus } from '@prisma/client';
import { randomBytes } from 'crypto';

type GrowthSummary = {
    userId: string;
    points: number;
    pendingPoints: number;
    referralCode: string | null;
    tags: Array<{ id: string; name: string; category: TagCategory }>;
    profile: { avatarUrl: string | null; bio: string | null } | null;
    referrals: {
        pendingCount: number;
        confirmedCount: number;
    };
};

@Injectable()
export class GrowthService {
    constructor(private readonly prisma: PrismaService) {}

    async listTags(filters: { category?: TagCategory; search?: string; limit?: number }) {
        const { category, search, limit = 60 } = filters;

        return this.prisma.tag.findMany({
            where: {
                ...(category ? { category } : {}),
                ...(search
                    ? { name: { contains: search.trim(), mode: 'insensitive' } }
                    : {}),
            },
            orderBy: [{ category: 'asc' }, { name: 'asc' }],
            take: Math.min(Math.max(limit, 1), 200),
        });
    }

    async updateMyTags(userId: string, tagIds: string[]) {
        const uniqueIds = Array.from(new Set(tagIds.map((id) => id.trim()).filter(Boolean)));

        if (uniqueIds.length === 0) {
            return this.prisma.user.update({
                where: { id: userId },
                data: { tags: { set: [] } },
                select: { id: true },
            });
        }

        const tags = await this.prisma.tag.findMany({
            where: { id: { in: uniqueIds } },
            select: { id: true },
        });

        if (tags.length === 0) {
            throw new NotFoundException('Tags non trouvés');
        }

        return this.prisma.user.update({
            where: { id: userId },
            data: {
                tags: {
                    set: tags.map((tag) => ({ id: tag.id })),
                },
                onboardingStep: 2,
            },
            select: {
                id: true,
                tags: { select: { id: true, name: true, category: true } },
            },
        });
    }

    async getMySummary(userId: string): Promise<GrowthSummary> {
        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: {
                id: true,
                points: true,
                referralCode: true,
                tags: { select: { id: true, name: true, category: true } },
                profile: { select: { avatarUrl: true, bio: true } },
            },
        });

        if (!user) {
            throw new NotFoundException('Utilisateur non trouvé');
        }

        const referralCode = user.referralCode ?? (await this.ensureReferralCode(userId));

        const [pendingPointsAgg, referralPending, referralConfirmed] = await Promise.all([
            this.prisma.pointLog.aggregate({
                where: { userId, status: PointLogStatus.PENDING },
                _sum: { amount: true },
            }),
            this.prisma.pointLog.count({
                where: { userId, action: 'REFERRAL', status: PointLogStatus.PENDING },
            }),
            this.prisma.pointLog.count({
                where: { userId, action: 'REFERRAL', status: PointLogStatus.CONFIRMED },
            }),
        ]);

        return {
            userId: user.id,
            points: user.points,
            pendingPoints: pendingPointsAgg._sum.amount ?? 0,
            referralCode,
            tags: user.tags,
            profile: user.profile,
            referrals: {
                pendingCount: referralPending,
                confirmedCount: referralConfirmed,
            },
        };
    }

    private async ensureReferralCode(userId: string): Promise<string> {
        const existing = await this.prisma.user.findUnique({
            where: { id: userId },
            select: { referralCode: true },
        });

        if (existing?.referralCode) return existing.referralCode;

        for (let attempt = 0; attempt < 12; attempt += 1) {
            const code = this.generateReferralCode(8);
            try {
                const updated = await this.prisma.user.update({
                    where: { id: userId },
                    data: { referralCode: code },
                    select: { referralCode: true },
                });
                if (updated.referralCode) return updated.referralCode;
            } catch {
                // collision (unique), retry
            }
        }

        const fallback = this.generateReferralCode(12);
        const updated = await this.prisma.user.update({
            where: { id: userId },
            data: { referralCode: fallback },
            select: { referralCode: true },
        });
        return updated.referralCode ?? fallback;
    }

    private generateReferralCode(length: number): string {
        const bytes = randomBytes(Math.ceil((length * 3) / 4));
        return bytes.toString('base64url').slice(0, length);
    }

    /**
     * Update user profile location (city, postalCode)
     */
    async updateProfileLocation(userId: string, data: { city?: string; postalCode?: string }) {
        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: { profile: { select: { id: true } } },
        });

        if (!user) {
            throw new NotFoundException('Utilisateur non trouvé');
        }

        if (user.profile) {
            // Update existing profile
            return this.prisma.profile.update({
                where: { userId },
                data: {
                    city: data.city?.trim() || undefined,
                    postalCode: data.postalCode?.trim() || undefined,
                },
                select: { id: true, city: true, postalCode: true },
            });
        }

        // Profile doesn't exist, cannot update location without basic info
        throw new NotFoundException('Profil non trouvé. Créez d\'abord un profil.');
    }

    /**
     * Complete onboarding - update profile and mark user as onboarded
     */
    async completeOnboarding(
        userId: string,
        data: {
            firstName?: string;
            lastName?: string;
            phone?: string;
            city?: string;
            postalCode?: string;
        },
    ) {
        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: { 
                id: true, 
                role: true,
                profile: { select: { id: true } },
            },
        });

        if (!user) {
            throw new NotFoundException('Utilisateur non trouvé');
        }

        // Update phone on user if provided
        const userUpdate = data.phone
            ? this.prisma.user.update({
                  where: { id: userId },
                  data: { 
                      phone: data.phone.trim(),
                      onboardingStep: 99, // Mark as completed
                  },
              })
            : this.prisma.user.update({
                  where: { id: userId },
                  data: { onboardingStep: 99 },
              });

        // Profile update/create
        const profileData = {
            firstName: data.firstName?.trim() || 'Utilisateur',
            lastName: data.lastName?.trim() || '',
            city: data.city?.trim() || undefined,
            postalCode: data.postalCode?.trim() || undefined,
        };

        const profileUpsert = this.prisma.profile.upsert({
            where: { userId },
            create: {
                userId,
                ...profileData,
            },
            update: profileData,
        });

        const [updatedUser, updatedProfile] = await this.prisma.$transaction([
            userUpdate,
            profileUpsert,
        ]);

        return {
            userId: updatedUser.id,
            role: user.role,
            profile: {
                firstName: updatedProfile.firstName,
                lastName: updatedProfile.lastName,
                city: updatedProfile.city,
                postalCode: updatedProfile.postalCode,
            },
            onboardingCompleted: true,
        };
    }
}
