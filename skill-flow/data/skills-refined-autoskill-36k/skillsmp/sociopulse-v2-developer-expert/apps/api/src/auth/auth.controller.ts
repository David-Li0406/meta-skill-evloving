import {
    Controller,
    Post,
    Get,
    Body,
    UseGuards,
    HttpCode,
    HttpStatus,
} from '@nestjs/common';
import {
    ApiTags,
    ApiOperation,
    ApiResponse,
    ApiBearerAuth,
} from '@nestjs/swagger';
import { Throttle } from '@nestjs/throttler';
import { AuthService } from './auth.service';
import { RegisterDto, LoginDto, RefreshTokenDto, AuthResponseDto } from './dto';
import { JwtAuthGuard } from '../common/guards';
import { CurrentUser, CurrentUserPayload } from '../common/decorators';

@ApiTags('auth')
@Controller('auth')
export class AuthController {
    constructor(private readonly authService: AuthService) { }

    @Post('register')
    @Throttle({ default: { limit: 5, ttl: 60000 } }) // 5 registrations per minute
    @ApiOperation({ summary: 'Créer un nouveau compte' })
    @ApiResponse({ status: 201, description: 'Compte créé', type: AuthResponseDto })
    @ApiResponse({ status: 409, description: 'Email déjà utilisé' })
    async register(@Body() dto: RegisterDto): Promise<AuthResponseDto> {
        return this.authService.register(dto);
    }

    @Post('login')
    @Throttle({ default: { limit: 10, ttl: 60000 } }) // 10 attempts per minute
    @HttpCode(HttpStatus.OK)
    @ApiOperation({ summary: 'Se connecter' })
    @ApiResponse({ status: 200, description: 'Connexion réussie', type: AuthResponseDto })
    @ApiResponse({ status: 401, description: 'Identifiants invalides' })
    @ApiResponse({ status: 429, description: 'Trop de tentatives - réessayez plus tard' })
    async login(@Body() dto: LoginDto): Promise<AuthResponseDto> {
        return this.authService.login(dto);
    }

    @Post('refresh')
    @HttpCode(HttpStatus.OK)
    @ApiOperation({ summary: 'Rafraîchir le token d\'accès' })
    @ApiResponse({ status: 200, description: 'Token rafraîchi', type: AuthResponseDto })
    @ApiResponse({ status: 401, description: 'Refresh token invalide' })
    async refreshToken(@Body() dto: RefreshTokenDto): Promise<AuthResponseDto> {
        return this.authService.refreshToken(dto.refreshToken);
    }

    @Get('me')
    @UseGuards(JwtAuthGuard)
    @ApiBearerAuth()
    @ApiOperation({ summary: 'Obtenir le profil de l\'utilisateur connecté' })
    @ApiResponse({ status: 200, description: 'Profil utilisateur' })
    @ApiResponse({ status: 401, description: 'Non authentifié' })
    async getMe(@CurrentUser() user: CurrentUserPayload) {
        return this.authService.getMe(user.id);
    }
}
