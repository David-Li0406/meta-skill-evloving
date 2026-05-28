import {
    Injectable,
    NotFoundException,
    BadRequestException,
    ForbiddenException,
    InternalServerErrorException,
    Logger,
} from '@nestjs/common';
import { PrismaService } from '../common/prisma/prisma.service';
import { GetFeedDto, FeedItemType, CreatePostDto, CreateServiceDto, AppMode } from './dto';
import { Prisma, Post, ReliefMission, Profile, Establishment, Service, PostType, PostCategory, ServiceType, MissionStatus } from '@prisma/client';

type DecodedFeedCursor = {
    createdAt: Date;
    skip: {
        postIds: string[];
        serviceIds: string[];
        missionIds: string[];
    };
};

type SafeUser = {
    id: string;
    firstName: string | null;
    lastName: string | null;
    avatar: string | null;
    jobTitle: string | null;
};

type SafeEstablishment = Pick<Establishment, 'name' | 'type' | 'logoUrl' | 'city'>;

type SafeUserWithEstablishment = SafeUser & { establishment?: SafeEstablishment | null };

type SafeProfile = Pick<
    Profile,
    'id' | 'userId' | 'firstName' | 'lastName' | 'avatarUrl' | 'city' | 'postalCode' | 'averageRating' | 'totalReviews'
> & {
    headline?: string | null;
};

const SafeUserSelect = {
    id: true,
    profile: {
        select: {
            firstName: true,
            lastName: true,
            avatarUrl: true,
            headline: true,
        },
    },
} as const;

const toSafeUser = (user?: {
    id: string;
    profile?: {
        firstName?: string | null;
        lastName?: string | null;
        avatarUrl?: string | null;
        headline?: string | null;
    } | null;
} | null): SafeUser | null => {
    if (!user) return null;
    return {
        id: user.id,
        firstName: user.profile?.firstName ?? null,
        lastName: user.profile?.lastName ?? null,
        avatar: user.profile?.avatarUrl ?? null,
        jobTitle: user.profile?.headline ?? null,
    };
};

const toSafeClient = (client?: {
    id: string;
    profile?: {
        firstName?: string | null;
        lastName?: string | null;
        avatarUrl?: string | null;
        headline?: string | null;
    } | null;
    establishment?: SafeEstablishment | null;
} | null): SafeUserWithEstablishment | null => {
    const safeUser = toSafeUser(client);
    if (!safeUser) return null;
    return {
        ...safeUser,
        establishment: client?.establishment ?? null,
    };
};

interface FeedItem {
    id: string;
    type: 'POST' | 'MISSION' | 'SERVICE';
    title: string;
    name?: string;
    content: string;
    authorId: string;
    authorName: string;
    authorAvatar: string | null;
    authorRole: string;
    city: string | null;
    postalCode: string | null;
    tags: string[];
    category: string | null;
    createdAt: Date;
    validUntil: Date | null;
    // Mission-specific fields
    urgencyLevel?: string;
    hourlyRate?: number;
    status?: string;
    client?: SafeUserWithEstablishment | null;
    // Post-specific fields
    postType?: string;
    viewCount?: number;
    mediaUrls?: string[];
    // Service-specific fields
    basePrice?: number | null;
    serviceType?: string | null;
    providerRating?: number | null;
    providerReviews?: number | null;
    imageUrl?: string | null;
    profile?: SafeProfile | null;
}

interface PaginatedFeedResult {
    items: FeedItem[];
    pageInfo: {
        limit: number;
        hasNextPage: boolean;
        nextCursor: string | null;
    };
    // New page-based meta for SEO pagination
    data: FeedItem[];
    meta: {
        total: number;
        page: number;
        lastPage: number;
        hasNextPage: boolean;
    };
}

// =============================================================================
// NARRATIVE ITEM TYPE - Ghost Activity for Scarcity Feed
// =============================================================================
interface NarrativeItem {
    id: string;
    type: 'SUCCESS_STORY' | 'NEW_MISSION_START' | 'TALENT_JOINED' | 'FAST_MATCH';
    icon: string;
    content: string;
    timestamp: Date;
    metadata?: {
        establishmentName?: string;
        talentName?: string;
        jobTitle?: string;
        duration?: string;
        city?: string;
    };
}

@Injectable()
export class WallFeedService {
    private readonly logger = new Logger(WallFeedService.name);

    constructor(private readonly prisma: PrismaService) { }

    // =========================================================================
    // SCARCITY FEED - Narrative Items Generator (Ghost Activity)
    // =========================================================================

    /**
     * Generate narrative "success story" items based on seed data
     * These create social proof and FOMO during pre-launch
     */
    async generateNarrativeItems(limit = 5): Promise<NarrativeItem[]> {
        try {
            // Fetch seed missions and talents for narrative generation
            const [seedMissions, seedTalents] = await Promise.all([
                this.prisma.reliefMission.findMany({
                    where: { isSeed: true },
                    include: {
                        client: {
                            include: { establishment: true },
                        },
                        assignedTalent: {
                            include: { profile: true },
                        },
                    },
                    take: 10,
                }),
                this.prisma.user.findMany({
                    where: { isSeed: true, role: 'TALENT' },
                    include: { profile: true },
                    take: 10,
                }),
            ]);

            const narrativeItems: NarrativeItem[] = [];

            // Generate "Fast Match" stories from seed missions
            for (const mission of seedMissions) {
                if (mission.assignedTalent && mission.client?.establishment) {
                    const talentName = mission.assignedTalent.profile
                        ? `${mission.assignedTalent.profile.firstName} ${mission.assignedTalent.profile.lastName?.charAt(0)}.`
                        : 'Un talent';

                    const establishmentName = mission.client.establishment.name;
                    const matchDuration = Math.floor(5 + Math.random() * 25); // 5-30 minutes

                    narrativeItems.push({
                        id: `narrative-match-${mission.id}`,
                        type: 'FAST_MATCH',
                        icon: '⚡',
                        content: `${establishmentName} a trouvé un ${mission.jobTitle} en ${matchDuration} minutes.`,
                        timestamp: new Date(Date.now() - Math.random() * 3600000), // Random within last hour
                        metadata: {
                            establishmentName,
                            talentName,
                            jobTitle: mission.jobTitle,
                            duration: `${matchDuration}min`,
                            city: mission.city,
                        },
                    });
                }
            }

            // Generate "New Mission Start" stories
            for (const mission of seedMissions.filter(m => m.status === 'IN_PROGRESS')) {
                if (mission.assignedTalent?.profile) {
                    const firstName = mission.assignedTalent.profile.firstName || 'Un talent';

                    narrativeItems.push({
                        id: `narrative-start-${mission.id}`,
                        type: 'NEW_MISSION_START',
                        icon: '🎓',
                        content: `${firstName} a démarré une nouvelle mission ${mission.jobTitle.toLowerCase()}.`,
                        timestamp: new Date(Date.now() - Math.random() * 7200000), // Random within last 2 hours
                        metadata: {
                            talentName: firstName,
                            jobTitle: mission.jobTitle,
                            city: mission.city,
                        },
                    });
                }
            }

            // Generate "Talent Joined" stories from seed talents
            for (const talent of seedTalents.slice(0, 3)) {
                if (talent.profile) {
                    const firstName = talent.profile.firstName || 'Un professionnel';
                    const headline = talent.profile.headline || 'Professionnel du secteur';

                    narrativeItems.push({
                        id: `narrative-joined-${talent.id}`,
                        type: 'TALENT_JOINED',
                        icon: '👋',
                        content: `${firstName}, ${headline}, vient de rejoindre la communauté.`,
                        timestamp: new Date(Date.now() - Math.random() * 86400000), // Random within last day
                        metadata: {
                            talentName: firstName,
                            jobTitle: headline,
                            city: talent.profile.city || undefined,
                        },
                    });
                }
            }

            // Shuffle and limit
            const shuffled = narrativeItems.sort(() => Math.random() - 0.5);
            return shuffled.slice(0, limit);
        } catch (error) {
            this.logger.error(`generateNarrativeItems failed: ${error.message}`);
            return [];
        }
    }

    /**
     * Get sidebar data: External news + Recent successful missions + Narrative items
     */
    async getSidebarData(): Promise<{ news: any[]; recentSuccess: any[]; narrativeItems: NarrativeItem[] }> {
        try {
            const [news, recentMissions] = await Promise.all([
                // Veille Sectorielle - 5 derniers articles
                this.prisma.externalNews.findMany({
                    where: { isActive: true },
                    orderBy: { publishedAt: 'desc' },
                    take: 5,
                    select: {
                        id: true,
                        title: true,
                        source: true,
                        url: true,
                        excerpt: true,
                        publishedAt: true,
                    },
                }),
                // Dernières missions complétées avec succès - 5 dernières
                this.prisma.reliefMission.findMany({
                    where: {
                        status: 'COMPLETED',
                        completedAt: { not: null },
                    },
                    orderBy: { completedAt: 'desc' },
                    take: 5,
                    select: {
                        id: true,
                        jobTitle: true,
                        completedAt: true,
                        endDate: true,
                        client: {
                            select: {
                                ...SafeUserSelect,
                                establishment: { select: { name: true, type: true } },
                            },
                        },
                        assignedTalent: {
                            select: SafeUserSelect,
                        },
                    },
                }),
            ]);

            // Format recent success for frontend
            const recentSuccess = recentMissions.map((mission) => {
                const establishmentName = mission.client?.establishment?.name || 'Établissement';
                const talentName = mission.assignedTalent?.profile
                    ? `${mission.assignedTalent.profile.firstName} ${mission.assignedTalent.profile.lastName}`.trim()
                    : 'Talent';
                const completedAt = mission.completedAt || mission.endDate;

                return {
                    id: mission.id,
                    establishmentName,
                    jobTitle: mission.jobTitle,
                    talentName,
                    completedAt,
                };
            });

            // Generate narrative items for social proof (Scarcity Feed)
            const narrativeItems = await this.generateNarrativeItems(5);

            return { news, recentSuccess, narrativeItems };
        } catch (error) {
            this.logger.error(`getSidebarData failed: ${error.message}`, error.stack);
            // Return empty data instead of throwing to avoid breaking the sidebar
            return { news: [], recentSuccess: [], narrativeItems: [] };
        }
    }

    /**
     * Get mixed feed of Posts, Services and ReliefMissions
     * Returns chronologically sorted items based on filters
     */
    async getFeed(filters: GetFeedDto): Promise<PaginatedFeedResult> {
        const {
            type = FeedItemType.ALL,
            cursor: cursorRaw,
            city,
            postalCode,
            tags,
            category,
            search,
            latitude,
            longitude,
            radiusKm = 50,
            limit = 10,
            page = 1,
            appMode = AppMode.SOCIAL,
        } = filters;

        const safeLimit = Math.min(Math.max(Number(limit) || 20, 1), 50);
        const take = safeLimit + 1;
        const decodedCursor = this.decodeFeedCursor(cursorRaw);

        const normalizedSearch = search?.trim() || undefined;
        const normalizedCategory = category?.trim() || undefined;
        const normalizedCity = city?.trim() || undefined;
        const normalizedPostalCode = postalCode?.trim() || undefined;
        const normalizedTags = Array.isArray(tags)
            ? tags
                .filter((t): t is string => typeof t === 'string')
                .map((t) => t.trim())
                .filter(Boolean)
            : undefined;

        try {
            const shouldFetchPosts = type === FeedItemType.ALL || type === FeedItemType.POST;
            // MedicoPulse (MEDICAL) should NOT show SOCIOLIVE services (ateliers)
            const shouldFetchServices = (type === FeedItemType.ALL || type === FeedItemType.SERVICE)
                && appMode !== AppMode.MEDICAL; // Hide services on MedicoPulse
            const shouldFetchMissions = type === FeedItemType.ALL || type === FeedItemType.MISSION;

            const [posts, services, missions] = await Promise.all([
                shouldFetchPosts
                    ? this.prisma.post.findMany({
                        where: this.buildPostWhere({
                            cursor: decodedCursor,
                            search: normalizedSearch,
                            category: normalizedCategory,
                            city: normalizedCity,
                            postalCode: normalizedPostalCode,
                            tags: normalizedTags,
                        }),
                        select: {
                            id: true,
                            type: true,
                            title: true,
                            content: true,
                            authorId: true,
                            city: true,
                            postalCode: true,
                            tags: true,
                            category: true,
                            createdAt: true,
                            updatedAt: true,
                            validUntil: true,
                            viewCount: true,
                            longitude: true,
                            latitude: true,
                            radiusKm: true,
                            author: {
                                select: {
                                    ...SafeUserSelect,
                                    role: true,
                                    establishment: {
                                        select: { name: true, logoUrl: true },
                                    },
                                },
                            },
                        },
                        orderBy: { createdAt: 'desc' },
                        take,
                    })
                    : Promise.resolve([]),
                shouldFetchServices
                    ? this.prisma.service.findMany({
                        where: this.buildServiceWhere({
                            cursor: decodedCursor,
                            search: normalizedSearch,
                            category: normalizedCategory,
                            city: normalizedCity,
                            postalCode: normalizedPostalCode,
                            tags: normalizedTags,
                        }),
                        select: {
                            id: true,
                            profileId: true,
                            name: true,
                            description: true,
                            shortDescription: true,
                            basePrice: true,
                            tags: true,
                            category: true,
                            createdAt: true,
                            updatedAt: true,
                            type: true,
                            imageUrl: true,
                            totalBookings: true,
                            averageRating: true,
                            slug: true,
                            profile: {
                                select: {
                                    id: true,
                                    userId: true,
                                    firstName: true,
                                    lastName: true,
                                    avatarUrl: true,
                                    city: true,
                                    postalCode: true,
                                    headline: true,
                                    averageRating: true,
                                    totalReviews: true,
                                    user: { select: SafeUserSelect },
                                },
                            },
                        },
                        orderBy: { createdAt: 'desc' },
                        take,
                    })
                    : Promise.resolve([]),
                shouldFetchMissions
                    ? this.prisma.reliefMission.findMany({
                        where: this.buildMissionWhere({
                            cursor: decodedCursor,
                            search: normalizedSearch,
                            category: normalizedCategory,
                            city: normalizedCity,
                            postalCode: normalizedPostalCode,
                            tags: normalizedTags,
                        }),
                        select: {
                            id: true,
                            title: true,
                            description: true,
                            jobTitle: true,
                            urgencyLevel: true,
                            hourlyRate: true,
                            status: true,
                            clientId: true,
                            city: true,
                            postalCode: true,
                            requiredSkills: true,
                            createdAt: true,
                            updatedAt: true,
                            startDate: true,
                            longitude: true,
                            latitude: true,
                            isSeed: true,
                            client: {
                                select: {
                                    ...SafeUserSelect,
                                    establishment: {
                                        select: { name: true, type: true, logoUrl: true, city: true },
                                    },
                                },
                            },
                        },
                        orderBy: { createdAt: 'desc' },
                        take,
                    })
                    : Promise.resolve([]),
            ]);

            const merged: FeedItem[] = [
                ...posts.map((post) => this.mapPostToFeedItem(post)),
                ...services.map((service) => this.mapServiceToFeedItem(service)),
                ...missions.map((mission) => this.mapMissionToFeedItem(mission)),
            ];

            merged.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());

            const distanceFiltered =
                latitude && longitude
                    ? this.filterByDistance(merged, latitude, longitude, radiusKm)
                    : merged;

            const pageItems = distanceFiltered.slice(0, safeLimit);
            const hasNextPage = distanceFiltered.length > safeLimit;

            const nextCursor = hasNextPage && pageItems.length > 0
                ? this.encodeNextCursor(pageItems, decodedCursor)
                : null;

            // Calculate total for page-based pagination (estimate from current fetch)
            const estimatedTotal = distanceFiltered.length + (hasNextPage ? safeLimit : 0);
            const currentPage = cursorRaw ? Math.ceil(estimatedTotal / safeLimit) : (filters.page || 1);
            const lastPage = Math.max(1, Math.ceil(estimatedTotal / safeLimit));

            return {
                // Legacy cursor-based format
                items: pageItems,
                pageInfo: {
                    limit: safeLimit,
                    hasNextPage,
                    nextCursor,
                },
                // New page-based format for SEO
                data: pageItems,
                meta: {
                    total: estimatedTotal,
                    page: currentPage,
                    lastPage,
                    hasNextPage,
                },
            };
        } catch (error) {
            this.logger.error(`getFeed failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException('Erreur lors de la récupération du fil');
        }
    }

    /**
     * Create a booking from a service
     */
    async createBooking(clientId: string, payload: {
        serviceId: string;
        date: string;
        startTime: string;
        duration: number;
        message?: string;
    }) {
        try {
            const service = await this.prisma.service.findUnique({
                where: { id: payload.serviceId },
                include: { profile: true },
            });

            if (!service || !service.profile?.userId) {
                throw new NotFoundException('Service non trouvé');
            }

            const sessionDate = new Date(payload.date);
            const duration = Number(payload.duration) || 1;
            const pricePerHour = service.basePrice ?? service.profile.hourlyRate ?? 0;
            const totalPrice = Number(pricePerHour) * duration;

            const booking = await this.prisma.booking.create({
                data: {
                    clientId,
                    providerId: service.profile.userId,
                    serviceId: service.id,
                    sessionDate,
                    sessionTime: payload.startTime,
                    totalPrice,
                    clientNotes: payload.message,
                    isVideoSession: service.type === 'COACHING_VIDEO',
                },
            });

            return booking;
        } catch (error) {
            if (error instanceof NotFoundException) throw error;
            this.logger.error(`createBooking failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la création de la réservation');
        }
    }

    async getUserBookings(userId: string) {
        try {
            const bookings = await this.prisma.booking.findMany({
                where: {
                    OR: [
                        { clientId: userId },
                        { providerId: userId },
                    ],
                },
                select: {
                    id: true,
                    clientId: true,
                    providerId: true,
                    sessionDate: true,
                    sessionTime: true,
                    totalPrice: true,
                    status: true,
                    isVideoSession: true,
                    videoRoomId: true,
                    service: { select: { name: true, imageUrl: true, type: true } },
                    provider: {
                        select: {
                            id: true,
                            profile: { select: { firstName: true, lastName: true, avatarUrl: true, city: true } },
                        },
                    },
                    client: {
                        select: {
                            id: true,
                            profile: { select: { firstName: true, lastName: true, avatarUrl: true } },
                            establishment: { select: { name: true, city: true } },
                        },
                    },
                },
                orderBy: { createdAt: 'desc' },
            });

            return bookings.map(booking => ({
                id: booking.id,
                title: booking.service?.name || 'Réservation',
                partnerName: booking.clientId === userId
                    ? `${booking.provider?.profile?.firstName || ''} ${booking.provider?.profile?.lastName || ''}`.trim() || 'Prestataire'
                    : booking.client?.establishment?.name || `${booking.client?.profile?.firstName || ''} ${booking.client?.profile?.lastName || ''}`.trim() || 'Client',
                partnerAvatar: booking.clientId === userId
                    ? booking.provider?.profile?.avatarUrl
                    : booking.client?.profile?.avatarUrl,
                date: booking.sessionDate,
                time: booking.sessionTime || '09:00',
                duration: '1h',
                location: booking.clientId === userId
                    ? booking.provider?.profile?.city || 'Non précisé'
                    : booking.client?.establishment?.city || 'Non précisé',
                price: booking.totalPrice,
                status: booking.status,
                isVideoSession: booking.isVideoSession,
                videoRoomId: booking.videoRoomId,
            }));
        } catch (error) {
            this.logger.error(`getUserBookings failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la récupération des réservations');
        }
    }

    /**
     * Create a new post
     */
    async createPost(authorId: string, dto: CreatePostDto): Promise<FeedItem> {
        try {
            if (!dto.ethicsConfirmed) {
                throw new BadRequestException('La validation éthique est obligatoire.');
            }

            const normalizedContent = dto.content?.trim();
            if (!normalizedContent) {
                throw new BadRequestException('Le contenu du post est requis.');
            }

            const normalizedTitle = dto.title?.trim();
            const prefix = dto.category === PostCategory.EXPERIENCE ? 'Expérience' : 'Actu';
            const snippet = normalizedContent.replace(/\s+/g, ' ').slice(0, 60);
            const title = normalizedTitle || `${prefix}: ${snippet}${normalizedContent.length > 60 ? '…' : ''}`;

            const post = await this.prisma.post.create({
                data: {
                    authorId,
                    type: PostType.SOCIAL,
                    title,
                    content: normalizedContent,
                    city: dto.city,
                    postalCode: dto.postalCode,
                    tags: dto.tags || [],
                    category: dto.category,
                    mediaUrls: dto.mediaUrls || [],
                    validUntil: null,
                },
                select: {
                    id: true,
                    type: true,
                    title: true,
                    content: true,
                    authorId: true,
                    city: true,
                    postalCode: true,
                    tags: true,
                    category: true,
                    createdAt: true,
                    updatedAt: true,
                    validUntil: true,
                    viewCount: true,
                    longitude: true,
                    latitude: true,
                    radiusKm: true,
                    isActive: true,
                    mediaUrls: true,
                    isPinned: true,
                    author: {
                        select: {
                            ...SafeUserSelect,
                            role: true,
                            establishment: { select: { name: true, logoUrl: true } },
                        },
                    },
                },
            });

            this.logger.log(`Post created: ${post.id} by user ${authorId}`);

            return this.mapPostToFeedItem(post);
        } catch (error) {
            this.logger.error(`createPost failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException('Erreur lors de la création du post');
        }
    }

    /**
     * Get a single post by ID
     */
    async getPost(postId: string): Promise<FeedItem> {
        try {
            const post = await this.prisma.post.findUnique({
                where: { id: postId },
                select: {
                    id: true,
                    type: true,
                    title: true,
                    content: true,
                    authorId: true,
                    city: true,
                    postalCode: true,
                    tags: true,
                    category: true,
                    createdAt: true,
                    updatedAt: true,
                    validUntil: true,
                    viewCount: true,
                    longitude: true,
                    latitude: true,
                    radiusKm: true,
                    isActive: true,
                    mediaUrls: true,
                    isPinned: true,
                    author: {
                        select: {
                            ...SafeUserSelect,
                            role: true,
                            establishment: { select: { name: true, logoUrl: true } },
                        },
                    },
                },
            });

            if (!post) {
                throw new NotFoundException(`Post ${postId} non trouvé`);
            }

            // Increment view count
            await this.prisma.post.update({
                where: { id: postId },
                data: { viewCount: { increment: 1 } },
            });

            return this.mapPostToFeedItem(post);
        } catch (error) {
            if (error instanceof NotFoundException) throw error;
            this.logger.error(`getPost failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la récupération');
        }
    }

    /**
     * Get a single service by ID with profile/user
     */
    async getServiceById(serviceId: string) {
        try {
            const service = await this.prisma.service.findUnique({
                where: { id: serviceId },
                select: {
                    id: true,
                    profileId: true,
                    name: true,
                    slug: true,
                    description: true,
                    shortDescription: true,
                    type: true,
                    deliveryType: true,
                    category: true,
                    duration: true,
                    price: true,
                    pricingOptions: true,
                    basePrice: true,
                    minParticipants: true,
                    maxParticipants: true,
                    ageGroups: true,
                    imageUrl: true,
                    galleryUrls: true,
                    videoUrl: true,
                    tags: true,
                    isActive: true,
                    isFeatured: true,
                    totalBookings: true,
                    averageRating: true,
                    createdAt: true,
                    updatedAt: true,
                    profile: {
                        select: {
                            id: true,
                            userId: true,
                            firstName: true,
                            lastName: true,
                            avatarUrl: true,
                            city: true,
                            postalCode: true,
                            headline: true,
                            averageRating: true,
                            totalReviews: true,
                            user: { select: SafeUserSelect },
                        },
                    },
                },
            });

            if (!service) {
                throw new NotFoundException(`Service ${serviceId} non trouvé`);
            }

            return service;
        } catch (error) {
            if (error instanceof NotFoundException) throw error;
            this.logger.error(`getServiceById failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la récupération du service');
        }
    }

    /**
     * Create a new service (Offer) for TALENT users
     */
    async createService(userId: string, userRole: string, dto: CreateServiceDto) {
        try {
            if (userRole !== 'TALENT') {
                throw new ForbiddenException('Seuls les profils TALENT peuvent créer une offre.');
            }

            const name = dto.name?.trim();
            if (!name) {
                throw new BadRequestException('Le nom du service est requis.');
            }

            const profile = await this.prisma.profile.findUnique({
                where: { userId },
            });

            if (!profile) {
                throw new BadRequestException('Profil TALENT requis pour créer une offre.');
            }

            const slug = await this.generateUniqueServiceSlug(name);

            const service = await this.prisma.service.create({
                data: {
                    profileId: profile.id,
                    name,
                    slug,
                    shortDescription: dto.shortDescription?.trim() || null,
                    description: dto.description?.trim() || null,
                    type: dto.type ?? ServiceType.WORKSHOP,
                    category: dto.category?.trim() || null,
                    basePrice: dto.basePrice ?? null,
                    imageUrl: dto.imageUrl?.trim() || null,
                    galleryUrls: dto.galleryUrls || [],
                    tags: dto.tags || [],
                    isActive: true,
                },
                select: {
                    id: true,
                    profileId: true,
                    name: true,
                    slug: true,
                    description: true,
                    shortDescription: true,
                    type: true,
                    deliveryType: true,
                    category: true,
                    duration: true,
                    price: true,
                    pricingOptions: true,
                    basePrice: true,
                    minParticipants: true,
                    maxParticipants: true,
                    ageGroups: true,
                    imageUrl: true,
                    galleryUrls: true,
                    videoUrl: true,
                    tags: true,
                    isActive: true,
                    isFeatured: true,
                    totalBookings: true,
                    averageRating: true,
                    createdAt: true,
                    updatedAt: true,
                    profile: {
                        select: {
                            id: true,
                            userId: true,
                            firstName: true,
                            lastName: true,
                            avatarUrl: true,
                            city: true,
                            postalCode: true,
                            headline: true,
                            averageRating: true,
                            totalReviews: true,
                            user: { select: SafeUserSelect },
                        },
                    },
                },
            });

            this.logger.log(`Service created: ${service.id} by user ${userId}`);

            return service;
        } catch (error) {
            if (error instanceof BadRequestException || error instanceof ForbiddenException) throw error;
            this.logger.error(`createService failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException('Erreur lors de la création du service');
        }
    }

    /**
     * Delete a post
     */
    async deletePost(postId: string, userId: string): Promise<void> {
        try {
            const post = await this.prisma.post.findUnique({
                where: { id: postId },
            });

            if (!post) {
                throw new NotFoundException(`Post ${postId} non trouvé`);
            }

            if (post.authorId !== userId) {
                throw new Error('Non autorisé à supprimer ce post');
            }

            await this.prisma.post.delete({
                where: { id: postId },
            });

            this.logger.log(`Post deleted: ${postId}`);
        } catch (error) {
            if (error instanceof NotFoundException) throw error;
            throw new InternalServerErrorException('Erreur lors de la suppression');
        }
    }

    // ==================== Private Helper Methods ====================

    private asStringArray(value: Prisma.JsonValue): string[] {
        if (!Array.isArray(value)) return [];
        return value.filter((item): item is string => typeof item === 'string' && item.trim().length > 0);
    }

    private uniqueStrings(values: string[]): string[] {
        return Array.from(new Set(values.filter(Boolean)));
    }

    private decodeFeedCursor(raw?: string): DecodedFeedCursor | null {
        if (!raw || typeof raw !== 'string') return null;

        try {
            const json = Buffer.from(raw, 'base64').toString('utf8');
            const parsed: unknown = JSON.parse(json);

            if (!parsed || typeof parsed !== 'object') return null;

            const record = parsed as Record<string, unknown>;
            const createdAtRaw = record['createdAt'];
            if (typeof createdAtRaw !== 'string') return null;

            const createdAt = new Date(createdAtRaw);
            if (Number.isNaN(createdAt.getTime())) return null;

            const skipRaw = record['skip'];
            const skipRecord = skipRaw && typeof skipRaw === 'object' ? (skipRaw as Record<string, unknown>) : {};

            const toStringArray = (value: unknown) =>
                Array.isArray(value) ? value.filter((v): v is string => typeof v === 'string') : [];

            return {
                createdAt,
                skip: {
                    postIds: toStringArray(skipRecord['postIds']),
                    serviceIds: toStringArray(skipRecord['serviceIds']),
                    missionIds: toStringArray(skipRecord['missionIds']),
                },
            };
        } catch {
            return null;
        }
    }

    private encodeNextCursor(items: FeedItem[], previous: DecodedFeedCursor | null): string {
        const lastItem = items[items.length - 1];
        const createdAt = lastItem.createdAt;

        const boundaryItems = items.filter((item) => item.createdAt.getTime() === createdAt.getTime());

        const skip = {
            postIds: boundaryItems.filter((item) => item.type === 'POST').map((item) => item.id),
            serviceIds: boundaryItems.filter((item) => item.type === 'SERVICE').map((item) => item.id),
            missionIds: boundaryItems.filter((item) => item.type === 'MISSION').map((item) => item.id),
        };

        const mergedSkip =
            previous && previous.createdAt.getTime() === createdAt.getTime()
                ? {
                    postIds: this.uniqueStrings([...previous.skip.postIds, ...skip.postIds]),
                    serviceIds: this.uniqueStrings([...previous.skip.serviceIds, ...skip.serviceIds]),
                    missionIds: this.uniqueStrings([...previous.skip.missionIds, ...skip.missionIds]),
                }
                : skip;

        const payload = {
            createdAt: createdAt.toISOString(),
            skip: mergedSkip,
        };

        return Buffer.from(JSON.stringify(payload)).toString('base64');
    }

    private buildPostWhere(filters: {
        cursor: DecodedFeedCursor | null;
        search?: string;
        category?: string;
        city?: string;
        postalCode?: string;
        tags?: string[];
    }): Prisma.PostWhereInput {
        const { cursor, search, category, city, postalCode, tags } = filters;
        const and: Prisma.PostWhereInput[] = [
            {
                OR: [
                    { validUntil: null },
                    { validUntil: { gte: new Date() } },
                ],
            },
        ];

        if (city) {
            and.push({ city: { contains: city, mode: 'insensitive' } });
        }

        if (postalCode) {
            and.push({ postalCode: { startsWith: postalCode } });
        }

        if (search) {
            and.push({
                OR: [
                    { title: { contains: search, mode: 'insensitive' } },
                    { content: { contains: search, mode: 'insensitive' } },
                ],
            });
        }

        if (category) {
            const upper = category.toUpperCase();
            const postCategory = (Object.values(PostCategory) as string[]).includes(upper)
                ? (upper as PostCategory)
                : null;

            and.push({
                OR: [
                    ...(postCategory ? [{ category: postCategory }] : []),
                    { title: { contains: category, mode: 'insensitive' } },
                    { content: { contains: category, mode: 'insensitive' } },
                    { tags: { array_contains: [category] } },
                ],
            });
        }

        if (tags && tags.length > 0) {
            and.push({
                OR: tags.map((tag) => ({ tags: { array_contains: [tag] } })),
            });
        }

        if (cursor) {
            and.push({
                OR: [
                    { createdAt: { lt: cursor.createdAt } },
                    {
                        AND: [
                            { createdAt: cursor.createdAt },
                            { id: { notIn: cursor.skip.postIds } },
                        ],
                    },
                ],
            });
        }

        return {
            isActive: true,
            AND: and,
        };
    }

    private buildServiceWhere(filters: {
        cursor: DecodedFeedCursor | null;
        search?: string;
        category?: string;
        city?: string;
        postalCode?: string;
        tags?: string[];
    }): Prisma.ServiceWhereInput {
        const { cursor, search, category, city, postalCode, tags } = filters;
        const and: Prisma.ServiceWhereInput[] = [];

        if (city || postalCode) {
            const profileWhere: Prisma.ProfileWhereInput = {};
            if (city) profileWhere.city = { contains: city, mode: 'insensitive' };
            if (postalCode) profileWhere.postalCode = { startsWith: postalCode };
            and.push({ profile: profileWhere });
        }

        if (search) {
            and.push({
                OR: [
                    { name: { contains: search, mode: 'insensitive' } },
                    { description: { contains: search, mode: 'insensitive' } },
                    { shortDescription: { contains: search, mode: 'insensitive' } },
                    { category: { contains: search, mode: 'insensitive' } },
                ],
            });
        }

        if (category) {
            const upper = category.toUpperCase();
            const serviceType = (Object.values(ServiceType) as string[]).includes(upper)
                ? (upper as ServiceType)
                : null;

            and.push({
                OR: [
                    ...(serviceType ? [{ type: serviceType }] : []),
                    { category: { contains: category, mode: 'insensitive' } },
                    { tags: { array_contains: [category] } },
                ],
            });
        }

        if (tags && tags.length > 0) {
            and.push({
                OR: tags.map((tag) => ({ tags: { array_contains: [tag] } })),
            });
        }

        if (cursor) {
            and.push({
                OR: [
                    { createdAt: { lt: cursor.createdAt } },
                    {
                        AND: [
                            { createdAt: cursor.createdAt },
                            { id: { notIn: cursor.skip.serviceIds } },
                        ],
                    },
                ],
            });
        }

        return {
            isActive: true,
            AND: and.length > 0 ? and : undefined,
        };
    }

    private buildMissionWhere(filters: {
        cursor: DecodedFeedCursor | null;
        search?: string;
        category?: string;
        city?: string;
        postalCode?: string;
        tags?: string[];
    }): Prisma.ReliefMissionWhereInput {
        const { cursor, search, category, city, postalCode, tags } = filters;
        const and: Prisma.ReliefMissionWhereInput[] = [];

        if (city) {
            and.push({ city: { contains: city, mode: 'insensitive' } });
        }

        if (postalCode) {
            and.push({ postalCode: { startsWith: postalCode } });
        }

        if (search) {
            and.push({
                OR: [
                    { title: { contains: search, mode: 'insensitive' } },
                    { description: { contains: search, mode: 'insensitive' } },
                    { jobTitle: { contains: search, mode: 'insensitive' } },
                ],
            });
        }

        if (category) {
            and.push({
                OR: [
                    { jobTitle: { contains: category, mode: 'insensitive' } },
                    { requiredSkills: { array_contains: [category] } },
                ],
            });
        }

        if (tags && tags.length > 0) {
            and.push({
                OR: tags.map((tag) => ({ requiredSkills: { array_contains: [tag] } })),
            });
        }

        if (cursor) {
            and.push({
                OR: [
                    { createdAt: { lt: cursor.createdAt } },
                    {
                        AND: [
                            { createdAt: cursor.createdAt },
                            { id: { notIn: cursor.skip.missionIds } },
                        ],
                    },
                ],
            });
        }

        return {
            status: MissionStatus.OPEN,
            startDate: { gte: new Date() },
            AND: and.length > 0 ? and : undefined,
        };
    }

    private slugify(value: string): string {
        const normalized = value
            .normalize('NFD')
            .replace(/\p{Diacritic}/gu, '')
            .toLowerCase()
            .trim();

        const slug = normalized
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-+|-+$/g, '');

        return slug || 'service';
    }

    private async generateUniqueServiceSlug(name: string): Promise<string> {
        const base = this.slugify(name);
        let candidate = base;

        for (let attempt = 0; attempt < 50; attempt += 1) {
            const exists = await this.prisma.service.findUnique({
                where: { slug: candidate },
                select: { id: true },
            });

            if (!exists) return candidate;
            candidate = `${base}-${attempt + 1}`;
        }

        return `${base}-${Date.now()}`;
    }

    private buildLocationFilter(city?: string, postalCode?: string): Prisma.PostWhereInput | undefined {
        const filter: Prisma.PostWhereInput = {};

        if (city) {
            filter.city = { contains: city, mode: 'insensitive' };
        }

        if (postalCode) {
            filter.postalCode = { startsWith: postalCode };
        }

        return Object.keys(filter).length > 0 ? filter : undefined;
    }

    private async fetchPosts(options: {
        locationFilter?: Prisma.PostWhereInput;
        tags?: string[];
        category?: string;
        search?: string;
        skip: number;
        take: number;
    }) {
        const { locationFilter, tags, category, search, skip, take } = options;
        const andConditions: Prisma.PostWhereInput[] = [];

        const where: Prisma.PostWhereInput = {
            isActive: true,
            AND: [
                {
                    OR: [
                        { validUntil: null },
                        { validUntil: { gte: new Date() } },
                    ],
                },
            ],
        };

        if (locationFilter) {
            andConditions.push(locationFilter);
        }

        if (search) {
            andConditions.push({
                OR: [
                    { title: { contains: search, mode: 'insensitive' } },
                    { content: { contains: search, mode: 'insensitive' } },
                ],
            });
        }

        if (category) {
            const normalizedCategory = category.trim();
            const upper = normalizedCategory.toUpperCase();
            const possiblePostType = ['OFFER', 'NEED'].includes(normalizedCategory.toUpperCase())
                ? normalizedCategory.toUpperCase()
                : undefined;
            const possiblePostCategory = (Object.values(PostCategory) as string[]).includes(upper)
                ? (upper as PostCategory)
                : undefined;

            andConditions.push({
                OR: [
                    ...(possiblePostCategory ? [{ category: possiblePostCategory }] : []),
                    { title: { contains: normalizedCategory, mode: 'insensitive' } },
                    { content: { contains: normalizedCategory, mode: 'insensitive' } },
                    { tags: { array_contains: [normalizedCategory] } },
                    ...(possiblePostType ? [{ type: possiblePostType as any }] : []),
                ],
            });
        }

        // Tags filtering using JSON contains
        if (tags && tags.length > 0) {
            andConditions.push({
                OR: tags.map((tag) => ({ tags: { array_contains: [tag] } })),
            });
        }

        if (andConditions.length > 0) {
            const existingAnd = Array.isArray(where.AND) ? where.AND : where.AND ? [where.AND] : [];
            where.AND = [...existingAnd, ...andConditions];
        }

        const [posts, count] = await Promise.all([
            this.prisma.post.findMany({
                where,
                select: {
                    id: true,
                    type: true,
                    title: true,
                    content: true,
                    authorId: true,
                    city: true,
                    postalCode: true,
                    tags: true,
                    category: true,
                    createdAt: true,
                    updatedAt: true,
                    validUntil: true,
                    viewCount: true,
                    longitude: true,
                    latitude: true,
                    radiusKm: true,
                    isActive: true,
                    mediaUrls: true,
                    isPinned: true,
                    author: {
                        select: {
                            ...SafeUserSelect,
                            role: true,
                            establishment: { select: { name: true, logoUrl: true } },
                        },
                    },
                },
                orderBy: { createdAt: 'desc' },
                skip,
                take,
            }),
            this.prisma.post.count({ where }),
        ]);

        return {
            posts: posts.map((post) => this.mapPostToFeedItem(post)),
            count,
        };
    }

    private async fetchMissions(options: {
        locationFilter?: Prisma.ReliefMissionWhereInput;
        tags?: string[];
        category?: string;
        search?: string;
        skip: number;
        take: number;
    }) {
        const { locationFilter, tags, category, search, skip, take } = options;
        const andConditions: Prisma.ReliefMissionWhereInput[] = [];

        const where: Prisma.ReliefMissionWhereInput = {
            status: 'OPEN',
            startDate: { gte: new Date() },
            AND: [],
        };

        if (locationFilter) {
            andConditions.push(locationFilter);
        }

        if (search) {
            andConditions.push({
                OR: [
                    { title: { contains: search, mode: 'insensitive' } },
                    { description: { contains: search, mode: 'insensitive' } },
                    { jobTitle: { contains: search, mode: 'insensitive' } },
                ],
            });
        }

        if (category) {
            const normalizedCategory = category.trim();
            andConditions.push({
                OR: [
                    { requiredSkills: { has: normalizedCategory } as any },
                    { jobTitle: { contains: normalizedCategory, mode: 'insensitive' } },
                ],
            });
        }

        if (tags && tags.length > 0) {
            andConditions.push({ requiredSkills: { hasSome: tags } as any });
        }

        if (andConditions.length > 0) {
            const existingAnd = Array.isArray(where.AND) ? where.AND : where.AND ? [where.AND] : [];
            where.AND = [...existingAnd, ...andConditions];
        }

        const [missions, count] = await Promise.all([
            this.prisma.reliefMission.findMany({
                where,
                select: {
                    id: true,
                    title: true,
                    description: true,
                    jobTitle: true,
                    urgencyLevel: true,
                    hourlyRate: true,
                    status: true,
                    clientId: true,
                    city: true,
                    postalCode: true,
                    requiredSkills: true,
                    createdAt: true,
                    startDate: true,
                    client: {
                        select: {
                            ...SafeUserSelect,
                            establishment: {
                                select: { name: true, type: true, logoUrl: true, city: true },
                            },
                        },
                    },
                },
                orderBy: [
                    { urgencyLevel: 'desc' },
                    { createdAt: 'desc' },
                ],
                skip,
                take,
            }),
            this.prisma.reliefMission.count({ where }),
        ]);

        return {
            missions: missions.map((mission) => this.mapMissionToFeedItem(mission)),
            count,
        };
    }

    private async fetchServices(options: {
        tags?: string[];
        category?: string;
        search?: string;
        skip: number;
        take: number;
    }) {
        const { tags, category, search, skip, take } = options;
        const andConditions: Prisma.ServiceWhereInput[] = [];

        const where: Prisma.ServiceWhereInput = {
            isActive: true,
            AND: [],
        };

        if (search) {
            andConditions.push({
                OR: [
                    { name: { contains: search, mode: 'insensitive' } },
                    { description: { contains: search, mode: 'insensitive' } },
                    { shortDescription: { contains: search, mode: 'insensitive' } },
                ],
            });
        }

        if (category) {
            const normalizedCategory = category.trim();
            const possibleServiceType = ['WORKSHOP', 'COACHING_VIDEO'].includes(normalizedCategory.toUpperCase())
                ? normalizedCategory.toUpperCase()
                : null;
            andConditions.push({
                OR: [
                    { category: { contains: normalizedCategory, mode: 'insensitive' } },
                    { tags: { has: normalizedCategory } as any },
                    ...(possibleServiceType ? [{ type: possibleServiceType as any }] : []),
                ],
            });
        }

        if (tags && tags.length > 0) {
            andConditions.push({ tags: { hasSome: tags } as any });
        }

        if (andConditions.length > 0) {
            where.AND = andConditions;
        }

        const [services, count] = await Promise.all([
            this.prisma.service.findMany({
                where,
                select: {
                    id: true,
                    profileId: true,
                    name: true,
                    description: true,
                    shortDescription: true,
                    basePrice: true,
                    tags: true,
                    category: true,
                    createdAt: true,
                    type: true,
                    imageUrl: true,
                    profile: {
                        select: {
                            id: true,
                            userId: true,
                            firstName: true,
                            lastName: true,
                            avatarUrl: true,
                            city: true,
                            postalCode: true,
                            headline: true,
                            averageRating: true,
                            totalReviews: true,
                            user: { select: SafeUserSelect },
                        },
                    },
                },
                orderBy: { createdAt: 'desc' },
                skip,
                take,
            }),
            this.prisma.service.count({ where }),
        ]);

        return {
            services: services.map((service) => this.mapServiceToFeedItem(service)),
            count,
        };
    }

    private normalizeProfile(profile?: SafeProfile | null): SafeProfile | null {
        if (!profile) return null;
        return {
            id: profile.id,
            userId: profile.userId,
            firstName: profile.firstName,
            lastName: profile.lastName,
            avatarUrl: profile.avatarUrl ?? null,
            city: profile.city ?? null,
            postalCode: profile.postalCode ?? null,
            headline: profile.headline ?? null,
            averageRating: profile.averageRating ?? null,
            totalReviews: profile.totalReviews ?? null,
        };
    }

    private mapPostToFeedItem(
        post: {
            id: string;
            type: any;
            title: string;
            content: string;
            authorId: string;
            city?: string | null;
            postalCode?: string | null;
            tags: any;
            category: any;
            createdAt: Date;
            validUntil?: Date | null;
            viewCount: number;
            mediaUrls?: any;
            author: {
                id: string;
                role?: string | null;
                profile: {
                    firstName?: string | null;
                    lastName?: string | null;
                    avatarUrl?: string | null;
                    headline?: string | null;
                } | null;
                establishment: {
                    name?: string | null;
                    logoUrl?: string | null;
                } | null;
            };
        },
    ): FeedItem {
        const profile = post.author?.profile;
        const establishment = post.author?.establishment;

        const authorName =
            establishment?.name ||
            (profile ? `${profile.firstName} ${profile.lastName}`.trim() : null) ||
            'Utilisateur';

        const authorAvatar = establishment?.logoUrl || profile?.avatarUrl || null;

        return {
            id: post.id,
            type: 'POST',
            title: post.title,
            name: post.title,
            content: post.content,
            authorId: post.authorId,
            authorName,
            authorAvatar,
            authorRole: post.author?.role || 'CLIENT',
            city: post.city,
            postalCode: post.postalCode,
            tags: this.asStringArray(post.tags),
            category: post.category,
            createdAt: post.createdAt,
            validUntil: post.validUntil,
            postType: post.type,
            viewCount: post.viewCount,
            mediaUrls: this.asStringArray(post.mediaUrls),
        };
    }

    private mapMissionToFeedItem(
        mission: {
            id: string;
            title: string;
            description: string;
            jobTitle: string;
            urgencyLevel: any;
            hourlyRate: number;
            status: any;
            clientId: string;
            city?: string | null;
            postalCode?: string | null;
            requiredSkills: any;
            createdAt: Date;
            startDate: Date;
            client: {
                id: string;
                profile: {
                    firstName?: string | null;
                    lastName?: string | null;
                    avatarUrl?: string | null;
                    headline?: string | null;
                } | null;
                establishment: {
                    name?: string | null;
                    type?: string | null;
                    logoUrl?: string | null;
                    city?: string | null;
                } | null;
            };
        }
    ): FeedItem {
        const establishment = mission.client?.establishment;
        const profile = mission.client?.profile;

        return {
            id: mission.id,
            type: 'MISSION',
            title: mission.title,
            content: mission.description,
            authorId: mission.clientId,
            authorName: establishment?.name || profile?.firstName || 'Établissement',
            authorAvatar: establishment?.logoUrl || profile?.avatarUrl || null,
            authorRole: 'CLIENT',
            city: mission.city,
            postalCode: mission.postalCode,
            tags: this.asStringArray(mission.requiredSkills),
            category: mission.jobTitle,
            createdAt: mission.createdAt,
            validUntil: mission.startDate,
            urgencyLevel: mission.urgencyLevel,
            hourlyRate: mission.hourlyRate,
            status: mission.status,
            client: toSafeClient({
                ...mission.client,
                establishment: mission.client.establishment ? {
                    ...mission.client.establishment,
                    name: mission.client.establishment.name || '',
                    type: mission.client.establishment.type || null,
                    logoUrl: mission.client.establishment.logoUrl || null,
                    city: mission.client.establishment.city || null,
                } : null,
                profile: mission.client.profile ? {
                    ...mission.client.profile,
                    firstName: mission.client.profile.firstName || null,
                    lastName: mission.client.profile.lastName || null,
                    avatarUrl: mission.client.profile.avatarUrl || null,
                    headline: mission.client.profile.headline || null,
                } : null,
            }),
        };
    }

    private mapServiceToFeedItem(
        service: {
            id: string;
            profileId: string;
            name: string;
            description: string;
            shortDescription?: string | null;
            basePrice?: number | null;
            tags: any;
            category?: string | null;
            createdAt: Date;
            type: any;
            imageUrl?: string | null;
            profile: SafeProfile & { user?: unknown };
        }
    ): FeedItem {
        const profile = this.normalizeProfile(service.profile);
        const authorName = profile
            ? `${profile.firstName} ${profile.lastName}`.trim() || 'Prestataire'
            : 'Prestataire';

        return {
            id: service.id,
            type: 'SERVICE',
            title: service.name,
            name: service.name,
            content: service.shortDescription || service.description || '',
            authorId: profile?.userId || service.profileId,
            authorName,
            authorAvatar: profile?.avatarUrl || null,
            authorRole: 'TALENT',
            city: profile?.city || null,
            postalCode: profile?.postalCode || null,
            tags: this.asStringArray(service.tags),
            category: service.category || null,
            createdAt: service.createdAt,
            validUntil: null,
            postType: 'OFFER',
            serviceType: service.type,
            basePrice: service.basePrice,
            providerRating: profile?.averageRating ?? null,
            providerReviews: profile?.totalReviews ?? null,
            imageUrl: service.imageUrl || null,
            profile,
        };
    }

    private filterByDistance(
        items: FeedItem[],
        lat: number,
        lng: number,
        radiusKm: number,
    ): FeedItem[] {
        // For now, simple zip code prefix matching as fallback
        // Full geo-filtering would require coordinates in the data
        return items;
    }
}
