import { Module } from '@nestjs/common';
import { PrismaModule } from '../common/prisma/prisma.module';
import { AuthModule } from '../auth/auth.module';
import { MessagesController } from './messages.controller';
import { MessagesService } from './messages.service';
import { MissionAccessGuard } from '../common/guards';

@Module({
    imports: [PrismaModule, AuthModule],
    controllers: [MessagesController],
    providers: [MessagesService, MissionAccessGuard],
})
export class MessagesModule { }
