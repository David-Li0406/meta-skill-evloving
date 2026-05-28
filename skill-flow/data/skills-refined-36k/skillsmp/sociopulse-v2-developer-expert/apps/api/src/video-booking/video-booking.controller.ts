import {
    Controller,
    Post,
    Get,
    Body,
    Param,
    UseGuards,
} from '@nestjs/common';
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
} from '@nestjs/swagger';
import { VideoBookingService } from './video-booking.service';
import { CreateVideoSessionDto, VideoRoomDto, VideoTokenDto, EndSessionDto } from './dto';
import { JwtAuthGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload } from '../common/decorators';

@ApiTags('video')
@Controller('video')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class VideoBookingController {
    constructor(private readonly videoService: VideoBookingService) { }

    @Get('join/:bookingId')
    @ApiOperation({ summary: 'Obtenir un token pour rejoindre une session vidéo' })
    @ApiResponse({ status: 200, type: VideoTokenDto })
    async getJoinToken(
        @Param('bookingId') bookingId: string,
        @CurrentUser() user: CurrentUserPayload,
    ): Promise<VideoTokenDto> {
        return this.videoService.getTokenForBooking(bookingId, user.id, user.email);
    }

    @Post('sessions')
    @ApiOperation({ summary: 'Créer une session vidéo pour un booking' })
    @ApiResponse({ status: 201, type: VideoRoomDto })
    async createSession(
        @Body() dto: CreateVideoSessionDto,
        @CurrentUser() user: CurrentUserPayload,
    ): Promise<VideoRoomDto> {
        return this.videoService.generateVideoSlot(dto, user.id);
    }

    @Post('sessions/:roomId/join')
    @ApiOperation({ summary: 'Rejoindre une session vidéo' })
    @ApiResponse({ status: 200, type: VideoTokenDto })
    async joinSession(
        @Param('roomId') roomId: string,
        @CurrentUser() user: CurrentUserPayload,
    ): Promise<VideoTokenDto> {
        return this.videoService.joinVideoSession(roomId, user.id, user.email);
    }

    @Post('sessions/:roomId/end')
    @ApiOperation({ summary: 'Terminer une session vidéo' })
    async endSession(
        @Param('roomId') roomId: string,
        @Body() dto: EndSessionDto,
    ): Promise<{ success: boolean }> {
        await this.videoService.endVideoSession(roomId, dto.recordingUrl);
        return { success: true };
    }

    @Get('upcoming')
    @ApiOperation({ summary: 'Lister les sessions vidéo à venir' })
    async getUpcoming(@CurrentUser() user: CurrentUserPayload) {
        return this.videoService.getUpcomingSessions(user.id);
    }
}
