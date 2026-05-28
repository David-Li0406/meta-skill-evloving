import { IsOptional, IsString } from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';

export class StartMissionDto {
    @ApiPropertyOptional({ description: 'Optional note when starting the mission' })
    @IsOptional()
    @IsString()
    note?: string;
}
