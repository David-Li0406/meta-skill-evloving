import {
    Controller,
    Get,
    Post,
    Body,
    Param,
    Query,
    UseGuards,
} from '@nestjs/common';
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
    ApiParam,
} from '@nestjs/swagger';
import { MatchingEngineService } from './matching-engine.service';
import {
    FindCandidatesDto,
    MatchingResultDto,
    CreateMissionDto,
    ApplyMissionDto,
    FindMatchingTalentsDto,
    MatchingTalentsResultDto,
} from './dto';
import { JwtAuthGuard, MissionAccessGuard, RolesGuard, SeedInterceptionGuard } from '../common/guards';
import { Roles, CurrentUser, CurrentUserPayload, SeedAction } from '../common/decorators';

@ApiTags('matching')
@Controller('matching')
export class MatchingEngineController {
    constructor(private readonly matchingService: MatchingEngineService) { }

    // =========================================================================
    // SOS RENFORT - Smart Matching
    // =========================================================================

    @Post('talents/search')
    @UseGuards(JwtAuthGuard, RolesGuard)
    @ApiBearerAuth()
    @Roles('CLIENT', 'ADMIN')
    @ApiOperation({
        summary: 'Find matching talents for SOS mission',
        description: `
        Smart matching algorithm:
        1. Filter by job ID (exact match)
        2. HARD FILTER: requiresCar → exclude talents without driver license
        3. HARD FILTER: requiresDiploma → exclude non-VALIDATED compliance
        4. HARD FILTER: requiresNight → exclude talents who can't do night
        5. SOFT SORT: Rank by specialties match, rating, distance, experience
        `,
    })
    @ApiResponse({ status: 200, type: MatchingTalentsResultDto })
    async findMatchingTalents(
        @Body() dto: FindMatchingTalentsDto,
    ): Promise<MatchingTalentsResultDto> {
        return this.matchingService.findMatchingTalents(dto);
    }

    // =========================================================================
    // Missions CRUD
    // =========================================================================

    @Post('missions')
    @UseGuards(JwtAuthGuard, RolesGuard)
    @ApiBearerAuth()
    @Roles('CLIENT', 'ADMIN')
    @ApiOperation({ summary: 'Créer une mission SOS' })
    @ApiResponse({ status: 201, description: 'Mission créée' })
    async createMission(
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: CreateMissionDto,
    ) {
        return this.matchingService.createMission(dto, user.id);
    }

    @Get('missions/:missionId/candidates')
    @UseGuards(JwtAuthGuard, MissionAccessGuard, RolesGuard)
    @ApiBearerAuth()
    @Roles('CLIENT', 'ADMIN')
    @ApiOperation({ summary: 'Trouver des candidats pour une mission SOS' })
    @ApiParam({ name: 'missionId', description: 'ID de la mission' })
    @ApiResponse({ status: 200, type: MatchingResultDto })
    async findCandidates(
        @Param('missionId') missionId: string,
        @Query() options: FindCandidatesDto,
    ): Promise<MatchingResultDto> {
        return this.matchingService.findCandidates(missionId, options);
    }

    @Get('missions/:missionId')
    @UseGuards(JwtAuthGuard, MissionAccessGuard)
    @ApiOperation({ summary: 'Obtenir les détails d\'une mission avec les candidatures' })
    @ApiParam({ name: 'missionId', description: 'ID de la mission' })
    async getMission(@Param('missionId') missionId: string) {
        return this.matchingService.getMissionWithApplications(missionId);
    }

    @Post('missions/:missionId/apply')
    @UseGuards(JwtAuthGuard, RolesGuard, SeedInterceptionGuard)
    @SeedAction('APPLY_MISSION')
    @ApiBearerAuth()
    @Roles('TALENT')
    @ApiOperation({ summary: 'Postuler à une mission SOS' })
    @ApiParam({ name: 'missionId', description: 'ID de la mission' })
    async applyToMission(
        @Param('missionId') missionId: string,
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: ApplyMissionDto,
    ) {
        return this.matchingService.applyToMission(
            missionId,
            user.id,
            dto.coverLetter,
            dto.proposedRate,
        );
    }
}
