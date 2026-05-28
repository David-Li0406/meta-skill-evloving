import {
    Injectable,
    NotFoundException,
    InternalServerErrorException,
    Logger,
    BadRequestException,
} from '@nestjs/common';
import { Prisma, ComplianceStatus } from '@prisma/client';
import { PrismaService } from '../common/prisma/prisma.service';
import {
    FindCandidatesDto,
    CandidateResultDto,
    MatchingResultDto,
    CreateMissionDto,
    FindMatchingTalentsDto,
    MatchingTalentResultDto,
    MatchingTalentsResultDto,
} from './dto';
import { MailService } from '../common/mailer';

interface GeoPoint {
    latitude: number;
    longitude: number;
}

@Injectable()
export class MatchingEngineService {
    private readonly logger = new Logger(MatchingEngineService.name);

    constructor(
        private readonly prisma: PrismaService,
        private readonly mailService: MailService,
    ) { }

    /**
     * Create a relief mission (SOS Renfort)
     */
    async createMission(dto: CreateMissionDto, clientId: string) {
        try {
            const startDate = new Date(dto.startDate);
            const endDate = dto.endDate
                ? new Date(dto.endDate)
                : new Date(startDate.getTime() + 8 * 60 * 60 * 1000);

            const mission = await this.prisma.reliefMission.create({
                data: {
                    clientId,
                    title: dto.title || `Renfort - ${dto.jobTitle}`,
                    description: dto.description || '',
                    jobTitle: dto.jobTitle,
                    hourlyRate: dto.hourlyRate,
                    isNightShift: dto.isNightShift || false,
                    urgencyLevel: dto.urgencyLevel || 'HIGH',
                    startDate,
                    endDate,
                    city: dto.city,
                    postalCode: dto.postalCode,
                    address: dto.address || dto.city,
                    latitude: dto.latitude,
                    longitude: dto.longitude,
                    radiusKm: dto.radiusKm || 30,
                    requiredSkills: dto.requiredSkills || [],
                    requiredDiplomas: dto.requiredDiplomas || [],
                    status: 'OPEN',
                    // SOS Renfort - Granular Job Data
                    jobId: dto.jobId,
                    specialtiesTags: dto.specialtiesTags || [],
                    requiresCar: dto.requiresCar || false,
                    requiresNight: dto.requiresNight || dto.isNightShift || false,
                    requiresDiploma: dto.requiresDiploma ?? true,
                    serviceName: dto.serviceName,
                    targetPublic: dto.targetPublic,
                },
            });

            this.logger.log(`Mission created: ${mission.id} by client ${clientId}`);

            if (mission.urgencyLevel === 'CRITICAL') {
                const client = await this.prisma.user.findUnique({
                    where: { id: clientId },
                    select: { email: true },
                });

                await this.mailService.sendCriticalMissionAlert({
                    title: mission.title,
                    jobTitle: mission.jobTitle,
                    city: mission.city,
                    startDate: mission.startDate,
                    clientEmail: client?.email,
                });
            }

            return mission;
        } catch (error) {
            this.logger.error(`createMission failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la création de la mission');
        }
    }

    /**
     * Find candidates for a relief mission
     * Implements the matching algorithm with:
     * - Role filtering (TALENT only)
     * - Skills/diplomas matching
     * - Geographic distance calculation
     * - Availability verification
     */
    async findCandidates(
        missionId: string,
        options: FindCandidatesDto = {},
    ): Promise<MatchingResultDto> {
        const { skills = [], radiusKm, limit = 10 } = options;

        try {
            // 1. Get the mission details
            const mission = await this.prisma.reliefMission.findUnique({
                where: { id: missionId },
                select: {
                    id: true,
                    title: true,
                    latitude: true,
                    longitude: true,
                    radiusKm: true,
                    requiredSkills: true,
                    requiredDiplomas: true,
                    startDate: true,
                    isNightShift: true,
                },
            });

            if (!mission) {
                throw new NotFoundException(`Mission ${missionId} non trouvee`);
            }

            if (mission.latitude === null || mission.longitude === null) {
                throw new BadRequestException(
                    'La mission doit contenir des coordonnées GPS pour trouver des talents',
                );
            }

            this.logger.log(`Finding candidates for mission: ${mission.title}`);

            const searchRadius = radiusKm ?? mission.radiusKm ?? 30;
            const missionLocation: GeoPoint = {
                latitude: mission.latitude,
                longitude: mission.longitude,
            };
            const boundingBox = this.calculateBoundingBox(missionLocation, searchRadius);

            const missionSkills = ((mission.requiredSkills as string[]) || []).filter(Boolean);
            const requiredSkills = Array.from(
                new Set([...missionSkills, ...skills].filter(Boolean)),
            );
            const requiredDiplomas = (mission.requiredDiplomas as string[]) || [];

            const profileFilters: Prisma.ProfileWhereInput = {
                latitude: { gte: boundingBox.minLat, lte: boundingBox.maxLat },
                longitude: { gte: boundingBox.minLng, lte: boundingBox.maxLng },
            };

            const specialtiesFilters: Prisma.ProfileWhereInput[] = requiredSkills.map((skill) => ({
                specialties: { array_contains: skill },
            }));

            if (specialtiesFilters.length) {
                profileFilters.AND = specialtiesFilters;
            }

            const fetchSize = Math.max(limit * 3, limit);

            // 2. Fetch TALENT users filtered directly in DB
            const talents = await this.prisma.user.findMany({
                where: {
                    role: 'TALENT',
                    status: 'VERIFIED',
                    profile: {
                        is: profileFilters,
                    },
                },
                include: {
                    profile: {
                        include: {
                            availabilitySlots: true,
                        },
                    },
                },
                take: fetchSize,
            });

            // 3. Filter and score candidates
            const missionDate = mission.startDate;

            const candidates: CandidateResultDto[] = [];

            for (const talent of talents) {
                if (!talent.profile) continue;

                const profile = talent.profile;
                const profileLocation: GeoPoint = {
                    latitude: profile.latitude ?? 0,
                    longitude: profile.longitude ?? 0,
                };

                // a. Calculate geographic distance
                const distance = this.calculateDistance(missionLocation, profileLocation);

                // Skip if outside radius
                if (distance > searchRadius) {
                    continue;
                }

                // b. Check skills/specialties match
                const profileSpecialties = profile.specialties as string[] || [];
                const skillsMatch = this.calculateSkillsMatch(requiredSkills, profileSpecialties);

                // c. Check diplomas match
                const profileDiplomas = profile.diplomas as any[] || [];
                const diplomasMatch = this.calculateDiplomasMatch(requiredDiplomas, profileDiplomas);

                // d. Verify availability
                const isAvailable = this.checkAvailability(
                    profile.availabilitySlots,
                    missionDate,
                    mission.isNightShift,
                );

                // e. Calculate match score (0-100)
                const matchScore = this.calculateMatchScore({
                    distance,
                    maxDistance: searchRadius,
                    skillsMatch,
                    diplomasMatch,
                    isAvailable,
                    averageRating: profile.averageRating,
                    totalMissions: profile.totalMissions,
                });

                candidates.push({
                    id: profile.id,
                    userId: talent.id,
                    firstName: profile.firstName,
                    lastName: profile.lastName,
                    avatarUrl: profile.avatarUrl,
                    headline: profile.headline,
                    specialties: profileSpecialties,
                    diplomas: profileDiplomas,
                    hourlyRate: profile.hourlyRate,
                    averageRating: profile.averageRating,
                    totalMissions: profile.totalMissions,
                    distance: Math.round(distance * 10) / 10,
                    matchScore,
                    isAvailable,
                });
            }

            // 4. Sort by match score and limit results
            const sortedCandidates = candidates
                .sort((a, b) => b.matchScore - a.matchScore)
                .slice(0, limit);

            this.logger.log(
                `Found ${sortedCandidates.length} candidates for mission ${missionId}`,
            );

            return {
                candidates: sortedCandidates,
                totalFound: candidates.length,
                searchRadius,
                missionId,
            };
        } catch (error) {
            if (error instanceof NotFoundException || error instanceof BadRequestException) {
                throw error;
            }
            this.logger.error(`findCandidates failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException(
                'Erreur lors de la recherche de candidats',
            );
        }
    }

    /**
     * Calculate distance between two geographic points using Haversine formula
     * Returns distance in kilometers
     */
    private calculateBoundingBox(center: GeoPoint, radiusKm: number) {
        const earthRadiusKmPerDegree = 111;
        const latDelta = radiusKm / earthRadiusKmPerDegree;
        const safeCos = Math.max(Math.cos(this.toRad(center.latitude)), 0.0001);
        const lngDelta = radiusKm / (earthRadiusKmPerDegree * safeCos);

        return {
            minLat: Math.max(-90, center.latitude - latDelta),
            maxLat: Math.min(90, center.latitude + latDelta),
            minLng: Math.max(-180, center.longitude - lngDelta),
            maxLng: Math.min(180, center.longitude + lngDelta),
        };
    }

    private calculateDistance(point1: GeoPoint, point2: GeoPoint): number {
        // If no coordinates, return max distance
        if (
            point1.latitude === undefined ||
            point1.latitude === null ||
            point1.longitude === undefined ||
            point1.longitude === null ||
            point2.latitude === undefined ||
            point2.latitude === null ||
            point2.longitude === undefined ||
            point2.longitude === null
        ) {
            return Infinity;
        }

        const R = 6371; // Earth's radius in km
        const dLat = this.toRad(point2.latitude - point1.latitude);
        const dLon = this.toRad(point2.longitude - point1.longitude);

        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(this.toRad(point1.latitude)) *
            Math.cos(this.toRad(point2.latitude)) *
            Math.sin(dLon / 2) *
            Math.sin(dLon / 2);

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    private toRad(deg: number): number {
        return deg * (Math.PI / 180);
    }

    /**
     * Calculate skills match percentage
     */
    private calculateSkillsMatch(required: string[], available: string[]): number {
        if (required.length === 0) return 1; // No requirements = full match

        const requiredLower = required.map((s) => s.toLowerCase());
        const availableLower = available.map((s) => s.toLowerCase());

        const matches = requiredLower.filter((skill) =>
            availableLower.some(
                (avail) => avail.includes(skill) || skill.includes(avail),
            ),
        );

        return matches.length / required.length;
    }

    /**
     * Calculate diplomas match percentage
     */
    private calculateDiplomasMatch(required: string[], available: any[]): number {
        if (required.length === 0) return 1;

        const availableNames = available.map((d) => (d.name || '').toLowerCase());
        const requiredLower = required.map((d) => d.toLowerCase());

        const matches = requiredLower.filter((diploma) =>
            availableNames.some(
                (avail) => avail.includes(diploma) || diploma.includes(avail),
            ),
        );

        return matches.length / required.length;
    }

    /**
     * Check if candidate is available for the mission date/time
     */
    private checkAvailability(
        slots: any[],
        missionDate: Date,
        isNightShift: boolean,
    ): boolean {
        if (!slots || slots.length === 0) {
            // No slots defined = assume available
            return true;
        }

        const dayOfWeek = missionDate.getDay();

        // Find slots for this day
        const daySlots = slots.filter(
            (slot) => slot.isActive && slot.dayOfWeek === dayOfWeek,
        );

        if (daySlots.length === 0) {
            // Check for specific date slots
            const specificSlots = slots.filter(
                (slot) =>
                    slot.isActive &&
                    slot.specificDate &&
                    new Date(slot.specificDate).toDateString() === missionDate.toDateString(),
            );
            return specificSlots.length > 0;
        }

        // For night shifts, check if they have evening/night slots
        if (isNightShift) {
            return daySlots.some((slot) => {
                const startHour = parseInt(slot.startTime.split(':')[0], 10);
                return startHour >= 18 || startHour < 6;
            });
        }

        return true;
    }

    /**
     * Calculate overall match score (0-100)
     */
    private calculateMatchScore(params: {
        distance: number;
        maxDistance: number;
        skillsMatch: number;
        diplomasMatch: number;
        isAvailable: boolean;
        averageRating: number;
        totalMissions: number;
    }): number {
        const {
            distance,
            maxDistance,
            skillsMatch,
            diplomasMatch,
            isAvailable,
            averageRating,
            totalMissions,
        } = params;

        // Weights for each factor
        const weights = {
            distance: 0.2,
            skills: 0.25,
            diplomas: 0.25,
            availability: 0.15,
            rating: 0.1,
            experience: 0.05,
        };

        // Distance score (closer = higher)
        const distanceScore = Math.max(0, 1 - distance / maxDistance);

        // Availability score
        const availabilityScore = isAvailable ? 1 : 0.3;

        // Rating score (normalized to 0-1)
        const ratingScore = averageRating / 5;

        // Experience score (caps at 50 missions)
        const experienceScore = Math.min(totalMissions / 50, 1);

        // Calculate weighted score
        const score =
            distanceScore * weights.distance +
            skillsMatch * weights.skills +
            diplomasMatch * weights.diplomas +
            availabilityScore * weights.availability +
            ratingScore * weights.rating +
            experienceScore * weights.experience;

        return Math.round(score * 100);
    }

    // =========================================================================
    // SOS RENFORT - Find Matching Talents
    // =========================================================================

    /**
     * Find matching talents for a SOS mission based on:
     * - Job ID (exact match)
     * - Hard filters: driver license, diploma/ADELI validation
     * - Soft sort: specialties matching, rating, experience
     * 
     * @param dto - Search criteria from the SOS Wizard
     * @returns Sorted list of matching talents
     */
    async findMatchingTalents(dto: FindMatchingTalentsDto): Promise<MatchingTalentsResultDto> {
        const {
            jobId,
            specialties = [],
            requiresCar = false,
            requiresNight = false,
            requiresDiploma = true,
            city,
            postalCode,
            latitude,
            longitude,
            radiusKm = 30,
            limit = 20,
        } = dto;

        this.logger.log(`Finding matching talents for job: ${jobId}`);

        try {
            // =====================================================================
            // 1. Build base filter: Job ID match
            // =====================================================================
            const profileWhere: Prisma.ProfileWhereInput = {
                jobId: jobId,
            };

            // =====================================================================
            // 2. HARD FILTER: Driver License
            // If mission.requiresCar = true → Exclude talents without license
            // =====================================================================
            if (requiresCar) {
                profileWhere.hasDriverLicense = true;
            }

            // =====================================================================
            // 3. HARD FILTER: Diploma/ADELI Validation
            // If mission.requiresDiploma = true → Exclude non-validated talents
            // =====================================================================
            if (requiresDiploma) {
                profileWhere.complianceStatus = ComplianceStatus.VALIDATED;
            }

            // =====================================================================
            // 4. HARD FILTER: Night Shift Capability
            // If mission.requiresNight = true → Only talents who can do night
            // =====================================================================
            if (requiresNight) {
                profileWhere.canDoNightShift = true;
            }

            // =====================================================================
            // 5. Geographic bounding box (if coordinates provided)
            // =====================================================================
            let missionLocation: GeoPoint | null = null;
            if (latitude !== undefined && longitude !== undefined) {
                missionLocation = { latitude, longitude };
                const boundingBox = this.calculateBoundingBox(missionLocation, radiusKm);
                profileWhere.latitude = { gte: boundingBox.minLat, lte: boundingBox.maxLat };
                profileWhere.longitude = { gte: boundingBox.minLng, lte: boundingBox.maxLng };
            }

            // =====================================================================
            // 6. Fetch TALENT users from DB
            // =====================================================================
            const talents = await this.prisma.user.findMany({
                where: {
                    role: 'TALENT',
                    status: 'VERIFIED',
                    profile: {
                        is: profileWhere,
                    },
                },
                include: {
                    profile: true,
                },
                take: limit * 3, // Fetch more for scoring/filtering
            });

            this.logger.log(`Found ${talents.length} potential talents after hard filters`);

            // =====================================================================
            // 7. Score and sort candidates
            // =====================================================================
            const scoredTalents: MatchingTalentResultDto[] = [];

            for (const talent of talents) {
                if (!talent.profile) continue;

                const profile = talent.profile;

                // Calculate distance if coordinates available
                let distance: number | null = null;
                if (missionLocation && profile.latitude && profile.longitude) {
                    const profileLocation: GeoPoint = {
                        latitude: profile.latitude,
                        longitude: profile.longitude,
                    };
                    distance = this.calculateDistance(missionLocation, profileLocation);

                    // Skip if outside radius
                    if (distance > radiusKm) continue;
                }

                // Calculate specialties match
                const profileSpecialties = (profile.specialties as string[]) || [];
                const matchingSpecialtiesCount = this.countMatchingSpecialties(
                    specialties,
                    profileSpecialties,
                );

                // Calculate match score
                const matchScore = this.calculateSOSMatchScore({
                    matchingSpecialties: matchingSpecialtiesCount,
                    totalRequiredSpecialties: specialties.length,
                    distance,
                    maxDistance: radiusKm,
                    averageRating: profile.averageRating,
                    totalMissions: profile.totalMissions,
                });

                scoredTalents.push({
                    id: profile.id,
                    userId: talent.id,
                    firstName: profile.firstName,
                    lastName: profile.lastName,
                    avatarUrl: profile.avatarUrl,
                    headline: profile.headline,
                    jobId: profile.jobId,
                    specialties: profileSpecialties,
                    hourlyRate: profile.hourlyRate,
                    averageRating: profile.averageRating,
                    totalMissions: profile.totalMissions,
                    hasDriverLicense: profile.hasDriverLicense,
                    canDoNightShift: profile.canDoNightShift,
                    complianceStatus: profile.complianceStatus,
                    distance: distance !== null ? Math.round(distance * 10) / 10 : null,
                    matchScore,
                    matchingSpecialties: matchingSpecialtiesCount,
                });
            }

            // =====================================================================
            // 8. SOFT SORT: Rank by match score (specialties + rating + distance)
            // =====================================================================
            const sortedTalents = scoredTalents
                .sort((a, b) => b.matchScore - a.matchScore)
                .slice(0, limit);

            this.logger.log(
                `Returning ${sortedTalents.length} matching talents for job ${jobId}`,
            );

            return {
                talents: sortedTalents,
                totalFound: scoredTalents.length,
                searchRadius: radiusKm,
                filters: {
                    jobId,
                    requiresCar,
                    requiresNight,
                    requiresDiploma,
                    specialties,
                },
            };
        } catch (error) {
            this.logger.error(`findMatchingTalents failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException(
                'Erreur lors de la recherche de talents',
            );
        }
    }

    /**
     * Count matching specialties between required and available
     */
    private countMatchingSpecialties(required: string[], available: string[]): number {
        if (required.length === 0) return 0;

        const requiredLower = required.map((s) => s.toLowerCase().trim());
        const availableLower = available.map((s) => s.toLowerCase().trim());

        return requiredLower.filter((req) =>
            availableLower.some((avail) => avail.includes(req) || req.includes(avail)),
        ).length;
    }

    /**
     * Calculate SOS match score (0-100)
     * Prioritizes: specialties match > rating > distance > experience
     */
    private calculateSOSMatchScore(params: {
        matchingSpecialties: number;
        totalRequiredSpecialties: number;
        distance: number | null;
        maxDistance: number;
        averageRating: number;
        totalMissions: number;
    }): number {
        const {
            matchingSpecialties,
            totalRequiredSpecialties,
            distance,
            maxDistance,
            averageRating,
            totalMissions,
        } = params;

        // Weights for SOS matching (specialties more important)
        const weights = {
            specialties: 0.35,
            rating: 0.25,
            distance: 0.25,
            experience: 0.15,
        };

        // Specialties score
        const specialtiesScore =
            totalRequiredSpecialties > 0
                ? matchingSpecialties / totalRequiredSpecialties
                : 1; // No requirements = full score

        // Distance score (closer = higher)
        const distanceScore =
            distance !== null ? Math.max(0, 1 - distance / maxDistance) : 0.5;

        // Rating score (normalized to 0-1)
        const ratingScore = averageRating / 5;

        // Experience score (caps at 30 missions for SOS)
        const experienceScore = Math.min(totalMissions / 30, 1);

        // Calculate weighted score
        const score =
            specialtiesScore * weights.specialties +
            ratingScore * weights.rating +
            distanceScore * weights.distance +
            experienceScore * weights.experience;

        return Math.round(score * 100);
    }

    /**
     * Get mission details with current applications
     */
    async getMissionWithApplications(missionId: string) {
        try {
            const mission = await this.prisma.reliefMission.findUnique({
                where: { id: missionId },
                include: {
                    client: {
                        include: { establishment: true },
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
                        orderBy: { createdAt: 'desc' },
                    },
                },
            });

            if (!mission) {
                throw new NotFoundException(`Mission ${missionId} non trouvée`);
            }

            return mission;
        } catch (error) {
            if (error instanceof NotFoundException) {
                throw error;
            }
            this.logger.error(`getMissionWithApplications failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la récupération');
        }
    }

    /**
     * Apply to a mission
     */
    async applyToMission(
        missionId: string,
        talentId: string,
        coverLetter?: string,
        proposedRate?: number,
    ) {
        try {
            // Check mission exists and is open
            const mission = await this.prisma.reliefMission.findUnique({
                where: { id: missionId },
            });

            if (!mission) {
                throw new NotFoundException(`Mission ${missionId} non trouvée`);
            }

            if (mission.status !== 'OPEN') {
                throw new Error('Cette mission n\'accepte plus de candidatures');
            }

            // Check not already applied
            const existingApplication = await this.prisma.missionApplication.findUnique({
                where: {
                    missionId_talentId: { missionId, talentId },
                },
            });

            if (existingApplication) {
                throw new Error('Vous avez déjà postulé à cette mission');
            }

            // Create application
            const application = await this.prisma.missionApplication.create({
                data: {
                    missionId,
                    talentId,
                    coverLetter,
                    proposedRate,
                    status: 'PENDING',
                },
                include: {
                    mission: true,
                    talent: {
                        include: { profile: true },
                    },
                },
            });

            this.logger.log(`Application created for mission ${missionId} by talent ${talentId}`);

            return application;
        } catch (error) {
            this.logger.error(`applyToMission failed: ${error.message}`);
            throw error;
        }
    }
}
