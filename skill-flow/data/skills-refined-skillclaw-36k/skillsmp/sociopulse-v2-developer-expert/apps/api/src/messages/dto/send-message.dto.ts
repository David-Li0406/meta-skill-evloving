import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsString, IsNotEmpty, IsOptional } from 'class-validator';

export class SendMessageDto {
    @ApiProperty({ description: 'ID du destinataire' })
    @IsString()
    @IsNotEmpty()
    recipientId: string;

    @ApiProperty({ description: 'Contenu du message' })
    @IsString()
    @IsNotEmpty()
    content: string;

    @ApiPropertyOptional({ description: 'Mission associée pour verrouillage automatique' })
    @IsOptional()
    @IsString()
    missionId?: string;
}
