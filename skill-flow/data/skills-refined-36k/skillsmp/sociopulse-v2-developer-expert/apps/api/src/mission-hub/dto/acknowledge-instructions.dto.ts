import { IsOptional, IsBoolean } from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';

export class AcknowledgeInstructionsDto {
    @ApiPropertyOptional({ description: 'Optional confirmation flag' })
    @IsOptional()
    @IsBoolean()
    @Type(() => Boolean)
    confirmed?: boolean;
}
