import { Body, Controller, Get, Param, Post, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { PaymentsService } from './payments.service';
import { CreateIntentDto, ConnectOnboardingDto } from './dto';
import { JwtAuthGuard, RolesGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload, Roles } from '../common/decorators';

@ApiTags('payments')
@Controller('payments')
export class PaymentsController {
    constructor(private readonly paymentsService: PaymentsService) { }

    @Post('create-intent')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Creer un PaymentIntent Stripe' })
    async createIntent(@Body() dto: CreateIntentDto) {
        return this.paymentsService.createIntent(dto);
    }

    @Post('create-intent/:bookingId')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Creer un PaymentIntent pour un booking' })
    async createIntentForBooking(
        @Param('bookingId') bookingId: string,
        @CurrentUser() user: CurrentUserPayload,
    ) {
        return this.paymentsService.createPaymentIntentForBooking(bookingId, user.id);
    }

    @Post('confirm-mock/:bookingId')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Valider le PaymentIntent Stripe et marquer le booking paye' })
    async confirmMock(
        @Param('bookingId') bookingId: string,
        @CurrentUser() user: CurrentUserPayload,
    ) {
        return this.paymentsService.confirmPaymentIntentForBooking(bookingId, user.id);
    }

    @Get('booking/:bookingId')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Recuperer les details du booking pour checkout' })
    async getBooking(
        @Param('bookingId') bookingId: string,
        @CurrentUser() user: CurrentUserPayload,
    ) {
        return this.paymentsService.getBookingForCheckout(bookingId, user.id);
    }

    @Post('connect/onboarding')
    @UseGuards(JwtAuthGuard, RolesGuard)
    @ApiBearerAuth()
    @Roles('TALENT')
    @ApiOperation({ summary: 'Creer un lien de onboarding Stripe Connect pour le talent' })
    async createOnboardingLink(
        @CurrentUser() user: CurrentUserPayload,
        @Body() dto: ConnectOnboardingDto,
    ) {
        return this.paymentsService.createOnboardingLink(user.id, dto.refreshUrl, dto.returnUrl);
    }

    @Get('connect/status')
    @UseGuards(JwtAuthGuard, RolesGuard)
    @ApiBearerAuth()
    @Roles('TALENT')
    @ApiOperation({ summary: 'Consulter le statut du compte Stripe Connect' })
    async getConnectStatus(@CurrentUser() user: CurrentUserPayload) {
        return this.paymentsService.getConnectStatus(user.id);
    }
}
