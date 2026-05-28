import {
    Controller,
    Get,
    Post,
    Delete,
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
} from '@nestjs/swagger';
import { WallFeedService } from './wall-feed.service';
import { GetFeedDto, CreatePostDto, CreateServiceDto, CreateBookingDto } from './dto';
import { JwtAuthGuard, SeedInterceptionGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload, SeedAction } from '../common/decorators';

@ApiTags('wall')
@Controller('wall')
export class WallFeedController {
    constructor(private readonly wallService: WallFeedService) { }

    @Get('sidebar')
    @ApiOperation({ summary: 'Obtenir les données de la Sidebar (News + Succès récents)' })
    @ApiResponse({ status: 200, description: 'Données sidebar' })
    async getSidebar(): Promise<any> {
        return this.wallService.getSidebarData();
    }

    @Get('feed')
    @ApiOperation({ summary: 'Obtenir le fil d\'actualité unifié (Missions + Services + Posts)' })
    @ApiResponse({ status: 200, description: 'Liste paginée des éléments du fil' })
    async getFeed(@Query() filters: GetFeedDto): Promise<any> {
        return this.wallService.getFeed(filters);
    }

    @Post('posts')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Créer un post social (expérience / actu)' })
    @ApiResponse({ status: 201, description: 'Post créé' })
    async createPost(
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: CreatePostDto,
    ): Promise<any> {
        return this.wallService.createPost(user.id, dto);
    }

    @Post('services')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Créer un service (Offre)' })
    @ApiResponse({ status: 201, description: 'Service créé' })
    async createService(
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: CreateServiceDto,
    ) {
        return this.wallService.createService(user.id, user.role, dto);
    }

    @Get('posts/:id')
    @ApiOperation({ summary: 'Obtenir le détail d\'une annonce' })
    async getPost(@Param('id') id: string): Promise<any> {
        return this.wallService.getPost(id);
    }

    @Get('services/:id')
    @ApiOperation({ summary: 'Obtenir le d\u00e9tail d\'un service' })
    async getService(@Param('id') id: string): Promise<any> {
        return this.wallService.getServiceById(id);
    }

    @Get('bookings')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Liste des réservations de l\'utilisateur' })
    @ApiResponse({ status: 200, description: 'Liste des réservations' })
    async getUserBookings(@CurrentUser() user: CurrentUserPayload) {
        return this.wallService.getUserBookings(user.id);
    }

    @Post('bookings')
    @UseGuards(JwtAuthGuard, SeedInterceptionGuard)
    @SeedAction('BOOK_SERVICE')
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Créer une réservation' })
    async createBooking(
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: CreateBookingDto,
    ) {
        return this.wallService.createBooking(user.id, dto);
    }

    @Delete('posts/:id')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Supprimer une annonce' })
    async deletePost(
        @Param('id') id: string,
        @CurrentUser() user: CurrentUserPayload,
    ) {
        await this.wallService.deletePost(id, user.id);
        return { success: true };
    }
}
