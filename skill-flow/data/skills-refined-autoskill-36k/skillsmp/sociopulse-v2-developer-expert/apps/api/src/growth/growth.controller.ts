import { Body, Controller, Get, Patch, Post, Query, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiResponse, ApiTags } from '@nestjs/swagger';
import { JwtAuthGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload } from '../common/decorators';
import { GrowthService } from './growth.service';
import { GamificationService } from './gamification.service';
import { AwardPointsDto, CompleteOnboardingDto, GetTagsDto, UpdateMyTagsDto, UpdateProfileLocationDto } from './dto';

@ApiTags('growth')
@Controller('growth')
export class GrowthController {
    constructor(
        private readonly growthService: GrowthService,
        private readonly gamificationService: GamificationService,
    ) {}

    @Get('tags')
    @ApiOperation({ summary: 'Lister les tags onboarding' })
    @ApiResponse({ status: 200, description: 'Liste des tags' })
    async listTags(@Query() query: GetTagsDto) {
        return this.growthService.listTags({
            category: query.category,
            search: query.search,
            limit: query.limit,
        });
    }

    @Get('me')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Résumé Growth (points, tags, parrainage)' })
    async getMySummary(@CurrentUser() user: CurrentUserPayload) {
        return this.growthService.getMySummary(user.id);
    }

    @Post('me/tags')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Mettre à jour mes tags onboarding' })
    async updateMyTags(@CurrentUser() user: CurrentUserPayload, @Body() body: UpdateMyTagsDto) {
        return this.growthService.updateMyTags(user.id, body.tagIds);
    }

    @Post('points/award')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Valider une quête et attribuer des points (idempotent)' })
    async awardPoints(@CurrentUser() user: CurrentUserPayload, @Body() body: AwardPointsDto) {
        return this.gamificationService.awardPoints(user.id, body.action, body.referenceId);
    }

    @Patch('me/location')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Mettre à jour la localisation du profil' })
    async updateLocation(@CurrentUser() user: CurrentUserPayload, @Body() body: UpdateProfileLocationDto) {
        return this.growthService.updateProfileLocation(user.id, body);
    }

    @Post('me/complete-onboarding')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Finaliser l\'onboarding et rediriger vers le dashboard' })
    async completeOnboarding(@CurrentUser() user: CurrentUserPayload, @Body() body: CompleteOnboardingDto) {
        return this.growthService.completeOnboarding(user.id, body);
    }
}

