import { Global, Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtAuthGuard, RolesGuard } from '../common/guards';

@Global()
@Module({
    imports: [
        ConfigModule,
        JwtModule.registerAsync({
            imports: [ConfigModule],
            useFactory: async (configService: ConfigService) => ({
                secret: configService.get<string>('JWT_SECRET') || 'prototype_secret_key',
                signOptions: {
                    expiresIn: configService.get<string>('JWT_EXPIRES_IN') || '7d',
                },
                global: true,
            }),
            inject: [ConfigService],
        }),
    ],
    controllers: [AuthController],
    providers: [AuthService, JwtAuthGuard, RolesGuard],
    exports: [AuthService, JwtModule, JwtAuthGuard, RolesGuard],
})
export class AuthModule { }
