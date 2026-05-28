import { Transform } from 'class-transformer';
import { IsArray, IsEnum, IsNumber, IsOptional, IsString, Max, Min } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { TagCategory } from '@prisma/client';

export enum PointActionType {
    PROFILE_PHOTO = 'PROFILE_PHOTO',
}

export class GetTagsDto {
    @ApiPropertyOptional({ enum: TagCategory })
    @IsOptional()
    @IsEnum(TagCategory)
    category?: TagCategory;

    @ApiPropertyOptional({ description: 'Recherche texte (name contains)' })
    @IsOptional()
    @IsString()
    search?: string;

    @ApiPropertyOptional({ default: 60 })
    @IsOptional()
    @IsNumber()
    @Min(1)
    @Max(200)
    @Transform(({ value }) => Number(value))
    limit?: number = 60;
}

export class UpdateMyTagsDto {
    @ApiProperty({ type: [String], description: 'IDs des tags sélectionnés' })
    @IsArray()
    @IsString({ each: true })
    tagIds: string[];
}

export class AwardPointsDto {
    @ApiProperty({ enum: PointActionType })
    @IsEnum(PointActionType)
    action: PointActionType;

    @ApiPropertyOptional({ description: 'Référence idempotence (optionnel)' })
    @IsOptional()
    @IsString()
    referenceId?: string;
}

export class UpdateProfileLocationDto {
    @ApiPropertyOptional({ example: 'Paris' })
    @IsOptional()
    @IsString()
    city?: string;

    @ApiPropertyOptional({ example: '75001' })
    @IsOptional()
    @IsString()
    postalCode?: string;
}

export class CompleteOnboardingDto {
    @ApiPropertyOptional({ example: 'Jean' })
    @IsOptional()
    @IsString()
    firstName?: string;

    @ApiPropertyOptional({ example: 'Dupont' })
    @IsOptional()
    @IsString()
    lastName?: string;

    @ApiPropertyOptional({ example: '+33612345678' })
    @IsOptional()
    @IsString()
    phone?: string;

    @ApiPropertyOptional({ example: 'Paris' })
    @IsOptional()
    @IsString()
    city?: string;

    @ApiPropertyOptional({ example: '75001' })
    @IsOptional()
    @IsString()
    postalCode?: string;
}

