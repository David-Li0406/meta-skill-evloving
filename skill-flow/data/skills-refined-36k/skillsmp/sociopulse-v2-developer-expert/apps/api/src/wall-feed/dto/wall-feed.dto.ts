import { IsString, IsEnum, IsOptional, IsNumber, IsArray, Min, Max, IsBoolean, Equals } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { Transform } from 'class-transformer';
import { PostCategory, ServiceType } from '@prisma/client';

export enum FeedItemType {
    POST = 'POST',
    MISSION = 'MISSION',
    SERVICE = 'SERVICE',
    ALL = 'ALL',
}

export enum AppMode {
    SOCIAL = 'SOCIAL',
    MEDICAL = 'MEDICAL',
}

// =============================================
// Pagination Response DTOs
// =============================================

export class FeedMetaDto {
    @ApiProperty({ description: 'Nombre total d\'items' })
    total: number;

    @ApiProperty({ description: 'Page actuelle (1-indexed)' })
    page: number;

    @ApiProperty({ description: 'Dernière page possible' })
    lastPage: number;

    @ApiProperty({ description: 'Y a-t-il une page suivante' })
    hasNextPage: boolean;
}

export class PaginatedFeedResponseDto {
    @ApiProperty({ description: 'Liste des items du feed', type: 'array' })
    data: any[];

    @ApiProperty({ description: 'Métadonnées de pagination', type: FeedMetaDto })
    meta: FeedMetaDto;
}

export class GetFeedDto {
    @ApiPropertyOptional({ enum: FeedItemType, default: FeedItemType.ALL })
    @IsOptional()
    @IsEnum(FeedItemType)
    type?: FeedItemType = FeedItemType.ALL;

    @ApiPropertyOptional({ description: 'Cursor (pagination cursor-based, base64 JSON)' })
    @IsOptional()
    @IsString()
    cursor?: string;

    @ApiPropertyOptional({ description: 'Filtrer par ville' })
    @IsOptional()
    @IsString()
    city?: string;

    @ApiPropertyOptional({ description: 'Filtrer par code postal (prefixe)' })
    @IsOptional()
    @IsString()
    postalCode?: string;

    @ApiPropertyOptional({ description: 'Filtrer par tags' })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    @Transform(({ value }) => (typeof value === 'string' ? [value] : value))
    tags?: string[];

    @ApiPropertyOptional({ description: 'Recherche texte' })
    @IsOptional()
    @IsString()
    search?: string;

    @ApiPropertyOptional({ description: 'Filtrer par categorie' })
    @IsOptional()
    @IsString()
    category?: string;

    @ApiPropertyOptional({ description: 'Latitude pour recherche geo' })
    @IsOptional()
    @IsNumber()
    latitude?: number;

    @ApiPropertyOptional({ description: 'Longitude pour recherche geo' })
    @IsOptional()
    @IsNumber()
    longitude?: number;

    @ApiPropertyOptional({ description: 'Rayon en km', default: 50 })
    @IsOptional()
    @IsNumber()
    @Min(1)
    @Max(200)
    radiusKm?: number = 50;

    @ApiPropertyOptional({ description: 'Page (legacy offset pagination, ignorée si cursor présent)', default: 1 })
    @IsOptional()
    @IsNumber()
    @Min(1)
    page?: number = 1;

    @ApiPropertyOptional({ description: 'Limite par page', default: 20 })
    @IsOptional()
    @IsNumber()
    @Min(1)
    @Max(50)
    limit?: number = 20;

    @ApiPropertyOptional({
        enum: AppMode,
        description: 'Mode de l\'application (SOCIAL=SocioPulse, MEDICAL=MedicoPulse). Filtre les services par marque.',
        default: AppMode.SOCIAL
    })
    @IsOptional()
    @IsEnum(AppMode)
    appMode?: AppMode = AppMode.SOCIAL;
}

export class CreatePostDto {
    @ApiPropertyOptional()
    @IsOptional()
    @IsString()
    title?: string;

    @ApiPropertyOptional()
    @IsString()
    content: string;

    @ApiPropertyOptional()
    @IsOptional()
    @IsString()
    city?: string;

    @ApiPropertyOptional()
    @IsOptional()
    @IsString()
    postalCode?: string;

    @ApiPropertyOptional()
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    tags?: string[];

    @ApiPropertyOptional({ enum: PostCategory, description: 'Catégorie de post social' })
    @IsEnum(PostCategory)
    category: PostCategory;

    @ApiPropertyOptional({ type: [String], description: 'URLs des médias (images)' })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    mediaUrls?: string[];

    @ApiPropertyOptional({
        description: 'Obligatoire: certifie ne pas divulguer d’informations confidentielles ni de visages sans autorisation',
        default: false,
    })
    @IsBoolean()
    @Equals(true)
    ethicsConfirmed: boolean;
}

export class CreateServiceDto {
    @ApiPropertyOptional({ description: 'Nom du service' })
    @IsString()
    name: string;

    @ApiPropertyOptional({ description: 'Description courte (pour les cartes)' })
    @IsOptional()
    @IsString()
    shortDescription?: string;

    @ApiPropertyOptional({ description: 'Description détaillée' })
    @IsOptional()
    @IsString()
    description?: string;

    @ApiPropertyOptional({ enum: ServiceType, default: ServiceType.WORKSHOP })
    @IsOptional()
    @IsEnum(ServiceType)
    type?: ServiceType = ServiceType.WORKSHOP;

    @ApiPropertyOptional({ description: 'Catégorie (ex: Bien-être, Art-thérapie)' })
    @IsOptional()
    @IsString()
    category?: string;

    @ApiPropertyOptional({ description: 'Prix de base' })
    @IsOptional()
    @IsNumber()
    basePrice?: number;

    @ApiPropertyOptional({ description: 'Image principale (URL)' })
    @IsOptional()
    @IsString()
    imageUrl?: string;

    @ApiPropertyOptional({ type: [String], description: 'Tags (array)' })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    tags?: string[];

    @ApiPropertyOptional({ type: [String], description: 'Galerie d’images (URLs)' })
    @IsOptional()
    @IsArray()
    @IsString({ each: true })
    galleryUrls?: string[];
}

export class CreateBookingDto {
    @ApiProperty({ description: 'ID du service à réserver' })
    @IsString()
    serviceId: string;

    @ApiProperty({ description: 'Date de réservation (ISO format)' })
    @IsString()
    date: string;

    @ApiProperty({ description: 'Heure de début (format HH:MM)' })
    @IsString()
    startTime: string;

    @ApiProperty({ description: 'Durée en heures' })
    @IsNumber()
    @Min(1)
    duration: number;

    @ApiPropertyOptional({ description: 'Message optionnel' })
    @IsOptional()
    @IsString()
    message?: string;
}
