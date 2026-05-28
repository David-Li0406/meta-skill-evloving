import { IsString, IsDateString, IsNumber, IsOptional, Min, Max } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateVideoSessionDto {
    @ApiProperty({ description: 'ID du booking associé' })
    @IsString()
    bookingId: string;

    @ApiPropertyOptional({ description: 'Durée en minutes', default: 60 })
    @IsOptional()
    @IsNumber()
    @Min(15)
    @Max(180)
    durationMinutes?: number;
}

export class VideoRoomDto {
    @ApiProperty()
    roomId: string;

    @ApiProperty()
    roomName: string;

    @ApiProperty()
    hostToken: string;

    @ApiProperty()
    participantToken: string;

    @ApiProperty()
    meetingUrl: string;

    @ApiProperty()
    expiresAt: Date;
}

export class JoinVideoSessionDto {
    @ApiProperty({ description: 'ID de la room vidéo' })
    @IsString()
    roomId: string;
}

export class VideoTokenDto {
    @ApiProperty()
    token: string;

    @ApiProperty()
    roomName: string;

    @ApiProperty()
    meetingUrl: string;
}

export class EndSessionDto {
    @ApiPropertyOptional({ description: 'URL de l\'enregistrement (si disponible)' })
    @IsOptional()
    @IsString()
    recordingUrl?: string;
}
