import { IsString, IsNumber, IsOptional, IsEnum, IsArray, Min, Max, IsBoolean } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';

export enum MissionUrgency {
    LOW = 'LOW',
    MEDIUM = 'MEDIUM',
    HIGH = 'HIGH',
    CRITICAL = 'CRITICAL',
}

export class FindCandidatesDto {
    @ApiPropertyOptional({ description: 'Filtrer par compétences requises' })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    skills?: string[];

    @ApiPropertyOptional({ description: 'Rayon de recherche en km', default: 30 })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @Min(1)
    @Max(200)
    radiusKm?: number;

    @ApiPropertyOptional({ description: 'Nombre maximum de candidats', default: 10 })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @Min(1)
    @Max(50)
    limit?: number;
}

// =============================================================================
// SOS RENFORT - Find Matching Talents DTO
// =============================================================================

export class FindMatchingTalentsDto {
    @ApiProperty({ description: 'Job ID from sos-config (e.g., "IDE", "ES")' })
    @IsString()
    jobId: string;

    @ApiPropertyOptional({ description: 'Specialties tags filter', type: [String] })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    specialties?: string[];

    @ApiPropertyOptional({ description: 'Require driver license', default: false })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    requiresCar?: boolean;

    @ApiPropertyOptional({ description: 'Night shift position', default: false })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    requiresNight?: boolean;

    @ApiPropertyOptional({ description: 'Require validated diploma/ADELI', default: true })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    requiresDiploma?: boolean;

    @ApiPropertyOptional({ description: 'City for geo filtering' })
    @IsOptional()
    @IsString()
    city?: string;

    @ApiPropertyOptional({ description: 'Postal code for geo filtering' })
    @IsOptional()
    @IsString()
    postalCode?: string;

    @ApiPropertyOptional({ description: 'Latitude for distance calculation' })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    latitude?: number;

    @ApiPropertyOptional({ description: 'Longitude for distance calculation' })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    longitude?: number;

    @ApiPropertyOptional({ description: 'Search radius in km', default: 30 })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @Min(1)
    @Max(200)
    radiusKm?: number;

    @ApiPropertyOptional({ description: 'Max results', default: 20 })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @Min(1)
    @Max(100)
    limit?: number;
}

export class MatchingTalentResultDto {
    @ApiProperty()
    id: string;

    @ApiProperty()
    userId: string;

    @ApiProperty()
    firstName: string;

    @ApiProperty()
    lastName: string;

    @ApiProperty()
    avatarUrl: string | null;

    @ApiProperty()
    headline: string | null;

    @ApiProperty()
    jobId: string | null;

    @ApiProperty()
    specialties: string[];

    @ApiProperty()
    hourlyRate: number | null;

    @ApiProperty()
    averageRating: number;

    @ApiProperty()
    totalMissions: number;

    @ApiProperty({ description: 'Has driver license' })
    hasDriverLicense: boolean;

    @ApiProperty({ description: 'Can do night shifts' })
    canDoNightShift: boolean;

    @ApiProperty({ description: 'Compliance status' })
    complianceStatus: string;

    @ApiProperty({ description: 'Distance from mission location in km' })
    distance: number | null;

    @ApiProperty({ description: 'Match score (0-100)' })
    matchScore: number;

    @ApiProperty({ description: 'Number of matching specialties' })
    matchingSpecialties: number;
}

export class MatchingTalentsResultDto {
    @ApiProperty({ type: [MatchingTalentResultDto] })
    talents: MatchingTalentResultDto[];

    @ApiProperty()
    totalFound: number;

    @ApiProperty()
    searchRadius: number;

    @ApiProperty({ description: 'Applied filters summary' })
    filters: {
        jobId: string;
        requiresCar: boolean;
        requiresNight: boolean;
        requiresDiploma: boolean;
        specialties: string[];
    };
}

export class CandidateResultDto {
    @ApiProperty()
    id: string;

    @ApiProperty()
    userId: string;

    @ApiProperty()
    firstName: string;

    @ApiProperty()
    lastName: string;

    @ApiProperty()
    avatarUrl: string | null;

    @ApiProperty()
    headline: string | null;

    @ApiProperty()
    specialties: string[];

    @ApiProperty()
    diplomas: any[];

    @ApiProperty()
    hourlyRate: number | null;

    @ApiProperty()
    averageRating: number;

    @ApiProperty()
    totalMissions: number;

    @ApiProperty({ description: 'Distance en km depuis la mission' })
    distance: number;

    @ApiProperty({ description: 'Score de matching (0-100)' })
    matchScore: number;

    @ApiProperty({ description: 'Disponibilité vérifiée' })
    isAvailable: boolean;
}

export class MatchingResultDto {
    @ApiProperty({ type: [CandidateResultDto] })
    candidates: CandidateResultDto[];

    @ApiProperty()
    totalFound: number;

    @ApiProperty()
    searchRadius: number;

    @ApiProperty()
    missionId: string;
}

export class CreateMissionDto {
    @ApiProperty({ description: 'Intitulé du poste' })
    @IsString()
    jobTitle: string;

    @ApiPropertyOptional({ description: 'Titre personnalisé de la mission' })
    @IsOptional()
    @IsString()
    title?: string;

    // ==========================================================================
    // SOS RENFORT - Granular Job Data
    // ==========================================================================

    @ApiPropertyOptional({ description: 'Job ID from sos-config (e.g., "IDE", "ES")' })
    @IsOptional()
    @IsString()
    jobId?: string;

    @ApiPropertyOptional({ description: 'Specialties tags', type: [String] })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    specialtiesTags?: string[];

    @ApiPropertyOptional({ description: 'Require driver license', default: false })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    requiresCar?: boolean;

    @ApiPropertyOptional({ description: 'Night shift required', default: false })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    requiresNight?: boolean;

    @ApiPropertyOptional({ description: 'Require validated diploma/ADELI', default: true })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    requiresDiploma?: boolean;

    @ApiPropertyOptional({ description: 'Service/Unit name (Medical)' })
    @IsOptional()
    @IsString()
    serviceName?: string;

    @ApiPropertyOptional({ description: 'Target public (Social)' })
    @IsOptional()
    @IsString()
    targetPublic?: string;

    // ==========================================================================

    @ApiProperty({ description: 'Taux horaire en EUR' })
    @IsNumber()
    @Type(() => Number)
    hourlyRate: number;

    @ApiPropertyOptional({ description: 'Mission de nuit', default: false })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    isNightShift?: boolean;

    @ApiProperty({ enum: MissionUrgency, default: MissionUrgency.HIGH })
    @IsEnum(MissionUrgency)
    urgencyLevel: MissionUrgency;

    @ApiPropertyOptional({ description: 'Description de la mission' })
    @IsOptional()
    @IsString()
    description?: string;

    @ApiProperty({ description: 'Date de début (ISO)' })
    @IsString()
    startDate: string;

    @ApiPropertyOptional({ description: 'Date de fin (ISO)' })
    @IsOptional()
    @IsString()
    endDate?: string;

    @ApiProperty({ description: 'Ville' })
    @IsString()
    city: string;

    @ApiProperty({ description: 'Code postal' })
    @IsString()
    postalCode: string;

    @ApiPropertyOptional({ description: 'Adresse complète' })
    @IsOptional()
    @IsString()
    address?: string;

    @ApiPropertyOptional({ description: 'Latitude' })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    latitude?: number;

    @ApiPropertyOptional({ description: 'Longitude' })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    longitude?: number;

    @ApiPropertyOptional({ description: 'Rayon de recherche', default: 30 })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    radiusKm?: number;

    @ApiPropertyOptional({ description: 'Compétences requises (legacy)', type: [String] })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    requiredSkills?: string[];

    @ApiPropertyOptional({ description: 'Diplômes requis (legacy)', type: [String] })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    requiredDiplomas?: string[];
}

export class ApplyMissionDto {
    @ApiPropertyOptional({ description: 'Lettre de motivation' })
    @IsOptional()
    @IsString()
    coverLetter?: string;

    @ApiPropertyOptional({ description: 'Taux horaire proposé (peut différer du taux mission)' })
    @IsOptional()
    @IsNumber()
    @Type(() => Number)
    @Min(0)
    proposedRate?: number;
}
