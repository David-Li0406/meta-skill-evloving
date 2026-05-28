import { Controller, Get, Post, Query, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { NotificationsService } from './notifications.service';
import { JwtAuthGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload } from '../common/decorators';

@ApiTags('notifications')
@ApiBearerAuth()
@UseGuards(JwtAuthGuard)
@Controller('notifications')
export class NotificationsController {
    constructor(private readonly notificationsService: NotificationsService) { }

    @Get()
    @ApiOperation({ summary: 'Lister les notifications utilisateur' })
    async listNotifications(
        @CurrentUser() user: CurrentUserPayload,
        @Query('unreadOnly') unreadOnly?: string,
    ) {
        const onlyUnread = unreadOnly === 'true';
        return this.notificationsService.listNotifications(user.id, onlyUnread);
    }

    @Post('mark-all-read')
    @ApiOperation({ summary: 'Marquer toutes les notifications comme lues' })
    async markAllAsRead(@CurrentUser() user: CurrentUserPayload) {
        return this.notificationsService.markAllAsRead(user.id);
    }
}
