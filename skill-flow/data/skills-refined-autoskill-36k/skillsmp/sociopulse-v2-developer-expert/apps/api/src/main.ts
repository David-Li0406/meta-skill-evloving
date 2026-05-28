import { NestFactory } from '@nestjs/core';
import { ValidationPipe, Logger } from '@nestjs/common';
import { NestExpressApplication } from '@nestjs/platform-express';
import { join } from 'path';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';
import { AllExceptionsFilter } from './common/filters';

async function bootstrap() {
    const logger = new Logger('Bootstrap');
    const app = await NestFactory.create<NestExpressApplication>(AppModule);

    // Root healthcheck endpoint (before prefix, for Coolify)
    const expressApp = app.getHttpAdapter().getInstance();
    expressApp.get('/', (_req: any, res: any) => {
        res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
    });

    // Global prefix
    app.setGlobalPrefix('api/v1');

    // Static assets for local uploads
    app.useStaticAssets(join(process.cwd(), 'uploads'), {
        prefix: '/uploads/',
    });

    // CORS - Multi-Domain Support for Multi-Tenant Architecture
    // FRONTEND_URL can be a comma-separated list: "https://sociopulse.fr,https://medicopulse.fr"
    const frontendUrlEnv = process.env.FRONTEND_URL || 'http://localhost:3000';
    const allowedOrigins = frontendUrlEnv
        .split(',')
        .map((origin) => origin.trim())
        .filter(Boolean);

    // Static origins always allowed
    const staticOrigins = [
        'http://localhost:3000',
        'http://localhost:3001',
        'https://sociopulse.fr',
        'https://www.sociopulse.fr',
        'https://dash.sociopulse.fr',
        'https://medicopulse.fr',
        'https://www.medicopulse.fr',
        'https://api.sociopulse.fr',
    ];

    // Combine static + dynamic origins (deduplicated)
    const allOrigins = [...new Set([...staticOrigins, ...allowedOrigins])];

    logger.log(`🌐 CORS enabled for origins: ${allOrigins.join(', ')}`);

    app.enableCors({
        origin: [
            ...allOrigins,
            /^http:\/\/localhost:\d+$/,      // Any localhost port (dev)
            /^https?:\/\/.*\.sslip\.io$/,    // sslip.io tunnels (dev)
        ],
        credentials: true,
        methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
        allowedHeaders: ['Content-Type', 'Authorization', 'Accept'],
    });

    // Global Exception Filter - standardized error responses
    app.useGlobalFilters(new AllExceptionsFilter());

    // Validation
    app.useGlobalPipes(
        new ValidationPipe({
            whitelist: true,
            forbidNonWhitelisted: true,
            transform: true,
            transformOptions: {
                enableImplicitConversion: true,
            },
        }),
    );

    // Swagger API Docs
    const config = new DocumentBuilder()
        .setTitle('Les Extras V2 API')
        .setDescription('API pour la plateforme Sociopulse V2 - Médico-social B2B2C')
        .setVersion('2.0')
        .addBearerAuth()
        .addTag('auth', 'Authentification et gestion des utilisateurs')
        .addTag('matching', 'Moteur de matching SOS Renfort')
        .addTag('video', 'Gestion des sessions vidéo Educat\'heure')
        .addTag('wall', 'Fil d\'actualité et annonces')
        .build();

    const document = SwaggerModule.createDocument(app, config);
    SwaggerModule.setup('docs', app, document);

    const port = process.env.PORT || 4000;
    const host = '0.0.0.0';

    // 👇 CRITICAL: Bind to 0.0.0.0 for Docker container accessibility
    await app.listen(port, host);

    logger.log(`🚀 API running on: http://${host}:${port}`);
    logger.log(`📚 Swagger docs: http://${host}:${port}/docs`);
    logger.log(`🌐 API endpoint: http://${host}:${port}/api/v1`);
    logger.log(`🔧 NODE_ENV: ${process.env.NODE_ENV || 'development'}`);
}

bootstrap();
