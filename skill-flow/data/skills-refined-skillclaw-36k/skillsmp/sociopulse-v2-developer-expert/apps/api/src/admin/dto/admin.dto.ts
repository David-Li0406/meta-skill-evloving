import { IsString, IsNotEmpty, MinLength, IsOptional, IsArray } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateAdminNoteDto {
    @ApiProperty({ description: 'Contenu de la note', example: 'Excellent profil, à privilégier pour les missions urgentes.' })
    @IsString()
    @IsNotEmpty()
    @MinLength(3)
    content: string;
}

export class AdminNoteResponseDto {
    @ApiProperty()
    id: string;

    @ApiProperty()
    content: string;

    @ApiProperty()
    adminId: string;

    @ApiProperty()
    targetUserId: string;

    @ApiProperty()
    createdAt: Date;
}

export class UserListDto {
    @ApiProperty()
    id: string;

    @ApiProperty()
    email: string;

    @ApiProperty()
    role: string;

    @ApiProperty()
    status: string;

    @ApiProperty({ required: false })
    clientType?: string;

    @ApiProperty()
    isVerified: boolean;

    @ApiProperty()
    onboardingStep: number;

    @ApiProperty()
    createdAt: Date;

    @ApiProperty({ required: false })
    profile?: {
        firstName: string;
        lastName: string;
        avatarUrl?: string;
    };

    @ApiProperty({ required: false })
    establishment?: {
        name: string;
    };
}

export class SuspendUserDto {
    @ApiPropertyOptional({ description: 'Raison de la suspension' })
    @IsOptional()
    @IsString()
    reason?: string;
}

export class BanUserDto {
    @ApiPropertyOptional({ description: 'Raison du bannissement' })
    @IsOptional()
    @IsString()
    reason?: string;
}

export class UpdateTagsDto {
    @ApiProperty({ description: 'Liste des tags CRM internes', type: [String] })
    @IsArray()
    @IsString({ each: true })
    tags: string[];
}

export class UpdateDocStatusDto {
    @ApiProperty({ description: 'Nouveau statut du document (APPROVED, REJECTED)' })
    @IsString()
    status: string;

    @ApiPropertyOptional({ description: 'Commentaire (notamment pour les rejets)' })
    @IsOptional()
    @IsString()
    comment?: string;
}
