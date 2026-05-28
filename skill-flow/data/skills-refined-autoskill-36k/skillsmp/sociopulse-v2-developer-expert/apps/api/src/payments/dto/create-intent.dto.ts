import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import { IsNumber, IsString, IsOptional, IsObject } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateIntentDto {
    @ApiProperty({ description: 'Montant en centimes' })
    @IsNumber()
    @Type(() => Number)
    amount: number;

    @ApiProperty({ description: 'Devise, ex: EUR' })
    @IsString()
    currency: string;

    @ApiPropertyOptional({ description: 'Metadata libre' })
    @IsOptional()
    @IsObject()
    metadata?: Record<string, any>;
}
