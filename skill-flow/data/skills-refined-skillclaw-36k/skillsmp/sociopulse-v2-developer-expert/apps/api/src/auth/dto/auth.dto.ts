import { IsEmail, IsString, MinLength, IsEnum, IsOptional, IsBoolean } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { UserRole } from '@sociopulse/types';

// Re-export UserRole for backward compatibility
export { UserRole } from '@sociopulse/types';

export class RegisterDto {
    @ApiProperty({ example: 'john.doe@example.com' })
    @IsEmail({}, { message: 'Email invalide' })
    email: string;

    @ApiProperty({ example: 'SecurePass123!' })
    @IsString()
    @MinLength(8, { message: 'Le mot de passe doit contenir au moins 8 caractères' })
    password: string;

    @ApiProperty({ enum: UserRole, example: UserRole.TALENT })
    @IsEnum(UserRole, { message: 'Rôle invalide' })
    role: UserRole;

    @ApiPropertyOptional({ example: '+33612345678' })
    @IsOptional()
    @IsString()
    phone?: string;

    @ApiPropertyOptional({ example: 'Jean' })
    @IsOptional()
    @IsString()
    firstName?: string;

    @ApiPropertyOptional({ example: 'Dupont' })
    @IsOptional()
    @IsString()
    lastName?: string;

    @ApiPropertyOptional({ enum: ['PARTICULAR', 'ESTABLISHMENT'], example: 'ESTABLISHMENT' })
    @IsOptional()
    @IsString()
    clientType?: 'PARTICULAR' | 'ESTABLISHMENT';

    @ApiPropertyOptional({ example: 'EHPAD Les Oliviers' })
    @IsOptional()
    @IsString()
    establishmentName?: string;

    @ApiPropertyOptional({ example: 'aB3kLm9_', description: 'Code parrain (optionnel)' })
    @IsOptional()
    @IsString()
    referrerCode?: string;

    @ApiPropertyOptional({ 
        example: false, 
        description: 'Enable cross-brand access (SocioPulse + MedicoPulse)' 
    })
    @IsOptional()
    @IsBoolean()
    enableCrossBrand?: boolean;
}

export class LoginDto {
    @ApiProperty({ example: 'john.doe@example.com' })
    @IsEmail({}, { message: 'Email invalide' })
    email: string;

    @ApiProperty({ example: 'SecurePass123!' })
    @IsString()
    password: string;
}

export class AuthResponseDto {
    @ApiProperty()
    accessToken: string;

    @ApiProperty()
    refreshToken: string;

    @ApiProperty()
    user: {
        id: string;
        email: string;
        role: UserRole;
        status: string;
    };
}

export class RefreshTokenDto {
    @ApiProperty()
    @IsString()
    refreshToken: string;
}
