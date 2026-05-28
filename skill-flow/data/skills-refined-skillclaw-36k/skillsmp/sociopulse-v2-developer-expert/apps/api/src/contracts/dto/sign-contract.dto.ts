import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsString, IsNotEmpty, IsOptional } from 'class-validator';

export class SignContractDto {
    @ApiProperty({ description: 'ID de la mission concernée' })
    @IsString()
    @IsNotEmpty()
    missionId: string;

    @ApiProperty({ description: 'Signature en data URL ou URL vers la signature' })
    @IsString()
    @IsNotEmpty()
    signature: string;

    @ApiPropertyOptional({ description: 'Contenu du contrat (fallback si non existant)' })
    @IsOptional()
    @IsString()
    content?: string;
}
