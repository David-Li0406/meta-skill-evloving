import { ApiPropertyOptional } from '@nestjs/swagger';
import { IsOptional, IsUrl } from 'class-validator';

export class ConnectOnboardingDto {
    @ApiPropertyOptional({ description: 'URL de retour apres onboarding' })
    @IsOptional()
    @IsUrl()
    returnUrl?: string;

    @ApiPropertyOptional({ description: "URL de rafraichissement si l'onboarding est interrompu" })
    @IsOptional()
    @IsUrl()
    refreshUrl?: string;
}
