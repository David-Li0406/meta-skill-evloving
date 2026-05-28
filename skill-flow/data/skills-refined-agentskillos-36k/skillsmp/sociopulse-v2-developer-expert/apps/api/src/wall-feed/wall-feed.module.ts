import { Module } from '@nestjs/common';
import { WallFeedController } from './wall-feed.controller';
import { WallFeedService } from './wall-feed.service';
import { AuthModule } from '../auth/auth.module';
import { PrismaModule } from '../common/prisma/prisma.module';

@Module({
    imports: [AuthModule, PrismaModule],
    controllers: [WallFeedController],
    providers: [WallFeedService],
    exports: [WallFeedService],
})
export class WallFeedModule { }
