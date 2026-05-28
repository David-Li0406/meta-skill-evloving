import {
    Injectable,
    UnauthorizedException,
    ConflictException,
    BadRequestException,
    InternalServerErrorException,
    Logger,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcrypt';
import { PrismaService } from '../common/prisma/prisma.service';
import { RegisterDto, LoginDto, AuthResponseDto } from './dto';
import { randomBytes } from 'crypto';
import { PointLogStatus, Prisma } from '@prisma/client';
import { UserRole } from '@sociopulse/types';

@Injectable()
export class AuthService {
    private readonly logger = new Logger(AuthService.name);
    private readonly SALT_ROUNDS = 12;

    constructor(
        private readonly prisma: PrismaService,
        private readonly jwtService: JwtService,
        private readonly configService: ConfigService,
    ) { }

    /**
     * Register a new user
     */
    async register(dto: RegisterDto): Promise<AuthResponseDto> {
        try {
            // Check if user already exists
            const existingUser = await this.prisma.user.findUnique({
                where: { email: dto.email.toLowerCase() },
            });

            if (existingUser) {
                throw new ConflictException('Un compte existe déjà avec cet email');
            }

            // Hash password
            const passwordHash = await bcrypt.hash(dto.password, this.SALT_ROUNDS);

            const normalizedReferrerCode = dto.referrerCode?.trim() || null;

            // Determine current brand from environment
            const currentMode = (this.configService.get<string>('NEXT_PUBLIC_APP_MODE') || 'SOCIAL') as 'SOCIAL' | 'MEDICAL';

            // Set allowedBrands based on enableCrossBrand flag
            const allowedBrands = dto.enableCrossBrand
                ? ['SOCIAL', 'MEDICAL'] as const
                : [currentMode] as const;

            // Create user with profile/establishment in a transaction
            const user = await this.prisma.$transaction(async (tx) => {
                const referralCode = await this.generateUniqueReferralCode(tx);

                const referrer = normalizedReferrerCode
                    ? await tx.user.findUnique({ where: { referralCode: normalizedReferrerCode } })
                    : null;

                if (normalizedReferrerCode && !referrer) {
                    throw new BadRequestException('Code parrain invalide');
                }

                // 1. Create the user with cross-brand access
                const newUser = await tx.user.create({
                    data: {
                        email: dto.email.toLowerCase(),
                        passwordHash,
                        role: dto.role,
                        phone: dto.phone,
                        status: 'PENDING',
                        clientType: dto.clientType,
                        isVerified: false,
                        onboardingStep: 1,
                        referralCode,
                        referrerId: referrer?.id ?? null,
                        points: 0,
                        allowedBrands: [...allowedBrands],
                    },
                });

                // 2. Create Profile if firstName/lastName provided (for TALENT or CLIENT)
                if (dto.firstName && dto.lastName) {
                    await tx.profile.create({
                        data: {
                            userId: newUser.id,
                            firstName: dto.firstName,
                            lastName: dto.lastName,
                        },
                    });
                }

                // 3. Create Establishment if clientType is ESTABLISHMENT
                if (dto.role === 'CLIENT' && dto.clientType === 'ESTABLISHMENT' && dto.establishmentName) {
                    await tx.establishment.create({
                        data: {
                            userId: newUser.id,
                            name: dto.establishmentName,
                            address: '', // À compléter dans l'onboarding
                            city: '',
                            postalCode: '',
                            // Cross-Brand Activation Flags
                            isSocialActive: allowedBrands.includes('SOCIAL'),
                            isMedicalActive: allowedBrands.includes('MEDICAL'),
                        },
                    });
                }

                // Referral points are pending until identity verification (anti-fraud)
                if (referrer) {
                    await tx.pointLog.upsert({
                        where: {
                            userId_action_referenceId: {
                                userId: referrer.id,
                                action: 'REFERRAL',
                                referenceId: newUser.id,
                            },
                        },
                        create: {
                            userId: referrer.id,
                            action: 'REFERRAL',
                            referenceId: newUser.id,
                            amount: 200,
                            status: PointLogStatus.PENDING,
                        },
                        update: {},
                    });
                }

                return newUser;
            });

            this.logger.log(`New user registered: ${user.email} (${user.role}) - Brands: ${user.allowedBrands.join(', ')}`);

            // Generate tokens with allowedBrands
            return this.generateAuthResponse(user);
        } catch (error) {
            if (error instanceof ConflictException || error instanceof BadRequestException) {
                throw error;
            }
            this.logger.error(`Registration failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException('Erreur lors de l\'inscription');
        }
    }

    /**
     * Login with email and password
     */
    async login(dto: LoginDto): Promise<AuthResponseDto> {
        try {
            const emailLower = dto.email.toLowerCase();
            this.logger.log(`Login attempt for: ${emailLower}`);

            // Find user
            const user = await this.prisma.user.findUnique({
                where: { email: emailLower },
            });

            if (!user) {
                this.logger.warn(`User not found: ${emailLower}`);
                throw new UnauthorizedException('Email ou mot de passe incorrect');
            }

            if (!user.passwordHash) {
                this.logger.warn(`No password hash for user: ${emailLower}`);
                throw new UnauthorizedException('Email ou mot de passe incorrect');
            }

            this.logger.log(`User found: ${user.id}, checking password...`);

            // Verify password
            const isPasswordValid = await bcrypt.compare(dto.password, user.passwordHash);

            this.logger.log(`Password valid: ${isPasswordValid}`);

            if (!isPasswordValid) {
                throw new UnauthorizedException('Email ou mot de passe incorrect');
            }

            // Check if user is banned
            if (user.status === 'BANNED') {
                throw new UnauthorizedException('Votre compte a été suspendu');
            }

            // Update last login
            await this.prisma.user.update({
                where: { id: user.id },
                data: { lastLoginAt: new Date() },
            });

            this.logger.log(`User logged in: ${user.email}`);

            return this.generateAuthResponse(user);
        } catch (error) {
            if (error instanceof UnauthorizedException) {
                throw error;
            }
            this.logger.error(`Login failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException('Erreur lors de la connexion');
        }
    }

    /**
     * Refresh access token using refresh token
     */
    async refreshToken(refreshToken: string): Promise<AuthResponseDto> {
        try {
            const payload = await this.jwtService.verifyAsync(refreshToken, {
                secret: this.configService.get<string>('JWT_REFRESH_SECRET'),
            });

            const user = await this.prisma.user.findUnique({
                where: { id: payload.sub },
            });

            if (!user) {
                throw new UnauthorizedException('Utilisateur non trouvé');
            }

            if (user.status === 'BANNED') {
                throw new UnauthorizedException('Votre compte a été suspendu');
            }

            return this.generateAuthResponse(user);
        } catch (error) {
            this.logger.warn(`Token refresh failed: ${error.message}`);
            throw new UnauthorizedException('Token de rafraîchissement invalide');
        }
    }

    /**
     * Get current user profile
     */
    async getMe(userId: string) {
        try {
            const user = await this.prisma.user.findUnique({
                where: { id: userId },
                select: {
                    id: true,
                    email: true,
                    phone: true,
                    role: true,
                    status: true,
                    walletBalance: true,
                    points: true,
                    referralCode: true,
                    tags: { select: { id: true, name: true, category: true } },
                    createdAt: true,
                    profile: true,
                    establishment: true,
                },
            });

            if (!user) {
                throw new UnauthorizedException('Utilisateur non trouvé');
            }

            return user;
        } catch (error) {
            if (error instanceof UnauthorizedException) {
                throw error;
            }
            this.logger.error(`GetMe failed: ${error.message}`, error.stack);
            throw new InternalServerErrorException('Erreur lors de la récupération du profil');
        }
    }

    /**
     * Generate JWT tokens and auth response
     */
    private async generateAuthResponse(user: {
        id: string;
        email: string;
        role: UserRole;
        status: string;
        allowedBrands?: string[];
    }): Promise<AuthResponseDto> {
        const payload = {
            sub: user.id,
            email: user.email,
            role: user.role,
            status: user.status,
            allowedBrands: user.allowedBrands || [],
        };

        const [accessToken, refreshToken] = await Promise.all([
            this.jwtService.signAsync(payload, {
                secret: this.configService.get<string>('JWT_SECRET'),
                expiresIn: this.configService.get<string>('JWT_EXPIRES_IN') || '15m',
            }),
            this.jwtService.signAsync(payload, {
                secret: this.configService.get<string>('JWT_REFRESH_SECRET'),
                expiresIn: this.configService.get<string>('JWT_REFRESH_EXPIRES_IN') || '7d',
            }),
        ]);

        return {
            accessToken,
            refreshToken,
            user: {
                id: user.id,
                email: user.email,
                role: user.role,
                status: user.status,
            },
        };
    }

    private async generateUniqueReferralCode(tx: Prisma.TransactionClient): Promise<string> {
        for (let attempt = 0; attempt < 12; attempt += 1) {
            const code = this.generateReferralCode(8);
            const exists = await tx.user.findUnique({
                where: { referralCode: code },
                select: { id: true },
            });
            if (!exists) return code;
        }

        return this.generateReferralCode(12);
    }

    private generateReferralCode(length: number): string {
        const bytes = randomBytes(Math.ceil((length * 3) / 4));
        return bytes.toString('base64url').slice(0, length);
    }
}

