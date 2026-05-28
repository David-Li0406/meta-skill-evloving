import {
    Controller,
    Get,
    Post,
    Body,
    Param,
    UseGuards,
    Request,
    HttpCode,
    HttpStatus,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiParam, ApiBearerAuth } from '@nestjs/swagger';
import { MissionHubService } from './mission-hub.service';
import { JwtAuthGuard, MissionAccessGuard } from '../common/guards';
import {
    AcknowledgeInstructionsDto,
    StartMissionDto,
    SubmitReportDto,
    SendMissionMessageDto,
    CreateInstructionsDto,
} from './dto';

@ApiTags('Mission Hub')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard, MissionAccessGuard)
@Controller('missions')
export class MissionHubController {
    constructor(private readonly missionHubService: MissionHubService) { }

    // ========================================
    // INSTRUCTIONS
    // ========================================

    @Post(':id/instructions')
    @HttpCode(HttpStatus.CREATED)
    @ApiOperation({ summary: 'Create or update mission instructions (Client only)' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async createInstructions(
        @Param('id') missionId: string,
        @Body() dto: CreateInstructionsDto,
        @Request() req,
    ) {
        return this.missionHubService.createInstructions(missionId, req.user.id, dto);
    }

    @Get(':id/instructions')
    @ApiOperation({ summary: 'Get mission instructions' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async getInstructions(@Param('id') missionId: string) {
        return this.missionHubService.getInstructions(missionId);
    }

    @Post(':id/acknowledge')
    @HttpCode(HttpStatus.OK)
    @ApiOperation({ summary: 'Acknowledge mission instructions (Talent only)' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async acknowledgeInstructions(
        @Param('id') missionId: string,
        @Body() dto: AcknowledgeInstructionsDto,
        @Request() req,
    ) {
        return this.missionHubService.acknowledgeInstructions(missionId, req.user.id);
    }

    // ========================================
    // MISSION LIFECYCLE
    // ========================================

    @Post(':id/start')
    @HttpCode(HttpStatus.OK)
    @ApiOperation({ summary: 'Start mission manually (Talent only)' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async startMission(
        @Param('id') missionId: string,
        @Body() dto: StartMissionDto,
        @Request() req,
    ) {
        return this.missionHubService.startMission(missionId, req.user.id, dto.note);
    }

    @Post(':id/report')
    @HttpCode(HttpStatus.CREATED)
    @ApiOperation({ summary: 'Submit mission report (Talent only)' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async submitReport(
        @Param('id') missionId: string,
        @Body() dto: SubmitReportDto,
        @Request() req,
    ) {
        return this.missionHubService.submitReport(missionId, req.user.id, dto);
    }

    // ========================================
    // CHAT
    // ========================================

    @Get(':id/chat')
    @ApiOperation({ summary: 'Get mission chat messages' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async getChatMessages(@Param('id') missionId: string, @Request() req) {
        return this.missionHubService.getChatMessages(missionId, req.user.id);
    }

    @Post(':id/chat')
    @HttpCode(HttpStatus.CREATED)
    @ApiOperation({ summary: 'Send message in mission chat' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async sendMessage(
        @Param('id') missionId: string,
        @Body() dto: SendMissionMessageDto,
        @Request() req,
    ) {
        return this.missionHubService.sendMessage(missionId, req.user.id, dto);
    }

    // ========================================
    // TIMELINE
    // ========================================

    @Get(':id/timeline')
    @ApiOperation({ summary: 'Get mission timeline events' })
    @ApiParam({ name: 'id', description: 'Mission ID' })
    async getTimeline(@Param('id') missionId: string, @Request() req) {
        return this.missionHubService.getTimeline(missionId, req.user.id);
    }

    // ========================================
    // ACTIVE MISSIONS
    // ========================================

    @Get('active/count')
    @ApiOperation({ summary: 'Get count of active missions for current user' })
    async getActiveMissionsCount(@Request() req) {
        const count = await this.missionHubService.getActiveMissionsCount(req.user.id);
        return { count };
    }

    @Get('active')
    @ApiOperation({ summary: 'Get active missions for current user' })
    async getActiveMissions(@Request() req) {
        return this.missionHubService.getActiveMissions(req.user.id);
    }
}
