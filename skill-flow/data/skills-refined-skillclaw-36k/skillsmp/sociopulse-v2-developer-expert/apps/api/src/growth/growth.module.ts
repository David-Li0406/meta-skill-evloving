import { Module } from '@nestjs/common';
import { PrismaModule } from '../common/prisma/prisma.module';
import { AuthModule } from '../auth/auth.module';
import { GrowthController } from './growth.controller';
import { GrowthService } from './growth.service';
import { GamificationService } from './gamification.service';

@Module({
    imports: [PrismaModule, AuthModule],
    controllers: [GrowthController],
    providers: [GrowthService, GamificationService],
    exports: [GrowthService, GamificationService],
})
export class GrowthModule {}

