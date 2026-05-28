import { Injectable, OnModuleInit, OnModuleDestroy, Logger } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
    private readonly logger = new Logger(PrismaService.name);

    constructor() {
        super({
            log: [
                { emit: 'event', level: 'query' },
                { emit: 'stdout', level: 'info' },
                { emit: 'stdout', level: 'warn' },
                { emit: 'stdout', level: 'error' },
            ],
            errorFormat: 'colorless',
        });
    }

    async onModuleInit() {
        const maxAttempts = 5;
        const baseDelay = 3000; // 3 seconds

        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                await this.$connect();
                this.logger.log('✅ Database connected successfully');
                return;
            } catch (error) {
                const errorMessage = error instanceof Error ? error.message : String(error);
                this.logger.error(`❌ Connection failed (Attempt ${attempt}/${maxAttempts}): ${errorMessage}`);

                if (attempt === maxAttempts) {
                    this.logger.error('💀 Max connection attempts reached - throwing error');
                    throw error;
                }

                const delay = baseDelay * attempt; // Linear backoff: 3s, 6s, 9s, 12s, 15s
                this.logger.warn(`⏳ Retrying in ${delay / 1000}s...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    async onModuleDestroy() {
        await this.$disconnect();
        this.logger.log('Database connection closed');
    }

    /**
     * Clean database for testing purposes
     * ⚠️ Never use in production!
     */
    async cleanDatabase() {
        if (process.env.NODE_ENV === 'production') {
            throw new Error('Cannot clean database in production');
        }

        const models = Reflect.ownKeys(this).filter(
            (key) => typeof key === 'string' && key[0] !== '_' && key[0] !== '$',
        );

        return Promise.all(
            models.map((modelKey) => {
                const model = (this as any)[modelKey as string];
                if (model?.deleteMany) {
                    return model.deleteMany();
                }
                return null;
            }),
        );
    }
}
