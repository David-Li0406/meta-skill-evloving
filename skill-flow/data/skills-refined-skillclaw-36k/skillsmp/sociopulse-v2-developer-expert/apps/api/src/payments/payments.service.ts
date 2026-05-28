import {
    Injectable,
    InternalServerErrorException,
    NotFoundException,
    Logger,
    BadRequestException,
    ForbiddenException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import Stripe from 'stripe';
import { PrismaService } from '../common/prisma/prisma.service';
import { CreateIntentDto } from './dto';

@Injectable()
export class PaymentsService {
    private readonly logger = new Logger(PaymentsService.name);
    private readonly stripe: Stripe | null;
    private readonly frontendUrl: string;
    private readonly stripeKey?: string;

    constructor(
        private readonly configService: ConfigService,
        private readonly prisma: PrismaService,
    ) {
        const secretKey = this.configService.get<string>('STRIPE_SECRET_KEY');
        this.frontendUrl = this.configService.get<string>('FRONTEND_URL') || 'http://localhost:3000';
        this.stripeKey = secretKey || undefined;

        if (!secretKey) {
            this.logger.log('MODE PROTOTYPE : Stripe non configure, paiements simules.');
            this.stripe = null;
        } else {
            this.stripe = new Stripe(secretKey);
        }
    }

    async createIntent(dto: CreateIntentDto) {
        const stripe = this.ensureStripe();

        if (!stripe) {
            this.logger.log('Paiement simulateur : retour mock clientSecret');
            return { clientSecret: 'pi_prototype_secret_123', paymentIntentId: 'pi_mock_123' };
        }

        try {
            const paymentIntent = await stripe.paymentIntents.create({
                amount: dto.amount,
                currency: dto.currency.toLowerCase(),
                metadata: dto.metadata || {},
                automatic_payment_methods: { enabled: true },
            });

            this.logger.log(`PaymentIntent created: ${paymentIntent.id} for ${dto.amount} ${dto.currency}`);

            return { clientSecret: paymentIntent.client_secret, paymentIntentId: paymentIntent.id };
        } catch (error) {
            this.logger.error(`createIntent failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la creation du paiement');
        }
    }

    async createPaymentIntentForBooking(bookingId: string, userId: string) {
        const stripe = this.ensureStripe();

        if (!stripe) {
            this.logger.log(`Paiement simulateur pour booking ${bookingId}`);
            return {
                clientSecret: 'pi_prototype_secret_123',
                paymentIntentId: 'pi_mock_booking',
                amount: 0,
            };
        }

        try {
            const booking = await this.prisma.booking.findUnique({
                where: { id: bookingId },
                include: {
                    service: true,
                    client: { select: { email: true } },
                    provider: {
                        select: {
                            id: true,
                            stripeAccountId: true,
                            profile: { select: { firstName: true, lastName: true } },
                        },
                    },
                },
            });

            if (!booking) {
                throw new NotFoundException(`Booking ${bookingId} non trouve`);
            }

            if (booking.clientId !== userId) {
                throw new ForbiddenException('Acces refuse a ce booking');
            }

            const amountInCents = Math.round(booking.totalPrice * 100);
            const transferDestination = booking.provider?.stripeAccountId || undefined;

            const paymentIntent = await stripe.paymentIntents.create({
                amount: amountInCents,
                currency: 'eur',
                metadata: {
                    bookingId: booking.id,
                    serviceId: booking.serviceId || '',
                    clientEmail: booking.client?.email || '',
                },
                automatic_payment_methods: { enabled: true },
                ...(transferDestination
                    ? {
                        transfer_data: {
                            destination: transferDestination,
                        },
                    }
                    : {}),
            });

            await this.prisma.booking.update({
                where: { id: bookingId },
                data: { stripePaymentIntentId: paymentIntent.id },
            });

            this.logger.log(
                `PaymentIntent ${paymentIntent.id} created for booking ${bookingId}` +
                `${transferDestination ? ` (Connect -> ${transferDestination})` : ''}`,
            );

            return {
                clientSecret: paymentIntent.client_secret,
                paymentIntentId: paymentIntent.id,
                amount: amountInCents,
            };
        } catch (error) {
            if (error instanceof NotFoundException || error instanceof ForbiddenException) throw error;
            this.logger.error(`createPaymentIntentForBooking failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la creation du paiement');
        }
    }

    async confirmPaymentIntentForBooking(bookingId: string, userId: string) {
        const stripe = this.ensureStripe();

        if (!stripe) {
            this.logger.log(`Confirmation simulateur pour booking ${bookingId}`);
            return {
                success: true,
                bookingId,
                status: 'PAID',
                paymentIntentId: 'pi_mock_booking',
            };
        }

        try {
            const booking = await this.prisma.booking.findUnique({
                where: { id: bookingId },
                select: {
                    id: true,
                    clientId: true,
                    stripePaymentIntentId: true,
                    status: true,
                },
            });

            if (!booking) {
                throw new NotFoundException(`Booking ${bookingId} non trouve`);
            }

            if (booking.clientId !== userId) {
                throw new ForbiddenException('Acces refuse a ce booking');
            }

            if (!booking.stripePaymentIntentId) {
                throw new BadRequestException('Aucun PaymentIntent associe a ce booking');
            }

            let intent = await stripe.paymentIntents.retrieve(booking.stripePaymentIntentId);

            if (intent.status === 'requires_confirmation') {
                intent = await stripe.paymentIntents.confirm(intent.id);
            }

            if (intent.status !== 'succeeded' && intent.status !== 'processing') {
                throw new BadRequestException(
                    `Le paiement n'est pas finalise (statut actuel: ${intent.status})`,
                );
            }

            const updated = await this.prisma.booking.update({
                where: { id: bookingId },
                data: {
                    status: 'PAID',
                    paidAt: new Date(),
                    confirmedAt: new Date(),
                    stripePaymentIntentId: intent.id,
                },
            });

            return {
                success: true,
                bookingId: updated.id,
                status: updated.status,
                paymentIntentId: intent.id,
            };
        } catch (error) {
            if (error instanceof NotFoundException || error instanceof BadRequestException || error instanceof ForbiddenException) {
                throw error;
            }
            this.logger.error(`confirmPaymentIntentForBooking failed: ${error.message}`);
            throw new InternalServerErrorException('Erreur lors de la confirmation du paiement');
        }
    }

    async getBookingForCheckout(bookingId: string, userId: string) {
        const booking = await this.prisma.booking.findUnique({
            where: { id: bookingId },
            include: {
                service: { select: { name: true, imageUrl: true } },
                provider: {
                    include: {
                        profile: { select: { firstName: true, lastName: true, avatarUrl: true } },
                    },
                },
            },
        });

        if (!booking) {
            throw new NotFoundException(`Booking ${bookingId} non trouve`);
        }

        if (booking.clientId !== userId) {
            throw new ForbiddenException('Acces refuse a ce booking');
        }

        return booking;
    }

    async createOnboardingLink(userId: string, refreshUrl?: string, returnUrl?: string) {
        const stripe = this.ensureStripe();

        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: {
                id: true,
                email: true,
                stripeAccountId: true,
                stripeOnboarded: true,
            },
        });

        if (!user) {
            throw new NotFoundException('Utilisateur introuvable');
        }

        const accountId = user.stripeAccountId || (await this.createConnectAccount(user.id, user.email));

        const link = await stripe.accountLinks.create({
            account: accountId,
            refresh_url: refreshUrl || `${this.frontendUrl}/payments/connect/refresh`,
            return_url: returnUrl || `${this.frontendUrl}/payments/connect/return`,
            type: 'account_onboarding',
        });

        return {
            url: link.url,
            expiresAt: link.expires_at,
            accountId,
        };
    }

    async getConnectStatus(userId: string) {
        const stripe = this.ensureStripe();

        const user = await this.prisma.user.findUnique({
            where: { id: userId },
            select: {
                stripeAccountId: true,
                stripeOnboarded: true,
            },
        });

        if (!user?.stripeAccountId) {
            throw new NotFoundException('Aucun compte Stripe Connect associe');
        }

        const account = await stripe.accounts.retrieve(user.stripeAccountId);
        const onboarded = Boolean(
            account.details_submitted && account.charges_enabled && account.payouts_enabled,
        );

        if (onboarded && !user.stripeOnboarded) {
            await this.prisma.user.update({
                where: { id: userId },
                data: { stripeOnboarded: true },
            });
        }

        return {
            accountId: user.stripeAccountId,
            chargesEnabled: account.charges_enabled,
            payoutsEnabled: account.payouts_enabled,
            onboarded,
        };
    }

    private async createConnectAccount(userId: string, email?: string | null) {
        const stripe = this.ensureStripe();

        const account = await stripe.accounts.create({
            type: 'express',
            email: email || undefined,
            capabilities: {
                transfers: { requested: true },
                card_payments: { requested: true },
            },
            business_type: 'individual',
        });

        await this.prisma.user.update({
            where: { id: userId },
            data: { stripeAccountId: account.id, stripeOnboarded: false },
        });

        this.logger.log(`Stripe Connect account created for user ${userId}: ${account.id}`);

        return account.id;
    }

    private ensureStripe(): Stripe {
        if (!this.stripe) {
            throw new InternalServerErrorException("Stripe n'est pas configure cote serveur");
        }

        return this.stripe;
    }
}
