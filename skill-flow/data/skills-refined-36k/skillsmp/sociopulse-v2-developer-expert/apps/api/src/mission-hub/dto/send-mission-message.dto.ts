import { IsString, MinLength, MaxLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class SendMissionMessageDto {
    @ApiProperty({ description: 'Message content', minLength: 1, maxLength: 2000 })
    @IsString()
    @MinLength(1, { message: 'Le message ne peut pas être vide' })
    @MaxLength(2000, { message: 'Le message est trop long (max 2000 caractères)' })
    content: string;
}
